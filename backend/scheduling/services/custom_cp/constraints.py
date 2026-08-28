# # scheduling/services/custom_cp/constraints.py


DAYS = [
    "Pazartesi",
    "Salı",
    "Çarşamba",
    "Perşembe",
    "Cuma",
]



def fits_working_hours(

    surgery,
    value,
    slots_per_day,
        
):
    return  (
            value.start_slot + surgery.duration
            <= slots_per_day
    )

# --------------------------------
# room
# --------------------------------


def is_room_compatible(

    surgery,
    value,
        
):     
    return (
            value.room 
            in surgery.compatible_rooms
    )



# --------------------------------
# surgeon specialty
# --------------------------------



def has_required_specialty (

    surgery,
    surgeons_by_name,
    value,
        
):  
    surgeon = surgeons_by_name[
                                value.surgeon]

    return (

        surgeon.specialty
        ==  surgery.required_specialty

    )



# ----------------------------------
# off day
# ----------------------------------


def surgeon_is_working(

    surgeons_by_name,
    value,
        
):  
    surgeon = surgeons_by_name[
                    value.surgeon]

    day_name = DAYS[
        value.day
    ]

    return (
            surgeon.off_day 
            != value.day)




# -----------------------------------
# occupancy
# -----------------------------------

# -------------------------------------
# slots
# -------------------------------------

def slots_are_available(

    occupancy,
    resource_name,
    day,
    start_slot,
    duration,
        
):
    end_slot = (
            start_slot + duration)

    for slot in range (
                start_slot, 
                end_slot
                ):

        if (
            occupancy[
                    resource_name][day][slot] 
                    is not None
                    ):
            return False

    return True


# -------------------------------------
# rooms
# -------------------------------------

def room_is_available(

    state,
    surgery,
    value,
        
):
    return slots_are_available(

        occupancy=state.room_occupancy,
        resource_name=value.room,
        day=value.day,
        start_slot=value.start_slot,
        duration=surgery.duration,

    )


# -------------------------------------
# surgeons
# -------------------------------------

def surgeon_is_available(
    state,
    surgery,
    value,
):

    return slots_are_available(
        occupancy=state.surgeon_occupancy,
        resource_name=value.surgeon,
        day=value.day,
        start_slot=value.start_slot,
        duration=surgery.duration,
    )


# -------------------------------------
# anesthesia
# -------------------------------------

def anesthesia_is_available(
    state,
    surgery,
    value,
):
    return slots_are_available(
        occupancy=state.anesthesia_occupancy,
        resource_name=value.anesthesia_team,
        day=value.day,
        start_slot=value.start_slot,
        duration=surgery.duration,
    )




def has_required_surgeon_rest   (

    surgery,
    value,
    state,
        
) :


    occupancy = state.surgeon_occupancy [

        value.surgeon

    ][value.day]


    start_slot = value.start_slot


    if start_slot == 0 :

        return True


    continuous_work = 0 


    slot = start_slot - 1


    while (

        slot >= 0
        and occupancy [slot] is not None

    ):

        continuous_work += 1

        slot -= 1


    if continuous_work >=4 :

        return False


    return True






# ---------------------------------------------
# rest valid control
# ---------------------------------------------

def surgeon_rest_is_valid (

    surgery,
    value,
    state,
        
):

    occupancy = state.surgeon_occupancy[

        value.surgeon

    ][value.day]

    start = value.start_slot
    end = start + surgery.duration


    simulated = occupancy.copy()

    for slot in range (start, end) :

        simulated [slot] = surgery.patient


    continuous_work = 0


    for slot in range   (len(simulated)) :

        if simulated [slot] is not None:

            continuous_work += 1

            continue


        if continuous_work >= 4:

            # çalışma bloğundan sonra gün bittiyse
            # en az bu boş slot rest görevi görür

            continuous_work = 0



        else :

            continuous_work = 0


    return True








# -------------------------------------
# rest rule
# -------------------------------------


def respects_rest_rule(
    state,
    surgery,
    value,
):


    occupancy = (
        state.surgeon_occupancy[
            value.surgeon
        ][value.day]
    )

    start_slot = value.start_slot

    end_slot = ( start_slot + surgery.duration )   


    # -------------------------------------------------
    # sol taraf
    # -------------------------------------------------

    continuous_before = 0

    slot = start_slot - 1

    while (

        slot >= 0
        and
        occupancy [slot] is not None

    ): 

        continuous_before += 1

        slot -= 1


    if continuous_before >= 4 :

        return False


    # -------------------------------------------------
    # sağ taraf
    # -------------------------------------------------

    continuous_after = 0

    slot = end_slot

    while (

        slot < len (occupancy)
        and
        occupancy[slot] is not None

    ):
            
        continuous_after += 1

        slot -= 1


    if (

        surgery.duration >= 4 
        and 
        continuous_after > 0

    ):


        return False


    return True




# ---------------------------------------
# control
# ---------------------------------------



def is_consistent(
    surgery,
    value,
    state,
    surgeons_by_name,
    slots_per_day,
):

    if not fits_working_hours(
        surgery=surgery,
        value=value,
        slots_per_day=slots_per_day,
    ):
        return False


    if not is_room_compatible(
        surgery=surgery,
        value=value,
    ):
        return False


    if not has_required_specialty(
        surgery=surgery,
        surgeons_by_name=surgeons_by_name,
        value=value,
    ):
        return False


    if not surgeon_is_working(
        surgeons_by_name=surgeons_by_name,
        value=value,
    ):
        return False


    if not room_is_available(
        state=state,
        surgery=surgery,
        value=value,
    ):
        return False


    if not surgeon_is_available(
        state=state,
        surgery=surgery,
        value=value,
    ):
        return False


    if not anesthesia_is_available(
        state=state,
        surgery=surgery,
        value=value,
    ):
        return False


    if not respects_rest_rule(
        state=state,
        surgery=surgery,
        value=value,
    ):
        return False


    return True
