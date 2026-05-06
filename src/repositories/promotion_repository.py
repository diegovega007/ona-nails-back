from .base_repository import BaseRepository
from ..models.promotion import Promotion
from sqlmodel import select, Session, or_

class PromotionRepository(BaseRepository):
    def __init__(self, session: Session):
        super().__init__(Promotion, session)

    def get_by_name_and_identifier(self, name: str, identifier: str) -> Promotion:
        return self.session.exec(select(Promotion).where(or_(Promotion.name == name, Promotion.identifier == identifier))).first()