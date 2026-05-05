from .base_model import BaseModel
from sqlmodel import Field, Relationship
from typing import Optional
from .service_type import ServiceType

class Service(BaseModel, table=True):
    __tablename__ = "services"

    service_type_id: int = Field(nullable=False, foreign_key="services_type.id")
    name: str = Field(nullable=False, max_length=255)
    description: str = Field(nullable=True, max_length=255)
    photo: str = Field(nullable=True, max_length=500)
    photo_public_id: str = Field(nullable=True, max_length=255)
    price: float = Field(nullable=False)
    enabled: bool = Field(nullable=False, default=True)
    created_by: str = Field(nullable=False, max_length=150)
    modified_by: str = Field(nullable=True, max_length=150)
    duration: int = Field(nullable=False)

    service_type: Optional["ServiceType"] = Relationship()