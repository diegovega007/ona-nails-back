from .base_repository import BaseRepository
from ..models.service_type import ServiceType
from sqlmodel import select
from sqlmodel import Session

class ServiceTypeRepository(BaseRepository):
    def __init__(self, session: Session):
        super().__init__(ServiceType, session)

    def get_by_name(self, name: str) -> ServiceType:
        return self.session.exec(select(ServiceType).where(ServiceType.name == name)).first()