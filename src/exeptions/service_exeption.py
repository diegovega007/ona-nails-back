from fastapi import HTTPException, status

class ServiceNotFound(HTTPException):
    def __init__(self, detail: str = "Servicio no encontrado"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)

class ServiceAlreadyExists(HTTPException):
    def __init__(self, detail: str = "El servicio ya existe"):
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=detail)