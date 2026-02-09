from .base_repository import BaseRepository
from ..models.client import Client
from sqlmodel import Session

class ClientRepository(BaseRepository):
    def __init__(self, session: Session):
        super().__init__(Client, session)
