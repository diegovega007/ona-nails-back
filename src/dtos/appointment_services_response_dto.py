from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from ..models import AppointmentStatus
from .service_dto import ServiceResponseDTO
from .promotion_dto import PromotionResponseDTO
from .user_dto import UserResponseDTO

class AppointmentServicesResponseDTO(BaseModel):
    id: int
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
    duration: int
    created_at: datetime
    modified_at: Optional[datetime] = None
