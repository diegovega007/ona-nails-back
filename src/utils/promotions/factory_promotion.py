from .discount_promotion import DiscountPromotion
from .promotion import Promotion
from ...exeptions import PromotionNotFound
from ...repositories import PromotionRepository

_DISCOUNT_IDENTIFIERS = frozenset(
    {"10_descuento", "15_descuento", "20_descuento", "25_descuento"}
)


def get_promotion(
    promotion_repository: PromotionRepository, promotion_id: int | None
) -> Promotion:
    if promotion_id is None:
        raise PromotionNotFound(
            detail="Se requiere promotion_id para aplicar la promoción de lealtad"
        )
    row = promotion_repository.get_by_id(promotion_id)
    if not row:
        raise PromotionNotFound()
    if row.identifier in _DISCOUNT_IDENTIFIERS:
        return DiscountPromotion(row.identifier)
    raise PromotionNotFound()