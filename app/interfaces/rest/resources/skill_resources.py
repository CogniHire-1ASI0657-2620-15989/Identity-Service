from typing import Literal

from pydantic import BaseModel, Field


class SkillResource(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    level: str | None = Field(default=None, max_length=50)


class SkillTypeResource(BaseModel):
    type: Literal["hard", "soft"]
