from scheduler.models import (
    Surgeon,
    OperatingRoom,
    AnesthesiaTeam,
    SurgeryRequest,
)


from scheduler.backtracking import BacktrackingScheduler
from scheduler.utils import format_time_range


surgeons = [
    Surgeon("Dr. Ahmet", "Genel Cerrahi", "Çarşamba"),
    Surgeon("Dr. Ayşe", "Kardiyoloji", "Pazartesi"),
    Surgeon("Dr. Mehmet", "Ortopedi", "Salı"),
    Surgeon("Dr. Elif", "Beyin Cerrahisi", "Perşembe"),
    Surgeon("Dr. Can", "Genel Cerrahi", "Cuma"),
]


rooms = [
    OperatingRoom("OR-1", "Genel Cerrahi"),
    OperatingRoom("OR-2", "Kardiyoloji"),
    OperatingRoom("OR-3", "Ortopedi"),
    OperatingRoom("OR-4", "Hibrit"),
]


anesthesia_teams = [
    AnesthesiaTeam("Team-A"),
    AnesthesiaTeam("Team-B"),
    AnesthesiaTeam("Team-C"),
]


surgeries = [
    SurgeryRequest("P1", "Apandisit", 2, "Yüksek", "Genel Cerrahi"),
    SurgeryRequest("P2", "Diz Protezi", 4, "Orta", "Ortopedi"),
    SurgeryRequest("P3", "Kalp Anjiyo", 3, "Kritik", "Kardiyoloji", "OR-2"),
    SurgeryRequest("P4", "Tümör Operasyonu", 6, "Kritik", "Beyin Cerrahisi", "OR-4"),
    SurgeryRequest("P5", "Safra Kesesi", 2, "Düşük", "Genel Cerrahi"),
    SurgeryRequest("P6", "Omurga Operasyonu", 5, "Yüksek", "Ortopedi", "OR-3"),
    SurgeryRequest("P7", "Menisküs", 2, "Orta", "Ortopedi"),
]


planning_day = "Cuma"


if __name__ == "__main__":
    scheduler = BacktrackingScheduler(
        surgeons=surgeons,
        rooms=rooms,
        anesthesia_teams=anesthesia_teams,
        surgeries=surgeries,
        planning_day=planning_day,
    )

    result = scheduler.generate()

    if result is None:
        print("Uygun ameliyat planı bulunamadı!")

    else:
        print("\n üretilen ameliyat planı: \n")

        for item in result:
            print(
                f"{format_time_range(item.start_slot, item.end_slot)} | "
                f"{item.room} | "
                f"{item.patient} - {item.operation} | "
                f"{item.surgeon} | "
                f"{item.anesthesia_team}"
            )
