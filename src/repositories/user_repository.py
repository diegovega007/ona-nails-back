from .base_repository import BaseRepository
from ..models.user import Roles, User
from ..models.appointment import Appointment, AppointmentStatus
from sqlmodel import Session, func, select
from datetime import datetime, timedelta

class UserRepository(BaseRepository):
    def __init__(self, session: Session):
        super().__init__(User, session)

    def get_by_email(self, email: str) -> User:
        statement = select(User).where(User.email == email)
        return self.session.exec(statement).first()

    def get_active_account(self, email: str) -> User:
        statement = select(User).where(User.email == email).where(User.is_active == True)
        return self.session.exec(statement).first()

    def count_active_bookable_staff(self) -> int:
        """Usuarios activos que pueden tomar citas en paralelo (no recepción)."""
        statement = (
            select(func.count())
            .select_from(User)
            .where(User.is_active == True)
            .where(User.rol != Roles.RECEPTIONIST)
        )
        return self.session.exec(statement).one()

    def get_available_user(self, appointment_date: datetime, duration: int) -> list[User]:
        """
        Retorna empleados activos (no recepcionistas) que estén libres en el
        intervalo [appointment_date, appointment_date + duration).

        Un usuario está ocupado si tiene una cita activa (RECEIVED o IN_PROGRESS)
        cuyo intervalo se empalma con el solicitado:
            cita_inicio < nueva_fin  AND  cita_fin > nueva_inicio
        """
        # La BD guarda datetimes naive; normalizamos el parámetro para poder comparar
        appointment_date = appointment_date.replace(tzinfo=None)
        new_end = appointment_date + timedelta(minutes=duration)

        # Citas activas que empiezan antes de que termine la nueva cita
        active_stmt = (
            select(Appointment)
            .where(Appointment.status.in_([AppointmentStatus.RECEIVED, AppointmentStatus.IN_PROGRESS]))
            .where(Appointment.appointment_date < new_end)
            .where(Appointment.user_id.is_not(None))
        )
        active_appointments = self.session.exec(active_stmt).all()

        # Filtramos en Python el otro lado del solapamiento
        # (cita_fin > nueva_inicio), ya que cita_fin = appointment_date + duration (columna entera)
        busy_user_ids = {
            a.user_id
            for a in active_appointments
            if a.appointment_date is not None
            and a.appointment_date + timedelta(minutes=a.duration or 0) > appointment_date
        }

        stmt = (
            select(User)
            .where(User.is_active == True)
            .where(User.rol != Roles.RECEPTIONIST)
        )
        if busy_user_ids:
            stmt = stmt.where(User.id.not_in(busy_user_ids))

        return self.session.exec(stmt).all()

