from ..repositories import UserRepository, UserSessionRepository
from ..services.auth_service import AuthService
from ..dtos import CreateUserDTO, UpdateUserDTO, UserResponseDTO
from ..exeptions import UserNotFound, UserAlreadyExists
from datetime import datetime
from ..models import User

class UserService:
    def __init__(self, user_repository: UserRepository, auth_service: AuthService, user_session_repository: UserSessionRepository):
        self.user_repository = user_repository
        self.auth_service = auth_service
        self.user_session_repository = user_session_repository

    def create_user(self, user_dto: CreateUserDTO) -> UserResponseDTO:
        if self.user_repository.get_by_email(user_dto.email):
            raise UserAlreadyExists()
        user = self.user_repository.create(
            User(**user_dto.model_dump(exclude={"password"}), password=self.auth_service.hash_password(user_dto.password), created_at=datetime.now())
        )
        return UserResponseDTO.model_validate(user)

    def get_all_users(self) -> list[UserResponseDTO]:
        users = self.user_repository.get_all()
        return [UserResponseDTO.model_validate(user) for user in users]

    def count_active_bookable_staff(self) -> int:
        return self.user_repository.count_active_bookable_staff()

    def get_user_by_id(self, id: int) -> UserResponseDTO:
        user = self.user_repository.get_by_id(id)
        if not user:
            raise UserNotFound()
        return UserResponseDTO.model_validate(user)     
    
    def update_user(self, user_dto: UpdateUserDTO) -> UserResponseDTO:
        user = self.user_repository.get_by_id(user_dto.id)
        if not user:
            raise UserNotFound()
        password = self.auth_service.hash_password(user_dto.password) if user_dto.password else user.password
        user.modified_at = datetime.now()
        user = self.user_repository.update(
            User(**user_dto.model_dump(exclude={"password"}), password=password, modified_at=datetime.now())
        )
        return UserResponseDTO.model_validate(user)

    def delete_user(self, id: int) -> bool:
        user = self.user_repository.get_by_id(id)
        if not user:
            raise UserNotFound()
        user_sessions = self.user_session_repository.get_all_by_user_id(id)
        for user_session in user_sessions:
            self.user_session_repository.delete(user_session.id)
        return self.user_repository.delete(id)