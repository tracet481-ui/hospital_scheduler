from scheduling.models import (

    SchedulePlan,
    ScheduleItem,
    SurgeryRequest,
    Surgeon,
    OperatingRoom,
    AnesthesiaTeam,


)


def save_schedule_plan(
    schedule,
    algorithm_name,
    planning_day,
    score,
    score_details=None,
    simulation_results=None,
):
    score_details = score_details or {}
    simulation_results = simulation_results or []

    # Yeni rapor yapısı geldiyse buradan oku.
    if "losses" in score_details:
        losses = score_details.get("losses", {})

        priority_score = (
            score_details
            .get("priority", {})
            .get("score", 0)
        )

        day_balance_penalty = (
            losses
            .get("day_balance", {})
            .get("loss", 0)
        )

        anesthesia_balance_penalty = (
            losses
            .get("anesthesia_balance", {})
            .get("loss", 0)
        )

        room_idle_penalty = (
            losses
            .get("room_idle", {})
            .get("loss", 0)
        )

        surgeon_idle_penalty = (
            losses
            .get("surgeon_idle", {})
            .get("loss", 0)
        )

    # Eski düz score_summary yapısı geldiyse buradan oku.
    else:
        priority_score = score_details.get(
            "priority_score",
            0,
        )

        day_balance_penalty = score_details.get(
            "day_balance_penalty",
            0,
        )

        anesthesia_balance_penalty = score_details.get(
            "anesthesia_balance_penalty",
            0,
        )

        room_idle_penalty = score_details.get(
            "room_idle_penalty",
            0,
        )

        surgeon_idle_penalty = score_details.get(
            "surgeon_idle_penalty",
            0,
        )

    plan = SchedulePlan.objects.create(
        planning_day=planning_day,
        algorithm_name=algorithm_name,
        score=score,
        is_feasible=True,
        simulation_results=simulation_results,

        # Yeni JSONField
        score_details=score_details,

        # Mevcut ayrı kolonlar
        priority_score=priority_score,
        day_balance_penalty=day_balance_penalty,
        anesthesia_balance_penalty=anesthesia_balance_penalty,
        room_idle_penalty=room_idle_penalty,
        surgeon_idle_penalty=surgeon_idle_penalty,

        success_rate=score_details.get(
            "success_rate",
            0,
        ),
    )

    for item in schedule:
        surgery_request = SurgeryRequest.objects.get(
            patient__code=item.patient,
            surgery_type__name=item.operation,
        )

        surgeon = Surgeon.objects.get(
            name=item.surgeon,
        )

        room = OperatingRoom.objects.get(
            name=item.room,
        )

        anesthesia_team = AnesthesiaTeam.objects.get(
            name=item.anesthesia_team,
        )

        ScheduleItem.objects.create(
            plan=plan,
            surgery_request=surgery_request,
            surgeon=surgeon,
            room=room,
            anesthesia_team=anesthesia_team,
            day_index=item.day_index,
            start_slot=item.start_slot,
            end_slot=item.end_slot,
        )

    return plan








# def save_schedule_plan (
#         schedule,
#         algorithm_name,
#         planning_day,
#         score,
#         score_details = None,
#         simulation_results = None,
# ) :
    
#     score_details = score_details or {}
#     simulation_results = simulation_results or []
    
#     plan = SchedulePlan.objects.create(
#         planning_day = planning_day,
#         algorithm_name = algorithm_name,
#         score = score,
#         is_feasible = True,
#         simulation_results = simulation_results,


#         priority_score = score_details.get("priority_score", 0),
#         day_balance_penalty = score_details.get("day_balance_penalty", 0),
#         anesthesia_balance_penalty = score_details.get("anesthesia_balance_penalty", 0),
#         room_idle_penalty = score_details.get("room_idle_penalty", 0),
#         surgeon_idle_penalty = score_details.get("surgeon_idle_penalty", 0),
#         success_rate = score_details.get("success_rate", 0),

#         # simulation_results = simulation_results,

#     )


#     for item in schedule :

#         surgery_request = SurgeryRequest.objects.get(

#             patient__code=item.patient,
#             surgery_type__name = item.operation,

#         )



#         surgeon = Surgeon.objects.get( name = item.surgeon ) 
#         room = OperatingRoom.objects.get (name = item.room )
#         anesthesia_team = AnesthesiaTeam.objects.get ( name = item.anesthesia_team )




#         ScheduleItem.objects.create(

#             plan= plan,
#             surgery_request = surgery_request,
#             surgeon = surgeon,
#             room = room,
#             anesthesia_team = anesthesia_team,
#             day_index = item.day_index ,
#             start_slot = item.start_slot,
#             end_slot = item.end_slot,

#         )


#     return plan 