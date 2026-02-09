from ..repositories import ServiceRepository
from ..dtos import CreateServiceDTO, UpdateServiceDTO, ServiceResponseDTO
from ..exeptions import ServiceNotFound, ServiceAlreadyExists
from datetime import datetime
from ..models import Service

class ServiceService:
    def __init__(self, service_repository: ServiceRepository):
        self.service_repository = service_repository

    def create_service(self, service_dto: CreateServiceDTO) -> ServiceResponseDTO:
        if self.service_repository.get_by_name(service_dto.name):
            raise ServiceAlreadyExists()
        service = self.service_repository.create(
            Service(**service_dto.model_dump(), created_by="system", created_at=datetime.now())
        )
        return ServiceResponseDTO.model_validate(service)

    def get_all_services(self) -> list[ServiceResponseDTO]:
        services = self.service_repository.get_all()
        return [ServiceResponseDTO.model_validate(service) for service in services]

    def get_service_by_id(self, id: int) -> ServiceResponseDTO:
        service = self.service_repository.get_by_id(id)
        if not service:
            raise ServiceNotFound()
        return ServiceResponseDTO.model_validate(service)     
    
    def update_service(self, service_dto: UpdateServiceDTO) -> ServiceResponseDTO:
        service = self.service_repository.get_by_id(service_dto.id)
        if not service:
            raise ServiceNotFound()
        service = self.service_repository.update(
            Service(**service_dto.model_dump(), modified_by="system", modified_at=datetime.now())
        )
        return ServiceResponseDTO.model_validate(service)

    def delete_service(self, id: int) -> bool:
        service = self.service_repository.get_by_id(id)
        if not service:
            raise ServiceNotFound()
        return self.service_repository.delete(id)