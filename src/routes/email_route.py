from fastapi import APIRouter, Depends, status
from ..services import EmailService
from ..dtos import SendContactEmailDTO, SendContactEmailResponseDTO

router = APIRouter(prefix="/email", tags=["Email"])

def get_email_service() -> EmailService:
    return EmailService()

@router.post("/send-contact-email", response_model=SendContactEmailResponseDTO, status_code=status.HTTP_200_OK)
def send_contact_email(send_contact_email_dto: SendContactEmailDTO, email_service: EmailService = Depends(get_email_service)) -> SendContactEmailResponseDTO:
    return email_service.send_contact_email(send_contact_email_dto)