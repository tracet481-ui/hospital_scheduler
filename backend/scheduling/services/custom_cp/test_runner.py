from scheduling.services.data_loader import (
                                    load_scheduler_input,
)

from scheduling.services.custom_cp.scheduler import (
                                    CustomCPScheduler,
)

from scheduling.services.validators import (

    validate_surgeon_rest_rule,

)


def run_custom_cp_test () :


    # data = load_scheduler_input ()

    surgeons, rooms, anesthesia_teams, surgeries = (
                load_scheduler_input()
    )


    # data = load_scheduler_input()

    print("\nLOADER DEBUG")
    print("============")
    print(
        0,
        type(surgeons),
        type(surgeons[0]) if surgeons else None,
    )



    print(
        1,
        type(rooms),
        type(rooms[0]) if rooms else None,
    )
    print(
        2,
        type(anesthesia_teams),
        type(anesthesia_teams[0])
        if anesthesia_teams
        else None,
    )
    print(
        3,
        type(surgeries),
        type(surgeries[0]) if surgeries else None,
    )


    groups = [
        surgeons,
        rooms,
        anesthesia_teams,
        surgeries,
    ]


    for index, group in enumerate(groups):

        print(
            index,
            type(group),
            type(group[0]) if group else None,
        )


    # for index, group in enumerate(data):

    #     print(
    #         index,
    #         type(group),
    #         type(group[0]) if group else None,
    #     )


    scheduler = CustomCPScheduler(

        surgeons = surgeons,
        rooms = rooms,
        anesthesia_teams = anesthesia_teams,
        surgeries = surgeries,
        planning_day = None,
        soft_constraints = {

            "day_balance" : 50,
            "anesthesia_balance" : 50,
            "room_idle" : 50,
            "surgeon_idle" : 50,

            },

    )   


    schedule = scheduler.generate ()



    if schedule is None :


        print("\nCustom CP RESULT")
        print("==================")
        print("INFEASIBLE")


        return



    print("\nCustom CP RESULT")
    print("\nCustom CP RESULT")
    print("FEASIBLE")



    print(
        "Schedule item count : ", 
        len(schedule),
    )

    # -------------------------------------------------------
    # CUSTOM CP VİOLATİON
    # -------------------------------------------------------

    rest_vialotions = validate_surgeon_rest_rule (

        schedule

    )


    print("\nCUSTOM CP VALIDATION")
    print("======================")


    print(

        "Rest violation count : ",
        len(rest_vialotions),

    )


    for violation in rest_vialotions :

        print(violation)






    for item in schedule :


        print(

            item.day_index,
            item.start_slot,
            item.end_slot,
            item.patient,
            item.operation,
            item.room,
            item.surgeon,
            item.anesthesia_team,

        )


# ----------------------------------------------------
# violation çıktı
# ----------------------------------------------------

    overlap_violations = (

        validate_resource_overlaps (

            schedule

        )

    )


    print(

        "Overlap violation count : ",
        len(overlap_violations),

    )

    for violation in overlap_violations :

        print(violation)



if __name__ == "__main__" :

    run_custom_cp_test() 


def validate_resource_overlaps (

    schedule,
        
):

    violations = []


    for i in range (len(schedule)) :

        for j in range (

            i + 1,
            len (schedule),

        ):


            first = schedule [i]
            second = schedule [j]


            if (

                first.day_index
                !=  second.day_index

            ):

                continue


            overlaps = (

                first.start_slot
                < second.end_slot

                and

                second.start_slot
                < first.end_slot

            )


            if not overlaps :

                continue 

            if first.room == second.room    :

                violations.append ({

                    "type" : "ROOM",
                    "first" : first.patient,
                    "second" : second.patient,

                })


            if (

                first.surgeon
                == second.surgeon

            ):

                violations.append ({

                    "type" : "SURGEON",
                    "first" : first.patient,
                    "second" : second.patient,

                })


            if (

                first.anesthesia_team
                == second.anesthesia_team

            ):

                violations.append ({

                    "type" : "ANESTHESIA",
                    "first" : first.patient,
                    "second" : second.patient,

                })


    return violations


        