from ..repositories import AppointmentServiceRepository
from ..dtos import  AppointmentServiceResponseDTO, CreateAppointmentServiceDTO, UpdateAppointmentServiceDTO
from ..models import AppointmentService
from ..exeptions import AppointmentServiceNotFound
from .service_service import ServiceService
from datetime import datetime

class AppointmentServiceService:
    def __init__(self, appointment_service_repository: AppointmentServiceRepository, service_service: ServiceService):
        self.appointment_service_repository = appointment_service_repository
        self.service_service = service_service

    def get_all_appointment_services(self, appointment_id: int = None) -> list[AppointmentServiceResponseDTO]:
        appointment_services = self.appointment_service_repository.get_all(appointment_id)
        return [AppointmentServiceResponseDTO.model_validate(appointment_service) for appointment_service in appointment_services]
    
    def get_appointment_service_by_id(self, id: int) -> AppointmentServiceResponseDTO:
        appointment_service = self.appointment_service_repository.get_by_id(id)
        if not appointment_service:
            raise AppointmentServiceNotFound()
        return AppointmentServiceResponseDTO.model_validate(appointment_service)

    def create_appointment_service(self, create_appointment_service_dto: CreateAppointmentServiceDTO, current_user: str = "system") -> list[AppointmentServiceResponseDTO]:
        appointment_services = []
        for service_id in create_appointment_service_dto.service_ids:
            service = self.service_service.get_service_by_id(service_id)
            appointment_services.append(AppointmentService(service_id=service.id, appointment_id=create_appointment_service_dto.appointment_id, created_at=datetime.now(), created_by=current_user))
        appointment_services = self.appointment_service_repository.create_many(appointment_services)
        return [AppointmentServiceResponseDTO.model_validate(appointment_service) for appointment_service in appointment_services]

    def update_appointment_service(self, update_appointment_service_dto: UpdateAppointmentServiceDTO, current_user: str = "system") -> list[AppointmentServiceResponseDTO]:
        appointment_services = []
        appointment_services_query  = self.get_all_appointment_services(update_appointment_service_dto.appointment_id)
        appointment_services_ids = [appointment_service.id for appointment_service in appointment_services_query]

        for appointment_service_id in appointment_services_ids:
            self.appointment_service_repository.delete(appointment_service_id)
    
        for service_id in update_appointment_service_dto.service_ids:
            service = self.service_service.get_service_by_id(service_id)
            appointment_services.append(AppointmentService(service_id=service.id, appointment_id=update_appointment_service_dto.appointment_id, created_at=datetime.now(), created_by=current_user))

        appointment_services = self.appointment_service_repository.create_many(appointment_services)
        return [AppointmentServiceResponseDTO.model_validate(appointment_service) for appointment_service in appointment_services]
