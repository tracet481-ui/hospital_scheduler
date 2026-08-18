from collections import defaultdict

TOTAL_SLOTS_PER_DAY = 20

DAY_COUNT = 5



TOTAL_SLOTS = 20 



PRIORITY_WEIGHTS = {

    "Kritik" : 100,
    "Yüksek" : 50,
    "Orta" : 20,
    "Düşük" : 5, 

}



def calculate_schedule_score (schedule, surgeries ) :

    """
        schedule : ScheduleItem DTO listesi
        surgeries : SurgeryRequest DTO listesi

        amaç :
        - Kritik hastalar erken başlasın
        - Günler dengeli dağılsın
        - Anestezi ekipleri dengeli kullanılsın
    """

    score = 0

    details = []


    surgery_map = {

        surgery.patient :surgery 

        for surgery in surgeries


    }



    #-------------

    # 1 Priority / erken başlama
    
    #--------------


    priority_score = 0

    for item in schedule :
        
        surgery =  surgery_map[item.patient]

        weight = PRIORITY_WEIGHTS.get(surgery.priority, 5 )



        global_start = (

            item.day_index * TOTAL_SLOTS_PER_DAY + item.start_slot

            
        )



        max_global_start = DAY_COUNT *TOTAL_SLOTS_PER_DAY


        contribution = (

            max_global_start - global_start

        ) * weight



        priority_score += contribution

        details.append ({

            "type":"priority",
            "patient":item.patient,
            "operation":item.operation,
            "priority":surgery.priority,
            "day_index":item.day_index,
            "start_slot":item.start_slot,
            "score":contribution,

        })



    score += priority_score


        #------------------
        # 2  Günlük yük dengesi
        #-------------------



    daily_load = defaultdict(int) 

    for item in schedule :

            duration = item.end_slot - item.start_slot

            daily_load[item.day_index] += duration 


        
    loads = [

            daily_load[ day_index ] 

            for day_index in range(DAY_COUNT)

        ]


    max_load = max(loads)
    min_load =min(loads)


    day_balance_penalty = (max_load - min_load) * 100

    score -= day_balance_penalty


    details.append ({

            "type":"day_balance",
            "daily_load":loads,
            "mox_loads":max_load,
            "min_loads":min_load,
            "penalty":day_balance_penalty


        })



        #--------------
        # 3  Anestezi dengesi
        #---------------



    anesthesia_load =defaultdict(int)


    for item in schedule :

            duration = item.end_slot - item.start_slot

            anesthesia_load [item.anesthesia_team] += duration


    anesthesia_values =  list (anesthesia_load.values())

    if anesthesia_values:

            max_anesthesia = max (anesthesia_values)
            min_anesthesia = min (anesthesia_values)


            anesthesia_balance_penalty = (
                
                max_anesthesia - min_anesthesia
            ) * 50 
        
    else : 

            max_anesthesia = 0
            min_anesthesia = 0 

            anesthesia_penalty = 0


    score -= anesthesia_balance_penalty


    details.append ({


            "type":"anesthesia_balance",
            "anesthesia_load":dict(anesthesia_load),
            "max_load":max_anesthesia,
            "min_load":min_anesthesia,
            "penalty":anesthesia_balance_penalty


        })







    #------------------
    # 4 Room idle time
    #------------------



    room_schedule = defaultdict(list)



    for item in schedule:

        room_schedule[( item.day_index, item.room)].append(item)

        total_room_idle = 0
        room_idle_details = []



    for (day_index, room), items in room_schedule.items() :

        sorted_items = sorted(

            items,
            key=lambda x: x.start_slot

            )


        for i in range(len(sorted_items) - 1 ) :

            current_item = sorted_items[i]
            next_item = sorted_items[ i + 1 ]

            gap=(

                next_item.start_slot   - 
                current_item.end_slot

            )


            if gap > 0 :

                total_room_idle += gap


                room_idle_details.append({

                        "day_index" : day_index,
                        "room" : room,
                        "from_patient" : current_item.patient,
                        "to_patient" : next_item.patient,
                        "gap" : gap,

                })


    ROOM_IDLE_WEIGHT= 30

    room_idle_penalty = total_room_idle* ROOM_IDLE_WEIGHT

    score -= room_idle_penalty

    details.append({

        "type" : "room_idle_time",
        "total_idle_slots" : total_room_idle,
        "penalty" : room_idle_penalty,
        "gaps" : room_idle_details,
        
    })





    #--------------------
    # 5  SUrgeon idle time 
    #----------------------



    surgeon_schedule = defaultdict(list)


    for item in schedule : 

        surgeon_schedule [

            (item.day_index, item.surgeon)
            
        ].append(item)



    total_surgeon_idle = 0

    surgeon_idle_details = []


    for( day_index, surgeon ) , items in surgeon_schedule.items() :


        sorted_items = sorted (

            items,
            key= lambda x : x .start_slot

        )


        for i in range (len(sorted_items) - 1 ) :

            current_item = sorted_items[i]

            next_item = sorted_items[ i + 1 ]

            gap = ( 

                next_item.start_slot -
                current_item.end_slot

            )

            if gap > 0 :

                total_surgeon_idle += gap


                surgeon_idle_details.append({

                    "day_index" : day_index,
                    "surgeon" : surgeon,
                    "from_patient" : current_item.patient,
                    "to_patient" : next_item.patient,
                    "gap" : gap,


                    })


    SURGEON_IDLE_WEIGHT = 40

    surgeon_idle_penalty = (

            total_surgeon_idle *

            SURGEON_IDLE_WEIGHT

    )


    score -= surgeon_idle_penalty


    details.append({

            "type" : "surgeon_idle_time",
            "total_idle_slots" : total_surgeon_idle,
            "penalty" : surgeon_idle_penalty,
            "gaps" : surgeon_idle_details,


    })


    details.append({
            "type": "score_summary",
            "priority_score": priority_score,
            "day_balance_penalty": day_balance_penalty,
            "anesthesia_balance_penalty": anesthesia_balance_penalty,
            "room_idle_penalty": room_idle_penalty,
            "surgeon_idle_penalty": surgeon_idle_penalty,
            "final_score": score,
    })




    return score, details
    






    


# def calculate_priority_score(schedule, surgeries ) :

#     total_score = 0
#     score_details = []


#     surgery_map = {


#         (surgery.patient, surgery.operation  ) : surgery 
#         for surgery in surgeries  
#     }


#     for item in schedule :

#         surgery = surgery_map[(item.patient, item.operation)] 


#         if surgery.priority == "Kritik" : 
#             weight = 100

        
#         elif surgery.priority == "Yüksek" :
#             weight = 50


        
#         elif surgery.priority == "Orta" :
#             weight = 20


#         else :
#             weight = 5 


        
#         # contribution = (TOTAL_SLOT - item.start_slot) * weight

#         WEEK_TOTAL_SLOT = 5 - TOTAL_SLOTS
#         global_start = item.day_index * TOTAL_SLOTS + item.start_slot
#         contrubition = (WEEK_TOTAL_SLOT - global_start) * weight

#         total_score += contrubition



#         score_details.append({

#             "patient" : item.patient,
#             "operation" : item.operation,
#             "priority" : surgery.priority,
#             "start_slot" : item.start_slot,
#             "score" : contrubition,

#         })


    
#     return total_score, score_details