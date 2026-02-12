from .base_repository import BaseRepository
from ..models.client import Client
from sqlmodel import Session, select

class ClientRepository(BaseRepository):
    def __init__(self, session: Session):
        super().__init__(Client, session)

    def get_by_cellphone(self, cellphone: str) -> Client:
        statement = (
            select(Client)
            .where(Client.cellphone == cellphone)
        )
        return self.session.exec(statement).first()
