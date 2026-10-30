from secrets import compare_digest

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.config import get_settings

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
    get_settings()
    initialize_database()


@app.middleware("http")
async def require_internal_api_key(request: Request, call_next):
    if request.url.path == "/health":
        return await call_next(request)
    if not compare_digest(request.headers.get("X-Internal-Api-Key", ""), get_settings().internal_api_key):
        return JSONResponse(status_code=401, content={"detail": "Unauthorized service request."})
    return await call_next(request)


@app.get("/health")
def health_check():
    return {
        "service": "identity-service",
        "status": "healthy",
    }
