from .base_model import BaseModel
from sqlmodel import Field

class Service(BaseModel, table=True):
    __tablename__ = "services"

    name: str = Field(nullable=False, max_length=255)
    description: str = Field(nullable=True, max_length=255)
    photo: str = Field(nullable=True, max_length=255)
    price: float = Field(nullable=False)
    enabled: bool = Field(nullable=False, default=True)
    created_by: str = Field(nullable=False, max_length=150)
    modified_by: str = Field(nullable=True, max_length=150)