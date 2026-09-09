from datetime import datetime, timezone

from app.application.ports.password_hasher import PasswordHasher
from app.application.ports.token_service import TokenService

from app.domain.model.aggregates.user import User

from app.domain.model.commands.register_user_command import (
    RegisterUserCommand,
)
from app.domain.model.commands.authenticate_user_command import (
    AuthenticateUserCommand,
)

from app.domain.model.value_objects.email_address import EmailAddress
from app.domain.model.value_objects.person_name import PersonName
from app.domain.model.value_objects.user_segment import UserSegment
from app.domain.model.value_objects.location import Location

from app.domain.repositories.user_repository import UserRepository
from app.domain.services.auth_command_service import AuthCommandService


class DefaultAuthCommandService(AuthCommandService):

    def __init__(
        self,
        user_repository: UserRepository,
        password_hasher: PasswordHasher,
        token_service: TokenService,
    ):
        self._user_repository = user_repository
        self._password_hasher = password_hasher
        self._token_service = token_service

    def handle_register(
        self,
        command: RegisterUserCommand
    ) -> tuple[User, str]:

        email = EmailAddress(command.email)

        existing_user = self._user_repository.find_by_email(email)

        if existing_user is not None:
            raise ValueError("El email ya está registrado.")

        name = PersonName(command.name)

        segment = UserSegment.from_value(command.segment)

        location = None

        if command.city is not None or command.country is not None:
            if not command.city or not command.country:
                raise ValueError(
                    "La ciudad y el país deben proporcionarse juntos."
                )

            location = Location(
                city=command.city,
                country=command.country,
            )

        if len(command.password) < 6:
            raise ValueError(
                "La contraseña debe tener al menos 6 caracteres."
            )

        password_hash = self._password_hasher.hash(
            command.password
        )

        user = User(
            user_id=None,
            name=name,
            email=email,
            password_hash=password_hash,
            segment=segment,
            location=location,
            created_at=datetime.now(timezone.utc),
        )

        saved_user = self._user_repository.save(user)

        access_token = self._token_service.generate(saved_user)

        return saved_user, access_token

    def handle_authenticate(
        self,
        command: AuthenticateUserCommand
    ) -> tuple[User, str]:

        email = EmailAddress(command.email)

        user = self._user_repository.find_by_email(email)

        if user is None:
            raise ValueError("Credenciales inválidas.")

        password_is_valid = self._password_hasher.verify(
            command.password,
            user.password_hash,
        )

        if not password_is_valid:
            raise ValueError("Credenciales inválidas.")

        access_token = self._token_service.generate(user)

        return user, access_token