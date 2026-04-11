from fastapi import HTTPException, status

class UserSessionNotFound(HTTPException):
    def __init__(self, detail: str = "Sesión de usuario no encontrada"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)

class UserSessionRevoked(HTTPException):
    def __init__(self, detail: str = "Sesión de usuario revocada"):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)