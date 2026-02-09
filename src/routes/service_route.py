from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from ..services import ServiceService
from ..dtos import CreateServiceDTO, UpdateServiceDTO, ServiceResponseDTO
from ..repositories import ServiceRepository
from ..config import get_session
from sqlmodel import Session

def get_service_service(session: Session = Depends(get_session)) -> ServiceService:
    return ServiceService(ServiceRepository(session))

router = APIRouter(prefix="/services", tags=["Services"])

@router.post("/", response_model=ServiceResponseDTO, status_code=status.HTTP_201_CREATED)
def create_service(service_dto: CreateServiceDTO, service_service: ServiceService = Depends(get_service_service)):
    return service_service.create_service(service_dto)

@router.get("/", response_model=list[ServiceResponseDTO], status_code=status.HTTP_200_OK)
def get_all_services(service_service: ServiceService = Depends(get_service_service)):
    return service_service.get_all_services()

@router.get("/{id}", response_model=ServiceResponseDTO, status_code=status.HTTP_200_OK)
def get_service_by_id(id: int, service_service: ServiceService = Depends(get_service_service)):
    return service_service.get_service_by_id(id)

@router.put("/", response_model=ServiceResponseDTO, status_code=status.HTTP_200_OK)
def update_service(service_dto: UpdateServiceDTO, service_service: ServiceService = Depends(get_service_service)):
    return service_service.update_service(service_dto)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_service(id: int, service_service: ServiceService = Depends(get_service_service)):
    return service_service.delete_service(id)