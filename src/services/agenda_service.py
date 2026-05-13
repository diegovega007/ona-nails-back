
from ..dtos import AgendaResponseDTO
from ..models import AppointmentStatus
from ..repositories import UserRepository
from .appointment_service import AppointmentService
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from ..utils.schedule import generate_available_slots

MX_TZ = ZoneInfo("America/Mexico_City")


class AgendaService:
    def __init__(self, appointment_service: AppointmentService, user_repository: UserRepository):
        self.appointment_service = appointment_service
        self.user_repository = user_repository

    def get_agenda(self, initial_date: datetime, final_date: datetime, duration: int | None = None) -> AgendaResponseDTO:
        # Convertir a timezone México antes de pasar al repositorio.
        # El campo appointment_date en BD es naive (hora local MX), por lo que
        # .date() sobre initial_date/final_date en UTC devolvería fechas incorrectas.
        mx_initial = initial_date.astimezone(MX_TZ) if initial_date.tzinfo else initial_date
        mx_final   = final_date.astimezone(MX_TZ)   if final_date.tzinfo   else final_date

        reserved_schedule = self.appointment_service.get_all_appointments(
            initial_date=mx_initial,
            final_date=mx_final,
            multiple_status=[AppointmentStatus.IN_PROGRESS, AppointmentStatus.RECEIVED],
        )

        concurrent_capacity = self.user_repository.count_active_bookable_staff()

        # Los appointment_date en BD son naive en hora México.
        # Los localizamos explícitamente como MX para que generate_available_slots
        # no los interprete como UTC al normalizarlos internamente.
        def _as_mx(dt: datetime) -> datetime:
            return dt.replace(tzinfo=MX_TZ) if dt.tzinfo is None else dt.astimezone(MX_TZ)

        reserved_intervals: list[tuple[datetime, datetime]] = [
            (_as_mx(a.appointment_date), _as_mx(a.appointment_date + timedelta(minutes=a.duration)))
            for a in reserved_schedule
            if a.appointment_date is not None and a.duration and a.duration > 0
        ]

        avilable_schedule = generate_available_slots(
            initial_date=initial_date,
            final_date=final_date,
            reserved_intervals=reserved_intervals,
            slot_minutes=30,
            max_concurrent=concurrent_capacity,
            appointment_duration_minutes=duration,
        )

        # Solo exponer citas donde la capacidad está completamente ocupada en su intervalo.
        # Si concurrent_count < capacity en todo el intervalo, aún hay usuarios libres
        # y el frontend no debe bloquear ese horario.
        fully_booked_schedule = [
            a for a in reserved_schedule
            if self._concurrent_count(a, reserved_schedule) >= concurrent_capacity
        ]

        return AgendaResponseDTO(
            avilable_schedule=avilable_schedule,
            reserved_schedule=fully_booked_schedule,
        )

    def _concurrent_count(self, appt, all_appointments) -> int:
        """Cantidad de citas activas que se empalman con el intervalo de appt."""
        if appt.appointment_date is None:
            return 0
        appt_start = appt.appointment_date.replace(tzinfo=None)
        appt_end = appt_start + timedelta(minutes=appt.duration or 0)
        return sum(
            1
            for other in all_appointments
            if other.appointment_date is not None
            and other.appointment_date.replace(tzinfo=None) < appt_end
            and other.appointment_date.replace(tzinfo=None) + timedelta(minutes=other.duration or 0) > appt_start
        )
