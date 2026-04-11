from fastapi import HTTPException, status

class AppointmentNotFound(HTTPException):
    def __init__(self, detail: str = "Cita no encontrada"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)

class AppointmentAlreadyExists(HTTPException):
    def __init__(self, detail: str = "Ya se tiene una cita registrada"):
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=detail)

class AppointmentDateNotAvailable(HTTPException):
    def __init__(self, detail: str = "La fecha de la cita no está disponible"):
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=detail)

class AppointmentClientNotFound(HTTPException):
    def __init__(self, detail: str = "El cliente no tiene citas"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)