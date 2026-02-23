from .base_model import BaseModel
from sqlmodel import Field
from typing import Text
from enum import Enum

class GalleryType(str, Enum):
    IMAGE = "image"
    VIDEO = "video"

class Gallery(BaseModel, table=True):
    __tablename__ = "gallery"

    url: Text = Field(nullable=False)
    type: GalleryType = Field(nullable=False)
    public_id: str = Field(nullable=False, max_length=255)
    active: bool = Field(nullable=False, default=True)