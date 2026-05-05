from pydantic import BaseModel
from datetime import datetime, time
from .appointment_dto import AppointmentResponseDTO


class WorkingHoursDTO(BaseModel):
    start: time
    end: time

class AgendaResponseDTO(BaseModel):
    avilable_schedule: list[datetime]
    reserved_schedule: list[AppointmentResponseDTO]

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "avilable_schedule": ["2021-01-01T00:00:00Z", "2021-01-01T00:00:00Z"],
                "reserved_schedule": [
                    {
                    "id": 1,
                    "client": {
                        "id": 1,
                        "name": "John",
                        "last_name": "Doe",
                        "cellphone": "+523178901234",
                        "email": "john.doe@example.com"
                    },
                    "list_services": [
                        {
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
                        }
                    ],
                    "appointment_date": "2021-01-01T00:00:00Z",
                    "detail_service": "Detail of service 1",
                    "status": "in_progress",
                    "duration": 60,
                    "created_at": "2021-01-01T00:00:00Z",
                    "modified_at": "2021-01-01T00:00:00Z"
                    }
                ]
            }
        }
