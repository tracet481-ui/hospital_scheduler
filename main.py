# from scheduler.models import (
#     Surgeon,
#     OperatingRoom,
#     AnesthesiaTeam,
#     SurgeryRequest,
# )


# from scheduler.backtracking import BacktrackingScheduler
# from scheduler.utils import format_time_range


# surgeons = [
#     Surgeon("Dr. Ahmet", "Genel Cerrahi", "Çarşamba"),
#     Surgeon("Dr. Ayşe", "Kardiyoloji", "Pazartesi"),
#     Surgeon("Dr. Mehmet", "Ortopedi", "Salı"),
#     Surgeon("Dr. Elif", "Beyin Cerrahisi", "Perşembe"),
#     Surgeon("Dr. Can", "Genel Cerrahi", "Cuma"),
# ]


# rooms = [
#     OperatingRoom("OR-1", "Genel Cerrahi"),
#     OperatingRoom("OR-2", "Kardiyoloji"),
#     OperatingRoom("OR-3", "Ortopedi"),
#     OperatingRoom("OR-4", "Hibrit"),
# ]


# anesthesia_teams = [
#     AnesthesiaTeam("Team-A"),
#     AnesthesiaTeam("Team-B"),
#     AnesthesiaTeam("Team-C"),
# ]


# surgeries = [
#     SurgeryRequest("P1", "Apandisit", 2, "Yüksek", "Genel Cerrahi"),
#     SurgeryRequest("P2", "Diz Protezi", 4, "Orta", "Ortopedi"),
#     SurgeryRequest("P3", "Kalp Anjiyo", 3, "Kritik", "Kardiyoloji", "OR-2"),
#     SurgeryRequest("P4", "Tümör Operasyonu", 6, "Kritik", "Beyin Cerrahisi", "OR-4"),
#     SurgeryRequest("P5", "Safra Kesesi", 2, "Düşük", "Genel Cerrahi"),
#     SurgeryRequest("P6", "Omurga Operasyonu", 5, "Yüksek", "Ortopedi", "OR-3"),
#     SurgeryRequest("P7", "Menisküs", 2, "Orta", "Ortopedi"),
# ]


# planning_day = "Cuma"


# if __name__ == "__main__":
#     scheduler = BacktrackingScheduler(
#         surgeons=surgeons,
#         rooms=rooms,
#         anesthesia_teams=anesthesia_teams,
#         surgeries=surgeries,
#         planning_day=planning_day,
#     )

#     result = scheduler.generate()

#     if result is None:
#         print("Uygun ameliyat planı bulunamadı!")

#     else:
#         print("\n üretilen ameliyat planı: \n")

#         for item in result:
#             print(
#                 f"{format_time_range(item.start_slot, item.end_slot)} | "
#                 f"{item.room} | "
#                 f"{item.patient} - {item.operation} | "
#                 f"{item.surgeon} | "
#                 f"{item.anesthesia_team}"
#             )


# ---------------------------------------------------------



import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

# from scheduling.services.data_loader import load_scheduler_input
# from scheduling.services.backtracking.scheduler import BacktrackingScheduler
# from scheduling.services.backtracking.utils import format_time_range


from scheduling.services.data_loader import load_scheduler_input
from scheduling.services.cp.scheduler import CPScheduler

from scheduling.services.schedule_saver import save_schedule_plan

from scheduling.services.scoring import calculate_priority_score



DAYS =["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", ]

surgeons, rooms, anesthesia_teams, surgeries = load_scheduler_input()


def slot_to_time(slot):
    start_hour = 8
    total_minutes = start_hour * 60 + slot * 30

    hour = total_minutes // 60
    minute = total_minutes % 60

    return f"{hour:02d}:{minute:02d}"


scheduler = CPScheduler(
    surgeons=surgeons,
    rooms=rooms,
    anesthesia_teams=anesthesia_teams,
    surgeries=surgeries,
    planning_day = "Cuma",

)


result = scheduler.generate()



if result is None:
    print("CP schedule bulunamadı.")


else:

    total_score , score_details = calculate_priority_score(

        schedule = result,
        surgeries = surgeries,

    )



    plan = save_schedule_plan(
        
        schedule = result,
        algorithm_name = "cp",
        planning_day = "Cuma",
        score = total_score,

    )


    print (f"Plan DB'ye Kaydedildi. Plan ID : { plan.id }")
    


    for item in sorted (result, key= lambda x: (x.day_index,  x.start_slot) ):

        print(

            f"{DAYS[item.day_index]}   |   "
            f"{item}"

        ) 


    # for item in sorted (

    #     result,
    #     key= lambda x: x.start_slot

    # ):
        
    #     print(item)




    
    
    for item in sorted(result, key=lambda x: (x.day_index, x.start_slot)):
        print(
            f"{DAYS[item.day_index]} | "
            f"{item.patient} | {item.operation} | "
            f"{slot_to_time(item.start_slot)} - {slot_to_time(item.end_slot)} | "
            f"Oda: {item.room} | "
            f"Cerrah: {item.surgeon} | "
            f"Anestezi: {item.anesthesia_team}"
        )





















# if __name__ == "__main__":
#     surgeons, rooms, anesthesia_teams, surgeries = load_scheduler_input()

#     scheduler = BacktrackingScheduler(
#         surgeons=surgeons,
#         rooms=rooms,
#         anesthesia_teams=anesthesia_teams,
#         surgeries=surgeries,
#         planning_day="Cumartesi",
#     )

#     result = scheduler.generate()

#     if result is None:
#         print("Uygun ameliyat planı bulunamadı!")
#     else:
#         print("\nÜretilen ameliyat planı:\n")

#         for item in sorted(result, key=lambda item: item.start_slot):
#             print(
#                 f"{format_time_range(item.start_slot, item.end_slot)} | "
#                 f"{item.room} | "
#                 f"{item.patient} - {item.operation} | "
#                 f"{item.surgeon} | "
#                 f"{item.anesthesia_team}"
#             )