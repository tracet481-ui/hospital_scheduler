TOTAL_SLOTS = 20


def has_enough_time(start_slot: int, duration: int) -> bool:
    return start_slot + duration <= TOTAL_SLOTS


def surgeon_matches_specialty(surgeon, surgery) -> bool:
    return surgeon.specialty == surgery.required_specialty


def room_is_compitable(room, surgery) -> bool:
    if surgery.required_room is not None:
        return room.name == surgery.required_room

    return room.room_type == surgery.required_specialty or room.room_type == "Hibrit"


def slots_are_free(
    occupancy: dict, resource_name: str, start_slot: int, duration: int
) -> bool:
    end_slot = start_slot + duration

    for slot in range(start_slot, end_slot):
        if occupancy[resource_name][slot] is not None:
            return False

    return True


def surgeon_has_required_rest(
    surgeon_occupancy: dict,
    surgeon_name: str,
    start_slot: int,
) -> bool:

    if start_slot == 0:
        return True

    previous_slot = start_slot - 1

    if surgeon_occupancy[surgeon_name][previous_slot] is None:
        return True

    previous_block_length = 0

    slot = previous_slot

    while slot >= 0 and surgeon_occupancy[surgeon_name][slot] is not None:
        previous_block_length += 1
        slot -= 1

    if previous_block_length >= 4:
        return False

    return True


def surgeon_is_avaiblable_on_day(
    surgeon,
    planning_day: str,
) -> bool:

    return surgeon.off_day != planning_day


def can_place_surgery(
    surgery,
    surgeon,
    room,
    anesthesia_team,
    start_slot: int,
    planning_day: str,
    room_occupancy: dict,
    surgeon_occupancy: dict,
    anesthesia_occupancy: dict,
) -> bool:

    if not has_enough_time(start_slot, surgery.duration):
        return False

    if not surgeon_is_avaiblable_on_day(surgeon, planning_day):
        return False

    if not surgeon_matches_specialty(
        surgeon,
        surgery,
    ):
        return False

    if not room_is_compitable(room, surgery):
        return False

    if not slots_are_free(room_occupancy, room.name, start_slot, surgery.duration):
        return False

    if not slots_are_free(
        surgeon_occupancy, surgeon.name, start_slot, surgery.duration
    ):
        return False

# --------------------------------------------------- surgeon rest

    if not surgeon_has_required_rest(
        surgeon_occupancy,
        surgeon.name,
        start_slot,
    ):

        return False


# surgeon rest   --------------------------------------------------- 


    if not slots_are_free(
        anesthesia_occupancy, anesthesia_team.name, start_slot, surgery.duration
    ):
        return False

    return True
