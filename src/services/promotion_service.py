from ..repositories import PromotionRepository
from ..dtos import CreatePromotionDTO, UpdatePromotionDTO, PromotionResponseDTO
from ..exeptions import PromotionNotFound, PromotionAlreadyExists
from datetime import datetime
from ..models import Promotion
from ..utils.auth_dependency import current_user

class PromotionService:
    def __init__(self, promotion_repository: PromotionRepository):
        self.promotion_repository = promotion_repository

    def get_all_promotions(self) -> list[PromotionResponseDTO]:
        promotions = self.promotion_repository.get_all()
        return [PromotionResponseDTO.model_validate(promotion) for promotion in promotions]

    def get_promotion_by_id(self, id: int) -> PromotionResponseDTO:
        promotion = self.promotion_repository.get_by_id(id)
        if not promotion:
            raise PromotionNotFound()
        return PromotionResponseDTO.model_validate(promotion)

    def create_promotion(self, promotion_dto: CreatePromotionDTO, current_user: str = "system") -> PromotionResponseDTO:
        if self.promotion_repository.get_by_name_and_identifier(promotion_dto.name, promotion_dto.identifier):
            raise PromotionAlreadyExists()
        promotion = self.promotion_repository.create(
            Promotion(**promotion_dto.model_dump(), created_by=current_user, created_at=datetime.now())
        )
        return PromotionResponseDTO.model_validate(promotion)

    def update_promotion(self, promotion_dto: UpdatePromotionDTO, current_user: str = "system") -> PromotionResponseDTO:
        promotion = self.promotion_repository.get_by_id(promotion_dto.id)
        if not promotion:
            raise PromotionNotFound()
        promotion = self.promotion_repository.update(
            Promotion(**promotion_dto.model_dump(), modified_by=current_user, modified_at=datetime.now())
        )
        return PromotionResponseDTO.model_validate(promotion)
    
    def delete_promotion(self, id: int) -> None:
        promotion = self.promotion_repository.get_by_id(id)
        if not promotion:
            raise PromotionNotFound()
        return self.promotion_repository.delete(id)