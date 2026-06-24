MAX_CONTINUOUS_SURGEON_WORK = 4
REQUIRED_REST_AFTER_MAX_WORK = 1

def validate_surgeon_rest_rule(schedule) :

    """"" 
    kural:
    Bir cerrah toplam 4 slot üst üste çalışınca 
    sonraki operasyondan önce 1 slot ara vermelidir.
    """


    violations = []

    surgeon_day_schedule = {}

    for item in schedule :

        key = (item.day_index, item.surgeon)

        if key not in surgeon_day_schedule:

            surgeon_day_schedule[key]  = []


        surgeon_day_schedule [key].append(item)

    
    for (day_index, surgeon), items in surgeon_day_schedule.items() :


        sorted_items = sorted (

            items,
            key = lambda x:x.start_slot,
            
        )


        continuous_work = 0
        previous_end = None


        for item in sorted_items :

            duration = item.end_slot - item.start_slot

            if previous_end is None :

                continuous_work = duration

                previous_end = item.end_slot

                continue

            gap = item.start_slot - previous_end

            if gap >= REQUIRED_REST_AFTER_MAX_WORK:

                continuous_work = duration

            
            else : 

                if continuous_work >= MAX_CONTINUOUS_SURGEON_WORK :

                    violations.append ({

                        "day_index" : day_index,
                        "surgeon" : surgeon,
                        "patient" : item.patient,
                        "operation" : item.operation,
                        "start_slot" : item.start_slot,
                        "previous_slot" : previous_end,
                        "continuous_work_before" : continuous_work,
                        "gap" : gap,

                    })

                continuous_work += duration

            previous_end = item.end_slot
        
        return violations
    

