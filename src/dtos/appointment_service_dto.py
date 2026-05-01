from pydantic import BaseModel
from .service_dto import ServiceResponseDTO
from .appointment_dto import AppointmentResponseDTO
from datetime import datetime
from typing import Optional

class CreateAppointmentServiceDTO(BaseModel):
    appointment_id: int
    service_ids: list[int]

    class Config:
        json_schema_extra = {
            "example": {
                "appointment_id": 1,
                "service_ids": [1, 2, 3]
            }
        }

class UpdateAppointmentServiceDTO(BaseModel):
    appointment_id: int
    service_ids: list[int]

    class Config:
        json_schema_extra = {
            "example": {
                "appointment_id": 1,
                "service_ids": [1, 2, 3]
            }
        }

class AppointmentServiceResponseDTO(BaseModel):
    id: int
    appointment: AppointmentResponseDTO
    service: ServiceResponseDTO
    created_at: datetime
    created_by: str
    modified_at: Optional[datetime] = None
    modified_by: Optional[str] = None

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "appointment": {
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
                },
                "service": {
                    "id": 1,
                    "name": "Service 1",
                    "description": "Description of service 1",
                    "photo": "https://res.cloudinary.com/example/image/upload/v1/service.jpg",
                    "photo_public_id": "service_1",
                    "price": 100.0,
                    "duration": 60,
                    "enabled": True,
                    "created_by": "system",
                    "modified_by": "system",
                    "created_at": "2021-01-01T00:00:00Z",
                    "modified_at": "2021-01-01T00:00:00Z"
                },
                "created_at": "2021-01-01T00:00:00Z",
                "modified_at": "2021-01-01T00:00:00Z",
                "created_by": "system",
                "modified_by": "system"
            }
        }