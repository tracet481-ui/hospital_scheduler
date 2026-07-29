from scheduling.services.cp.scheduler import CPScheduler
from scheduling.services.scoring import calculate_schedule_score
from scheduling.services.scoring import build_score_details
from scheduling.services.validators import validate_surgeon_rest_rule


class SimulationEngine:

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
        self.surgeries = surgeries
        self.planning_day = planning_day

    def run(self, valid_plan_target=10, max_attempts=15):

        best_schedule = None
        best_score = float("-inf")
        best_details = None

        all_results = []

        attempt = 0
        valid_count = 0

        while valid_count < valid_plan_target and attempt < max_attempts:

            attempt += 1

            print(
                f"\n=== Attempt {attempt} | "
                f"Valid {valid_count}/{valid_plan_target} ==="
            )

            scheduler = CPScheduler(
                surgeons=self.surgeons,
                rooms=self.rooms,
                anesthesia_teams=self.anesthesia_teams,
                surgeries=self.surgeries,
                planning_day=self.planning_day,
            )

            schedule = scheduler.generate()

            if not schedule:
                print("Plan üretilemedi, geçildi.")
                continue

            rest_violations = validate_surgeon_rest_rule(schedule)

            if rest_violations:
                print("Rest violation bulundu! Plan elendi.")

                for violation in rest_violations:
                    print(violation)

                continue

            score, details = calculate_schedule_score(
                schedule=schedule,
                surgeries=self.surgeries,
            )

# score details ----------------------------------------


            valid_count += 1

            result = {
                "attempt": attempt,
                "valid_index": valid_count,
                "score": score,
                "details": details,
                "schedule": schedule,
            }

            all_results.append(result)

            if score > best_score:
                best_score = score
                best_schedule = schedule
                best_details = details


        report_score_details = build_score_details(
            score=best_score,
            details=best_details,
        )


        from pprint import pprint

        print("\n========== BEST PLAN SCORE DETAILS ==========\n")
        pprint(report_score_details, width=120)



        return (
            best_schedule,
            best_score,
            best_details,
            all_results,
        )
    
        