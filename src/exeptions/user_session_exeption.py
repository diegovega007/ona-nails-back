from fastapi import HTTPException, status

class UserSessionNotFound(HTTPException):
    def __init__(self, detail: str = "User session not found"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)

class UserSessionRevoked(HTTPException):
    def __init__(self, detail: str = "User session revoked"):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)