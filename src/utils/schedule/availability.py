from __future__ import annotations

from datetime import date, datetime, timedelta

from .calendar_mx import is_working_day_mx, working_hours_mx


def generate_available_slots(
    *,
    initial_date: datetime,
    final_date: datetime,
    reserved_intervals: list[tuple[datetime, datetime]],
    slot_minutes: int = 30,
) -> list[datetime]:
    """
    Genera horarios disponibles dentro de un rango (inclusive),
    respetando horario laboral MX y excluyendo intervalos reservados.
    """
    available: list[datetime] = []

    day: date = initial_date.date()
    last_day: date = final_date.date()

    while day <= last_day:
        if not is_working_day_mx(day):
            day += timedelta(days=1)
            continue

        hours = working_hours_mx(day)
        if hours is None:
            day += timedelta(days=1)
            continue

        cursor = datetime.combine(day, hours.start)
        day_end = datetime.combine(day, hours.end)

        while cursor < day_end:
            if cursor < initial_date or cursor > final_date:
                cursor += timedelta(minutes=slot_minutes)
                continue

            slot_end = cursor + timedelta(minutes=slot_minutes)

            overlaps = False
            for reserved_start, reserved_end in reserved_intervals:
                if cursor < reserved_end and slot_end > reserved_start:
                    overlaps = True
                    break

            if not overlaps:
                available.append(cursor)

            cursor += timedelta(minutes=slot_minutes)

        day += timedelta(days=1)

    return available

