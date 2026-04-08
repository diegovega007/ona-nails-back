from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CreateServiceDTO(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    enabled: bool = True

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Service 1",
                "description": "Description of service 1",
                "price": 100.0,
                "enabled": True
            }
        }

class UpdateServiceDTO(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    price: float
    enabled: bool = True

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "Service 1",
                "description": "Description of service 1",
                "price": 100.0,
                "enabled": True
            }
        }

class ServiceResponseDTO(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    photo: Optional[str] = None
    photo_public_id: Optional[str] = None
    price: float
    enabled: bool
    created_at: datetime
    created_by: str
    modified_at: Optional[datetime] = None
    modified_by: Optional[str] = None

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "Service 1",
                "description": "Description of service 1",
                "photo": "https://res.cloudinary.com/example/image/upload/v1/service.jpg",
                "photo_public_id": "service_1",
                "price": 100.0,
                "enabled": True,
                "created_by": "system",
                "modified_by": "system",
                "created_at": "2021-01-01T00:00:00Z",
                "modified_at": "2021-01-01T00:00:00Z"
            }
        }
