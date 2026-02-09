from .base_model import BaseModel
from sqlmodel import Field

class Client(BaseModel, table=True):
    __tablename__ = "clients"

    name: str = Field(nullable=False, max_length=255)
    last_name: str = Field(nullable=False, max_length=255)
    cellphone: str = Field(nullable=False, max_length=20)
    email: str = Field(nullable=True, max_length=255)
