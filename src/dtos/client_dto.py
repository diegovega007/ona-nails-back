from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from .appointment_services_response_dto import AppointmentServicesResponseDTO

class CreateClientDTO(BaseModel):
    name: str
    last_name: str
    cellphone: str
    email: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "name": "John",
                "last_name": "Doe",
                "cellphone": "+523178901234",
                "email": "john.doe@example.com"
            }
        }

class UpdateClientDTO(BaseModel):
    id: int
    name: str
    last_name: str
    cellphone: str
    email: Optional[str] = None
    loyalty_completed: int
    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "John",
                "last_name": "Doe",
                "cellphone": "+523178901234",
                "email": "john.doe@example.com",
                "loyalty_completed": 0
            }
        }

class ClientResponseDTO(BaseModel):
    id: int
    name: str
    last_name: str
    cellphone: str
    email: Optional[str] = None
    loyalty_completed: int
    created_at: datetime
    modified_at: Optional[datetime] = None

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "John",
                "last_name": "Doe",
                "cellphone": "+523178901234",
                "email": "john.doe@example.com",
                "created_at": "2021-01-01T00:00:00Z",
                "modified_at": "2021-01-01T00:00:00Z"
            }
        }

class ClientAppointmentsResponseDTO(BaseModel):
    id: int
    name: str
    last_name: str
    cellphone: str
    email: Optional[str] = None
    loyalty_completed: int
    created_at: datetime
    modified_at: Optional[datetime] = None
    appointments: Optional[list[AppointmentServicesResponseDTO]] = None

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "John",
                "last_name": "Doe",
                "cellphone": "+523178901234",
                "email": "john.doe@example.com",
                "loyalty_completed": 0,
                "created_at": "2021-01-01T00:00:00Z",
                "modified_at": "2021-01-01T00:00:00Z",
                "appointments": [
                    {
                        "id": 1,
                        "appointment_date": "2021-01-01T00:00:00Z",
                        "detail_service": "Detail of service 1",
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
                                "modified_at": "2021-01-01T00:00:00Z",
                                "service_type": {
                                    "id": 1,
                                    "name": "Service Type 1",
                                    "description": "Description of service type 1",
                                    "created_at": "2021-01-01T00:00:00Z",
                                    "created_by": "system",
                                    "modified_at": "2021-01-01T00:00:00Z",
                                    "modified_by": "system"
                                }
                            }
                        ],
                        "status": "in_progress",
                        "duration": 60,
                        "promotion_id": 1,
                        "promotion": {
                            "id": 1,
                            "identifier": "PROMO123",
                            "name": "Promotion 1",
                            "description": "Description of promotion 1",
                            "created_at": "2021-01-01T00:00:00Z",
                            "created_by": "system",
                            "modified_at": "2021-01-01T00:00:00Z",
                            "modified_by": "system"
                        },
                        "subtotal": 100.0,
                        "total": 100.0,
                        "created_at": "2021-01-01T00:00:00Z",
                        "modified_at": "2021-01-01T00:00:00Z"
                    }
                ]
            }
        }