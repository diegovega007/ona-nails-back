from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from ..models import Roles

class CreateUserDTO(BaseModel):
    email: str
    password: str
    first_name: str
    last_name: str
    cellphone: Optional[str] = None
    rol : Roles

    class Config:
        json_schema_extra = {
            "example": {
                "email": "john.doe@example.com",
                "password": "password",
                "first_name": "John",
                "last_name": "Doe",
                "cellphone": "+523178901234",
                "rol": Roles.ADMIN
            }
        }

class UpdateUserDTO(BaseModel):
    id: int
    email: str
    password: str
    first_name: str
    last_name: str
    cellphone: Optional[str] = None
    rol : Roles
    is_active: bool

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "email": "john.doe@example.com",
                "password": "password",
                "first_name": "John",
                "last_name": "Doe",
                "cellphone": "+523178901234",
                "rol": Roles.ADMIN,
                "is_active": True
            }
        }

class UserResponseDTO(BaseModel):
    id: int
    email: str
    first_name: str
    last_name: str
    cellphone: Optional[str] = None
    rol : Roles
    is_active: bool
    last_login: Optional[datetime] = None
    created_at: datetime
    modified_at: Optional[datetime] = None
    last_login: Optional[datetime] = None

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "email": "john.doe@example.com",
                "first_name": "John",
                "last_name": "Doe",
                "cellphone": "+523178901234",
                "rol": Roles.ADMIN,
                "is_active": True,
                "last_login": "2021-01-01T00:00:00Z",
                "created_at": "2021-01-01T00:00:00Z",
                "modified_at": "2021-01-01T00:00:00Z",
                "last_login": "2021-01-01T00:00:00Z"
            }
        }

