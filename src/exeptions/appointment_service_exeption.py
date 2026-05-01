from fastapi import HTTPException, status

class AppointmentServiceNotFound(HTTPException):
    def __init__(self, detail: str = "Servicio de cita no encontrado"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)