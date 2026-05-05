from ..repositories import AppointmentRepository
from .service_service import ServiceService
from .client_service import ClientService
from .appointment_service_service import AppointmentServiceService
from ..dtos import CreateAppointmentDTO, UpdateAppointmentDTO, AppointmentResponseDTO, CreateAppointmentServiceDTO, UpdateAppointmentServiceDTO, UpdateClientDTO
from ..exeptions import AppointmentNotFound, AppointmentAlreadyExists, AppointmentDateNotAvailable
from datetime import datetime
from ..models import Appointment, AppointmentStatus, PromotionType
from ..utils.promotions import get_promotion

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

        subtotal = self._subtotal_from_service_ids(appointment_dto.list_services)
        appointment_dto.subtotal = subtotal
        appointment_dto.total = subtotal

        appointment = self.appointment_repository.create(
            Appointment(
                **appointment_dto.model_dump(exclude={"client", "list_services"}),
                client_id=client.id,
                created_at=datetime.now(),
            )
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
                "promotion": appointment.promotion,
                "subtotal": appointment.subtotal,
                "total": appointment.total,
                "created_at": appointment.created_at,
                "modified_at": appointment.modified_at,
                "list_services": list_services,
            }
        )
    
    def update_appointment(self, appointment_dto: UpdateAppointmentDTO) -> AppointmentResponseDTO:
        appointment = self.appointment_repository.get_by_id(appointment_dto.id)
        if not appointment:
            raise AppointmentNotFound()

        client = appointment.client
        if client is None:
            raise AppointmentNotFound()

        was_done = appointment.status == AppointmentStatus.DONE
        will_be_done = appointment_dto.status == AppointmentStatus.DONE
        completing_now = not was_done and will_be_done

        service_ids = appointment_dto.list_services
        if service_ids is None:
            service_ids = [link.service_id for link in appointment.appointment_services]

        subtotal = self._subtotal_from_service_ids(service_ids)
        appointment_dto.subtotal = subtotal
        appointment_dto.total = subtotal

        loyalty_updated = False
        if completing_now:
            if client.loyalty_completed == 5:
                promotion = get_promotion(appointment_dto.promotion)
                appointment_dto = promotion.apply(appointment_dto)
                client.loyalty_completed = 1
            else:
                client.loyalty_completed += 1
            loyalty_updated = True


        if loyalty_updated:
            self.client_service.update_client(
                UpdateClientDTO(
                    id=client.id,
                    name=client.name,
                    last_name=client.last_name,
                    cellphone=client.cellphone,
                    email=client.email,
                    loyalty_completed=client.loyalty_completed,
                )
            )
        appointment = self.appointment_repository.update(
            Appointment(
                **appointment_dto.model_dump(exclude={"list_services", "discount"}),
                modified_at=datetime.now(),
            )
        )
        appointment = self.appointment_repository.get_by_id(appointment.id) or appointment
        appointment_services = self.appointment_service_service.update_appointment_service(
            UpdateAppointmentServiceDTO(
                appointment_id=appointment.id,
                service_ids=service_ids,
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
                "promotion": appointment.promotion,
                "subtotal": appointment.subtotal,
                "total": appointment.total,
                "created_at": appointment.created_at,
                "modified_at": appointment.modified_at,
            }
        )

    def _subtotal_from_service_ids(self, service_ids: list[int] | None) -> float:
        if not service_ids:
            return 0.0
        return sum(self.service_service.get_service_by_id(sid).price for sid in service_ids)

