from .base_model import BaseModel
from sqlmodel import Field, Relationship
from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING, Optional

from .client import Client

if TYPE_CHECKING:
    from .appointment_service import AppointmentService

class AppointmentStatus(str, Enum):
    IN_PROGRESS = "in_progress"
    DONE = "done"
    CANCELLED = "cancelled"
    RECEIVED = "received"

class Appointment(BaseModel, table=True):
    __tablename__ = "appointments"

    client_id: int = Field(nullable=True, foreign_key="clients.id")
    appointment_date: datetime = Field(nullable=False)
    detail_service: str = Field(nullable=True, max_length=500)
    status: AppointmentStatus = Field(default=AppointmentStatus.RECEIVED)

    client: Optional["Client"] = Relationship()
    appointment_services: list["AppointmentService"] = Relationship(
        back_populates="appointment"
    )

