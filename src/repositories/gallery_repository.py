from .base_repository import BaseRepository
from ..models import Gallery
from sqlmodel import Session, select, delete

class GalleryRepository(BaseRepository):
    def __init__(self, session: Session):
        super().__init__(Gallery, session)

    def get_by_ids(self, ids: list[int]) -> list[Gallery]:
        statement = select(Gallery).where(Gallery.id.in_(ids))
        return self.session.exec(statement).all()

    def delete_by_ids(self, ids: list[int]) -> bool:
        self.session.exec(delete(Gallery).where(Gallery.id.in_(ids)))
        self.session.commit()
        return True
