from .base_model import BaseModel
from sqlmodel import Field
from typing import Optional
from datetime import datetime
from enum import Enum

class Roles(str, Enum):
    ADMIN = "admin"
    RECEPTIONIST = "receptionist"

class User(BaseModel, table=True):
    __tablename__ = "users"

    email: str = Field(nullable=False, unique=True, max_length=255)
    password: str = Field(nullable=False, max_length=255)
    first_name: str = Field(nullable=False, max_length=255)
    last_name: str = Field(nullable=False, max_length=255)
    cellphone: str = Field(nullable=True, max_length=20)
    rol: Roles = Field(nullable=False)
    is_active: bool = Field(nullable=False, default=True)
    last_login: datetime = Field(nullable=True)