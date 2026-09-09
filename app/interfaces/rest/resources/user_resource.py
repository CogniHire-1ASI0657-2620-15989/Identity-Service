from datetime import datetime

from pydantic import BaseModel, Field

from app.interfaces.rest.resources.professional_resources import (
    EducationResource,
    ExperienceResource,
    LanguageResource,
)
from app.interfaces.rest.resources.skill_resources import SkillResource


class UserResource(BaseModel):
    id: int
    name: str
    email: str
    segment: str

    city: str | None = None
    country: str | None = None
    target_position: str | None = None
    expected_city: str | None = None
    expected_country: str | None = None
    work_modality: str | None = None
    hard_skills: list[SkillResource] = Field(default_factory=list)
    soft_skills: list[SkillResource] = Field(default_factory=list)
    education: list[EducationResource] = Field(default_factory=list)
    experience: list[ExperienceResource] = Field(default_factory=list)
    languages: list[LanguageResource] = Field(default_factory=list)
    professional_summary: str | None = None

    created_at: datetime