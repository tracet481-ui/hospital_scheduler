from ortools.sat.python import cp_model

from scheduling.services.backtracking.dto import ScheduleItem

from scheduling.services.scoring import calculate_schedule_score



DAYS = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", ]

TOTAL_SLOTS = 20


class CPScheduler:

    def __init__(self, surgeons, rooms, anesthesia_teams, surgeries, planning_day ) :

        self.surgeons = surgeons
        self.rooms = rooms
        self.anesthesia_teams = anesthesia_teams
        self.surgeries = surgeries
        self.planning_day = planning_day



    def generate  (self) :

        model = cp_model.CpModel()

        start_vars = {}
        room_vars = {}
        surgeon_vars = {}
        anesthesia_vars = {}
        day_vars = {}




        for surgery_index, surgery in enumerate(self.surgeries):

            latest_start = TOTAL_SLOTS - surgery.duration


            day_vars[surgery_index] = model.NewIntVar(


                0,
                4,
                f"day_{surgery_index}",


            )
            
            
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
                # if surgeon.specialty == surgery.required_specialty:
                #     compatible_surgeon_indexes.append(surgeon_index)
                
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





        for i in range(len(self.surgeries)):
            for j in range(i + 1, len(self.surgeries)):
                surgery_i = self.surgeries[i]
                surgery_j = self.surgeries[j]

                same_day = model.NewBoolVar(f"same_day_{i}_{j}")
                same_room = model.NewBoolVar(f"same_room_{i}_{j}")
                same_surgeon = model.NewBoolVar(f"same_surgeon_{i}_{j}")
                same_anesthesia = model.NewBoolVar(f"same_anesthesia_{i}_{j}")

                i_before_j = model.NewBoolVar(f"i_before_j_{i}_{j}")
                j_before_i = model.NewBoolVar(f"j_before_i_{i}_{j}")

                # Aynı gün mü?
                model.Add(day_vars[i] == day_vars[j]).OnlyEnforceIf(same_day)
                model.Add(day_vars[i] != day_vars[j]).OnlyEnforceIf(same_day.Not())

                # Aynı oda mı?
                model.Add(room_vars[i] == room_vars[j]).OnlyEnforceIf(same_room)
                model.Add(room_vars[i] != room_vars[j]).OnlyEnforceIf(same_room.Not())

                # Aynı cerrah mı?
                model.Add(surgeon_vars[i] == surgeon_vars[j]).OnlyEnforceIf(same_surgeon)
                model.Add(surgeon_vars[i] != surgeon_vars[j]).OnlyEnforceIf(same_surgeon.Not())

                # Aynı anestezi ekibi mi?
                model.Add(anesthesia_vars[i] == anesthesia_vars[j]).OnlyEnforceIf(same_anesthesia)
                model.Add(anesthesia_vars[i] != anesthesia_vars[j]).OnlyEnforceIf(same_anesthesia.Not())

                rest_after_i = 1 if surgery_i.duration >= 4 else 0
                rest_after_j = 1 if surgery_j.duration >= 4 else 0

                # ---------------------------------------------------------
                # HAFTALIK ÇAKIŞMA KURALI
                # ---------------------------------------------------------
                # Aynı gün + aynı oda ise ameliyatlar çakışamaz.
                model.AddBoolOr([
                    i_before_j,
                    j_before_i,
                ]).OnlyEnforceIf([same_day, same_room])

                model.Add(
                    start_vars[i] + surgery_i.duration <= start_vars[j]
                ).OnlyEnforceIf([same_day, same_room, i_before_j])

                model.Add(
                    start_vars[j] + surgery_j.duration <= start_vars[i]
                ).OnlyEnforceIf([same_day, same_room, j_before_i])

                # Aynı gün + aynı anestezi ekibi ise ameliyatlar çakışamaz.
                model.AddBoolOr([
                    i_before_j,
                    j_before_i,
                ]).OnlyEnforceIf([same_day, same_anesthesia])

                model.Add(
                    start_vars[i] + surgery_i.duration <= start_vars[j]
                ).OnlyEnforceIf([same_day, same_anesthesia, i_before_j])

                model.Add(
                    start_vars[j] + surgery_j.duration <= start_vars[i]
                ).OnlyEnforceIf([same_day, same_anesthesia, j_before_i])

                # Aynı gün + aynı cerrah ise ameliyatlar çakışamaz.
                # 4+ slot ameliyattan sonra 1 slot dinlenme eklenir.
                model.AddBoolOr([
                    i_before_j,
                    j_before_i,
                ]).OnlyEnforceIf([same_day, same_surgeon])

                model.Add(
                    start_vars[i] + surgery_i.duration + rest_after_i <= start_vars[j]
                ).OnlyEnforceIf([same_day, same_surgeon, i_before_j])

                model.Add(
                    start_vars[j] + surgery_j.duration + rest_after_j <= start_vars[i]
                ).OnlyEnforceIf([same_day, same_surgeon, j_before_i])




        daily_load_vars = []


        for day_index in range(5) :

            day_usage_terms = []

            for surgery_index, surgery  in enumerate(self.surgeries) :

                is_on_day = model.NewBoolVar(

                    f"surgery_{surgery_index}_on_day_{day_index}"

                )

                model.Add(

                    day_vars [surgery_index] == day_index

                ).OnlyEnforceIf(is_on_day)


                model.Add(

                    day_vars[surgery_index] != day_index

                ).OnlyEnforceIf(is_on_day.Not())


                usage = model.NewIntVar(

                    0,
                    surgery.duration,
                    f"usage_s{surgery_index}_d{day_index}"

                )

                model.Add(

                    usage == surgery.duration

                ).OnlyEnforceIf(is_on_day)


                model.Add(

                    usage == 0

                ).OnlyEnforceIf(is_on_day.Not())


                day_usage_terms.append(usage)


            daily_load = model.NewIntVar(

                0,
                100,
                f"daily_load_{day_index}"

            )



            model.Add(

                daily_load == sum(day_usage_terms)

            )



            daily_load_vars.append(daily_load)


        max_daily_load = model.NewIntVar(

            0,
            100,
            "max_daily_load"


        )


        # anestezi ekibi  yoğunluğu ölçeceğiz


        anesthesia_load_vars= []

        for team_index in range(len(self.anesthesia_teams)) :


            team_usage_terms = []


            for surgery_index, surgery in enumerate(self.surgeries):

                assigned_to_team = model.NewBoolVar(

                    f"surgery_{surgery_index}_team_{team_index}"

                )


                model.Add(

                    anesthesia_vars[surgery_index] == team_index
                ).OnlyEnforceIf(assigned_to_team)


                model.Add(

                    anesthesia_vars[surgery_index] != team_index

                ).OnlyEnforceIf(assigned_to_team.Not())


                usage = model.NewIntVar(

                    0,
                    surgery.duration,
                    f"team_usage_s{surgery_index}_t{team_index}"
                )



                model.Add(

                    usage == surgery.duration
                ).OnlyEnforceIf(assigned_to_team)


                model.Add(

                    usage == 0
                ).OnlyEnforceIf(assigned_to_team.Not())


                team_usage_terms.append(usage)

            
            team_load = model.NewIntVar(

                0,
                100,
                f"team_load_{team_index}"


            )


            model.Add(

                team_load == sum(team_usage_terms)


            )



            anesthesia_load_vars.append(team_load)



        max_anesthesia_load = model.NewIntVar(

            0,
            100,
            "max_anesthesia_load"


        )

        min_anesthesia_load  = model.NewIntVar(

            0,
            100,
            "min_anesthesia_load"


        )


        model.AddMaxEquality(

            max_anesthesia_load,
            anesthesia_load_vars,


        )


        model.AddMinEquality(

            min_anesthesia_load,
            anesthesia_load_vars,


        )



        anesthesia_balance_penalty = model.NewIntVar(

            0,
            100,
            "anesthesia_balance_penalty"


        )


        model.Add(

            anesthesia_balance_penalty ==
            max_anesthesia_load -
            min_anesthesia_load


        )








            


        min_daily_load = model.NewIntVar(

            0,
            100,
            "min_daily_load"

        )



        model.AddMaxEquality(

            max_daily_load,
            daily_load_vars,


        )



        model.AddMinEquality(

            min_daily_load,
            daily_load_vars,


        )



        day_balance_penalty =  model.NewIntVar(

            0,
            100,
            "day_balance_pealty",


        )


        model.Add(

            day_balance_penalty == max_daily_load - min_daily_load


        )














        objective_terms = []

        for surgery_index, surgery in enumerate(self.surgeries) :

            global_start = day_vars[surgery_index] * TOTAL_SLOTS + start_vars[surgery_index]

            if surgery.priority == "Kritik":
                weight = 100


            elif surgery.priority == "Yüksek":
                weight = 50


            elif surgery.priority == "Orta":
                weight = 20


            else:
                weight = 5


            objective_terms.append(global_start * weight)

            
        
        # model.Minimize(sum(objective_terms))
        #  penalty ve weight çarpımı ile toplanır. min sonuç optimal sonuçtur



        DAY_BALANCE_WEIGHT = 300
        ANESTHESIA_BALANCE_WEIGHT = 120

        

        model.Minimize(
            sum(objective_terms) +
            day_balance_penalty *
            DAY_BALANCE_WEIGHT
        )


        model.minimize(


            sum(objective_terms) +

            day_balance_penalty *

            DAY_BALANCE_WEIGHT +

            anesthesia_balance_penalty *

            ANESTHESIA_BALANCE_WEIGHT


        )



        

        # for surgery_index, surgery in enumerate(self.surgeries) :

        #     for surgeon_index, surgeon in enumerate(self.surgeons)  : 

        #         surgeon_assigned = model.NewBoolVar(

        #             f"surgeon_{surgeon_index}_assigned_to_{surgery_index}"
        #         )


        #         model.Add(surgeon_vars[surgery_index]  ==  surgery_index).OnlyEnforceIf(
        #                                                                 surgeon_assigned
        #                                                                 )
                

        #         model.Add(surgeon_vars[surgery_index]  != surgeon_index ).OnlyEnforceIf(
        #                                                                 surgeon_assigned.Not()
        #                                                                 )
                

        #         off_day_index = DAYS.index(surgeon.off_day)

        #         model.Add(day_vars[surgery_index]  !=  off_day_index).OnlyEnforceIf(
        #                                                             surgeon_assigned
        #                                                             )

        


        for surgery_index, surgery in enumerate(self.surgeries):
            allowed_pairs = []

            for surgeon_index, surgeon in enumerate(self.surgeons):
                if surgeon.specialty != surgery.required_specialty:
                    continue

                for day_index, day_name in enumerate(DAYS):
                    if surgeon.off_day != day_name:
                        allowed_pairs.append((surgeon_index, day_index))

            model.AddAllowedAssignments(
                [surgeon_vars[surgery_index], day_vars[surgery_index]],
                allowed_pairs
            )



        #değişkenler kurulacak

        solver = cp_model.CpSolver()

        # CP-SAT optimizasyonu bazen optimal olduğunu kanıtlamak için uzun süre arar.
        # Bu yüzden süre limiti koyuyoruz; süre bitince bulduğu en iyi FEASIBLE planı döndürür.
        solver.parameters.max_time_in_seconds = 10
        solver.parameters.num_search_workers = 8
        solver.parameters.log_search_progress = True

        print("CP-SAT çözüm arıyor...")
        status = solver.Solve(model)
        print("CP-SAT status:", solver.StatusName(status))


        if status not in [cp_model.OPTIMAL, 
                          cp_model.FEASIBLE] :
            return None



        print("\nDAY LOADS")
        print("===========")

        for day in range(5) :
            print(
                DAYS[day_index],
                solver.Value(daily_load_vars[day_index])
            )

        print("Day balance penalty : ", solver.Value(day_balance_penalty))



        print("\n ANESTHESIA LOADS ")
        print("====================")


        for team_index, team in enumerate(self.anesthesia_teams):


            print(

                team.name,
                solver.Value(

                    anesthesia_load_vars[team_index]
                )
            )


        print(

            "Anesthesia penalty : ",
            solver.Value(

                anesthesia_balance_penalty
            )


        )
        



        schedule = []


        total_score = 0



        for surgery_index, surgery in enumerate(
            self.surgeries):


            start_slot = solver.Value(start_vars[surgery_index])
            end_slot = start_slot + surgery.duration
            day_index = solver.Value(day_vars[surgery_index])



            if surgery.priority == "Kritik" :
                contribution = (20 - start_slot ) * 100


            elif surgery.priority == "Yüksek" :
                contribution = (20 - start_slot ) * 50


            
            elif surgery.priority == "Orta" :
                contribution = (20 - start_slot ) * 20


            else :
                contribution = (20 - start_slot ) * 5


            total_score += contribution


            print(

                f"{ surgery.operation :20} "
                f"{ surgery.priority :10}"
                f"day = { DAYS[day_index] :10} "
                f"start = { start_slot :2} "
                f"score =+ { contribution }"

            ) 


            room_index = solver.Value(room_vars[surgery_index])
            surgeon_index = solver.Value(surgeon_vars[surgery_index])
            anesthesia_index = solver.Value(anesthesia_vars[surgery_index])



            schedule.append(
                ScheduleItem(
                    patient = surgery.patient,
                    operation = surgery.operation,
                    day_index = day_index,
                    start_slot = start_slot,
                    end_slot = end_slot,
                    room = self.rooms[room_index].name,
                    surgeon = self.surgeons[surgeon_index].name,
                    anesthesia_team = self.anesthesia_teams[anesthesia_index].name,


                )
            )   


        print("\n==================")
        print ("TOTAL_SCORE = ", total_score)
        print("==================\n")

       # totalscorehesaplama kısmı ( scoring te tanımladık burdan işliyoruz) 


        total_score, score_details = calculate_schedule_score(
                schedule=schedule,
                surgeries=self.surgeries,
        )


        print("\nSCORE DETAILS")
        print("==============")

        # for detail in score_details : 

        #     print (

        #         f"{ detail['patient']} - "
        #         f"{ detail['operation'] :20} "
        #         f"{ detail['priority'] :10} "
        #         f"start= { detail['start_slot'] :2} "
        #         f"score=+{detail['score']} "
 
        #     )



        
        print("==================")
        print("TOTAL SCORE: ", total_score) 
        print("===================\n")


        #solver in sonucunu dto scheduleIteM a çeviriyoeuz

        return schedule