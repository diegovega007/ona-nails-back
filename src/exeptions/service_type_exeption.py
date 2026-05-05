from fastapi import HTTPException, status

class ServiceTypeNotFound(HTTPException):
    def __init__(self, detail: str = "Tipo de servicio no encontrado"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)

class ServiceTypeAlreadyExists(HTTPException):
    def __init__(self, detail: str = "El tipo de servicio ya existe"):
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=detail)