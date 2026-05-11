from ..repositories import ClientRepository
from ..dtos import CreateClientDTO, ClientResponseDTO, ClientAppointmentsResponseDTO, AppointmentServicesResponseDTO, ServiceResponseDTO, UpdateClientDTO
from ..models import Client
from datetime import datetime
from ..exeptions import ClientNotFound
class ClientService:
    def __init__(self, client_repository: ClientRepository):
        self.client_repository = client_repository

    def create(self, client_dto: CreateClientDTO) -> ClientResponseDTO:
        client = self.client_repository.get_by_cellphone(client_dto.cellphone)
        if client:
            return ClientResponseDTO.model_validate(client)
        client = self.client_repository.create(
            Client(**client_dto.model_dump(), created_at=datetime.now())
        )
        return ClientResponseDTO.model_validate(client)

    def get_all_clients(self) -> list[ClientAppointmentsResponseDTO]:
        clients = self.client_repository.get_all()
        clients_response = []
        for client in clients:
            appointments_response = []
            for appointment in client.appointments:
                list_services = [
                    ServiceResponseDTO.model_validate(link.service)
                    for link in appointment.appointment_services
                    if link.service is not None and link.service is not None
                ]
                appointments_response.append(AppointmentServicesResponseDTO.model_validate(
                    {
                        "id": appointment.id,
                        "appointment_date": appointment.appointment_date,
                        "user_id": appointment.user_id,
                        "user": appointment.user,
                        "detail_service": appointment.detail_service,
                        "list_services": list_services,
                        "status": appointment.status,
                        "promotion_id": appointment.promotion_id,
                        "promotion": appointment.promotion,
                        "subtotal": appointment.subtotal,
                        "total": appointment.total,
                        "duration": self._duration_from_services(list_services),
                        "created_at": appointment.created_at,
                        "modified_at": appointment.modified_at,
                    }
                ))
            clients_response.append(ClientAppointmentsResponseDTO.model_validate(
                {
                    "id": client.id,
                    "name": client.name,
                    "last_name": client.last_name,
                    "cellphone": client.cellphone,
                    "email": client.email,
                    "loyalty_completed": client.loyalty_completed,
                    "created_at": client.created_at,
                    "modified_at": client.modified_at,
                    "appointments": appointments_response,
                }
            ))
        return clients_response

    def update_client(self, client_dto: UpdateClientDTO) -> ClientResponseDTO:
        client = self.client_repository.get_by_id(client_dto.id)
        if not client:
            raise ClientNotFound()
        client = self.client_repository.update(
            Client(**client_dto.model_dump(), modified_at=datetime.now())
        )
        return ClientResponseDTO.model_validate(client)

    def _duration_from_services(self, services: list[ServiceResponseDTO] | None) -> int:
        if not services:
            return 0
        return sum(service.duration for service in services)