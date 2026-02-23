from pydantic import BaseModel

class GallerySettingDTO(BaseModel):
    collage_limit: int

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "collage_limit": 20
            }
        }