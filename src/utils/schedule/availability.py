from __future__ import annotations

from datetime import date, datetime, timedelta, timezone
from zoneinfo import ZoneInfo

from .calendar_mx import is_working_day_mx, working_hours_mx

MX_TZ = ZoneInfo("America/Mexico_City")


def _to_mx(dt: datetime) -> datetime:
    """Convierte un datetime a zona horaria MX. Si es naive, se asume UTC."""
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(MX_TZ)


def generate_available_slots(
    *,
    initial_date: datetime,
    final_date: datetime,
    reserved_intervals: list[tuple[datetime, datetime]],
    slot_minutes: int = 30,
    max_concurrent: int = 1,
) -> list[datetime]:
    """
    Genera horarios disponibles dentro de un rango (inclusive),
    respetando horario laboral MX y excluyendo intervalos reservados.
    Los slots se generan siempre en zona horaria America/Mexico_City.

    max_concurrent: cuántas citas pueden solaparse en el mismo instante (p. ej.
    cantidad de profesionales activos). Con valor 1 se comporta como antes: una sola
    reserva bloquea el hueco.
    """
    mx_initial = _to_mx(initial_date)
    mx_final = _to_mx(final_date)

    # Normalizar intervalos reservados: naive → asumir UTC, luego convertir a MX
    normalized: list[tuple[datetime, datetime]] = []
    for start, end in reserved_intervals:
        normalized.append((_to_mx(start), _to_mx(end)))

    capacity = max(0, max_concurrent)
    available: list[datetime] = []

    day: date = mx_initial.date()
    last_day: date = mx_final.date()

    while day <= last_day:
        if not is_working_day_mx(day):
            day += timedelta(days=1)
            continue

        hours = working_hours_mx(day)
        if hours is None:
            day += timedelta(days=1)
            continue

        cursor = datetime.combine(day, hours.start, tzinfo=MX_TZ)
        day_end = datetime.combine(day, hours.end, tzinfo=MX_TZ)

        while cursor < day_end:
            if cursor < mx_initial or cursor > mx_final:
                cursor += timedelta(minutes=slot_minutes)
                continue

            slot_end = cursor + timedelta(minutes=slot_minutes)

            overlap_count = sum(
                1
                for reserved_start, reserved_end in normalized
                if cursor < reserved_end and slot_end > reserved_start
            )

            if overlap_count < capacity:
                available.append(cursor)

            cursor += timedelta(minutes=slot_minutes)

        day += timedelta(days=1)

    return available

