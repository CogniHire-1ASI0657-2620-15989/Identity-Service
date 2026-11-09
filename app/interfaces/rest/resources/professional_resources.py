from pydantic import BaseModel, Field, model_validator


class EducationInputResource(BaseModel):
    degree: str | None = Field(default=None, max_length=150)
    institution: str | None = Field(default=None, max_length=150)
    field_of_study: str | None = Field(default=None, max_length=150)
    start_year: int | None = Field(default=None, ge=1900, le=2100)
    end_year: int | None = Field(default=None, ge=1900, le=2100)


class EducationResource(EducationInputResource):
    id: str


class ExperienceResource(BaseModel):
    position: str | None = Field(default=None, max_length=150)
    company: str | None = Field(default=None, max_length=150)
    description: str | None = Field(default=None, max_length=2000)
    start_date: str | None = Field(default=None, max_length=20)
    end_date: str | None = Field(default=None, max_length=20)
    current: bool = False


class ExperienceInputResource(BaseModel):
    company: str = Field(min_length=1, max_length=150)
    position: str = Field(min_length=1, max_length=150)
    start_date: str = Field(pattern=r"^\d{4}-(0[1-9]|1[0-2])$")
    end_date: str = Field(pattern=r"^\d{4}-(0[1-9]|1[0-2])$")

    @model_validator(mode="after")
    def validate_date_range(self):
        if self.end_date < self.start_date:
            raise ValueError("La fecha hasta no puede ser anterior a la fecha desde.")
        return self


class LanguageResource(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    level: str | None = Field(default=None, max_length=50)
