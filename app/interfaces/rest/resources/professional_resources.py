from pydantic import BaseModel, Field


class EducationResource(BaseModel):
    degree: str | None = Field(default=None, max_length=150)
    institution: str | None = Field(default=None, max_length=150)
    field_of_study: str | None = Field(default=None, max_length=150)
    start_year: int | None = Field(default=None, ge=1900, le=2100)
    end_year: int | None = Field(default=None, ge=1900, le=2100)


class ExperienceResource(BaseModel):
    position: str | None = Field(default=None, max_length=150)
    company: str | None = Field(default=None, max_length=150)
    description: str | None = Field(default=None, max_length=2000)
    start_date: str | None = Field(default=None, max_length=20)
    end_date: str | None = Field(default=None, max_length=20)
    current: bool = False


class LanguageResource(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    level: str | None = Field(default=None, max_length=50)
