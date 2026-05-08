from pydantic import BaseModel

class InstagramMediaResponseDTO(BaseModel):
    id: str
    caption: str
    media_url: str
    permalink: str
    thumbnail_url: str
    media_type: str


    