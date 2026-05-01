from ..repositories import AppointmentRepository
from .service_service import ServiceService
from .client_service import ClientService
from .appointment_service_service import AppointmentServiceService
from ..dtos import CreateAppointmentDTO, UpdateAppointmentDTO, AppointmentResponseDTO, CreateAppointmentServiceDTO, UpdateAppointmentServiceDTO
from ..exeptions import AppointmentNotFound, AppointmentAlreadyExists, AppointmentDateNotAvailable
from datetime import datetime
from ..models import Appointment, AppointmentStatus

class AppointmentService:
    def __init__(self, appointment_repository: AppointmentRepository, service_service: ServiceService,
    client_service: ClientService, appointment_service_service: AppointmentServiceService):
        self.appointment_repository = appointment_repository
        self.client_service = client_service
        self.service_service = service_service
        self.appointment_service_service = appointment_service_service

    def create_appointment(self, appointment_dto: CreateAppointmentDTO) -> AppointmentResponseDTO:
        client = self.client_service.create(appointment_dto.client)
        if self.appointment_repository.get_all(cellphone=client.cellphone, status=AppointmentStatus.RECEIVED):
            raise AppointmentAlreadyExists()
        if self.appointment_repository.get_all(date=appointment_dto.appointment_date):
            raise AppointmentDateNotAvailable()
        appointment = self.appointment_repository.create(
            Appointment(**appointment_dto.model_dump(exclude={"client", "list_services"}), client_id=client.id, created_at=datetime.now())
        )
        appointment_services = self.appointment_service_service.create_appointment_service(
            CreateAppointmentServiceDTO(
                appointment_id=appointment.id, 
                service_ids=appointment_dto.list_services
            )
        )
        list_services = [appointment_service.service for appointment_service in appointment_services]

        return AppointmentResponseDTO.model_validate(
            {
                "id": appointment.id,
                "client": client,
                "appointment_date": appointment.appointment_date,
                "detail_service": appointment.detail_service,
                "status": appointment.status,
                "created_at": appointment.created_at,
                "modified_at": appointment.modified_at,
                "list_services": list_services,
            }
        )
    
    def update_appointment(self, appointment_dto: UpdateAppointmentDTO) -> AppointmentResponseDTO:
        appointment = self.appointment_repository.get_by_id(appointment_dto.id)
        if not appointment:
            raise AppointmentNotFound()
        appointment = self.appointment_repository.update(
            Appointment(**appointment_dto.model_dump(), modified_by="system", modified_at=datetime.now())
        )
        appointment_services = self.appointment_service_service.update_appointment_service(
            UpdateAppointmentServiceDTO(
                appointment_id=appointment.id,
                service_ids=appointment_dto.list_services
            )
        )
        list_services = [
            appointment_service.service
            for appointment_service in appointment_services
            if appointment_service.service is not None
        ]
        return self._appointment_to_response(appointment, list_services=list_services)

    def get_all_appointments(self, cellphone: str = None, status: AppointmentStatus = None, date: datetime = None) -> list[AppointmentResponseDTO]:
        appointments = self.appointment_repository.get_all(cellphone=cellphone, status=status, date=date)

        return [self._appointment_to_response(a) for a in appointments]

    def get_appointment_by_id(self, id: int) -> AppointmentResponseDTO:
        appointment = self.appointment_repository.get_by_id(id)
        if not appointment:
            raise AppointmentNotFound()
        return self._appointment_to_response(appointment)
    
    def delete_appointment(self, id: int) -> bool:
        appointment = self.appointment_repository.get_by_id(id)
        if not appointment:
            raise AppointmentNotFound()
        return self.appointment_repository.delete(id)

    def _appointment_to_response(self, appointment: Appointment, list_services: list = None) -> AppointmentResponseDTO:
        if list_services is None:
            list_services = [
                link.service
                for link in appointment.appointment_services
                if link.service is not None and link.service is not None
            ]
        return AppointmentResponseDTO.model_validate(
            {
                "id": appointment.id,
                "client": appointment.client,
                "appointment_date": appointment.appointment_date,
                "detail_service": appointment.detail_service,
                "list_services": list_services,
                "status": appointment.status,
                "created_at": appointment.created_at,
                "modified_at": appointment.modified_at,
            }
        )

