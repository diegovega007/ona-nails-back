
from ..dtos import AgendaResponseDTO, AppointmentResponseDTO
from ..models import AppointmentStatus
from ..services import AppointmentService
from datetime import datetime, timedelta
from ..utils.schedule import generate_available_slots


class AgendaService:
    def __init__(self, appointment_service: AppointmentService):
        self.appointment_service = appointment_service

    def get_agenda(self, initial_date: datetime, final_date: datetime) -> AgendaResponseDTO:
        reserved_schedule = self.appointment_service.get_all_appointments(initial_date=initial_date, final_date=final_date,
            multiple_status=[AppointmentStatus.IN_PROGRESS, AppointmentStatus.RECEIVED]
        )
        total_duration_per_appointement = []

        for appointment in reserved_schedule:
            total_duration_per_appointement.append(
                self._appointment_duration(appointment)
            )

        avilable_schedule = self._avilable_schedule(
            initial_date=initial_date,
            final_date=final_date,
            total_duration_per_appointement=total_duration_per_appointement,
        )

        return AgendaResponseDTO(
            avilable_schedule=avilable_schedule,
            reserved_schedule=reserved_schedule
        )

    def _appointment_duration(self, appointment: AppointmentResponseDTO) -> dict:
        total = 0
        for service in appointment.list_services:
            total += service.duration
        return {
            **appointment.model_dump(exclude={"list_services", "client"}),
            "total_duration": total
        }

    def _avilable_schedule(
        self,
        initial_date: datetime,
        final_date: datetime,
        total_duration_per_appointement: list[dict],
    ) -> list[datetime]:
        reserved_intervals: list[tuple[datetime, datetime]] = []
        for a in total_duration_per_appointement:
            start = a.get("appointment_date")
            minutes = a.get("total_duration", 0) or 0
            if isinstance(start, datetime) and minutes > 0:
                reserved_intervals.append((start, start + timedelta(minutes=minutes)))

        return generate_available_slots(
            initial_date=initial_date,
            final_date=final_date,
            reserved_intervals=reserved_intervals,
            slot_minutes=30,
        )