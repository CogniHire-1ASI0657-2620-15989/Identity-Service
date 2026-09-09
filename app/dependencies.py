import os

import jwt
from fastapi import (
    Depends,
    HTTPException,
    Security,
    status,
)
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
)
from sqlalchemy.orm import Session

from app.application.internal.command_services.default_auth_command_service import (
    DefaultAuthCommandService,
)
from app.application.internal.command_services.default_profile_command_service import (
    DefaultProfileCommandService,
)
from app.application.internal.query_service.default_profile_query_service import (
    DefaultProfileQueryService,
)
from app.application.internal.command_services.password_recovery_service import (
    PasswordRecoveryService,
)

from app.infrastructure.persistence.sqlalchemy.configuration.database import (
    get_db,
)
from app.infrastructure.persistence.sqlalchemy.repositories.sqlalchemy_user_repository import (
    SQLAlchemyUserRepository,
)

from app.infrastructure.security.bcrypt_password_hasher import (
    BcryptPasswordHasher,
)
from app.infrastructure.security.jwt_token_service import (
    JwtTokenService,
)


def get_user_repository(
    db: Session = Depends(get_db),
):
    return SQLAlchemyUserRepository(db)


def get_password_hasher():
    return BcryptPasswordHasher()


def get_token_service():

    return JwtTokenService(
        secret_key=os.getenv(
            "JWT_SECRET_KEY",
            "development-secret"
        ),
        issuer=os.getenv(
            "JWT_ISSUER",
            "identity-service"
        ),
        audience=os.getenv(
            "JWT_AUDIENCE",
            "job-platform-services"
        ),
        expiration_minutes=int(
            os.getenv(
                "JWT_EXPIRATION_MINUTES",
                "60"
            )
        ),
    )

bearer_scheme = HTTPBearer(auto_error=False)

def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Security(
        bearer_scheme
    ),
    token_service: JwtTokenService = Depends(get_token_service),
):

    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token de autenticación requerido.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        payload = token_service.decode(credentials.credentials)
        user_id = int(payload["sub"])
    except (jwt.InvalidTokenError, KeyError, TypeError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token de autenticación inválido.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return {"id": user_id, "claims": payload}


def get_auth_command_service(
    repository=Depends(get_user_repository),
    password_hasher=Depends(get_password_hasher),
    token_service=Depends(get_token_service),
):

    return DefaultAuthCommandService(
        user_repository=repository,
        password_hasher=password_hasher,
        token_service=token_service,
    )


def get_profile_command_service(
    repository=Depends(get_user_repository),
    password_hasher=Depends(get_password_hasher),
):

    return DefaultProfileCommandService(
        user_repository=repository,
        password_hasher=password_hasher,
    )


def get_profile_query_service(
    repository=Depends(get_user_repository),
):

    return DefaultProfileQueryService(
        user_repository=repository,
    )


def get_password_recovery_service(
    db: Session = Depends(get_db),
    repository=Depends(get_user_repository),
    password_hasher=Depends(get_password_hasher),
):
    return PasswordRecoveryService(
        db=db,
        user_repository=repository,
        password_hasher=password_hasher,
    )