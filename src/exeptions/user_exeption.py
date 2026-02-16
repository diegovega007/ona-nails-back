from fastapi import HTTPException, status

class UserNotFound(HTTPException):
    def __init__(self, detail: str = "User not found"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)

class UserAlreadyExists(HTTPException):
    def __init__(self, detail: str = "User already exists"):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)

class UserInactive(HTTPException):
    def __init__(self, detail: str = "User is inactive"):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)