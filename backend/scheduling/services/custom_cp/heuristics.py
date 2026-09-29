from .constraints import is_consistent


from .soft_heuristics import (

    calculate_soft_value_cost,

)


from .soft_heuristics import (

    calculate_combined_cost,

)



def select_unassigned_surgery (

    surgeries,
    assignments,
    domains,
        
) :

    
    # MRV + Degree Heuristic

    # 1. En küçük domain'e sahip ameliyatı seçer.
    # 2. Eşitlik varsa daha fazla diğer ameliyatı
    #    etkileyebilecek olanı öne alır.
    
    unassigned = [

        surgery 
        for surgery in surgeries 

        if surgery.patient not in assignments

    ] 

    if not unassigned:

        return None

    return min (

        unassigned,
        key = lambda surgery: (

            len(

                domains[

                    surgery.patient

                ]

            ),

            -calculate_degree (

                surgery = surgery,
                surgeries = surgeries,
                assignments = assignments,

            ),

        ),

    )



def calculate_degree (

    surgery,
    surgeries,
    assignments,
        
): 

    # Seçilen ameliyatın henüz atanmamış
    # diğer ameliyatlarla ne kadar kaynak
    # ilişkisi olduğunu yaklaşık olarak ölçer.


    degree = 0

    for other_surgery in surgeries :

        if (

            other_surgery.patient
            == surgery.patient  

        ):

            continue

        if (

            other_surgery.patient
            in assignments

        ):

            continue

        if surgeries_share_constraint(

            surgery,
            other_surgery,

        ):

            degree += 1 


    return degree


def surgeries_share_constraint (

    surgery_a,
    surgery_b,
        
):

    # İki ameliyatın ortak kaynak/constraint
    # nedeniyle birbirini etkileme ihtimali var mı?

    same_specialty = (

        surgery_a.required_specialty
        == surgery_b.required_specialty

    )

    shared_room = bool (

        set(surgery_a.compatible_rooms)
        &
        set(surgery_b.compatible_rooms)

    )

    return (

        same_specialty
        or shared_room
        
    )



def order_domain_values(

    surgery,
    domains,
    state,
    surgeries,
    surgeons_by_name,
    slots_per_day,
    surgeries_by_patient,
    soft_constraints,
        
):

    # Şimdilik mevcut domain sırasını döndürür.

    # Bir sonraki aşamada LCV:
    # diğer ameliyatların domainlerinden
    # en az değer eleyen seçenek önce gelecek.


    values = domains [surgery.patient]

    scored_values = []

    for value in values:

        if not is_consistent(   
            surgery=surgery,
            value=value,
            state=state,
            surgeons_by_name=surgeons_by_name,
            slots_per_day=slots_per_day,
        ):
            continue


        combined_cost = calculate_combined_cost     (

            surgery = surgery,
            value = value,
            state = state,
            surgeries_by_patiet = surgeries_by_patient,
            soft_constraints = soft_constraints,
            slots_per_day = slots_per_day,

        )
        


        # 1) Candidate'i geçici olarak state'e koy
        state.assign(
            surgery,
            value,
        )

        # 2) LCV elimination hesabı
        elimination_count = 0

        for other_surgery in surgeries:

            if (
                other_surgery.patient
                == surgery.patient
            ):
                continue

            if (
                other_surgery.patient
                in state.assignments
            ):
                continue

            for other_value in domains[
                other_surgery.patient
            ]:

                if not is_consistent(
                    surgery=other_surgery,
                    value=other_value,
                    state=state,
                    surgeons_by_name=surgeons_by_name,
                    slots_per_day=slots_per_day,
                ):
                    elimination_count += 1

        # 3) Candidate state içindeyken soft cost hesapla
        soft_cost = calculate_soft_value_cost(
            surgery=surgery,
            value=value,
            state=state,
            surgeries_by_patient=surgeries_by_patient,
            soft_constraints=soft_constraints,
        )

        # 4) Priority candidate'in zamanından hesaplanıyor
        priority_cost = calculate_priority_cost(
            surgery=surgery,
            value=value,
            slots_per_day=slots_per_day,
        )

        # 5) Geçici atamayı geri al
        state.unassign(
            surgery,
            value,
        )

        # 6) Adayın üç heuristic değerini sakla
        scored_values.append(
            (
                elimination_count,
                priority_cost,
                soft_cost,
                value,
                combined_cost,
            )
        )


    scored_values.sort  (

        # key = lambda item : item[0]

        key = lambda item : (

            item[0],  # elimination_count
            item[1],  # priority_cost
            item[2],  # soft_cost

        )

    )


    print(
        "LCV SCORED VALUES:",
        len(scored_values),
    )


    return [

        value

        for _, _, _, value in scored_values

    ]



def calculate_priority_cost (

    surgery,
    value,
    slots_per_day,
        
) :

    priority_weight = {

        "Kritik" : 100,
        "Yüksek" : 50,
        "Orta" : 20,
        "Düşük" : 5,

    }



    weight =   priority_weight.get (

        surgery.priority,
        5,
        
    )


    global_start = (

        value.day * slots_per_day
        +
        value.start_slot

    )


    return global_start * weight



        







            