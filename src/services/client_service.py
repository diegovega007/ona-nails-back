from ..repositories import ClientRepository
from ..dtos import CreateClientDTO, ClientResponseDTO
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