from fastapi import FastAPI

from app.infrastructure.persistence.sqlalchemy.configuration.database import (
    initialize_database,
)
from app.infrastructure.persistence.sqlalchemy.models import user_model
from app.infrastructure.persistence.sqlalchemy.models import password_reset_token_model

from app.interfaces.rest.controller.auth_controller import (
    router as auth_router,
)
from app.interfaces.rest.controller.profile_controller import (
    router as profile_router,
)
from app.interfaces.rest.controller.internal_controller import (
    router as internal_router,
)


app = FastAPI(
    title="Identity Service",
    description=(
        "Microservicio encargado de autenticación "
        "y gestión del perfil del usuario."
    ),
    version="1.0.0",
)


app.include_router(auth_router)
app.include_router(profile_router)
app.include_router(internal_router)


@app.on_event("startup")
def create_database_schema():
    initialize_database()


@app.get("/health")
def health_check():
    return {
        "service": "identity-service",
        "status": "healthy",
    }