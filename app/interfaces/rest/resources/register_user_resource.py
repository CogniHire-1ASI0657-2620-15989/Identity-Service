from pydantic import BaseModel, EmailStr, Field


class RegisterUserResource(BaseModel):
    name: str = Field(min_length=1, max_length=150)
    email: EmailStr
    password: str = Field(min_length=6, max_length=128)
    segment: str

    city: str | None = None
    country: str | None = None