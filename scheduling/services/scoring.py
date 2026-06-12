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
            ) * 80 
        
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




        return score, details



def calculate_priority_score(schedule, surgeries ) :

    total_score = 0
    score_details = []


    surgery_map = {


        (surgery.patient, surgery.operation  ) : surgery 
        for surgery in surgeries  
    }


    for item in schedule :

        surgery = surgery_map[(item.patient, item.operation)] 


        if surgery.priority == "Kritik" : 
            weight = 100

        
        elif surgery.priority == "Yüksek" :
            weight = 50


        
        elif surgery.priority == "Orta" :
            weight = 20


        else :
            weight = 5 


        
        # contribution = (TOTAL_SLOT - item.start_slot) * weight

        WEEK_TOTAL_SLOT = 5 - TOTAL_SLOTS
        global_start = item.day_index * TOTAL_SLOTS + item.start_slot
        contrubition = (WEEK_TOTAL_SLOT - global_start) * weight

        total_score += contrubition



        score_details.append({

            "patient" : item.patient,
            "operation" : item.operation,
            "priority" : surgery.priority,
            "start_slot" : item.start_slot,
            "score" : contrubition,

        })


    
    return total_score, score_details