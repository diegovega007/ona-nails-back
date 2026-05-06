from fastapi import APIRouter, Depends
from ..services import AgendaService, AppointmentService
from ..repositories import AppointmentRepository, ServiceRepository, ClientRepository, AppointmentServiceRepository, PromotionRepository
from ..config import get_session
from sqlmodel import Session
from ..services import ServiceService, CloudinaryService, ClientService, AppointmentServiceService
from ..dtos import AgendaResponseDTO
from datetime import datetime

def get_agenda_service(session: Session = Depends(get_session)) -> AgendaService:
    return AgendaService(
        appointment_service=AppointmentService(
            appointment_repository=AppointmentRepository(session),
            service_service=ServiceService(ServiceRepository(session), CloudinaryService()),
            client_service=ClientService(ClientRepository(session)),
            appointment_service_service=AppointmentServiceService(AppointmentServiceRepository(session), ServiceService(ServiceRepository(session), CloudinaryService())),
            promotion_repository=PromotionRepository(session),
        )
    )

router = APIRouter(prefix="/agenda", tags=["Agenda"])

@router.get("/", response_model=AgendaResponseDTO)
def get_agenda(initial_date: datetime, final_date: datetime, agenda_service: AgendaService = Depends(get_agenda_service)):
    return agenda_service.get_agenda(initial_date, final_date)