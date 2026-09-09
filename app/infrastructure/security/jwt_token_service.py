from datetime import datetime, timedelta, timezone

import jwt

from app.application.ports.token_service import TokenService
from app.domain.model.aggregates.user import User


class JwtTokenService(TokenService):

    def __init__(
        self,
        secret_key: str,
        issuer: str,
        audience: str,
        expiration_minutes: int = 60,
    ):
        self._secret_key = secret_key
        self._issuer = issuer
        self._audience = audience
        self._expiration_minutes = expiration_minutes

    def generate(
        self,
        user: User
    ) -> str:

        now = datetime.now(timezone.utc)

        payload = {
            "sub": str(user.id),
            "email": user.email.value,
            "name": user.name.value,
            "segment": user.segment.value,
            "iss": self._issuer,
            "aud": self._audience,
            "iat": now,
            "exp": now + timedelta(
                minutes=self._expiration_minutes
            ),
        }

        return jwt.encode(
            payload,
            self._secret_key,
            algorithm="HS256",
        )

    def decode(
        self,
        token: str
    ) -> dict:

        return jwt.decode(
            token,
            self._secret_key,
            algorithms=["HS256"],
            issuer=self._issuer,
            audience=self._audience,
        )