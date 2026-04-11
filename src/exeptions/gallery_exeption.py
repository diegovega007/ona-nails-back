from fastapi import HTTPException, status

class GalleryNotFound(HTTPException):
    def __init__(self, detail: str = "Galería no encontrada"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)