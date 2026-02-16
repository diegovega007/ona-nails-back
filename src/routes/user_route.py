from fastapi import APIRouter, Depends, status

from ..services import UserService, AuthService
from ..dtos import CreateUserDTO, UpdateUserDTO, UserResponseDTO
from ..repositories import UserRepository
from ..config import get_session
from sqlmodel import Session

def get_user_service(session: Session = Depends(get_session)) -> UserService:
    return UserService(UserRepository(session), AuthService())

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=UserResponseDTO, status_code=status.HTTP_201_CREATED)
def create_user(user_dto: CreateUserDTO, user_service: UserService = Depends(get_user_service)):
    return user_service.create_user(user_dto)

@router.get("/", response_model=list[UserResponseDTO], status_code=status.HTTP_200_OK)
def get_all_users(user_service: UserService = Depends(get_user_service)):
    return user_service.get_all_users()

@router.get("/{id}", response_model=UserResponseDTO, status_code=status.HTTP_200_OK)
def get_user_by_id(id: int, user_service: UserService = Depends(get_user_service)):
    return user_service.get_user_by_id(id)

@router.put("/", response_model=UserResponseDTO, status_code=status.HTTP_200_OK)
def update_user(user_dto: UpdateUserDTO, user_service: UserService = Depends(get_user_service)):
    return user_service.update_user(user_dto)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int, user_service: UserService = Depends(get_user_service)):
    return user_service.delete_user(id)