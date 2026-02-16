from pydantic import BaseModel
from .user_dto import UserResponseDTO
from ..models import Roles
from typing import Text

class LoginRequestDTO(BaseModel):
    email: str
    password: str
    ip_address: str
    user_agent: Text

    class Config:
        json_schema_extra = {
            "example": {
                "email": "john.doe@example.com",
                "password": "password",
                "ip_address": "127.0.0.1",
                "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }
        }

class LoginResponseDTO(BaseModel):
    token: str
    refresh_token: str
    user: UserResponseDTO

    class Config:
        json_schema_extra = {
            "example": {
                "token": "token",
                "refresh_token": "refresh_token",
                "user": {
                    "id": 1,
                    "email": "john.doe@example.com",
                    "first_name": "John",
                    "last_name": "Doe",
                    "cellphone": "+523178901234",
                    "rol": Roles.ADMIN,
                    "is_active": True,
                    "last_login": "2021-01-01T00:00:00Z",
                    "created_at": "2021-01-01T00:00:00Z",
                    "modified_at": "2021-01-01T00:00:00Z"
                }
            }
        }