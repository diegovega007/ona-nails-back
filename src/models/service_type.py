from .base_model import BaseModel
from sqlmodel import Field

class ServiceType(BaseModel, table=True):
    __tablename__ = "services_type"

    name: str = Field(nullable=False, max_length=255)
    description: str = Field(nullable=True, max_length=255)
    created_by: str = Field(nullable=False, max_length=150)
    modified_by: str = Field(nullable=True, max_length=150)