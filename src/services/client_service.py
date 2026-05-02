from ..repositories import ClientRepository
from ..dtos import CreateClientDTO, ClientResponseDTO, ClientAppointmentsResponseDTO, AppointmentServicesResponseDTO, ServiceResponseDTO
from ..models import Client
from datetime import datetime

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
                        "detail_service": appointment.detail_service,
                        "list_services": list_services,
                        "status": appointment.status,
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
                    "created_at": client.created_at,
                    "modified_at": client.modified_at,
                    "appointments": appointments_response,
                }
            ))
        return clients_response