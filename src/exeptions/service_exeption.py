from fastapi import HTTPException, status

class ServiceNotFound(HTTPException):
    def __init__(self, detail: str = "Service not found"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)

class ServiceAlreadyExists(HTTPException):
    def __init__(self, detail: str = "Service already exists"):
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=detail)