from .base_model import BaseModel
from sqlmodel import Field, Relationship
from typing import Optional
from .appointment import Appointment
from .service import Service

class AppointmentService(BaseModel, table=True):
    __tablename__ = "appointment_services"

    appointment_id: int = Field(nullable=False, foreign_key="appointments.id")
    service_id: int = Field(nullable=False, foreign_key="services.id")
    created_by: str = Field(nullable=False, max_length=150)
    modified_by: str = Field(nullable=True, max_length=150)

    appointment: Optional["Appointment"] = Relationship()
    service: Optional["Service"] = Relationship()