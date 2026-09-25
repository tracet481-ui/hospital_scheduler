from scheduling.services.scoring import (
    slider_to_multiplier,
)


def calculate_soft_value_cost(
    surgery,
    value,
    state,
    surgeries_by_patient,
    soft_constraints,
):
    if not soft_constraints:
        return 0

    day_balance_value = soft_constraints.get(
        "day_balance",
        50,
    )

    return calculate_day_balance_cost(
        surgery=surgery,
        value=value,
        state=state,
        surgeries_by_patient=surgeries_by_patient,
        slider_value=day_balance_value,
    )


def calculate_day_balance_cost(
    surgery,
    value,
    state,
    surgeries_by_patient,
    slider_value,
):
    day_loads = [0, 0, 0, 0, 0 ]

    for patient, assigned_value in state.assignments.items():

        if assigned_value.day != value.day:
            continue

        assigned_surgery = surgeries_by_patient[
            patient
        ]

        # day_loads += assigned_surgery.duration


        day_loads[ 

            assigned_value.day 

        ]   +=  assigned_surgery.duration

    
    

    max_load = max (day_loads)

    min_load = min (day_loads)



    imbalance = max_load - min_load

    # projected_day_load = (
    #     day_load
    #     + surgery.duration
    # )

    multiplier = slider_to_multiplier(
        slider_value
    )

    # return projected_day_load * multiplier

    return imbalance * multiplier




    