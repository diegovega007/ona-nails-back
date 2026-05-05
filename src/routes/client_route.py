from fastapi import APIRouter, Depends, status
from ..services import ClientService
from ..dtos import ClientAppointmentsResponseDTO, ClientResponseDTO, UpdateClientDTO
from ..repositories import ClientRepository
from ..config import get_session
from sqlmodel import Session
from ..utils.auth_dependency import authorization_header

def get_client_service(session: Session = Depends(get_session)) -> ClientService:
    return ClientService(ClientRepository(session))

router = APIRouter(prefix="/clients", tags=["Clients"])

@router.get("/", response_model=list[ClientAppointmentsResponseDTO], status_code=status.HTTP_200_OK)
def get_all_clients(client_service: ClientService = Depends(get_client_service)):
    return client_service.get_all_clients()

@router.put("/", response_model=ClientResponseDTO, status_code=status.HTTP_200_OK)
def update_client(client_dto: UpdateClientDTO, client_service: ClientService = Depends(get_client_service), auth: dict = Depends(authorization_header)):
    return client_service.update_client(client_dto)