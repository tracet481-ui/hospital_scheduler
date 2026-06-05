from ortools.sat.python import cp_model

from scheduling.services.backtracking.dto import ScheduleItem

TOTAL_SLOTS = 20


class CPScheduler:

    def __init__(self, surgeons, rooms, anesthesia_teams, surgeries, ) :

        self.surgeons = surgeons
        self.rooms = rooms
        self.anesthesia_teams = anesthesia_teams
        self.surgeries = surgeries



    def generate  (self) :

        model = cp_model.CpModel()

        start_vars = {}
        room_vars = {}
        surgeon_vars = {}
        anesthesia_vars = {}


        for surgery_index, surgery in enumerate(self.surgeries):

            latest_start = TOTAL_SLOTS - surgery.duration
            
            
            start_vars[surgery_index] = model.NewIntVar(
                0,
                latest_start,
                f"start_{surgery_index}",
            )



            room_vars[surgery_index] = model.NewIntVar(
                0,
                len(self.rooms) - 1,
                f"room_{surgery_index}",
            )


            surgeon_vars[surgery_index] = model.NewIntVar(
                0,
                len(self.surgeons) - 1,
                f"surgeon_{surgery_index}",
            )


            anesthesia_vars[surgery_index] = model.NewIntVar(
                0,
                len(self.anesthesia_teams) - 1,
                f"anesthesia_{surgery_index}",
            )


        for surgery_index, surgery in enumerate (self.surgeries):

            compatible_surgeon_indexes = []

            for surgeon_index, surgeon in enumerate(self.surgeons):
                if surgeon.specialty == surgery.required_specialty:
                    compatible_surgeon_indexes.append(surgeon_index)


            model.AddAllowedAssignments(
                [surgeon_vars[surgery_index]],
                [(index,) for index in compatible_surgeon_indexes]
            )



        for surgery_index, surgery in enumerate(self.surgeries) :

            compatible_room_indexes= []

            for room_index, room in enumerate(self.rooms) :
                
                if room.name in surgery.compatible_rooms :
                    compatible_room_indexes.append(room_index)


             
                
            model.AddAllowedAssignments(
                [room_vars[surgery_index]],
                [(index,) for index in compatible_room_indexes]
            )





        for i in range (len(self.surgeries)):
            for j in range (i + 1 , len(self.surgeries)):
                surgery_i = self.surgeries[i]
                surgery_j = self.surgeries[j]


                same_room = model.NewBoolVar(f"same_room_{i}_{j}")
                same_surgeon = model.NewBoolVar(f"same_Surgeon_{i}_{j}")
                same_anesthesia = model.NewBoolVar(f"same_anesthesia_{i}_{j}")


                i_before_j =  model.NewBoolVar(f"i_before_j_{i}_{j}")
                j_before_i = model.NewBoolVar(f"j_before_i_{i}_{j}")


                model.Add(room_vars[i] == room_vars[j]).OnlyEnforceIf(same_room)
                model.Add(room_vars[i] != room_vars[j]).OnlyEnforceIf(same_room.Not())



                model.Add(surgeon_vars[i] == surgeon_vars[j]).OnlyEnforceIf(same_surgeon)
                model.Add(surgeon_vars[i] != surgeon_vars[j]).OnlyEnforceIf(same_surgeon.Not())


                model.Add(anesthesia_vars[i] == anesthesia_vars[j]).OnlyEnforceIf(same_anesthesia)
                model.Add(anesthesia_vars[i] != anesthesia_vars[j]).OnlyEnforceIf(same_anesthesia.Not())

                
                model.Add(start_vars[i] + surgery_i.duration <= start_vars[j] ).OnlyEnforceIf(i_before_j)
                model.Add(start_vars[j] + surgery_j.duration <= start_vars[i] ).OnlyEnforceIf(j_before_i)


                same_resource = model.NewBoolVar(f"same_resource_{i}_{j}")

                model.AddBoolOr([
                    same_room,
                    same_surgeon,
                    same_anesthesia,
                ]).OnlyEnforceIf(same_resource)


                model.AddBoolAnd([
                    same_room.Not(),
                    same_surgeon.Not(),
                    same_anesthesia.Not(),
                ]).OnlyEnforceIf(same_resource.Not())
                

                model.AddBoolOr([
                    i_before_j,
                    j_before_i,

                ]).OnlyEnforceIf(same_resource)


                


                
                
                






        


        



        #değişkenler kurulacak

        solver = cp_model.CpSolver()
        status = solver.Solve(model)


        if status not in [cp_model.OPTIMAL, 
                          cp_model.FEASIBLE] :
            return None
        

        schedule = []


        for surgery_index, surgery in enumerate(
            self.surgeries):
            start_slot = solver.Value(start_vars[surgery_index])
            end_slot = start_slot + surgery.duration


            room_index = solver.value(room_vars[surgery_index])
            surgeon_index = solver.value(surgeon_vars[surgery_index])
            anesthesia_index = solver.value(anesthesia_vars[surgery_index])



            schedule.append(
                ScheduleItem(
                    patient = surgery.patient,
                    operation = surgery.operation,
                    start_slot = start_slot,
                    end_slot = end_slot,
                    room = self.rooms[room_index].name,
                    surgeon = self.surgeons[surgeon_index].name,
                    anesthesia_team = self.anesthesia_teams[anesthesia_index].name,


                )
            )   

        #solver in sonucunu dto scheduleIteM a çeviriyoeuz

        return schedule