from fastapi import APIRouter, Depends, status

from ..services import AppointmentService, ClientService, ServiceService, CloudinaryService, AppointmentServiceService
from ..dtos import CreateAppointmentDTO, UpdateAppointmentDTO, AppointmentResponseDTO
from ..repositories import AppointmentRepository, ClientRepository, ServiceRepository, AppointmentServiceRepository, PromotionRepository, UserRepository
from ..config import get_session
from sqlmodel import Session
from ..models import AppointmentStatus
from ..utils.auth_dependency import authorization_header, current_user, optional_current_user
from ..models import User
from datetime import datetime
from typing import Optional

def get_appointment_service(session: Session = Depends(get_session)) -> AppointmentService:
    return AppointmentService(
        appointment_repository=AppointmentRepository(session),
        service_service=ServiceService(ServiceRepository(session), CloudinaryService()),
        client_service=ClientService(ClientRepository(session)),
        appointment_service_service=AppointmentServiceService(AppointmentServiceRepository(session), ServiceService(ServiceRepository(session), CloudinaryService())),
        promotion_repository=PromotionRepository(session),
        user_repository=UserRepository(session),
    )

router = APIRouter(prefix="/appointments", tags=["Appointments"])

@router.post("/", response_model=AppointmentResponseDTO, status_code=status.HTTP_201_CREATED)
def create_appointment(
    appointment_dto: CreateAppointmentDTO,
    appointment_service: AppointmentService = Depends(get_appointment_service),
    user: Optional[User] = Depends(optional_current_user),
):
    return appointment_service.create_appointment(appointment_dto, current_user=user.email if user else "system")

@router.get("/", response_model=list[AppointmentResponseDTO], status_code=status.HTTP_200_OK)
def get_all_appointments(
    cellphone: str = None, 
    status: AppointmentStatus = None, 
    date: datetime = None, 
    appointment_service: AppointmentService = Depends(get_appointment_service)
    ):
    return appointment_service.get_all_appointments(cellphone, status, date)

@router.get("/{id}", response_model=AppointmentResponseDTO, status_code=status.HTTP_200_OK)
def get_appointment_by_id(id: int, appointment_service: AppointmentService = Depends(get_appointment_service)):
    return appointment_service.get_appointment_by_id(id)

@router.put("/", response_model=AppointmentResponseDTO, status_code=status.HTTP_200_OK)
def update_appointment(
    appointment_dto: UpdateAppointmentDTO,
    appointment_service: AppointmentService = Depends(get_appointment_service),
    user: User = Depends(current_user),
):
    return appointment_service.update_appointment(appointment_dto, current_user=user.email)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_appointment(id: int, appointment_service: AppointmentService = Depends(get_appointment_service), auth: dict = Depends(authorization_header)):
    return appointment_service.delete_appointment(id)