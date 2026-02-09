from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CreateClientDTO(BaseModel):
    name: str
    last_name: str
    cellphone: str
    email: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "name": "John",
                "last_name": "Doe",
                "cellphone": "+523178901234",
                "email": "john.doe@example.com"
            }
        }

class UpdateClientDTO(BaseModel):
    id: int
    name: str
    last_name: str
    cellphone: str
    email: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "John",
                "last_name": "Doe",
                "cellphone": "+523178901234",
                "email": "john.doe@example.com"
            }
        }

class ClientResponseDTO(BaseModel):
    id: int
    name: str
    last_name: str
    cellphone: str
    email: Optional[str] = None
    created_at: datetime
    modified_at: datetime