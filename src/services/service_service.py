from ..repositories import ServiceRepository
from ..dtos import CreateServiceDTO, UpdateServiceDTO, ServiceResponseDTO
from ..exeptions import ServiceNotFound, ServiceAlreadyExists
from .cloudinary_service import CloudinaryService
from datetime import datetime
from ..models import Service
from fastapi import UploadFile

class ServiceService:
    def __init__(self, service_repository: ServiceRepository, cloudinary_service: CloudinaryService):
        self.service_repository = service_repository
        self.cloudinary_service = cloudinary_service

    def create_service(self, service_dto: CreateServiceDTO, current_user: str = "system") -> ServiceResponseDTO:
        if self.service_repository.get_by_name(service_dto.name):
            raise ServiceAlreadyExists()
        service = self.service_repository.create(
            Service(**service_dto.model_dump(), created_by=current_user, created_at=datetime.now())
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

    def update_service(self, service_dto: UpdateServiceDTO, current_user: str = "system") -> ServiceResponseDTO:
        service = self.service_repository.get_by_id(service_dto.id)
        if not service:
            raise ServiceNotFound()
        service = self.service_repository.update(
            Service(
                **service_dto.model_dump(),
                photo=service.photo,
                photo_public_id=service.photo_public_id,
                modified_by=current_user,
                modified_at=datetime.now(),
            )
        )
        return ServiceResponseDTO.model_validate(service)

    def upload_photo(self, id: int, file: UploadFile) -> ServiceResponseDTO:
        service = self.service_repository.get_by_id(id)
        if not service:
            raise ServiceNotFound()
        if service.photo_public_id:
            self.cloudinary_service.delete([service.photo_public_id])
        uploaded = self.cloudinary_service.upload(file.file)
        service = self.service_repository.update(
            Service(
                id=service.id,
                photo=uploaded.get("url"),
                photo_public_id=uploaded.get("public_id"),
            )
        )
        return ServiceResponseDTO.model_validate(service)

    def delete_service(self, id: int) -> bool:
        service = self.service_repository.get_by_id(id)
        if not service:
            raise ServiceNotFound()
        if service.photo_public_id:
            self.cloudinary_service.delete([service.photo_public_id])
        return self.service_repository.delete(id)

