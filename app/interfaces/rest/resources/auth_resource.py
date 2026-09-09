from pydantic import BaseModel

from app.interfaces.rest.resources.user_resource import UserResource


class AuthResource(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResource