from .base_repository import BaseRepository
from ..models import AppointmentService
from sqlmodel import Session, select

class AppointmentServiceRepository(BaseRepository):
    def __init__(self, session: Session):
        super().__init__(AppointmentService, session)

    def get_all(self, appointment_id: int = None) -> list[AppointmentService]:
        statement = select(self.model)
        if appointment_id:
            statement = statement.where(self.model.appointment_id == appointment_id)
        return self.session.exec(statement).all()
