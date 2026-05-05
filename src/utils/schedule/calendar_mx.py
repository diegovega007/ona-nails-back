from __future__ import annotations

from datetime import date, time, timedelta

from ...dtos.agenda_dto import WorkingHoursDTO


def _first_monday(year: int, month: int) -> date:
    d = date(year, month, 1)
    while d.weekday() != 0:  # 0 = Monday
        d += timedelta(days=1)
    return d


def _nth_monday(year: int, month: int, n: int) -> date:
    d = _first_monday(year, month)
    return d + timedelta(days=7 * (n - 1))


def working_hours_mx(d: date) -> WorkingHoursDTO | None:
    """
    Horario laboral:
    - Lunes a Viernes: 10:00 a 19:00
    - Sábado: 10:00 a 14:00
    - Domingo: no se trabaja
    """
    weekday = d.weekday()  # Mon=0 .. Sun=6
    if weekday <= 4:
        return WorkingHoursDTO(start=time(10, 0), end=time(19, 0))
    if weekday == 5:
        return WorkingHoursDTO(start=time(10, 0), end=time(14, 0))
    return None


def mexico_statutory_holidays(d: date) -> set[date]:
    """
    Días de descanso obligatorio (México) calculados por año.
    Fuente normativa general (LFT) y práctica común:
    - 1 de enero
    - Primer lunes de febrero (Constitución)
    - Tercer lunes de marzo (Natalicio de Benito Juárez)
    - 1 de mayo
    - 16 de septiembre
    - Tercer lunes de noviembre (Revolución)
    - 25 de diciembre
    """
    y = d.year
    return {
        date(y, 1, 1),
        _nth_monday(y, 2, 1),
        _nth_monday(y, 3, 3),
        date(y, 5, 1),
        date(y, 9, 16),
        _nth_monday(y, 11, 3),
        date(y, 12, 25),
    }


def is_mexico_non_working_day(d: date) -> bool:
    return d in mexico_statutory_holidays(d)


def is_working_day_mx(d: date) -> bool:
    hours = working_hours_mx(d)
    if hours is None:
        return False
    if is_mexico_non_working_day(d):
        return False
    return True

