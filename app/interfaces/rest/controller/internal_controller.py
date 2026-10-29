from fastapi import APIRouter, Depends, HTTPException, Response, status

from app.application.internal.query_service.default_profile_query_service import (
    DefaultProfileQueryService,
)
from app.dependencies import get_profile_command_service, get_profile_query_service
from app.application.internal.command_services.default_profile_command_service import DefaultProfileCommandService
from app.domain.model.queries.get_user_by_id_query import GetUserByIdQuery
from app.interfaces.rest.resources.job_profile_resource import JobProfileResource
from app.interfaces.rest.resources.verified_hard_skill_resource import VerifiedHardSkillResource


router = APIRouter(prefix="/api/v1/internal", tags=["Internal"])


@router.get("/users/{user_id}/job-profile", response_model=JobProfileResource)
def get_job_profile(
    user_id: int,
    service: DefaultProfileQueryService = Depends(get_profile_query_service),
):
    user = service.handle_get_by_id(GetUserByIdQuery(user_id=user_id))
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado.")
    return JobProfileResource(
        id=user.id,
        name=user.name.value,
        target_position=user.target_position,
        expected_city=user.expected_city,
        expected_country=user.expected_country,
        work_modality=user.work_modality,
        hard_skills=user.hard_skills,
        soft_skills=user.soft_skills,
        education=user.education,
        experience=user.experience,
        languages=user.languages,
        professional_summary=user.professional_summary,
    )


@router.post("/users/{user_id}/verified-hard-skills", status_code=status.HTTP_204_NO_CONTENT)
def ensure_verified_hard_skill(
    user_id: int,
    resource: VerifiedHardSkillResource,
    service: DefaultProfileCommandService = Depends(get_profile_command_service),
) -> Response:
    try:
        service.handle_ensure_verified_hard_skill(user_id, resource.name)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    return Response(status_code=status.HTTP_204_NO_CONTENT)
