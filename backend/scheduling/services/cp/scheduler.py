from ortools.sat.python import cp_model

from scheduling.services.backtracking.dto import ScheduleItem
from scheduling.services.scoring import calculate_schedule_score

from scheduling.services.validators import validate_surgeon_rest_rule


DAYS = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma"]

TOTAL_SLOTS_PER_DAY = 20

DAY_BALANCE_WEIGHT = 300
ANESTHESIA_BALANCE_WEIGHT = 50
SURGEON_IDLE_WEIGHT = 10
MAX_CONTINUOUS_SURGEON_WORK = 4


class CPScheduler:

    def __init__(self, surgeons, rooms, anesthesia_teams, surgeries, planning_day):
        self.surgeons = surgeons
        self.rooms = rooms
        self.anesthesia_teams = anesthesia_teams
        self.surgeries = surgeries
        self.planning_day = planning_day

    def generate(self):

        model = cp_model.CpModel()

        start_vars = {}
        room_vars = {}
        surgeon_vars = {}
        anesthesia_vars = {}
        day_vars = {}

        # -------------------------
        # Decision Variables
        # -------------------------

        for surgery_index, surgery in enumerate(self.surgeries):

            latest_start = TOTAL_SLOTS_PER_DAY - surgery.duration

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

        # -------------------------
        # Surgeon specialty constraint
        # -------------------------

        for surgery_index, surgery in enumerate(self.surgeries):

            compatible_surgeon_indexes = []

            for surgeon_index, surgeon in enumerate(self.surgeons):
                if surgeon.specialty == surgery.required_specialty:
                    compatible_surgeon_indexes.append(surgeon_index)

            model.AddAllowedAssignments(
                [surgeon_vars[surgery_index]],
                [(index,) for index in compatible_surgeon_indexes],
            )

        # -------------------------
        # Room compatibility constraint
        # -------------------------

        for surgery_index, surgery in enumerate(self.surgeries):

            compatible_room_indexes = []

            for room_index, room in enumerate(self.rooms):
                if room.name in surgery.compatible_rooms:
                    compatible_room_indexes.append(room_index)

            model.AddAllowedAssignments(
                [room_vars[surgery_index]],
                [(index,) for index in compatible_room_indexes],
            )

        # -------------------------
        # Weekly overlap constraints
        # -------------------------

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

                model.Add(day_vars[i] == day_vars[j]).OnlyEnforceIf(same_day)
                model.Add(day_vars[i] != day_vars[j]).OnlyEnforceIf(same_day.Not())

                model.Add(room_vars[i] == room_vars[j]).OnlyEnforceIf(same_room)
                model.Add(room_vars[i] != room_vars[j]).OnlyEnforceIf(same_room.Not())

                model.Add(surgeon_vars[i] == surgeon_vars[j]).OnlyEnforceIf(same_surgeon)
                model.Add(surgeon_vars[i] != surgeon_vars[j]).OnlyEnforceIf(same_surgeon.Not())

                model.Add(anesthesia_vars[i] == anesthesia_vars[j]).OnlyEnforceIf(same_anesthesia)
                model.Add(anesthesia_vars[i] != anesthesia_vars[j]).OnlyEnforceIf(same_anesthesia.Not())

                rest_after_i = 1 if surgery_i.duration >= 4 else 0
                rest_after_j = 1 if surgery_j.duration >= 4 else 0

                # Same day + same room
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

                # Same day + same anesthesia team
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

                # Same day + same surgeon + rest rule
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

        

        ## ---------------------------------------------------


        # -------------------------
        # Surgeon rest hard constraint
        # -------------------------
        ##         # Kural:
        # Bir cerrah önceki 4 slot boyunca çalıştıysa,
        # aynı anda yeni ameliyata başlayamaz.
        #
        # Örnek:
        # 08:00-09:00 = 2 slot
        # 09:00-10:00 = 2 slot
        # 10:00'da yeni ameliyat başlayamaz.
        #
        # Ama 5-6 slotluk tek ameliyat yasaklanmaz.
        # Çünkü burada "çalışmaya devam etmek" değil,
        # "yeni ameliyata başlamak" engelleniyor.

        surgeon_work_terms = {}
        surgeon_start_terms = {}

        for surgeon_index in range(len(self.surgeons)):
            for day_index in range(5):
                for slot in range(TOTAL_SLOTS_PER_DAY):
                    surgeon_work_terms[(surgeon_index, day_index, slot)] = []
                    surgeon_start_terms[(surgeon_index, day_index, slot)] = []


        for surgery_index, surgery in enumerate(self.surgeries):

            latest_start = TOTAL_SLOTS_PER_DAY - surgery.duration

            for surgeon_index in range(len(self.surgeons)):
                for day_index in range(5):
                    for possible_start in range(latest_start + 1):

                        is_surgeon = model.NewBoolVar(
                            f"rest_s{surgery_index}_surgeon_{surgeon_index}_d{day_index}_t{possible_start}"
                        )

                        is_day = model.NewBoolVar(
                            f"rest_s{surgery_index}_day_{day_index}_surgeon_{surgeon_index}_t{possible_start}"
                        )

                        is_start = model.NewBoolVar(
                            f"rest_s{surgery_index}_start_{possible_start}_surgeon_{surgeon_index}_d{day_index}"
                        )

                        assigned_start = model.NewBoolVar(
                            f"rest_s{surgery_index}_assigned_{surgeon_index}_{day_index}_{possible_start}"
                        )

                        model.Add(
                            surgeon_vars[surgery_index] == surgeon_index
                        ).OnlyEnforceIf(is_surgeon)

                        model.Add(
                            surgeon_vars[surgery_index] != surgeon_index
                        ).OnlyEnforceIf(is_surgeon.Not())

                        model.Add(
                            day_vars[surgery_index] == day_index
                        ).OnlyEnforceIf(is_day)

                        model.Add(
                            day_vars[surgery_index] != day_index
                        ).OnlyEnforceIf(is_day.Not())

                        model.Add(
                            start_vars[surgery_index] == possible_start
                        ).OnlyEnforceIf(is_start)

                        model.Add(
                            start_vars[surgery_index] != possible_start
                        ).OnlyEnforceIf(is_start.Not())

                        model.AddImplication(assigned_start, is_surgeon)
                        model.AddImplication(assigned_start, is_day)
                        model.AddImplication(assigned_start, is_start)

                        model.AddBoolOr([
                            is_surgeon.Not(),
                            is_day.Not(),
                            is_start.Not(),
                            assigned_start,
                        ])

                        surgeon_start_terms[
                            (surgeon_index, day_index, possible_start)
                        ].append(assigned_start)

                        for work_slot in range(
                            possible_start,
                            possible_start + surgery.duration
                        ):
                            surgeon_work_terms[
                                (surgeon_index, day_index, work_slot)
                            ].append(assigned_start)


        for surgeon_index in range(len(self.surgeons)):
            for day_index in range(5):
                for slot in range(MAX_CONTINUOUS_SURGEON_WORK, TOTAL_SLOTS_PER_DAY):

                    previous_work_terms = []

                    for previous_slot in range(
                        slot - MAX_CONTINUOUS_SURGEON_WORK,
                        slot
                    ):
                        previous_work_terms.extend(
                            surgeon_work_terms[
                                (surgeon_index, day_index, previous_slot)
                            ]
                        )

                    current_start_terms = surgeon_start_terms[
                        (surgeon_index, day_index, slot)
                    ]

                    model.Add(
                        sum(previous_work_terms)
                        + sum(current_start_terms)
                        <= MAX_CONTINUOUS_SURGEON_WORK
                    )






        # -------------------------
        # Day balance objective vars
        # -------------------------

        daily_load_vars = []

        for day_index in range(5):

            day_usage_terms = []

            for surgery_index, surgery in enumerate(self.surgeries):

                is_on_day = model.NewBoolVar(
                    f"surgery_{surgery_index}_on_day_{day_index}"
                )

                model.Add(
                    day_vars[surgery_index] == day_index
                ).OnlyEnforceIf(is_on_day)

                model.Add(
                    day_vars[surgery_index] != day_index
                ).OnlyEnforceIf(is_on_day.Not())

                usage = model.NewIntVar(
                    0,
                    surgery.duration,
                    f"usage_s{surgery_index}_d{day_index}",
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
                f"daily_load_{day_index}",
            )

            model.Add(
                daily_load == sum(day_usage_terms)
            )

            daily_load_vars.append(daily_load)

        max_daily_load = model.NewIntVar(0, 100, "max_daily_load")
        min_daily_load = model.NewIntVar(0, 100, "min_daily_load")

        model.AddMaxEquality(max_daily_load, daily_load_vars)
        model.AddMinEquality(min_daily_load, daily_load_vars)

        day_balance_penalty = model.NewIntVar(
            0,
            100,
            "day_balance_penalty",
        )

        model.Add(
            day_balance_penalty == max_daily_load - min_daily_load
        )

        # -------------------------
        # Anesthesia balance objective vars
        # -------------------------

        anesthesia_load_vars = []

        for team_index in range(len(self.anesthesia_teams)):

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
                    f"team_usage_s{surgery_index}_t{team_index}",
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
                f"team_load_{team_index}",
            )

            model.Add(
                team_load == sum(team_usage_terms)
            )

            anesthesia_load_vars.append(team_load)

        max_anesthesia_load = model.NewIntVar(0, 100, "max_anesthesia_load")
        min_anesthesia_load = model.NewIntVar(0, 100, "min_anesthesia_load")

        model.AddMaxEquality(max_anesthesia_load, anesthesia_load_vars)
        model.AddMinEquality(min_anesthesia_load, anesthesia_load_vars)

        anesthesia_balance_penalty = model.NewIntVar(
            0,
            100,
            "anesthesia_balance_penalty",
        )

        model.Add(
            anesthesia_balance_penalty
            == max_anesthesia_load - min_anesthesia_load
        )


        # -------------------------
        # Surgeon idle objective vars
        # -------------------------

        surgeon_idle_vars = []

        for surgeon_index, surgeon in enumerate(self.surgeons):
            for day_index in range(5):

                assigned_list = []
                usage_terms = []

                for surgery_index, surgery in enumerate(self.surgeries):

                    is_surgeon = model.NewBoolVar(
                        f"s{surgery_index}_is_surgeon_{surgeon_index}_{day_index}"
                    )

                    is_day = model.NewBoolVar(
                        f"s{surgery_index}_is_day_{day_index}_{surgeon_index}"
                    )

                    assigned = model.NewBoolVar(
                        f"s{surgery_index}_surgeon_{surgeon_index}_day_{day_index}"
                    )

                    model.Add(
                        surgeon_vars[surgery_index] == surgeon_index
                    ).OnlyEnforceIf(is_surgeon)

                    model.Add(
                        surgeon_vars[surgery_index] != surgeon_index
                    ).OnlyEnforceIf(is_surgeon.Not())

                    model.Add(
                        day_vars[surgery_index] == day_index
                    ).OnlyEnforceIf(is_day)

                    model.Add(
                        day_vars[surgery_index] != day_index
                    ).OnlyEnforceIf(is_day.Not())

                    model.AddImplication(assigned, is_surgeon)
                    model.AddImplication(assigned, is_day)

                    model.AddBoolOr([
                        is_surgeon.Not(),
                        is_day.Not(),
                        assigned,
                    ])

                    usage = model.NewIntVar(
                        0,
                        surgery.duration,
                        f"surgeon_usage_s{surgery_index}_{surgeon_index}_{day_index}",
                    )

                    model.Add(
                        usage == surgery.duration
                    ).OnlyEnforceIf(assigned)

                    model.Add(
                        usage == 0
                    ).OnlyEnforceIf(assigned.Not())

                    assigned_list.append(assigned)
                    usage_terms.append(usage)

                surgeon_used = model.NewBoolVar(
                    f"surgeon_{surgeon_index}_used_day_{day_index}"
                )

                model.AddBoolOr(assigned_list).OnlyEnforceIf(surgeon_used)

                model.AddBoolAnd(
                    [assigned.Not() for assigned in assigned_list]
                ).OnlyEnforceIf(surgeon_used.Not())

                first_start = model.NewIntVar(
                    0,
                    TOTAL_SLOTS_PER_DAY,
                    f"first_start_surgeon_{surgeon_index}_day_{day_index}",
                )

                last_end = model.NewIntVar(
                    0,
                    TOTAL_SLOTS_PER_DAY,
                    f"last_end_surgeon_{surgeon_index}_day_{day_index}",
                )

                total_work = model.NewIntVar(
                    0,
                    TOTAL_SLOTS_PER_DAY,
                    f"total_work_surgeon_{surgeon_index}_day_{day_index}",
                )

                for surgery_index, surgery in enumerate(self.surgeries):

                    assigned = assigned_list[surgery_index]

                    model.Add(
                        first_start <= start_vars[surgery_index]
                    ).OnlyEnforceIf(assigned)

                    model.Add(
                        last_end >= start_vars[surgery_index] + surgery.duration
                    ).OnlyEnforceIf(assigned)

                model.Add(
                    total_work == sum(usage_terms)
                )

                idle = model.NewIntVar(
                    0,
                    TOTAL_SLOTS_PER_DAY,
                    f"surgeon_idle_{surgeon_index}_{day_index}",
                )

                model.Add(
                    idle == last_end - first_start - total_work
                ).OnlyEnforceIf(surgeon_used)

                model.Add(
                    idle == 0
                ).OnlyEnforceIf(surgeon_used.Not())

                surgeon_idle_vars.append(idle)

        # -------------------------
        # Priority objective
        # -------------------------

        objective_terms = []

        for surgery_index, surgery in enumerate(self.surgeries):

            global_start = (
                day_vars[surgery_index] * TOTAL_SLOTS_PER_DAY
                + start_vars[surgery_index]
            )

            if surgery.priority == "Kritik":
                weight = 100
            elif surgery.priority == "Yüksek":
                weight = 50
            elif surgery.priority == "Orta":
                weight = 20
            else:
                weight = 5

            objective_terms.append(global_start * weight)

        model.Minimize(
            sum(objective_terms)
            + day_balance_penalty * DAY_BALANCE_WEIGHT
            + anesthesia_balance_penalty * ANESTHESIA_BALANCE_WEIGHT
            + sum(surgeon_idle_vars) * SURGEON_IDLE_WEIGHT
        )

        # -------------------------
        # Surgeon off-day constraint
        # -------------------------

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
                allowed_pairs,
            )

        # -------------------------
        # Solve
        # -------------------------

        solver = cp_model.CpSolver()

        solver.parameters.max_time_in_seconds = 20
        solver.parameters.num_search_workers = 8
        solver.parameters.log_search_progress = True

        print("CP-SAT çözüm arıyor...")
        status = solver.Solve(model)
        print("CP-SAT status:", solver.StatusName(status))

        if status not in [cp_model.OPTIMAL, cp_model.FEASIBLE]:
            return None

        print(
            "Surgeon idle objective:",
            sum(
                solver.Value(var)
                for var in surgeon_idle_vars
            )
        )

        print("\nDAY LOADS")
        print("===========")

        for day_index in range(5):
            print(
                DAYS[day_index],
                solver.Value(daily_load_vars[day_index]),
            )

        print(
            "Day balance penalty:",
            solver.Value(day_balance_penalty),
        )

        print("\nANESTHESIA LOADS")
        print("====================")

        for team_index, team in enumerate(self.anesthesia_teams):
            print(
                team.name,
                solver.Value(anesthesia_load_vars[team_index]),
            )

        print(
            "Anesthesia penalty:",
            solver.Value(anesthesia_balance_penalty),
        )

        # -------------------------
        # Convert solver output to DTO
        # -------------------------

        schedule = []

        for surgery_index, surgery in enumerate(self.surgeries):

            start_slot = solver.Value(start_vars[surgery_index])
            end_slot = start_slot + surgery.duration
            day_index = solver.Value(day_vars[surgery_index])

            room_index = solver.Value(room_vars[surgery_index])
            surgeon_index = solver.Value(surgeon_vars[surgery_index])
            anesthesia_index = solver.Value(anesthesia_vars[surgery_index])


            schedule.append(
                ScheduleItem(
                    patient=surgery.patient,
                    operation=surgery.operation,
                    day_index=day_index,
                    start_slot=start_slot,
                    end_slot=end_slot,
                    room=self.rooms[room_index].name,
                    surgeon=self.surgeons[surgeon_index].name,
                    anesthesia_team=self.anesthesia_teams[anesthesia_index].name,
                )
            )
        

        print("\nValidator çalıştı.")
        print("Schedule item count:", len(schedule))


        

        ##  doktor 4 slot sonrası dinlenme violation

        rest_violations = validate_surgeon_rest_rule(schedule)

        print("Violation count:", len(rest_violations))



        if rest_violations:

            print("\nSURGEON REST VİOLATİONS")
            print("=========================")


            for violation in rest_violations: 

                print(violation)

            else:

                print("\n Surgeon rest rule OK ")


        return schedule
    