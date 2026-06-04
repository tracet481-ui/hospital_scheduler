from scheduler.models import ScheduleItem
from scheduler.constraints import TOTAL_SLOTS, can_place_surgery
from scheduler.utils import priority_value


class BacktrackingScheduler:

    def __init__(
        self,
        surgeons,
        rooms,
        anesthesia_teams,
        surgeries,
        planning_day,
    ):
        self.surgeons = surgeons
        self.rooms = rooms
        self.anesthesia_teams = anesthesia_teams
        self.planning_day = planning_day

        self.surgeries = sorted(
            surgeries, key=lambda surgery: priority_value(surgery.priority)
        )

        self.schedule = []

        self.room_occupancy = {room.name: [None] * TOTAL_SLOTS for room in rooms}

        self.surgeon_occupancy = {
            surgeon.name: [None] * TOTAL_SLOTS for surgeon in surgeons
        }

        self.anesthesia_occupancy = {
            team.name: [None] * TOTAL_SLOTS for team in anesthesia_teams
        }

    def generate(self):

        succcess = self._backtrack(0)

        if not succcess:
            return None

        return self.schedule

    def _backtrack(self, surgery_index):
        if surgery_index == len(self.surgeries):
            return True

        surgery = self.surgeries[surgery_index]

        for start_slot in range(TOTAL_SLOTS):
            for room in self.rooms:
                for surgeon in self.surgeons:
                    for anesthesia_team in self.anesthesia_teams:

                        if can_place_surgery(
                            surgery=surgery,
                            surgeon=surgeon,
                            room=room,
                            anesthesia_team=anesthesia_team,
                            start_slot=start_slot,
                            planning_day=self.planning_day,
                            room_occupancy=self.room_occupancy,
                            surgeon_occupancy=self.surgeon_occupancy,
                            anesthesia_occupancy=self.anesthesia_occupancy,
                        ):

                            self._place_surgery(
                                surgery,
                                surgeon,
                                room,
                                anesthesia_team,
                                start_slot,
                            )

                            if self._backtrack(surgery_index + 1):
                                return True

                            self._remove_surgery(
                                surgery,
                                surgeon,
                                room,
                                anesthesia_team,
                                start_slot,
                            )

        return False

    def _place_surgery(self, surgery, surgeon, room, anesthesia_team, start_slot):
        end_slot = start_slot + surgery.duration

        item = ScheduleItem(
            patient=surgery.patient,
            operation=surgery.operation,
            start_slot=start_slot,
            end_slot=end_slot,
            room=room.name,
            surgeon=surgeon.name,
            anesthesia_team=anesthesia_team.name,
        )

        self.schedule.append(item)

        for slot in range(start_slot, end_slot):
            self.room_occupancy[room.name][slot] = surgery.patient
            self.surgeon_occupancy[surgeon.name][slot] = surgery.patient
            self.anesthesia_occupancy[anesthesia_team.name][slot] = surgery.patient

    def _remove_surgery(self, surgery, surgeon, room, anesthesia_team, start_slot):
        end_slot = start_slot + surgery.duration

        self.schedule.pop()

        for slot in range(start_slot, end_slot):
            self.room_occupancy[room.name][slot] = None
            self.surgeon_occupancy[surgeon.name][slot] = None
            self.anesthesia_occupancy[anesthesia_team.name][slot] = None
