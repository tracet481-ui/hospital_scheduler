def slot_to_time(slot: int) -> str:
    total_minutes = 8 * 60 + slot * 30
    hour = total_minutes // 60
    minute = total_minutes % 60
    return f"{hour:02d}:{minute:02d}"


def format_time_range(start_slot: int, end_slot: int) -> str:
    return f"{slot_to_time(start_slot)} - {slot_to_time(end_slot)}"


def priority_value(priority: str) -> int:
    values = {
        "Kritik": 0,
        "Yüksek": 1,
        "Orta": 2,
        "Düşük": 3,
    }

    return values.get(priority, 99)
