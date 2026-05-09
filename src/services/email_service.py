import os
import smtplib
from email.mime.text import MIMEText

from dotenv import load_dotenv

from ..exeptions.email_exeption import EmailException
from ..dtos import SendContactEmailDTO, SendContactEmailResponseDTO

load_dotenv()


class EmailService:

    def __init__(self):
        self._host = os.getenv("SMTP_HOST")
        self._port = 587
        self._user = os.getenv("SMTP_USER")
        self._password = os.getenv("SMTP_PASSWORD")
        self._from_email = os.getenv("SMTP_FROM_EMAIL")
        self._to_email = os.getenv("SMTP_TO_EMAIL")
        self._use_tls = os.getenv("SMTP_USE_TLS", "true").lower() in (
            "1",
            "true",
            "yes",
        )

    def send_contact_email(self, send_contact_email_dto: SendContactEmailDTO) -> SendContactEmailResponseDTO:
        full_name = send_contact_email_dto.full_name
        email = send_contact_email_dto.email
        message = send_contact_email_dto.message
        phone = send_contact_email_dto.phone
        subject_prefix = send_contact_email_dto.subject_prefix

        full_name = (full_name or "").strip()
        email = (email or "").strip()
        message = (message or "").strip()
        phone = phone.strip() if phone else None

        if not full_name:
            raise ValueError("El nombre completo es obligatorio")
        if not email:
            raise ValueError("El correo electrónico es obligatorio")
        if not message:
            raise ValueError("El mensaje es obligatorio")

        if not all([self._host, self._from_email, self._to_email]):
            raise EmailException(
                "Falta configuración SMTP (SMTP_HOST, SMTP_FROM_EMAIL, SMTP_TO_EMAIL)"
            )

        body_parts = [
            f"Nombre: {full_name}",
            f"Correo: {email}",
        ]
        if phone:
            body_parts.append(f"Teléfono: {phone}")
        body_parts.extend(["", "Mensaje:", message])

        body = "\n".join(body_parts)
        msg = MIMEText(body)
        msg["Subject"] = f"{subject_prefix} {full_name}"
        msg["From"] = self._from_email
        msg["To"] = self._to_email
        msg["Reply-To"] = email

        try:
            with smtplib.SMTP(self._host, self._port) as server:
                if self._use_tls:
                    server.starttls()
                if self._user and self._password:
                    server.login(self._user, self._password)
                server.sendmail(
                    self._from_email, [self._to_email], msg.as_string()
                )
        except smtplib.SMTPException as e:
            raise EmailException(str(e)) from e
        except OSError as e:
            raise EmailException(str(e)) from e

        return SendContactEmailResponseDTO(success=True)