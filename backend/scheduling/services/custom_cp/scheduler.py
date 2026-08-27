from scheduling.services.backtracking.dto import ScheduleItem

from .domains import build_domains
from .state import SolverState
from .constraints import is_consistent

from .heuristics import (

    select_unassigned_surgery,
    order_domain_values,

)

from .propagation import forward_check



TOTAL_DAYS = 5

SLOTS_PER_DAY = 20



class CustomCPScheduler :

    def __init__(

        self,
        surgeons,
        rooms,
        anesthesia_teams,
        surgeries,
        planning_day,
        soft_constraints = None,
            
    ):

        self.surgeons = surgeons
        self.rooms = rooms
        self.anesthesia_teams = anesthesia_teams
        self.surgeries = surgeries
        self.planning_day = planning_day


        self.soft_constraints = (

            soft_constraints or {}

        )


        self.surgeons_by_name = {

            surgeon.name : surgeon
            for surgeon in surgeons 

        }


        self.state = None


        self.nodes_visited = 0
        self.backtrack_count = 0
        self.pruned_branches = 0


    def generate (self) :


        domains = build_domains (

            surgeries = self.surgeries,
            surgeons = self.surgeons,
            anesthesia_teams = self.anesthesia_teams,
            days_count = TOTAL_DAYS,
            slots_per_day = SLOTS_PER_DAY,

        )



        print("\nDOMAIN DEBUG")
        print("============")
    
        print(
            "Surgery count:",
            len(self.surgeries),
        )
    
        print(
            "Domain count:",
            len(domains),
        )
    
        for surgery in self.surgeries[:10]:
    
            print(
                surgery.patient,
                "->",
                len(
                    domains.get(
                        surgery.patient,
                        [],
                    )
                ),
                "values",
            )




        self.state = SolverState(
            surgeons=self.surgeons,
            rooms=self.rooms,
            anesthesia_teams=self.anesthesia_teams,
            total_days=TOTAL_DAYS,
            slots_per_day=SLOTS_PER_DAY,
        )


        success = self._search (

            state = self.state,
            domains = domains,

        )


        if not success :


            print("\nCUSTOM CP")
            print("===========")
            print("No feasible solution")
            print(
                "Nodes visited:",
                self.nodes_visited,
            )

            print(
                "Backtracks:",
                self.backtrack_count,
                  )

            print (
                "Pruned branches:",
                self.pruned_branches,
            )


            return None


        schedule = self._build_schedule(

            self.state.assignments

        )


        print("\nCUSTOM CP")
        print("===========")
        print("Feasible")
        print(
            "Nodes visited:",
            self.nodes_visited,
        )

        print(
            "Backtracks:",
            self.backtrack_count,
                )

        print (
            "Pruned branches:",
            self.pruned_branches,
        )    


        return schedule




    

    





    def _search (

        self,
        state,
        domains,
            
    ) : 

        self.nodes_visited += 1


        

        if (

            len(state.assignments)
            ==
            len(self.surgeries  )

        ):

            return True


        surgery  = select_unassigned_surgery (

            surgeries = self.surgeries,
            assignments = state.assignments,
            domains = domains,

        )


        if surgery is None:

            return False


        values = order_domain_values (

            surgery = surgery,
            domains = domains,
            state = state,

        )


        for value in values :

            if not is_consistent (

                surgery = surgery,
                value = value,
                state = state,
                surgeons_by_name = 
                        self.surgeons_by_name,

                slots_per_day = SLOTS_PER_DAY,

            ):

                continue


            state.assign(

                surgery = surgery,
                value = value,

            )

            reduced_domains = forward_check(

                selected_surgery = surgery,
                surgeries = self.surgeries,
                domains = domains,
                state = state,
                surgeons_by_name = 
                        self.surgeons_by_name,
                slots_per_day = SLOTS_PER_DAY,

            )


            if reduced_domains is not None : 

                if self._search(

                    state = state,
                    domains = reduced_domains,
                    
                ):

                    return True


            else :

                self.pruned_branches += 1




            state.unassign(

                surgery = surgery,
                value = value,

            )

        #  Burası FOR'un DIŞINDA
        self.backtrack_count += 1





        return False



    def _build_schedule (

        self,
        assignments,
            
    ):

        schedule = []

        surgeries_by_patient = {

            surgery.patient : surgery

            for surgery in self.surgeries

        }


        for patient, value in assignments.items () :


            surgery =  surgeries_by_patient[

                patient

            ]


            start_slot = value.start_slot

            end_slot =  (

                start_slot + 
                surgery.duration    

            )


            schedule.append(

                ScheduleItem(

                    patient = surgery.patient,
                    operation = surgery.operation,
                    day_index = value.day,
                    start_slot = start_slot,
                    end_slot = end_slot,
                    room = value.room,
                    surgeon = value.surgeon,
                    anesthesia_team = 
                        value.anesthesia_team,

                )

            )


        schedule.sort   (

            key = lambda item :(

                item.day_index,
                item.start_slot,

            )

        )


        return schedule



# class SolverState:

#     def __init__(
#         self,
#         surgeons,
#         rooms,
#         anesthesia_teams,
#         total_days=5,
#         slots_per_day=20,
#     ):

#         self.assignments = {}

#         self.room_occupancy = {
#             room.name: [
#                 [None for _ in range(slots_per_day)]
#                 for _ in range(total_days)
#             ]
#             for room in rooms
#         }

#         self.surgeon_occupancy = {
#             surgeon.name: [
#                 [None for _ in range(slots_per_day)]
#                 for _ in range(total_days)
#             ]
#             for surgeon in surgeons
#         }

#         self.anesthesia_occupancy = {
#             team.name: [
#                 [None for _ in range(slots_per_day)]
#                 for _ in range(total_days)
#             ]
#             for team in anesthesia_teams
#         }


        



        