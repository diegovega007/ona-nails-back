from .base_repository import BaseRepository
from ..models.user_session import UserSession
from sqlmodel import Session, select, update

class UserSessionRepository(BaseRepository):
    def __init__(self, session: Session):
        super().__init__(UserSession, session)

    def get_by_refresh_token(self, refresh_token: str) -> UserSession:
        statement = select(UserSession).where(UserSession.refresh_token == refresh_token)
        return self.session.exec(statement).first()

    def revoke_refresh_token(self, refresh_token: str) -> None:
        statement = update(UserSession).where(UserSession.refresh_token == refresh_token).values(is_revoked=True)
        self.session.exec(statement)
        self.session.commit()

    def get_all_by_user_id(self, user_id: int) -> list[UserSession]:
        statement = select(UserSession).where(UserSession.user_id == user_id)
        return self.session.exec(statement).all()