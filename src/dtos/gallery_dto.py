from pydantic import BaseModel
from ..models import GalleryType

class CreateGalleryDTO(BaseModel):
    type: GalleryType

    class Config:
        json_schema_extra = {
            "example": {
                "type": GalleryType.IMAGE
            }
        }

class UpdateGalleryDTO(BaseModel):
    id: int
    type: GalleryType

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "type": GalleryType.IMAGE
            }
        }

class GalleryResponseDTO(BaseModel):
    id: int
    url: str
    type: GalleryType
    public_id: str
    active: bool

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "url": "https://example.com/photo.jpg",
                "type": GalleryType.IMAGE,
                "public_id": "1234567890",
                "active": True
            }
        }