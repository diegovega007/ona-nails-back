from fastapi import APIRouter, Depends, status

from ..services import LoginService, AuthService
from ..dtos import LoginRequestDTO, LoginResponseDTO
from ..repositories import UserRepository, UserSessionRepository
from ..config import get_session
from sqlmodel import Session

def get_login_service(session: Session = Depends(get_session)) -> LoginService:
    return LoginService(UserRepository(session), AuthService(), UserSessionRepository(session))

router = APIRouter(prefix="/login", tags=["Login"])

@router.post("/", response_model=LoginResponseDTO, status_code=status.HTTP_200_OK)
def login(login_dto: LoginRequestDTO, login_service: LoginService = Depends(get_login_service)):
    return login_service.login(login_dto)