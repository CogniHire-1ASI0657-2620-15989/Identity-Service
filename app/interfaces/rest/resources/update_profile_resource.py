from pydantic import BaseModel, EmailStr, Field

from app.interfaces.rest.resources.professional_resources import (
    EducationResource,
    ExperienceResource,
    LanguageResource,
)
from app.interfaces.rest.resources.skill_resources import SkillResource


class UpdateProfileResource(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=1,
        max_length=150
    )

    email: EmailStr | None = None

    segment: str | None = None

    city: str | None = None
    country: str | None = None
    target_position: str | None = Field(default=None, max_length=150)
    expected_city: str | None = Field(default=None, max_length=100)
    expected_country: str | None = Field(default=None, max_length=100)
    work_modality: str | None = Field(default=None, pattern="^(remoto|hibrido|presencial)$")
    hard_skills: list[SkillResource] | None = None
    soft_skills: list[SkillResource] | None = None
    education: list[EducationResource] | None = None
    experience: list[ExperienceResource] | None = None
    languages: list[LanguageResource] | None = None
    professional_summary: str | None = Field(default=None, max_length=2000)