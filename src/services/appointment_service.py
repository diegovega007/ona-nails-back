from ..repositories import AppointmentRepository
from .service_service import ServiceService
from .client_service import ClientService
from ..dtos import CreateAppointmentDTO, UpdateAppointmentDTO, AppointmentResponseDTO
from ..exeptions import AppointmentNotFound, AppointmentAlreadyExists, AppointmentDateNotAvailable, AppointmentClientNotFound
from datetime import datetime
from ..models import Appointment, AppointmentStatus

class AppointmentService:
    def __init__(self, appointment_repository: AppointmentRepository, service_service: ServiceService,
    client_service: ClientService):
        self.appointment_repository = appointment_repository
        self.client_service = client_service
        self.service_service = service_service

    def create_appointment(self, appointment_dto: CreateAppointmentDTO) -> AppointmentResponseDTO:
        service = self.service_service.get_service_by_id(appointment_dto.service_id)
        client = self.client_service.create(appointment_dto.client)
        if self.appointment_repository.get_all(cellphone=client.cellphone, status=AppointmentStatus.RECEIVED):
            raise AppointmentAlreadyExists()
        if self.appointment_repository.get_all(date=appointment_dto.appointment_date):
            raise AppointmentDateNotAvailable()
        appointment = self.appointment_repository.create(
            Appointment(**appointment_dto.model_dump(exclude={"client"}), client_id=client.id, created_at=datetime.now())
        )

        return AppointmentResponseDTO.model_validate(
            {
                "id": appointment.id,
                "client": client,
                "service":service,
                "appointment_date": appointment.appointment_date,
                "appintment_duration": appointment.appintment_duration,
                "detail_service": appointment.detail_service,
                "status": appointment.status,
                "created_at": appointment.created_at,
                "modified_at": appointment.modified_at,
            }
        )
    
    def update_appointment(self, appointment_dto: UpdateAppointmentDTO) -> AppointmentResponseDTO:
        appointment = self.appointment_repository.get_by_id(appointment_dto.id)
        if not appointment:
            raise AppointmentNotFound()
        appointment = self.appointment_repository.update(
            Appointment(**appointment_dto.model_dump(), modified_by="system", modified_at=datetime.now())
        )
        return AppointmentResponseDTO.model_validate(appointment)

    def get_all_appointments(self, cellphone: str = None, status: AppointmentStatus = None, date: datetime = None) -> list[AppointmentResponseDTO]:
        appointments = self.appointment_repository.get_all(cellphone=cellphone, status=status, date=date)
        if not appointments:
            raise AppointmentClientNotFound()
        
        return [AppointmentResponseDTO.model_validate(appointment) for appointment in appointments]

    def get_appointment_by_id(self, id: int) -> AppointmentResponseDTO:
        appointment = self.appointment_repository.get_by_id(id)
        if not appointment:
            raise AppointmentNotFound()
        return AppointmentResponseDTO.model_validate(appointment)
    
    def delete_appointment(self, id: int) -> bool:
        appointment = self.appointment_repository.get_by_id(id)
        if not appointment:
            raise AppointmentNotFound()
        return self.appointment_repository.delete(id)

