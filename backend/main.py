import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from scheduling.services.data_loader import load_scheduler_input
from scheduling.services.scoring import calculate_schedule_score
from scheduling.services.schedule_saver import save_schedule_plan
from scheduling.services.simulation import SimulationEngine

from scheduling.services.validators import validate_surgeon_rest_rule

from scheduling.services.scoring import (
    calculate_schedule_score,
    build_score_details,
)




DAYS = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma"]


def slot_to_time(slot):
    start_hour = 8
    total_minutes = start_hour * 60 + slot * 30

    hour = total_minutes // 60
    minute = total_minutes % 60

    return f"{hour:02d}:{minute:02d}"


surgeons, rooms, anesthesia_teams, surgeries = load_scheduler_input()


simulation = SimulationEngine(
    surgeons=surgeons,
    rooms=rooms,
    anesthesia_teams=anesthesia_teams,
    surgeries=surgeries,
    planning_day="week",
)

best_schedule, best_score, best_details, all_results = simulation.run(
    valid_plan_target=5,
    max_attempts=20,
)


report_score_details = build_score_details(
    score=best_score,
    details=best_details,
)


##    score check
print("\n Best Plan Selection Check")
print("============================")
print (" Best Score: ", best_score)
print (
        "Max All Results : ",
        max(result["score"] for result in all_results)
        if all_results else None
)

print ("Best Schedule item count : ", len(best_schedule) if best_schedule else 0)

##    score check



if best_schedule is None:
    print("CP schedule bulunamadı.")
    exit()


rest_violations = validate_surgeon_rest_rule(best_schedule)

if rest_violations :
    print ("\n BEST PLANREST VIOLATION İÇERİYOR! ")
    print("======================================")

    for violation in rest_violations :
        print(violation)

    exit()





total_score, score_details = calculate_schedule_score(
    schedule=best_schedule,
    surgeries=surgeries,
)

report_score_details = build_score_details(
    score=total_score,
    details=score_details,
)

from pprint import pprint


#  list details  --------------------------------------  

print("\n===== KAYDEDİLECEK SCORE DETAILS =====\n")

pprint(report_score_details, width=140)


# -------------------------------------- list details


print("\nBEST PLAN SCORE CHECK")
print("=====================")
print("Simulation Best Score :", best_score)
print("Recalculated Score    :", total_score)
print("Difference            :", best_score - total_score)



# success_rate = min (
#     100,
#     max(0, int(total_score / 1300))
# )


# score_details["success_rate"] = success_rate


plan = save_schedule_plan(
    schedule=best_schedule,
    algorithm_name="cp",
    planning_day="week",
    score=total_score,
    # score_details=score_details,
    score_details=report_score_details,
    simulation_results=all_results,


)



# ## ----------------------------------------------


# print("\nSAVED PLAN CHECK")
# print("================")
# print("Saved Plan ID :", plan.id)
# print("Saved Score   :", plan.score)
# print("Expected Best :", best_score)
# print("Item Count    :", len(best_schedule))

# ##  ------------------------------------------------


# print("\nPLAN DB'YE KAYDEDİLDİ")
# print("=====================")
# print(f"Plan ID    : {plan.id}")
# print(f"Best Score : {best_score}")
# print(f"DB Score   : {total_score}")


# ##  -------------------------------------------------


print("\nSIMULATION RESULTS")
print("==================")

for index, result in enumerate(all_results, start=1):
    print(
        f"Plan {index:2} | "
        f"Score = {result['score']}"
    )


print("\nSCORE SUMMARY")
print("=============")

for detail in best_details:
    if detail["type"] == "score_summary":
        print(f"Priority Score           : {detail['priority_score']}")
        print(f"Day Balance Penalty      : {detail['day_balance_penalty']}")
        print(f"Anesthesia Balance       : {detail['anesthesia_balance_penalty']}")
        print(f"Room Idle Penalty        : {detail['room_idle_penalty']}")
        print(f"Surgeon Idle Penalty     : {detail['surgeon_idle_penalty']}")
        print(f"Final Score              : {detail['final_score']}")
        break


print("\nBEST WEEKLY SCHEDULE")
print("====================")

current_day = None

for item in sorted(
    best_schedule,
    key=lambda x: (x.day_index, x.start_slot, x.room)
):
    if current_day != item.day_index:
        current_day = item.day_index

        print("\n" + "=" * 70)
        print(DAYS[current_day].upper())
        print("=" * 70)

    print(
        f"{slot_to_time(item.start_slot)} - "
        f"{slot_to_time(item.end_slot)} | "
        f"{item.patient:4} | "
        f"{item.operation:20} | "
        f"{item.room:4} | "
        f"{item.surgeon:12} | "
        f"{item.anesthesia_team}"
    )


violations = validate_surgeon_rest_rule(best_schedule)


print(best_score)
print(total_score)

print("\n REST CHECK RESULT")
print("====================")







