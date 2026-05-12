from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from ..services.auth_service import AuthService
from typing import Annotated, Optional
from ..models import User
from ..services import UserService
from ..repositories import UserRepository, UserSessionRepository
from ..config import get_session
from sqlmodel import Session

security = HTTPBearer()
security_optional = HTTPBearer(auto_error=False)

def authorization_header(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)]
) -> dict:
    try:
        auth_service = AuthService()
        username = auth_service.decode_token(credentials.credentials)
        return {"username": username}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )


def current_user(
    auth: dict = Depends(authorization_header),
    session: Session = Depends(get_session),
) -> User:
    user_service = UserService(UserRepository(session), AuthService(), UserSessionRepository(session))
    return user_service.get_user_by_email(auth["username"])


def optional_current_user(
    credentials: Annotated[Optional[HTTPAuthorizationCredentials], Depends(security_optional)] = None,
    session: Session = Depends(get_session),
) -> Optional[User]:
    if not credentials:
        return None
    try:
        auth_service = AuthService()
        username = auth_service.decode_token(credentials.credentials)
        user_service = UserService(UserRepository(session), AuthService(), UserSessionRepository(session))
        return user_service.get_user_by_email(username)
    except Exception:
        return None