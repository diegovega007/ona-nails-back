from .base_repository import BaseRepository
from ..models.user import Roles, User
from sqlmodel import Session, func, select
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

    def count_active_bookable_staff(self) -> int:
        """Usuarios activos que pueden tomar citas en paralelo (no recepción)."""
        statement = (
            select(func.count())
            .select_from(User)
            .where(User.is_active == True)
            .where(User.rol != Roles.RECEPTIONIST)
        )
        return self.session.exec(statement).one()

    def get_available_user(self) -> User:
        statement = select(User).where(User.is_active == True).where(User.rol != Roles.RECEPTIONIST)
        return self.session.exec(statement).all()

