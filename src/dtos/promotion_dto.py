from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CreatePromotionDTO(BaseModel):
    identifier: str
    name: str
    description: Optional[str] = None

class UpdatePromotionDTO(BaseModel):
    id: int
    identifier: str
    name: str
    description: Optional[str] = None

class PromotionResponseDTO(BaseModel):
    id: int
    identifier: str
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
                "identifier": "PROMO123",
                "name": "Promotion 1",
                "description": "Description of promotion 1",
                "created_at": "2021-01-01T00:00:00Z",
                "created_by": "system",
                "modified_at": "2021-01-01T00:00:00Z",
                "modified_by": "system",
            }
        }