from fastapi import HTTPException, status

class UserNotFound(HTTPException):
    def __init__(self, detail: str = "Usuario no encontrado"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)

class UserAlreadyExists(HTTPException):
    def __init__(self, detail: str = "El usuario ya existe"):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)

class UserInactive(HTTPException):
    def __init__(self, detail: str = "El usuario está inactivo"):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)