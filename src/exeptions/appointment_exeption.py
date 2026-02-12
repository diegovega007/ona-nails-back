from fastapi import HTTPException, status

class AppointmentNotFound(HTTPException):
    def __init__(self, detail: str = "Appointment not found"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)

class AppointmentAlreadyExists(HTTPException):
    def __init__(self, detail: str = "The client already has an appointment"):
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=detail)

class AppointmentDateNotAvailable(HTTPException):
    def __init__(self, detail: str = "Appointment date not available"):
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=detail)

class AppointmentClientNotFound(HTTPException):
    def __init__(self, detail: str = "The client has no appointments"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)