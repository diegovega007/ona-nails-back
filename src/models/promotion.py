from .base_model import BaseModel
from sqlmodel import Field

class Promotion(BaseModel, table=True):
    __tablename__ = "promotions"

    identifier: str = Field(nullable=False, max_length=50)
    name: str = Field(nullable=False, max_length=150)
    description: str = Field(nullable=True, max_length=255)
    created_by: str = Field(nullable=False, max_length=150)
    modified_by: str = Field(nullable=True, max_length=150)