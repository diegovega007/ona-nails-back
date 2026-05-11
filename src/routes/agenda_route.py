from fastapi import APIRouter, Depends
from ..services import AgendaService, AppointmentService, AuthService, UserService
from ..repositories import AppointmentRepository, ServiceRepository, ClientRepository, AppointmentServiceRepository, PromotionRepository, UserRepository, UserSessionRepository
from ..config import get_session
from sqlmodel import Session
from ..services import ServiceService, CloudinaryService, ClientService, AppointmentServiceService
from ..dtos import AgendaResponseDTO
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

MX_TZ = ZoneInfo("America/Mexico_City")

def get_agenda_service(session: Session = Depends(get_session)) -> AgendaService:
    return AgendaService(
        appointment_service=AppointmentService(
            appointment_repository=AppointmentRepository(session),
            service_service=ServiceService(ServiceRepository(session), CloudinaryService()),
            client_service=ClientService(ClientRepository(session)),
            appointment_service_service=AppointmentServiceService(AppointmentServiceRepository(session), ServiceService(ServiceRepository(session), CloudinaryService())),
            promotion_repository=PromotionRepository(session),
        ),
        user_service=UserService(UserRepository(session), AuthService(), UserSessionRepository(session)),
    )

router = APIRouter(prefix="/agenda", tags=["Agenda"])

@router.get("/", response_model=AgendaResponseDTO)
def get_agenda(initial_date: datetime, final_date: datetime, agenda_service: AgendaService = Depends(get_agenda_service)):
    # Si initial_date es naive, asumir UTC (viene de toISOString() del frontend)
    if initial_date.tzinfo is None:
        initial_date = initial_date.replace(tzinfo=timezone.utc)
    if final_date.tzinfo is None:
        final_date = final_date.replace(tzinfo=timezone.utc)

    # Para el día de hoy, no mostrar slots que ya pasaron
    now_mx = datetime.now(tz=MX_TZ)
    initial_date_mx = initial_date.astimezone(MX_TZ)
    if initial_date_mx.date() == now_mx.date():
        if now_mx > initial_date_mx:
            initial_date = now_mx

    return agenda_service.get_agenda(initial_date, final_date)