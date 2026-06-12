from scheduling.models import (

    SchedulePlan,
    ScheduleItem,
    SurgeryRequest,
    Surgeon,
    OperatingRoom,
    AnesthesiaTeam,


)


def save_schedule_plan (
        schedule,
        algorithm_name,
        planning_day,
        score,
) :
    
    plan = SchedulePlan.objects.create(
        planning_day = planning_day,
        algorithm_name = algorithm_name,
        score = score,
        is_feasible = True,

    )


    for item in schedule :

        surgery_request = SurgeryRequest.objects.get(

            patient__code=item.patient,
            surgery_type__name = item.operation,

        )



        surgeon = Surgeon.objects.get( name = item.surgeon ) 
        room = OperatingRoom.objects.get (name = item.room )
        anesthesia_team = AnesthesiaTeam.objects.get ( name = item.anesthesia_team )




        ScheduleItem.objects.create(

            plan= plan,
            surgery_request = surgery_request,
            surgeon = surgeon,
            room = room,
            anesthesia_team = anesthesia_team,
            day_index = item.day_index ,
            start_slot = item.start_slot,
            end_slot = item.end_slot,

        )


    return plan 