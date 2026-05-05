from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import ENUM as PG_ENUM

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

class PromotionType(str, Enum):
    DISCOUNT = "discount"
    SERVICE_FREE = "service_free"
    NO_PROMOTION = "no_promotion"


_promotion_pg = PG_ENUM(
    PromotionType,
    name="promotiontype",
    create_type=False,
    values_callable=lambda objs: [e.value for e in objs],
)


class Appointment(BaseModel, table=True):
    __tablename__ = "appointments"

    client_id: int = Field(nullable=True, foreign_key="clients.id")
    appointment_date: datetime = Field(nullable=False)
    detail_service: str = Field(nullable=True, max_length=500)
    status: AppointmentStatus = Field(default=AppointmentStatus.RECEIVED)
    promotion: PromotionType = Field(
        default=PromotionType.NO_PROMOTION,
        sa_column=Column(_promotion_pg, nullable=False),
    )
    subtotal : float = Field(nullable=False)
    total : float = Field(nullable=False)
    
    client: Optional["Client"] = Relationship(back_populates="appointments")
    appointment_services: list["AppointmentService"] = Relationship(
        back_populates="appointment"
    )

