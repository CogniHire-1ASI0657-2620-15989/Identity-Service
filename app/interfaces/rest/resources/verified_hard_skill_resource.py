from pydantic import BaseModel, Field


class VerifiedHardSkillResource(BaseModel):
    """Skill confirmed by an approved certificate in a trusted internal workflow."""

    name: str = Field(min_length=1, max_length=100)
