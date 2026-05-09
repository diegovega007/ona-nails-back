from pydantic import BaseModel

class SendContactEmailDTO(BaseModel):
    full_name: str
    email: str
    message: str
    phone: str | None = None
    subject_prefix: str = "[Contacto]"

    class Config:
        json_schema_extra = {
            "example": {
                "full_name": "John Doe",
                "email": "john.doe@example.com",
                "message": "Hello, how are you?",
                "phone": "+523178901234",
                "subject_prefix": "[Contacto]"
            }
        }

class SendContactEmailResponseDTO(BaseModel):
    success: bool

    class Config:
        json_schema_extra = {
            "example": {
                "success": True
            }
        }