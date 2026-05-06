from .promotion import Promotion
from ...dtos import UpdateAppointmentDTO
from ...exeptions import PromotionNotFound

_DISCOUNT_RATES = {
    "10_descuento": 0.1,
    "15_descuento": 0.15,
    "20_descuento": 0.2,
    "25_descuento": 0.25,
}


class DiscountPromotion(Promotion):
    def __init__(self, identifier: str):
        self._identifier = identifier

    def apply(self, appointment: UpdateAppointmentDTO) -> UpdateAppointmentDTO:
        rate = _DISCOUNT_RATES.get(self._identifier)
        if rate is None:
            raise PromotionNotFound()
        subtotal = appointment.subtotal
        appointment.subtotal = subtotal
        appointment.total = subtotal - (subtotal * rate)
        return appointment