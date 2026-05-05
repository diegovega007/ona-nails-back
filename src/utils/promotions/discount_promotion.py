from .promotion import Promotion
from ...dtos import UpdateAppointmentDTO
from ...models import PromotionType
from ...exeptions import PromotionDiscountRateNotSet

class DiscountPromotion(Promotion):
    """Expects `subtotal` set from service prices; `discount` is a rate in (0, 1], e.g. 0.1 = 10%."""

    def apply(self, appointment: UpdateAppointmentDTO) -> UpdateAppointmentDTO:
        if appointment.subtotal is None:
            return appointment
        subtotal = appointment.subtotal
        if appointment.discount is None:
            raise PromotionDiscountRateNotSet()
        appointment.subtotal = subtotal
        appointment.total = subtotal - (subtotal * appointment.discount)
        appointment.promotion = PromotionType.DISCOUNT
        return appointment