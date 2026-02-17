from ..repositories import UserRepository, UserSessionRepository
from ..services.auth_service import AuthService
from ..dtos import LoginRequestDTO, LoginResponseDTO, UserResponseDTO, CreateUserSessionDTO
from ..exeptions import UserNotFound, UserInactive, InvalidCredentialsException, UserSessionNotFound, TokenExpiredException, UserSessionRevoked
from datetime import datetime, timedelta
import os
from ..models import UserSession

class LoginService:
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
    REFRESH_TOKEN_EXPIRE_MINUTES = int(os.getenv("REFRESH_TOKEN_EXPIRE_MINUTES"))
    
    def __init__(self, user_repository: UserRepository, auth_service: AuthService, user_session_repository: UserSessionRepository):
        self.user_repository = user_repository
        self.auth_service = auth_service
        self.user_session_repository = user_session_repository

    def login(self, login_dto: LoginRequestDTO) -> LoginResponseDTO:
        user = self.user_repository.get_by_email(login_dto.email)
        if not user:
            raise UserNotFound()
        
        user = self.user_repository.get_active_account(login_dto.email)
        if not user:
            raise UserInactive()
        
        if not self.auth_service.verify_password(
            login_dto.password, 
            user.password
        ):
            raise InvalidCredentialsException()
        
        token = self.auth_service.encode_token(
            user.email,
            user.password,
            timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        refresh_token = self.auth_service.encode_token(
            user.email,
            user.password,
            timedelta(minutes=self.REFRESH_TOKEN_EXPIRE_MINUTES)
        )
        
        user_session_dto = CreateUserSessionDTO(
            user_id=user.id,
            refresh_token=refresh_token,
            ip_address=login_dto.ip_address,
            user_agent=login_dto.user_agent,
            expires_at=datetime.now() + timedelta(
                minutes=self.REFRESH_TOKEN_EXPIRE_MINUTES
            )
        )
        self.user_session_repository.create(
            UserSession(**user_session_dto.model_dump(), created_at=datetime.now())
        )
        
        return LoginResponseDTO(
            token=token,
            refresh_token=refresh_token,
            user=UserResponseDTO.model_validate(user)
        )

    def logout(self, refresh_token: str) -> bool:
        user_session = self.user_session_repository.get_by_refresh_token(refresh_token)
        if not user_session:
            raise UserSessionNotFound()
        self.user_session_repository.revoke_refresh_token(refresh_token)
        return True

    def refresh_session(self, refresh_token: str) -> LoginResponseDTO:
        user_session = self.user_session_repository.get_by_refresh_token(refresh_token)
        if not user_session:
            raise UserSessionNotFound()
        if user_session.is_revoked:
            raise UserSessionRevoked()
        if user_session.expires_at < datetime.now():
            self.user_session_repository.revoke_refresh_token(refresh_token)
            raise TokenExpiredException()

        token = self.auth_service.encode_token(
            user_session.user.email,
            user_session.user.password,
            timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES)
        )

        return LoginResponseDTO(
            token=token,
            refresh_token=refresh_token,
            user=UserResponseDTO.model_validate(user_session.user)
        )