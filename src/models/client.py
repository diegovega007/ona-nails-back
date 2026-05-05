from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship

from .base_model import BaseModel

if TYPE_CHECKING:
    from .appointment import Appointment


class Client(BaseModel, table=True):
    __tablename__ = "clients"

    name: str = Field(nullable=False, max_length=255)
    last_name: str = Field(nullable=False, max_length=255)
    cellphone: str = Field(nullable=False, max_length=20)
    email: str = Field(nullable=True, max_length=255)
    loyalty_completed: int = Field(nullable=False, default=0)

    appointments: list["Appointment"] = Relationship(back_populates="client")
