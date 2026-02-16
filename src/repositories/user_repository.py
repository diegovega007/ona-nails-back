from .base_repository import BaseRepository
from ..models.user import User
from sqlmodel import Session, select
import hashlib

class UserRepository(BaseRepository):
    def __init__(self, session: Session):
        super().__init__(User, session)

    def get_by_email(self, email: str) -> User:
        statement = select(User).where(User.email == email)
        return self.session.exec(statement).first()

    def get_active_account(self, email: str) -> User:
        statement = select(User).where(User.email == email).where(User.is_active == True)
        return self.session.exec(statement).first()
    
