from pydantic import BaseModel
from datetime import datetime
from typing import Optional

from ..models import AppointmentStatus
from .client_dto import ClientResponseDTO, CreateClientDTO
from .service_dto import ServiceResponseDTO

class CreateAppointmentDTO(BaseModel):
    client: CreateClientDTO
    appointment_date: datetime
    appintment_duration: Optional[int] = None
    detail_service: Optional[str] = None
    status: AppointmentStatus

class UpdateAppointmentDTO(BaseModel):
    id: int
    client_id: int
    appointment_date: datetime
    appintment_duration: Optional[int] = None
    detail_service: Optional[str] = None
    status: AppointmentStatus

class AppointmentResponseDTO(BaseModel):
    id: int
    client: ClientResponseDTO
    appointment_date: datetime
    appintment_duration: Optional[int] = None
    detail_service: Optional[str] = None
    status: AppointmentStatus
    created_at: datetime
    modified_at: Optional[datetime] = None

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "client": {
                    "id": 1,
                    "name": "John",
                    "last_name": "Doe",
                    "cellphone": "+523178901234",
                    "email": "john.doe@example.com"
                },
                "appointment_date": "2021-01-01T00:00:00Z",
                "appintment_duration": 60,
                "detail_service": "Detail of service 1",
                "status": "in_progress",
                "created_at": "2021-01-01T00:00:00Z",
                "modified_at": "2021-01-01T00:00:00Z"
            }
        }
