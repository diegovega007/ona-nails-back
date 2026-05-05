from fastapi import HTTPException, status

class PromotionNotFound(HTTPException):
    def __init__(self, detail: str = "Promoción no encontrada"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)

class PromotionDiscountRateNotSet(HTTPException):
    def __init__(self, detail: str = "Tasa de descuento de promoción no establecida"):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)