from pydantic import BaseModel, EmailStr, Field


class PasswordRecoveryRequest(BaseModel):
    email: EmailStr


class PasswordRecoveryResponse(BaseModel):
    message: str
    token: str | None = None


class PasswordResetRequest(BaseModel):
    token: str = Field(min_length=20)
    new_password: str = Field(min_length=6, max_length=128)
