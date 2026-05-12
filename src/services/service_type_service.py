from ..repositories import ServiceTypeRepository
from ..dtos import CreateServiceTypeDTO, UpdateServiceTypeDTO, ServiceTypeResponseDTO
from ..exeptions import ServiceTypeNotFound, ServiceTypeAlreadyExists
from datetime import datetime
from ..models import ServiceType
from ..utils.auth_dependency import current_user

class ServiceTypeService:
    def __init__(self, service_type_repository: ServiceTypeRepository):
        self.service_type_repository = service_type_repository

    def get_all_service_types(self) -> list[ServiceTypeResponseDTO]:
        service_types = self.service_type_repository.get_all()
        return [ServiceTypeResponseDTO.model_validate(service_type) for service_type in service_types]

    def get_service_type_by_id(self, id: int) -> ServiceTypeResponseDTO:
        service_type = self.service_type_repository.get_by_id(id)
        if not service_type:
            raise ServiceTypeNotFound()
        return ServiceTypeResponseDTO.model_validate(service_type)

    def create_service_type(self, service_type_dto: CreateServiceTypeDTO, current_user: str = "system") -> ServiceTypeResponseDTO:
        if self.service_type_repository.get_by_name(service_type_dto.name):
            raise ServiceTypeAlreadyExists()
        service_type = self.service_type_repository.create(
            ServiceType(**service_type_dto.model_dump(), created_by=current_user, created_at=datetime.now())
        )
        return ServiceTypeResponseDTO.model_validate(service_type)

    def update_service_type(self, service_type_dto: UpdateServiceTypeDTO, current_user: str = "system") -> ServiceTypeResponseDTO:
        service_type = self.service_type_repository.get_by_id(service_type_dto.id)
        if not service_type:
            raise ServiceTypeNotFound()
        service_type = self.service_type_repository.update(
            ServiceType(**service_type_dto.model_dump(), modified_by=current_user, modified_at=datetime.now())
        )
        return ServiceTypeResponseDTO.model_validate(service_type)
    
    def delete_service_type(self, id: int) -> None:
        service_type = self.service_type_repository.get_by_id(id)
        if not service_type:
            raise ServiceTypeNotFound()
        return self.service_type_repository.delete(id)