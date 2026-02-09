from .base_repository import BaseRepository
from ..models.service import Service
from sqlmodel import select
from sqlmodel import Session

class ServiceRepository(BaseRepository):
    def __init__(self, session: Session):
        super().__init__(Service, session)

    def get_by_name(self, name: str) -> Service:
        return self.session.exec(select(Service).where(Service.name == name)).first()