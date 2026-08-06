from collections import defaultdict

TOTAL_SLOTS_PER_DAY = 20

DAY_COUNT = 5

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


    details.append({
         
        "type": "day_balance",
        "daily_loads": loads,
        "max_load": max_load,
        "min_load": min_load,
        "raw_value": max_load - min_load,
        "penalty": day_balance_penalty,

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

            anesthesia_balance_penalty = 0


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

    total_room_idle = 0
    room_idle_details = []

    for item in schedule:
        room_schedule[
            (item.day_index, item.room)
        ].append(item)



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


def build_score_details(score: int, details: list) -> dict :

    
    # calculate_schedule_score tarafından üretilen details listesini
    # DB'ye kaydedilecek düzenli score_details yapısına dönüştürür.

    # Bu fonksiyon yeni bir ceza hesaplamaz.
    # Yalnızca mevcut hesap sonuçlarını düzenler.
    
    priority_items = []
    day_balance = {}
    anesthesia_balance = {}
    room_idle = {}
    surgeon_idle = {}
    score_summary = {}

    for detail in details:
        detail_type = detail.get("type")

        if detail_type == "priority":
            priority_items.append(detail)

        elif detail_type == "day_balance":
            day_balance = {
                "raw_value": detail.get("raw_value", 0),
                "loss": detail.get("penalty", 0),
                "details": {
                    "daily_loads": detail.get(
                        "daily_loads",
                        [],
                    ),
                    "max_load": detail.get("max_load", 0),
                    "min_load": detail.get("min_load", 0),
                },
            }

        elif detail_type == "anesthesia_balance" :

             anesthesia_balance = {

                # "raw value" : (
                "raw_value" : (

                    detail.get("max_load", 0)
                    -   detail.get("min_load", 0)
                     
                ),

                "loss" : detail.get("penalty", 0),
                "details" : {

                    "team_loads" :detail.get(
                        "anesthesia_load",
                        {},
                    ),

                    "max_load" : detail.get("max_load", 0),
                    "min_load": detail.get("min_load", 0),
                     
                },
                  
             }


        elif detail_type == "room_idle_time" :

             room_idle = {

                "raw_value" : detail.get(

                    "total_idle_slots",
                    0,
                     
                ),

                "loss" : detail.get("penalty", 0),
                "details" : detail.get("gaps", []), 
                  
             } 


        elif detail_type == "surgeon_idle_time":

             surgeon_idle = {

                "raw_value" : detail.get(

                    "total_idle_slots",
                    0,
                     
                ),

                "loss" : detail.get("penalty", 0),
                "details" : detail.get("gaps", []),
                  
             }


        elif detail_type == "score_summary" :

             score_summary= detail



    losses = {

        "day_balance" : day_balance,
        "anesthesia_balance" : anesthesia_balance,
        "room_idle" : room_idle,
        "surgeon_idle" : surgeon_idle,
         
    }

    total_loss = sum (

        loss_data.get("loss", 0)

        for loss_data in losses.values()
         
    )

    return {

        "priority": {

            "score" : score_summary.get(

                "priority_score",
                0,
                 
            ),

            "details" : priority_items,
             
        },

        "losses": losses,
        "total_losses" : total_loss,
        "final_score" : score,  
         
    }




     
    






    

