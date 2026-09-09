from fastapi import APIRouter, Depends, HTTPException, status

from app.application.internal.query_service.default_profile_query_service import (
    DefaultProfileQueryService,
)
from app.dependencies import get_profile_query_service
from app.domain.model.queries.get_user_by_id_query import GetUserByIdQuery
from app.interfaces.rest.resources.job_profile_resource import JobProfileResource


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