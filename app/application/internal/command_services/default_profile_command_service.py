from app.application.ports.password_hasher import PasswordHasher

from app.domain.model.aggregates.user import User

from app.domain.model.commands.update_profile_command import (
    UpdateProfileCommand,
)
from app.domain.model.commands.change_password_command import (
    ChangePasswordCommand,
)

from app.domain.model.value_objects.email_address import EmailAddress
from app.domain.model.value_objects.person_name import PersonName
from app.domain.model.value_objects.user_segment import UserSegment
from app.domain.model.value_objects.location import Location

from app.domain.repositories.user_repository import UserRepository
from app.domain.services.profile_command_service import (
    ProfileCommandService,
)


class DefaultProfileCommandService(ProfileCommandService):

    def __init__(
        self,
        user_repository: UserRepository,
        password_hasher: PasswordHasher,
    ):
        self._user_repository = user_repository
        self._password_hasher = password_hasher

    def handle_update_profile(
        self,
        command: UpdateProfileCommand
    ) -> User:

        user = self._user_repository.find_by_id(
            command.user_id
        )

        if user is None:
            raise ValueError("Usuario no encontrado.")

        if command.name is not None:
            user.change_name(
                PersonName(command.name)
            )

        if command.email is not None:

            new_email = EmailAddress(command.email)

            existing_user = (
                self._user_repository.find_by_email(
                    new_email
                )
            )

            if (
                existing_user is not None
                and existing_user.id != user.id
            ):
                raise ValueError(
                    "El email ya está registrado."
                )

            user.change_email(new_email)

        if command.segment is not None:
            user.change_segment(
                UserSegment.from_value(
                    command.segment
                )
            )

        if (
            command.city is not None
            or command.country is not None
        ):

            current_city = (
                user.location.city
                if user.location
                else None
            )

            current_country = (
                user.location.country
                if user.location
                else None
            )

            city = command.city or current_city
            country = command.country or current_country

            if not city or not country:
                raise ValueError(
                    "La ubicación requiere ciudad y país."
                )

            user.change_location(
                Location(
                    city=city,
                    country=country,
                )
            )

        user.update_job_profile(
            target_position=command.target_position,
            expected_city=command.expected_city,
            expected_country=command.expected_country,
            work_modality=command.work_modality,
            hard_skills=command.hard_skills,
            soft_skills=command.soft_skills,
            education=command.education,
            experience=command.experience,
            languages=command.languages,
            professional_summary=command.professional_summary,
        )

        return self._user_repository.update(user)

    def handle_change_password(
        self,
        command: ChangePasswordCommand
    ) -> User:

        user = self._user_repository.find_by_id(
            command.user_id
        )

        if user is None:
            raise ValueError("Usuario no encontrado.")

        if not self._password_hasher.verify(
            command.current_password,
            user.password_hash,
        ):
            raise ValueError(
                "La contraseña actual es incorrecta."
            )

        if len(command.new_password) < 6:
            raise ValueError(
                "La nueva contraseña debe tener "
                "al menos 6 caracteres."
            )

        new_password_hash = self._password_hasher.hash(
            command.new_password
        )

        user.change_password(
            new_password_hash
        )

        return self._user_repository.update(user)

    def handle_add_skill(self, user_id: int, skill_type: str, skill: dict) -> User:
        user = self._user_repository.find_by_id(user_id)
        if user is None:
            raise ValueError("Usuario no encontrado.")
        user.add_skill(skill_type, skill)
        return self._user_repository.update(user)

    def handle_update_skill(self, user_id: int, skill_type: str, name: str, skill: dict) -> User:
        user = self._user_repository.find_by_id(user_id)
        if user is None:
            raise ValueError("Usuario no encontrado.")
        user.update_skill(skill_type, name, skill)
        return self._user_repository.update(user)

    def handle_remove_skill(self, user_id: int, skill_type: str, name: str) -> User:
        user = self._user_repository.find_by_id(user_id)
        if user is None:
            raise ValueError("Usuario no encontrado.")
        user.remove_skill(skill_type, name)
        return self._user_repository.update(user)