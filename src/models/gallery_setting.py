from .base_model import BaseModel
from sqlmodel import Field

class GallerySetting(BaseModel, table=True):
    __tablename__ = "gallery_settings"

    collage_limit: int = Field(nullable=False, default=20)
    