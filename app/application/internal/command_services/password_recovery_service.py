from datetime import datetime, timedelta, timezone
import hashlib
import secrets

from sqlalchemy.orm import Session

from app.application.ports.password_hasher import PasswordHasher
from app.domain.model.value_objects.email_address import EmailAddress
from app.domain.repositories.user_repository import UserRepository
from app.infrastructure.persistence.sqlalchemy.models.password_reset_token_model import (
    PasswordResetTokenModel,
)


class PasswordRecoveryService:
    def __init__(
        self,
        db: Session,
        user_repository: UserRepository,
        password_hasher: PasswordHasher,
        expiration_minutes: int = 30,
    ):
        self._db = db
        self._user_repository = user_repository
        self._password_hasher = password_hasher
        self._expiration_minutes = expiration_minutes

    def request_recovery(self, email: str) -> str | None:
        user = self._user_repository.find_by_email(EmailAddress(email))
        if user is None:
            return None

        raw_token = secrets.token_urlsafe(32)
        token_hash = hashlib.sha256(raw_token.encode()).hexdigest()
        now = datetime.now(timezone.utc)
        self._db.add(
            PasswordResetTokenModel(
                user_id=user.id,
                token_hash=token_hash,
                expires_at=now + timedelta(minutes=self._expiration_minutes),
            )
        )
        self._db.commit()
        return raw_token

    def reset_password(self, raw_token: str, new_password: str) -> None:
        token_hash = hashlib.sha256(raw_token.encode()).hexdigest()
        token = (
            self._db.query(PasswordResetTokenModel)
            .filter(PasswordResetTokenModel.token_hash == token_hash)
            .first()
        )
        now = datetime.now(timezone.utc)
        if token is None or token.used_at is not None or token.expires_at <= now:
            raise ValueError("El token de recuperación no es válido o ha expirado.")
        if len(new_password) < 6:
            raise ValueError("La nueva contraseña debe tener al menos 6 caracteres.")

        user = self._user_repository.find_by_id(token.user_id)
        if user is None:
            raise ValueError("Usuario no encontrado.")
        user.change_password(self._password_hasher.hash(new_password))
        self._user_repository.update(user)
        token.used_at = now
        self._db.commit()
