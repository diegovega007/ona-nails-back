import os
from datetime import datetime

from sqlmodel import Session

from ..config import engine
from ..models import Roles, User
from ..repositories import UserRepository
from ..services import AuthService


def seed_admin() -> None:
    """
    Crea un usuario con rol admin en estado inactivo (is_active=False) si no existe
    otro con el mismo email.

    Contraseña: argumento `password` o variable de entorno ADMIN_SEED_PASSWORD.
    Email: argumento `email` o ADMIN_SEED_EMAIL; por defecto admin@onanails.local.
    """
    email = os.getenv("ADMIN_SEED_EMAIL")
    password = os.getenv("ADMIN_SEED_PASSWORD")
    if not password:
        raise ValueError(
            "Indicá la contraseña con el argumento password= o la variable ADMIN_SEED_PASSWORD."
        )

    with Session(engine) as session:
        repo = UserRepository(session)
        if repo.get_by_email(email):
            return

        auth = AuthService()
        user = User(
            email=email,
            password=auth.hash_password(password),
            first_name="Admin",
            last_name="Admin",
            cellphone="+52111111111",
            rol=Roles.ADMIN,
            is_active=False,
            created_at=datetime.now(),
        )
        repo.create(user)
