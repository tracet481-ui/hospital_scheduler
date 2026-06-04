from scheduling.services.backtracking.dto import (
    Surgeon as AlgoSurgeon,
    OperatingRoom as AlgoOperatingRoom,
    AnesthesiaTeam as AlgoAnesthesiaTeam,
    SurgeryRequest as AlgoSurgeryRequest,
)

from scheduling.models import (
    Surgeon,
    OperatingRoom,
    AnesthesiaTeam,
    SurgeryRequest,
)


def load_scheduler_input():
    surgeons = [
        AlgoSurgeon(
            name=surgeon.name,
            specialty=surgeon.specialty.name,
            off_day=surgeon.off_day,
        )
        for surgeon in Surgeon.objects.select_related("specialty").all()
    ]

    rooms = [
        AlgoOperatingRoom(
            name=room.name,
            room_type=room.room_type.name if room.room_type else "Hibrit",
        )
        for room in OperatingRoom.objects.select_related("room_type").all()
    ]

    anesthesia_teams = [
        AlgoAnesthesiaTeam(name=team.name)
        for team in AnesthesiaTeam.objects.all()
    ]

    surgeries = []

    for request in SurgeryRequest.objects.select_related(
        "patient",
        "surgery_type",
        "surgery_type__required_specialty",
    ).all():
        compatible_rooms = list(
            request.surgery_type.compatible_rooms.values_list("name", flat=True)
        )

        required_room = None

        if len(compatible_rooms) == 1:
            required_room = compatible_rooms[0]

        surgeries.append(
            AlgoSurgeryRequest(
                patient=request.patient.code,
                operation=request.surgery_type.name,
                duration=request.surgery_type.duration_slots,
                priority=request.get_priority_display(),
                required_specialty=request.surgery_type.required_specialty.name,
                required_room=required_room,
            )
        )

    return surgeons, rooms, anesthesia_teams, surgeries