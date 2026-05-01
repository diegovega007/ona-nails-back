from fastapi import APIRouter, Depends, status
from ..services import AppointmentServiceService, ServiceService, CloudinaryService
from ..dtos import CreateAppointmentServiceDTO, UpdateAppointmentServiceDTO, AppointmentServiceResponseDTO
from ..repositories import AppointmentServiceRepository, ServiceRepository
from ..config import get_session
from sqlmodel import Session

def get_appointment_service_service(session: Session = Depends(get_session)) -> AppointmentServiceService:
    return AppointmentServiceService(
        appointment_service_repository=AppointmentServiceRepository(session),
        service_service=ServiceService(ServiceRepository(session), CloudinaryService()))

router = APIRouter(prefix="/appointment-services", tags=["Appointment Services"])

@router.get("/", response_model=list[AppointmentServiceResponseDTO], status_code=status.HTTP_200_OK)
def get_all_appointment_services(
        appointment_id: int = None,
        appointment_service_service: AppointmentServiceService = Depends(get_appointment_service_service)
    ):
    return appointment_service_service.get_all_appointment_services(appointment_id)

@router.get("/{id}", response_model=AppointmentServiceResponseDTO, status_code=status.HTTP_200_OK)
def get_appointment_service_by_id(
        id: int, 
        appointment_service_service: AppointmentServiceService = Depends(get_appointment_service_service)
    ):
    return appointment_service_service.get_appointment_service_by_id(id)

@router.post("/", response_model=list[AppointmentServiceResponseDTO], status_code=status.HTTP_201_CREATED)
def create_appointment_service(
        create_appointment_service_dto: CreateAppointmentServiceDTO,
        appointment_service_service: AppointmentServiceService = Depends(get_appointment_service_service)
    ):
    return appointment_service_service.create_appointment_service(create_appointment_service_dto)

@router.put("/", response_model=list[AppointmentServiceResponseDTO], status_code=status.HTTP_200_OK)
def update_appointment_service(
        update_appointment_service_dto: UpdateAppointmentServiceDTO,
        appointment_service_service: AppointmentServiceService = Depends(get_appointment_service_service)
    ):
    return appointment_service_service.update_appointment_service(update_appointment_service_dto)