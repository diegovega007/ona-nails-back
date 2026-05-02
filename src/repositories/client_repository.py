from .base_repository import BaseRepository
from ..models import Client, Appointment, AppointmentService
from sqlmodel import Session, select
from sqlalchemy.orm import selectinload


_LOAD_CLIENT_TREE = (
    selectinload(Client.appointments)
    .selectinload(Appointment.appointment_services)
    .selectinload(AppointmentService.service),
)

class ClientRepository(BaseRepository):
    def __init__(self, session: Session):
        super().__init__(Client, session)

    def get_by_cellphone(self, cellphone: str) -> Client:
        statement = (
            select(Client)
            .where(Client.cellphone == cellphone)
        )
        return self.session.exec(statement).first()

    def get_all(self) -> list[Client]:
        statement = select(Client).options(*_LOAD_CLIENT_TREE)
        return list(self.session.exec(statement).all())
