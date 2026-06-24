from django.shortcuts import render

from rest_framework.views import APIView

from rest_framework.response import Response

from rest_framework import status

##  endpoint i bağlıyoruz

from scheduling.services.data_loader import load_scheduler_input

from scheduling.services.simulation import SimulationEngine

from scheduling.services.validators import validate_surgeon_rest_rule

from scheduling.services.schedule_saver import save_schedule_plan

from scheduling.services.scoring import calculate_schedule_score

from scheduling.models import SchedulePlan


# Create your views here.


DAYS = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma"]

def slot_to_time(slot):

    hour = 8 + (slot // 2 )
    minute = 30 * (slot % 2 )
    return f"{hour:02d} : {minute:02d}"


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


        best_schedule, best_score, best_details, all_results = simulation.run ()


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


        score_summary = next (

            detail
            for detail in score_details
            if detail["type"] == "score_summary"

        )




        

        weekly_schedule = []

        for day_index, day_name in enumerate(DAYS):

            day_items = [

                item for item in best_schedule
                if item.day_index == day_index

            ]

            day_items = sorted(
                
                day_items, key=lambda item: item.start_slot
                
                )

            
            weekly_schedule.append({

                "day_index" : day_index,
                "day_name" : day_name,
                "items" : [{

                    "patient" : item.patient,
                    "operation" : item.operation,
                    "room" : item.room,
                    "surgeon" : item.surgeon,
                    "anesthesia_team" : item.anesthesia_team,
                    "start_slot" : item.start_slot,
                    "end_slot" : item.end_slot,
                    "start_time" : slot_to_time(item.start_slot),
                    "end_time" : slot_to_time (item.end_slot),

                }
                
                for item in day_items
                
                ],

            })



        plan = save_schedule_plan (

                schedule = best_schedule,
                algorithm_name = "cp",
                planning_day = "Haftalık Plan",
                score = total_score,
        )





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
    




        return Response ({

            "message" : "Schedule generate endpoint çalışıyor"




        })
    

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
