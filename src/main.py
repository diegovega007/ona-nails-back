from fastapi import FastAPI
from .config import API_VERSION, create_db_and_tables
from .utils.error_handler_middleware import ErrorHandlerMiddleware

#Registro de modelos
from .models import Service, Client

#Rutas
from .routes.service_route import router as service_router

app = FastAPI(
    title="OnaNails API",
    description="API para el sistema de OnaNails",
    version=API_VERSION,
)

create_db_and_tables()

app.add_middleware(ErrorHandlerMiddleware)

#Registro de rutas
app.include_router(service_router)