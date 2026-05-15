from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

from ..models import AppointmentStatus
from .client_dto import ClientResponseDTO, CreateClientDTO
from .promotion_dto import PromotionResponseDTO
from .service_dto import ServiceResponseDTO
from .user_dto import UserResponseDTO
class CreateAppointmentDTO(BaseModel):
    client: CreateClientDTO
    appointment_date: datetime
    detail_service: Optional[str] = None
    list_services: Optional[list[int]] = None
    status: AppointmentStatus
    promotion_id: Optional[int] = None
    subtotal: Optional[float] = None
    total: Optional[float] = None
    duration: Optional[int] = None
    user_id: Optional[int] = Field(
        default=None,
        description="Profesional asignado (panel admin: sin comprobar agenda). Si no se envía, se elige al azar entre los libres en ese horario.",
    )

class UpdateAppointmentDTO(BaseModel):
    id: int
    client_id: int
    user_id: Optional[int] = None
    appointment_date: datetime
    detail_service: Optional[str] = None
    list_services: Optional[list[int]] = None
    status: AppointmentStatus
    promotion_id: Optional[int] = None
    subtotal: Optional[float] = None
    total: Optional[float] = None
    duration: Optional[int] = None

class AppointmentResponseDTO(BaseModel):
    id: int
    client: ClientResponseDTO
    user_id: Optional[int] = None
    user: Optional[UserResponseDTO] = None
    appointment_date: datetime
    detail_service: Optional[str] = None
    list_services: Optional[list[ServiceResponseDTO]] = None
    status: AppointmentStatus
    promotion_id: Optional[int] = None
    promotion: Optional[PromotionResponseDTO] = None
    subtotal: float
    total: float
    duration: Optional[int] = None
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
                "user_id": 1,
                "user": {
                    "id": 1,
                    "email": "john.doe@example.com",
                    "first_name": "John",
                    "last_name": "Doe",
                    "cellphone": "+523178901234",
                    "rol": "admin",
                    "is_active": True,
                    "last_login": "2021-01-01T00:00:00Z",
                    "created_at": "2021-01-01T00:00:00Z",
                    "modified_at": "2021-01-01T00:00:00Z",
                    "last_login": "2021-01-01T00:00:00Z"
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
                "appointment_date": "2021-01-01T00:00:00Z",
                "detail_service": "Detail of service 1",
                "status": "in_progress",
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
                "duration": 60,
                "created_at": "2021-01-01T00:00:00Z",
                "modified_at": "2021-01-01T00:00:00Z"
            }
        }
