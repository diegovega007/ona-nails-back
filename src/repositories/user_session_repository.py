from .base_repository import BaseRepository
from ..models.user_session import UserSession
from sqlmodel import Session, select

class UserSessionRepository(BaseRepository):
    def __init__(self, session: Session):
        super().__init__(UserSession, session)

    def get_by_user_id(self, user_id: int) -> UserSession:
        statement = select(UserSession).where(UserSession.user_id == user_id)
        return self.session.exec(statement).first()