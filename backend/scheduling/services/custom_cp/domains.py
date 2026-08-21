from dataclasses import dataclass


@dataclass(frozen=True)
class DomainValue:

    day:int
    start_slot : int
    room : str
    surgeon : str
    anesthesia_team : str


# -----------------------------------------------------------
# her ameliyat için olası kombinasyonları  üreteceğiz
# -----------------------------------------------------------




def build_domains (

    surgeries,
    surgeons,
    anesthesia_teams,
    days_count,
    slots_per_day,
        
):  

    domains = {}

    for surgery in surgeries :

        surgery_domain = []

        for day in range(days_count) :

            for start_slot in range (slots_per_day):

                end_slot = (

                    start_slot
                    + surgery.duration

                )

                # gün sınırını aşan operasyonlar listeye giremez

                if end_slot > slots_per_day :

                    continue

                for room in surgery.compitable_rooms:

                    for surgeon in surgeons :


                        # uzmanlığı uyuşmayan operasyonlar da geçerli değil

                        if (

                            surgeon.specialty
                            != surgery.required_specialty

                        ) :

                            continue

                        for anesthesia_team in anesthesia_teams :

                            value = DomainValue(

                                day = day,
                                start_slot = start_slot,
                                room = room,
                                surgeon = surgeon.name,
                                anesthesia_team = anesthesia_team.name,

                            )

        domains [surgery.patient] = surgery_domain

    return domains












# ----------------------------------------------------------------------


