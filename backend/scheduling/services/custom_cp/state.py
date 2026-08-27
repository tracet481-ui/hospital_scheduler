class SolverState:

    # ------------------------------------------
    # solver çalışma durumu
    # ------------------------------------------

    def __init__(
        self,
        surgeons,
        rooms,
        anesthesia_teams,
        total_days=5,
        slots_per_day=20,
    ):
        self.assignments = {}

        self.room_occupancy = {
            room.name: [
                [None for _ in range(slots_per_day)]
                for _ in range(total_days)
            ]
            for room in rooms
        }

        self.surgeon_occupancy = {
            surgeon.name: [
                [None for _ in range(slots_per_day)]
                for _ in range(total_days)
            ]
            for surgeon in surgeons
        }

        self.anesthesia_occupancy = {
            team.name: [
                [None for _ in range(slots_per_day)]
                for _ in range(total_days)
            ]
            for team in anesthesia_teams
        }



    # -----------------------------------------------------
    # assignments için 
    # -----------------------------------------------------


    def assign(
        self,
        surgery,
        value,
    ):

        self.assignments[
            surgery.patient
        ] = value

        day = value.day
        start = value.start_slot

        end = (
            start
            + surgery.duration
        )

        for slot in range(
            start,
            end,
        ):

            self.room_occupancy[
                value.room
            ][day][slot] = surgery.patient

            self.surgeon_occupancy[
                value.surgeon
            ][day][slot] = surgery.patient

            self.anesthesia_occupancy[
                value.anesthesia_team
            ][day][slot] = surgery.patient

    # ---------------------------------------------------
    # Geri alma
    # ---------------------------------------------------


    def unassign(
        self,
        surgery,
        value,
    ):

        self.assignments.pop(
            surgery.patient,
            None,
        )

        day = value.day
        start = value.start_slot

        end = (
            start
            + surgery.duration
        )

        for slot in range(
            start,
            end,
        ):

            self.room_occupancy[
                value.room
            ][day][slot] = None

            self.surgeon_occupancy[
                value.surgeon
            ][day][slot] = None

            self.anesthesia_occupancy[
                value.anesthesia_team
            ][day][slot] = None
    