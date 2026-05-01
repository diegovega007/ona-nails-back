from sqlalchemy import Date, cast
from .base_repository import BaseRepository
from ..models import Appointment, Client, AppointmentStatus, AppointmentService
from sqlmodel import Session, select
from sqlalchemy.orm import selectinload
from datetime import datetime

_APPOINTMENT_LOAD_OPTIONS = (
    selectinload(Appointment.client),
    selectinload(Appointment.appointment_services).selectinload(
        AppointmentService.service
    ),
)

class AppointmentRepository(BaseRepository):
    def __init__(self, session: Session):
        super().__init__(Appointment, session)

    def get_all(
        self,
        cellphone: str = None,
        status: AppointmentStatus = None,
        date: datetime = None,
    ) -> list[Appointment]:
        statement = select(Appointment).options(*_APPOINTMENT_LOAD_OPTIONS)
        if cellphone:
            statement = statement.join(Client).where(
                Client.cellphone.contains(cellphone)
            )
        if status:
            statement = statement.where(Appointment.status == status)
        if date:
            statement = statement.where(
                cast(Appointment.appointment_date, Date) == date.date()
            )
        return list(self.session.exec(statement).all())

    def get_by_id(self, id: int) -> Appointment | None:
        statement = (
            select(Appointment)
            .where(Appointment.id == id)
            .options(*_APPOINTMENT_LOAD_OPTIONS)
        )
        return self.session.exec(statement).first()
