from fastapi import APIRouter, Depends, status
from ..services import ServiceTypeService
from ..repositories import ServiceTypeRepository
from ..config import get_session
from sqlmodel import Session
from ..dtos import ServiceTypeResponseDTO, CreateServiceTypeDTO, UpdateServiceTypeDTO
from ..utils.auth_dependency import authorization_header

def get_service_type_service(session: Session = Depends(get_session)) -> ServiceTypeService:
    return ServiceTypeService(ServiceTypeRepository(session))

router = APIRouter(prefix="/services-type", tags=["Services Type"])

@router.get("/", response_model=list[ServiceTypeResponseDTO], status_code=status.HTTP_200_OK)
def get_service_types(service_type_service: ServiceTypeService = Depends(get_service_type_service),
     auth: dict = Depends(authorization_header)):
    return service_type_service.get_all_service_types()

@router.get("/{id}", response_model=ServiceTypeResponseDTO, status_code=status.HTTP_200_OK)
def get_service_type_by_id(id: int, service_type_service: ServiceTypeService = Depends(get_service_type_service), 
    auth: dict = Depends(authorization_header)):
    return service_type_service.get_service_type_by_id(id)

@router.post("/", response_model=ServiceTypeResponseDTO, status_code=status.HTTP_201_CREATED)
def create_service_type(service_type_dto: CreateServiceTypeDTO, service_type_service: ServiceTypeService = Depends(get_service_type_service),
     auth: dict = Depends(authorization_header)):
    return service_type_service.create_service_type(service_type_dto)

@router.put("/{id}", response_model=ServiceTypeResponseDTO, status_code=status.HTTP_200_OK)
def update_service_type(service_type_dto: UpdateServiceTypeDTO, service_type_service: ServiceTypeService = Depends(get_service_type_service), 
    auth: dict = Depends(authorization_header)):
    return service_type_service.update_service_type(service_type_dto)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_service_type(id: int, service_type_service: ServiceTypeService = Depends(get_service_type_service),
     auth: dict = Depends(authorization_header)):
    return service_type_service.delete_service_type(id)