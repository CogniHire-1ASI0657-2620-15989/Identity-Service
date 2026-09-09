from pydantic import BaseModel, Field


class ChangePasswordResource(BaseModel):
    current_password: str

    new_password: str = Field(
        min_length=6,
        max_length=128
    )