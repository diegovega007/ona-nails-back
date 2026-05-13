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
    appointment_duration_minutes: int | None = None,
) -> list[datetime]:
    """
    Genera horarios disponibles dentro de un rango (inclusive),
    respetando horario laboral MX y excluyendo intervalos reservados.
    Los slots se generan siempre en zona horaria America/Mexico_City.

    max_concurrent: cuántas citas pueden solaparse en el mismo instante.
    appointment_duration_minutes: duración real de la cita a agendar. Si se
        provee, la ventana de verificación de solapamiento cubre el intervalo
        completo [cursor, cursor + duration) y se descartan slots donde la cita
        no cabe antes del fin del horario laboral. Si es None, se usa slot_minutes.

    Los candidatos incluyen tanto los slots regulares cada slot_minutes como
    los instantes en que terminan citas existentes — así si una cita acaba a
    las 12:07, ese momento también se ofrece como inicio disponible.
    """
    mx_initial = _to_mx(initial_date)
    mx_final = _to_mx(final_date)

    # Normalizar intervalos reservados: naive → asumir UTC, luego convertir a MX
    normalized: list[tuple[datetime, datetime]] = []
    for start, end in reserved_intervals:
        normalized.append((_to_mx(start), _to_mx(end)))

    capacity = max(0, max_concurrent)
    check_minutes = appointment_duration_minutes if appointment_duration_minutes and appointment_duration_minutes > 0 else slot_minutes
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

        day_start = datetime.combine(day, hours.start, tzinfo=MX_TZ)
        day_end   = datetime.combine(day, hours.end,   tzinfo=MX_TZ)

        # Candidatos: slots regulares cada slot_minutes
        candidates: set[datetime] = set()
        cursor = day_start
        while cursor < day_end:
            candidates.add(cursor)
            cursor += timedelta(minutes=slot_minutes)

        # Candidatos adicionales: fin de cada cita existente en este día
        # (son los momentos naturales en que un profesional queda libre)
        for _, reserved_end in normalized:
            if reserved_end.date() == day and day_start <= reserved_end < day_end:
                candidates.add(reserved_end)

        for slot in sorted(candidates):
            # Fuera del rango solicitado
            if slot < mx_initial or slot > mx_final:
                continue

            appt_end = slot + timedelta(minutes=check_minutes)

            # La cita completa no cabe dentro del horario laboral
            if appt_end > day_end:
                continue

            overlap_count = sum(
                1
                for reserved_start, reserved_end in normalized
                if slot < reserved_end and appt_end > reserved_start
            )

            if overlap_count < capacity:
                available.append(slot)

        day += timedelta(days=1)

    return available

