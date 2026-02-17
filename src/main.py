from fastapi import FastAPI
from .config import API_VERSION, create_db_and_tables
from .utils.error_handler_middleware import ErrorHandlerMiddleware

#Registro de modelos
from .models import Service, Client, Appointment, User, UserSession

#Rutas
from .routes.service_route import router as service_router
from .routes.appointment_route import router as appointment_router
from .routes.user_route import router as user_router
from .routes.login_route import router as login_router
from .routes.login_route import router_logout as login_router_logout
from .routes.login_route import router_refresh as login_router_refresh

app = FastAPI(
    title="OnaNails API",
    description="API para el sistema de OnaNails",
    version=API_VERSION,
)

create_db_and_tables()

app.add_middleware(ErrorHandlerMiddleware)

#Registro de rutas
app.include_router(login_router, prefix=f"/{API_VERSION}")
app.include_router(login_router_logout, prefix=f"/{API_VERSION}")
app.include_router(login_router_refresh, prefix=f"/{API_VERSION}")
app.include_router(user_router, prefix=f"/{API_VERSION}")
app.include_router(service_router, prefix=f"/{API_VERSION}")
app.include_router(appointment_router, prefix=f"/{API_VERSION}")