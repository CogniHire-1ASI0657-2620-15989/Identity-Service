from pydantic import BaseModel, EmailStr, Field


class RegisterUserResource(BaseModel):
    dni: str = Field(pattern=r"^\d{8}$")
    first_name: str = Field(min_length=1, max_length=100)
    first_last_name: str = Field(min_length=1, max_length=100)
    second_last_name: str = Field(min_length=1, max_length=100)
    email: EmailStr
    password: str = Field(min_length=6, max_length=128)
    segment: str

    city: str | None = None
    country: str | None = None
