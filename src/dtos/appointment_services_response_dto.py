from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from ..models import AppointmentStatus
from .service_dto import ServiceResponseDTO


class AppointmentServicesResponseDTO(BaseModel):
    id: int
    appointment_date: datetime
    detail_service: Optional[str] = None
    list_services: Optional[list[ServiceResponseDTO]] = None
    status: AppointmentStatus
    created_at: datetime
    modified_at: Optional[datetime] = None
