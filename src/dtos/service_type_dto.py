from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CreateServiceTypeDTO(BaseModel):
    name: str
    description: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Service Type 1",
                "description": "Description of service type 1"
            }
        }

class UpdateServiceTypeDTO(BaseModel):
    id: int
    name: str
    description: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "Service Type 1",
                "description": "Description of service type 1"
            }
        }

class ServiceTypeResponseDTO(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    created_at: datetime
    created_by: str
    modified_at: Optional[datetime] = None
    modified_by: Optional[str] = None

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "Service Type 1",
                "description": "Description of service type 1",
                "created_at": "2021-01-01T00:00:00Z",
                "created_by": "system",
                "modified_at": "2021-01-01T00:00:00Z",
                "modified_by": "system"
            }
        }