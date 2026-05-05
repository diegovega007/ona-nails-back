from pydantic import BaseModel
from datetime import datetime
from typing import Optional

from ..models import AppointmentStatus, PromotionType
from .client_dto import ClientResponseDTO, CreateClientDTO
from .service_dto import ServiceResponseDTO
class CreateAppointmentDTO(BaseModel):
    client: CreateClientDTO
    appointment_date: datetime
    detail_service: Optional[str] = None
    list_services: Optional[list[int]] = None
    status: AppointmentStatus
    promotion: Optional[PromotionType] = PromotionType.NO_PROMOTION
    subtotal: Optional[float] = None
    total: Optional[float] = None

class UpdateAppointmentDTO(BaseModel):
    id: int
    client_id: int
    appointment_date: datetime
    detail_service: Optional[str] = None
    list_services: Optional[list[int]] = None
    status: AppointmentStatus
    promotion: Optional[PromotionType] = PromotionType.NO_PROMOTION
    discount: Optional[float] = None
    subtotal: Optional[float] = None
    total: Optional[float] = None

class AppointmentResponseDTO(BaseModel):
    id: int
    client: ClientResponseDTO
    appointment_date: datetime
    detail_service: Optional[str] = None
    list_services: Optional[list[ServiceResponseDTO]] = None
    status: AppointmentStatus
    promotion: PromotionType
    subtotal: float
    total: float
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
                "created_at": "2021-01-01T00:00:00Z",
                "modified_at": "2021-01-01T00:00:00Z"
            }
        }
