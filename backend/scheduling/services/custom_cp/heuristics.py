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
        
):

    # Şimdilik mevcut domain sırasını döndürür.

    # Bir sonraki aşamada LCV:
    # diğer ameliyatların domainlerinden
    # en az değer eleyen seçenek önce gelecek.


    return domains[
        surgery.patient
    ]




            