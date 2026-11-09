import unittest

from app.application.internal.command_services.default_auth_command_service import DefaultAuthCommandService
from app.application.ports.reniec_identity_verifier import ReniecIdentity, ReniecIdentityNotFound
from app.domain.model.aggregates.user import User
from app.domain.model.commands.register_user_command import RegisterUserCommand
from app.domain.model.value_objects.email_address import EmailAddress
from app.domain.model.value_objects.person_name import PersonName
from app.domain.model.value_objects.user_segment import UserSegment


class InMemoryUserRepository:
    def __init__(self):
        self.saved_user = None

    def find_by_email(self, _):
        return None

    def save(self, user):
        self.saved_user = user
        return User(
            user_id=1,
            name=user.name,
            email=user.email,
            password_hash=user.password_hash,
            segment=user.segment,
            location=user.location,
            created_at=user.created_at,
        )


class PasswordHasher:
    def hash(self, password):
        return f"hash:{password}"


class TokenService:
    def generate(self, _):
        return "token"


class MatchingReniecVerifier:
    def find_by_dni(self, dni):
        return ReniecIdentity("ROXANA KARINA", "DELGADO", "CUELLAR", dni)


class MismatchedReniecVerifier:
    def find_by_dni(self, dni):
        return ReniecIdentity("MARIA", "DELGADO", "CUELLAR", dni)


def registration_command():
    return RegisterUserCommand(
        dni="46027896",
        first_name="Roxana",
        first_last_name="Delgado",
        second_last_name="Cuellar",
        email="roxana@example.com",
        password="secret123",
        segment="trabajador",
    )


class RegistrationAndExperienceTests(unittest.TestCase):
    def test_registration_persists_only_after_matching_reniec_identity(self):
        repository = InMemoryUserRepository()
        service = DefaultAuthCommandService(
            repository,
            PasswordHasher(),
            TokenService(),
            MatchingReniecVerifier(),
        )

        user, token = service.handle_register(registration_command())

        self.assertEqual(token, "token")
        self.assertEqual(user.name.value, "Roxana Delgado Cuellar")
        self.assertIsNotNone(repository.saved_user)

    def test_registration_rejects_mismatched_reniec_identity_without_persisting(self):
        repository = InMemoryUserRepository()
        service = DefaultAuthCommandService(
            repository,
            PasswordHasher(),
            TokenService(),
            MismatchedReniecVerifier(),
        )

        with self.assertRaises(ReniecIdentityNotFound):
            service.handle_register(registration_command())

        self.assertIsNone(repository.saved_user)

    def test_user_adds_valid_experience_and_rejects_invalid_date_range(self):
        user = User(
            user_id=1,
            name=PersonName("Ana García"),
            email=EmailAddress("ana@example.com"),
            password_hash="hash",
            segment=UserSegment.from_value("trabajador"),
        )

        user.add_experience(
            {
                "company": "Empresa X",
                "position": "Developer",
                "start_date": "2022-01",
                "end_date": "2024-06",
            }
        )
        self.assertEqual(user.experience[0]["company"], "Empresa X")

        with self.assertRaises(ValueError):
            user.add_experience(
                {
                    "company": "Empresa X",
                    "position": "Developer",
                    "start_date": "2024-06",
                    "end_date": "2022-01",
                }
            )
