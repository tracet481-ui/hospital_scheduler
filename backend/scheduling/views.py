from django.shortcuts import render

from rest_framework.views import APIView

from rest_framework.response import Response

from rest_framework import status

from rest_framework.authtoken.models import Token

from rest_framework.decorators import api_view

from rest_framework.generics import (
                         ListCreateAPIView,
                         ListAPIView, )



##  endpoint i bağlıyoruz

from scheduling.services.data_loader import load_scheduler_input

from scheduling.services.simulation import SimulationEngine

from scheduling.services.validators import validate_surgeon_rest_rule

from scheduling.services.schedule_saver import save_schedule_plan

from scheduling.services.scoring import calculate_schedule_score

from .models import (
    SchedulePlan,
    ScheduleItem,
    SurgeryRequest,
    Patient,
    SurgeryType,
)


from django.contrib.auth import authenticate

from .serializer import (
                        # SchedulePlanListSerializer,
                        # SchedulePlanDetailSerializer,
                        SurgeryRequestSerializer,
                        PatientSerializer,
                        SurgeryTypeSerializer, 
                        )       




# Create your views here.


DAYS = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma"]

def slot_to_time(slot):

    hour = 8 + (slot // 2 )
    minute = 30 * (slot % 2 )
    return f"{hour:02d} : {minute:02d}"



@api_view (["POST"])

def login_view (request) :

    username = request.data.get("username")
    password = request.data.get("password")


    user =authenticate (

        username = username ,
        password = password,

    )

    if user is None :

        return Response (

            { " error:" "Kullanıcı adı veya şifre hatalı!"},

            status = status.HTTP_400_BAD_REQUEST
        )


    token, created = Token.objects.get_or_create ( user = user )


    return Response ({

        "token" : token.key

    })







class GenerateScheduleView(APIView) :

    def post(self, reequest) :

        surgeons, rooms, anesthesia_teams, surgeries = load_scheduler_input()

        simulation = SimulationEngine(

            surgeons = surgeons,
            rooms = rooms,
            anesthesia_teams = anesthesia_teams,
            surgeries = surgeries,
            planning_day = "Haftalık Plan"

        )


        # best_schedule, best_score, best_details, all_results = simulation.run ()


        best_schedule, best_score, best_details, all_results = simulation.run()


            ##   detail sayfasında son plan kayıtlarını göster --------

        simulation_results = [

            {

                "attempt" : result ["attempt"],
                "valid_index" : result ["valid_index"],
                "score" : result ["score"] ,
                "is_best" : result ["score"] == best_score ,

            }
                for result in all_results

        ]

        score_summary = next (

            detail
            for detail in best_details
            if detail["type"] == "score_summary"

        )


        success_rate = min (

            100,
            max (   0, int (best_score/1300)),
            
        )

        score_summary ["success_rate"] = success_rate



    ## ---------- detail sayfasında son plan kayıtlarını göster 
        
        ##  score check ----------------------------


        print("\nBEST PLAN SELECTION CHECK")
        print("=========================")
        print("Best Score           :", best_score)
        print(
            "Max All Results      :",
            max(result["score"] for result in all_results)
            if all_results else None
        )
        print(
            "Best Schedule Count  :",
            len(best_schedule) if best_schedule else 0
        )

        
        
        ## ----------------------------  score check 



        if best_schedule is None :

            return Response (

                {"Error" : "Geçerli schedule bulunamadı!"},
                status = status.HTTP_400_BAD_REQUEST,

            )


        ## violations denetimi

        rest_violations =  validate_surgeon_rest_rule(best_schedule)


        if rest_violations :

            return Response ({

                "error" : "Best plan rest violation içeriyor!",
                "violations" : rest_violations,

                },
                status = status.HTTP_400_BAD_REQUEST,
            )

        total_score, score_details = calculate_schedule_score(

            schedule = best_schedule,
            surgeries = surgeries,

        )

        ##  score check ----------------------------

        print("\nBEST PLAN SCORE CHECK")
        print("=====================")
        print("Simulation Best Score :", best_score)
        print("Recalculated Score     :", total_score)
        print("Difference             :", best_score - total_score)

        
        ##  score check ----------------------------






        score_summary = next (

            detail
            for detail in score_details
            if detail["type"] == "score_summary"

        )


        success_rate = min (

            100,
            max(0, int(total_score / 1300)),

        )

        score_summary["success_rate"] = success_rate





        ## ----------------------------  score check 




        weekly_schedule = []

        for day_index, day_name in enumerate(DAYS):

            day_items = [
                item for item in best_schedule
                if item.day_index == day_index
            ]

            day_items = sorted(
                day_items,
                key=lambda item: item.start_slot
            )

            weekly_schedule.append({
                "day_index": day_index,
                "day_name": day_name,
                "items": [
                    {
                        "patient": item.patient,
                        "operation": item.operation,
                        "room": item.room,
                        "surgeon": item.surgeon,
                        "anesthesia_team": item.anesthesia_team,
                        "start_slot": item.start_slot,
                        "end_slot": item.end_slot,
                        "start_time": slot_to_time(item.start_slot),
                        "end_time": slot_to_time(item.end_slot),
                    }
                    for item in day_items
                ],
            })


        plan = save_schedule_plan (

                schedule = best_schedule,
                algorithm_name = "cp",
                planning_day = "Haftalık Plan",
                score = total_score,
                score_details = score_summary,
                simulation_results = simulation_results,
                # success_rate = score_details.get("success_rate",0),
        )


        print("\nSUCCESS RATE CHECK")
        print("==================")
        print("Calculated Success Rate :", success_rate)
        print("Summary Success Rate    :", score_summary.get("success_rate"))
        print("Saved Success Rate      :", plan.success_rate)




        
        ##  score check ----------------------------
        
        print("\nSAVED PLAN CHECK")
        print("================")
        print("Saved Plan ID :", plan.id)
        print("Saved Score   :", plan.score)
        print("Expected Best :", best_score)
        print("Item Count    :", len(best_schedule))




        ## ---------------------------- score check 





        return Response({

                "success" : True,
                "message" : "Schedule başarıyla üretildi.",
                "plan_id" : str(plan.id),
                "score" : total_score,
                "valid_plan_count" : len(all_results),
                "score_summary" : score_summary,
                "weekly_schedule" : weekly_schedule,
            },
                status = status.HTTP_201_CREATED,
        )





        # return Response ({

        #     "message" : "Schedule generate endpoint çalışıyor"




        # })









class SchedulePlanListView(APIView) :

    def get(self, request) :

        plans = SchedulePlan.objects.all().order_by("-created_at")

        data = []

        for plan in plans:

            data.append  ({

                  "id" : str(plan.id),
                  "planning_day" : plan.planning_day,
                  "algorithm_name" : plan.algorithm_name,
                  "score" : plan.score,
                  "is_feasible" : plan.is_feasible,
                  "created_at" : plan.created_at,

             })

        return Response(data)



class ScheduleDetailView(APIView) :

    def get (self, request, plan_id) :

        plan = SchedulePlan.objects.get(id = plan_id)

        items = ScheduleItem.objects.filter(plan = plan).order_by(

            "day_index",
            "start_slot",

        )

        return Response ({

            "id" : plan.id,
            "score" : plan.score,
            "algorithm_name" : plan.algorithm_name,
            "is_feasible" : plan.is_feasible,
            "created_at" : plan.created_at,

            "simulation_results" : plan.simulation_results ,

            "priority_score" : plan.priority_score,
            "day_balance_penalty" : plan.day_balance_penalty,
            "anesthesia_balance_penalty" : plan.anesthesia_balance_penalty,
            "room_idle_penalty" : plan.room_idle_penalty,
            "surgeon_idle_penalty" : plan.surgeon_idle_penalty,
            "success_rate" : plan.success_rate,


            "items" : [{

                # "priority_score" : plan.priority_score,
                # "day_balance_penalty" : plan.day_balance_penalty,
                # "anesthesia_balance_penalty" : plan.anesthesia_balance_penalty,
                # "room_idle_penalty" : plan.room_idle_penalty,
                # "surgeon_idle_penalty" : plan.surgeon_idle_penalty,
                # "success_rate" : plan.success_rate,



                "patient" : item.surgery_request.patient.code,
                "operation" : item.surgery_request.surgery_type.name,
                "room" : item.room.name,
                "surgeon" : item.surgeon.name,
                "anesthesia_team" : item.anesthesia_team.name,
                "day_index" : item.day_index,
                "start_slot" : item.start_slot,
                "end_slot" : item.end_slot,
                "start_time" : slot_to_time(item.start_slot),
                "end_time" : slot_to_time(item.end_slot),

            }
                for item in items

            ],

        })

 ## son üretilen planın verilerini tabloya yazdırıcaz

class LatestScheduleView(APIView) :

    def get(self, request) :

        plan = SchedulePlan.objects.order_by("-created_at").first()

        if plan is None :
            return Response (

                {"error":"Kayıtlı plan bulunamadı!"},
                status = 404,

            )


        items = ScheduleItem.objects.filter(plan = plan).order_by(

            "day_index",
            "start_slot",

        )

        return Response ({

            "id" : plan.id,
            "score" : plan.score,
            "algorithm_name" : plan.algorithm_name,
            "is_feasible" : plan.is_feasible,
            "created_at" : plan.created_at,
            "items" : [{

                "patient" : item.surgery_request.patient.code,
                "operation" : item. surgery_request.surgery_type.name,
                "room" : item.room.name,
                "surgeon" : item.surgeon.name,
                "anesthesia_team" : item.anesthesia_team.name,
                "day_index" : item.day_index,
                "start_slot" : item.start_slot,
                "end_slot" : item.end_slot,
                "start_time" : slot_to_time(item.start_slot),
                "end_time" : slot_to_time (item.end_slot),


                }

            for item in items

            ],

        })
    

##  operasyon ekleme    ------------------------------------


# class SurgeryTypeListCreateView (ListCreateAPIView) :

#     queryset = SurgeryType.objects.all().order_by("name")

#     serializer_class = SurgeryTypeSerializer


class SurgeryRequestListCreateView (ListCreateAPIView) :

    queryset = (

        SurgeryRequest.objects
        .select_related(

            "patient",
            "surgery_type",
            "surgery_type__required_specialty",

        )
        .order_by ("-created_at")

    )

    serializer_class = SurgeryRequestSerializer


## Hasta listesi --------------------------

class PatientlistView (ListAPIView) :

    queryset = Patient.objects.order_by ("code")
    serializer_class = PatientSerializer



## -------------------------- Hasta listesi 



##  operasyon tipleri  --------------------------------

class SurgeryTypeListView(ListAPIView) :

    queryset = (

        SurgeryType.objects
        .select_related("required_specialty")
        .order_by("name")

    )

    serializer_class = SurgeryTypeSerializer


##  -------------------------------- operasyon tipleri  




## ------------------------------------  operasyon ekleme    


class SurgeryRequestListCreateView(ListCreateAPIView):
    queryset = (
        SurgeryRequest.objects
        .select_related(
            "patient",
            "surgery_type",
            "surgery_type__required_specialty",
        )
        .order_by("-created_at")
    )

    serializer_class = SurgeryRequestSerializer


class PatientListView(ListAPIView):
    queryset = Patient.objects.order_by("code")
    serializer_class = PatientSerializer


class SurgeryTypeListView(ListAPIView):
    queryset = (
        SurgeryType.objects
        .select_related("required_specialty")
        .order_by("name")
    )

    serializer_class = SurgeryTypeSerializer