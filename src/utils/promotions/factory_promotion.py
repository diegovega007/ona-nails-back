from .discount_promotion import DiscountPromotion
from .promotion import Promotion
from ...models import PromotionType
from ...exeptions import PromotionNotFound

def get_promotion(promotion_type: PromotionType) -> Promotion:
    if promotion_type == PromotionType.DISCOUNT:
        return DiscountPromotion()
    raise PromotionNotFound()