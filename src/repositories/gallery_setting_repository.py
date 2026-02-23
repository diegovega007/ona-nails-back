from .base_repository import BaseRepository
from ..models import GallerySetting
from sqlmodel import Session

class GallerySettingRepository(BaseRepository):
    def __init__(self, session: Session):
        super().__init__(GallerySetting, session)
