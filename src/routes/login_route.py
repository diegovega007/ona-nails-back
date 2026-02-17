from fastapi import APIRouter, Depends, status

from ..services import LoginService, AuthService
from ..dtos import LoginRequestDTO, LoginResponseDTO, RefreshSessionRequestDTO
from ..repositories import UserRepository, UserSessionRepository
from ..config import get_session
from sqlmodel import Session

def get_login_service(session: Session = Depends(get_session)) -> LoginService:
    return LoginService(UserRepository(session), AuthService(), UserSessionRepository(session))

router = APIRouter(prefix="/login", tags=["Login"])
router_logout = APIRouter(prefix="/logout", tags=["Login"])
router_refresh = APIRouter(prefix="/refresh", tags=["Login"])

@router.post("/", response_model=LoginResponseDTO, status_code=status.HTTP_200_OK)
def login(login_dto: LoginRequestDTO, login_service: LoginService = Depends(get_login_service)):
    return login_service.login(login_dto)

@router_logout.post("/", status_code=status.HTTP_204_NO_CONTENT)
def logout(logout_dto: RefreshSessionRequestDTO, login_service: LoginService = Depends(get_login_service)):
    return login_service.logout(logout_dto.refresh_token)

@router_refresh.post("/", response_model=LoginResponseDTO, status_code=status.HTTP_200_OK)
def refresh_session(refresh_session_dto: RefreshSessionRequestDTO, login_service: LoginService = Depends(get_login_service)):
    return login_service.refresh_session(refresh_session_dto.refresh_token)