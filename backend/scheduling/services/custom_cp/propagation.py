from .constraints import is_consistent


def forward_check (

    selected_surgery,
    surgeries,
    domains,
    state,
    surgeons_by_name,
    slots_per_day,
        
):

    # Bir assignment yapıldıktan sonra kalan
    # ameliyatların domainlerini yeniden filtreler.

    # Herhangi bir atanmamış ameliyatın domaini
    # boşalırsa branch artık çözüm üretemez ve
    # None döndürülür.
    
    new_domains = {

        patient: values.copy()
        for patient, values in domains.items()

    }

    pruned_count = 0


    for surgery in surgeries :

    # Seçilen ameliyat zaten atanmış durumda.

        if (

            surgery.patient

            == selected_surgery.patient

        ): 
            continue



        # Daha önce atanmış ameliyatları
        # tekrar filtrelemiyoruz.


        if(

            surgery.patient

            in state.assignments

        ):
            continue


        old_values = new_domains [
            surgery.patient
        ]


        valid_values = []


        for value in old_values :

            if is_consistent(

                surgery = surgery,
                value = value,
                state = state,
                surgeons_by_name = surgeons_by_name,
                slots_per_day = slots_per_day,

            ):

                valid_values.append(

                    value

                )


        pruned_count += (

            len(old_values)
            -
            len(valid_values)

        )


        new_domains[

            surgery.patient

        ] = valid_values

        # Domain tamamen boşaldıysa
        # bu branch artık çözümsüz


        if not valid_values:

            return None, pruned_count
         

    return new_domains, pruned_count



def get_domain_stats (


    domains,
    assignments,
        
) :

    remaining_sizes = {

        patient : len (values)

        for patient, values in domains.items()
        if patient not in assignments

    }

    if not remaining_sizes :

        return {

            "unassigned_count" : 0,
            "min_domain" : 0,
            "max_domain" : 0,
            "total_values" : 0,

        }

    sizes = list (

        remaining_sizes.values() 
    )

    return {

        "unassigned_count" :
            len(remaining_sizes),

        "min_domain" :
            min(sizes),

        "max_domain" :
            max(sizes),

        "total_values":
            sum(sizes),

    }







    
