from django.core.management.base import BaseCommand



from scheduling.models import (

    Specialty,
    Surgeon,
    OperatingRoom,
    AnesthesiaTeam,
    Patient,
    SurgeryType,
    SurgeryRequest,
    
)


class Command (BaseCommand) :

    help = "Seed hospital scheduling data"


    def handle(self, *args, **kwargs) :
        
        SurgeryRequest.objects.all().delete()
        SurgeryType.objects.all().delete()
        Patient.objects.all().delete()
        AnesthesiaTeam.objects.all().delete()
        OperatingRoom.objects.all().delete()
        Surgeon.objects.all().delete()
        Specialty.objects.all().delete()


        general = Specialty.objects.create(name="Genel Cerrahi")
        cardio = Specialty.objects.create(name="Kardiyoloji")
        ortho = Specialty.objects.create(name="Ortopedi")
        neuro = Specialty.objects.create(name="Beyin Cerrahisi")


        Surgeon.objects.create(name="Dr. Ahmet", specialty=general, off_day= "Çarşamba")
        Surgeon.objects.create(name="Dr. Ayşe",specialty=cardio, off_day="Pazartesi")
        Surgeon.objects.create(name="Dr. Mehmet", specialty=ortho,  off_day="Salı")
        Surgeon.objects.create(name="Dr. Elif", specialty=neuro, off_day="Perşembe")
        Surgeon.objects.create(name="Dr. Can", specialty= general, off_day="Cuma" )


        or1 = OperatingRoom.objects.create(name="OR-1", room_type= general)
        or2 = OperatingRoom.objects.create(name="OR-2", room_type= cardio)
        or3 = OperatingRoom.objects.create(name="OR-3", room_type= ortho)
        or4 = OperatingRoom.objects.create(name="OR-4", is_hybrid= True)

        AnesthesiaTeam.objects.create(name="Team-A")
        AnesthesiaTeam.objects.create(name="Team-B")
        AnesthesiaTeam.objects.create(name="Team-C")




        surgery_defs = [
            ("Apandisit", general, 2, [or1, or4]),
            ("Diz Protezi", ortho, 4, [or3, or4]),
            ("Kalp Anjiyo", cardio, 3, [or2]),
            ("Tümör Operasyonu", neuro, 6, [or4]),
            ("Safra Kesesi", general, 2, [or1, or4]),
            ("Omurga Operasyonu", ortho, 5, [or3]),
            ("Menisküs", ortho, 2, [or3, or4]),
        ]






        surgery_type_map = {}

        for name, specialty, duration_slots, rooms in surgery_defs:
            surgery_type = SurgeryType.objects.create(
                name=name,
                required_specialty=specialty,
                duration_slots = duration_slots,
            )
            surgery_type.compatible_rooms.set(rooms)
            surgery_type_map[name] = surgery_type

        requests = [
            ("P1", "Apandisit", 2, "high"),
            ("P2", "Diz Protezi", 4, "medium"),
            ("P3", "Kalp Anjiyo", 3, "critical"),
            ("P4", "Tümör Operasyonu", 6, "critical"),
            ("P5", "Safra Kesesi", 2, "low"),
            ("P6", "Omurga Operasyonu", 5, "high"),
            ("P7", "Menisküs", 2, "medium"),
        ]

        for patient_code, surgery_name, duration, priority in requests:
            patient = Patient.objects.create(code=patient_code)

            SurgeryRequest.objects.create(
                patient=patient,
                surgery_type=surgery_type_map[surgery_name],
                # duration=duration,
                priority=priority,
            )

        self.stdout.write(self.style.SUCCESS("Scheduling seed data created."))