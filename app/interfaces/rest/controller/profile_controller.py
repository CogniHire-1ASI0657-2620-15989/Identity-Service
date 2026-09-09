from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Security,
    status,
)

from app.application.internal.command_services.default_profile_command_service import (
    DefaultProfileCommandService,
)
from app.application.internal.query_service.default_profile_query_service import (
    DefaultProfileQueryService,
)
from app.dependencies import (
    get_current_user,
    get_profile_command_service,
    get_profile_query_service,
)
from app.interfaces.rest.resources.change_password_resource import (
    ChangePasswordResource,
)
from app.interfaces.rest.resources.update_profile_resource import (
    UpdateProfileResource,
)
from app.interfaces.rest.resources.user_resource import UserResource
from app.interfaces.rest.resources.skill_resources import SkillResource
from app.interfaces.rest.transform.change_password_command_from_resource_assembler import (
    ChangePasswordCommandFromResourceAssembler,
)
from app.interfaces.rest.transform.update_profile_command_from_resource_assembler import (
    UpdateProfileCommandFromResourceAssembler,
)
from app.interfaces.rest.transform.user_resource_from_entity_assembler import (
    UserResourceFromEntityAssembler,
)
from app.domain.model.queries.get_current_profile_query import (
    GetCurrentProfileQuery,
)

router = APIRouter(
    prefix="/api/v1/profile",
    tags=["Profile"],
)

@router.get(
    "/me",
    response_model=UserResource,
)
def get_current_profile(
    current_user: dict = Security(get_current_user),
    service: DefaultProfileQueryService = Depends(
        get_profile_query_service
    ),
):

    user = service.handle_get_current_profile(
        GetCurrentProfileQuery(user_id=current_user["id"])
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado.",
        )

    return UserResourceFromEntityAssembler.to_resource(user)

@router.put(
    "/me",
    response_model=UserResource,
)
def update_profile(
    resource: UpdateProfileResource,
    current_user: dict = Security(get_current_user),
    service: DefaultProfileCommandService = Depends(
        get_profile_command_service
    ),
):

    try:
        command = UpdateProfileCommandFromResourceAssembler.to_command(
            current_user["id"],
            resource,
        )
        user = service.handle_update_profile(command)
        return UserResourceFromEntityAssembler.to_resource(user)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )

@router.put(
    "/me/password",
    response_model=UserResource,
)
def change_password(
    resource: ChangePasswordResource,
    current_user: dict = Security(get_current_user),
    service: DefaultProfileCommandService = Depends(
        get_profile_command_service
    ),
):

    try:
        command = ChangePasswordCommandFromResourceAssembler.to_command(
            current_user["id"],
            resource,
        )
        user = service.handle_change_password(command)
        return UserResourceFromEntityAssembler.to_resource(user)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )


@router.post("/me/skills/{skill_type}", response_model=UserResource)
def add_skill(
    skill_type: str,
    resource: SkillResource,
    current_user: dict = Security(get_current_user),
    service: DefaultProfileCommandService = Depends(get_profile_command_service),
):
    try:
        user = service.handle_add_skill(current_user["id"], skill_type, resource.model_dump())
        return UserResourceFromEntityAssembler.to_resource(user)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))


@router.put("/me/skills/{skill_type}/{skill_name}", response_model=UserResource)
def update_skill(
    skill_type: str,
    skill_name: str,
    resource: SkillResource,
    current_user: dict = Security(get_current_user),
    service: DefaultProfileCommandService = Depends(get_profile_command_service),
):
    try:
        user = service.handle_update_skill(current_user["id"], skill_type, skill_name, resource.model_dump())
        return UserResourceFromEntityAssembler.to_resource(user)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))


@router.delete("/me/skills/{skill_type}/{skill_name}", response_model=UserResource)
def remove_skill(
    skill_type: str,
    skill_name: str,
    current_user: dict = Security(get_current_user),
    service: DefaultProfileCommandService = Depends(get_profile_command_service),
):
    try:
        user = service.handle_remove_skill(current_user["id"], skill_type, skill_name)
        return UserResourceFromEntityAssembler.to_resource(user)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))
