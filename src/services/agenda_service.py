
from ..dtos import AgendaResponseDTO
from ..models import AppointmentStatus
from .appointment_service import AppointmentService
from .user_service import UserService
from datetime import datetime, timedelta
from ..utils.schedule import generate_available_slots


class AgendaService:
    def __init__(self, appointment_service: AppointmentService, user_service: UserService):
        self.appointment_service = appointment_service
        self.user_service = user_service

    def get_agenda(self, initial_date: datetime, final_date: datetime) -> AgendaResponseDTO:
        reserved_schedule = self.appointment_service.get_all_appointments(
            initial_date=initial_date,
            final_date=final_date,
            multiple_status=[AppointmentStatus.IN_PROGRESS, AppointmentStatus.RECEIVED],
        )

        reserved_intervals: list[tuple[datetime, datetime]] = [
            (a.appointment_date, a.appointment_date + timedelta(minutes=a.duration))
            for a in reserved_schedule
            if a.duration and a.duration > 0
        ]

        concurrent_capacity = self.user_service.count_active_bookable_staff()

        avilable_schedule = generate_available_slots(
            initial_date=initial_date,
            final_date=final_date,
            reserved_intervals=reserved_intervals,
            slot_minutes=30,
            max_concurrent=concurrent_capacity,
        )

        return AgendaResponseDTO(
            avilable_schedule=avilable_schedule,
            reserved_schedule=reserved_schedule,
        )
