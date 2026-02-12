from .base_repository import BaseRepository
from ..models import Appointment, Client, AppointmentStatus
from sqlmodel import Session, select
from sqlalchemy.orm import selectinload
from datetime import datetime

class AppointmentRepository(BaseRepository):
    def __init__(self, session: Session):
        super().__init__(Appointment, session)

    def get_all(self, cellphone: str = None, status: AppointmentStatus = None, date: datetime = None) -> list[Appointment]:
        statement = (
            select(Appointment)
            .join(Client)
            .options(selectinload(Appointment.client), selectinload(Appointment.service))
        )
        if cellphone:
            statement = statement.where(Client.cellphone == cellphone)
        if status:
            statement = statement.where(Appointment.status == status)
        if date:
            statement = statement.where(Appointment.appointment_date == date)
        return self.session.exec(statement).all()