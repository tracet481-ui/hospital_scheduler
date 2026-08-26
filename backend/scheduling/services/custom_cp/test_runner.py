from scheduling.services.data_loader import (
                                    load_scheduler_input,
)

from scheduling.services.custom_cp.scheduler import (
                                    CustomCPScheduler,
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



if __name__ == "__main__" :

    run_custom_cp_test() 





        