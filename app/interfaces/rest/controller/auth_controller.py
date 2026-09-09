from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)

from app.application.internal.command_services.default_auth_command_service import (
    DefaultAuthCommandService,
)
from app.dependencies import get_auth_command_service
from app.dependencies import get_password_recovery_service
from app.application.internal.command_services.password_recovery_service import (
    PasswordRecoveryService,
)
from app.interfaces.rest.resources.password_recovery_resources import (
    PasswordRecoveryRequest,
    PasswordRecoveryResponse,
    PasswordResetRequest,
)

from app.interfaces.rest.resources.auth_resource import (
    AuthResource,
)
from app.interfaces.rest.resources.login_resource import (
    LoginResource,
)
from app.interfaces.rest.resources.register_user_resource import (
    RegisterUserResource,
)

from app.interfaces.rest.transform.authenticate_user_command_from_resource_assembler import (
    AuthenticateUserCommandFromResourceAssembler,
)
from app.interfaces.rest.transform.register_user_command_from_resource_assembler import (
    RegisterUserCommandFromResourceAssembler,
)
from app.interfaces.rest.transform.user_resource_from_entity_assembler import (
    UserResourceFromEntityAssembler,
)


router = APIRouter(
    prefix="/api/v1/auth",
    tags=["Authentication"],
)


@router.post(
    "/register",
    response_model=AuthResource,
    status_code=status.HTTP_201_CREATED,
)
def register(
    resource: RegisterUserResource,
    service: DefaultAuthCommandService = Depends(
        get_auth_command_service
    ),
):

    try:
        command = (
            RegisterUserCommandFromResourceAssembler
            .to_command(resource)
        )

        user, token = service.handle_register(
            command
        )

        return AuthResource(
            access_token=token,
            user=(
                UserResourceFromEntityAssembler
                .to_resource(user)
            ),
        )

    except ValueError as exc:
        message = str(exc)

        if "email ya está registrado" in message.lower():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=message,
            )

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=message,
        )


@router.post(
    "/login",
    response_model=AuthResource,
)
def login(
    resource: LoginResource,
    service: DefaultAuthCommandService = Depends(
        get_auth_command_service
    ),
):

    try:
        command = (
            AuthenticateUserCommandFromResourceAssembler
            .to_command(resource)
        )

        user, token = service.handle_authenticate(
            command
        )

        return AuthResource(
            access_token=token,
            user=(
                UserResourceFromEntityAssembler
                .to_resource(user)
            ),
        )

    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas.",
        )


@router.post("/password-recovery", response_model=PasswordRecoveryResponse)
def request_password_recovery(
    resource: PasswordRecoveryRequest,
    service: PasswordRecoveryService = Depends(get_password_recovery_service),
):
    token = service.request_recovery(str(resource.email))
    return PasswordRecoveryResponse(
        message="Si el correo existe, se ha generado un token de recuperación.",
        token=token,
    )


@router.post("/password-reset", status_code=status.HTTP_204_NO_CONTENT)
def reset_password(
    resource: PasswordResetRequest,
    service: PasswordRecoveryService = Depends(get_password_recovery_service),
):
    try:
        service.reset_password(resource.token, resource.new_password)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )