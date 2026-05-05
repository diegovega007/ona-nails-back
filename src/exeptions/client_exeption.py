from fastapi import HTTPException, status

class ClientAlreadyExists(HTTPException):
    def __init__(self, detail: str = "El cliente ya existe"):
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=detail)

class ClientNotFound(HTTPException):
    def __init__(self, detail: str = "Cliente no encontrado"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)