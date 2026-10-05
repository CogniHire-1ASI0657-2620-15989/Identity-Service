from datetime import datetime, timezone

from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.application.internal.command_services.default_auth_command_service import (
    DefaultAuthCommandService,
)
from app.dependencies import get_auth_command_service
from app.domain.model.aggregates.user import User
from app.domain.model.value_objects.email_address import EmailAddress
from app.domain.model.value_objects.person_name import PersonName
from app.domain.model.value_objects.user_segment import UserSegment
from app.infrastructure.security.bcrypt_password_hasher import BcryptPasswordHasher
from app.interfaces.rest.controller.auth_controller import router as auth_router

VALID_PASSWORD = "secreto123"


class TokenServiceStub:
    def generate(self, user: User) -> str:
        return "stub-access-token"

    def decode(self, token: str) -> dict:
        return {"sub": "1"}


class UserRepositoryStub:
    def __init__(self) -> None:
        self.user = User(
            user_id=1,
            name=PersonName("Jeremy Quijada"),
            email=EmailAddress("jeremy@upc.edu.pe"),
            password_hash=BcryptPasswordHasher().hash(VALID_PASSWORD),
            segment=UserSegment.INTERN,
            created_at=datetime(2026, 9, 15, 12, 0, tzinfo=timezone.utc),
        )

    def find_by_email(self, email: EmailAddress):
        return self.user if email.value == self.user.email.value else None


def build_client() -> TestClient:
    app = FastAPI()
    app.include_router(auth_router)
    app.dependency_overrides[get_auth_command_service] = lambda: DefaultAuthCommandService(
        user_repository=UserRepositoryStub(),
        password_hasher=BcryptPasswordHasher(),
        token_service=TokenServiceStub(),
    )
    return TestClient(app)


def test_login_rejects_a_wrong_password():
    # Arrange
    client = build_client()
    payload = {"email": "jeremy@upc.edu.pe", "password": "incorrecta"}

    # Act
    response = client.post("/api/v1/auth/login", json=payload)

    # Assert
    assert response.status_code == 401
    assert response.json()["detail"] == "Credenciales inválidas."


def test_login_hides_whether_the_email_exists():
    # Arrange
    client = build_client()
    payload = {"email": "desconocido@upc.edu.pe", "password": VALID_PASSWORD}

    # Act
    response = client.post("/api/v1/auth/login", json=payload)

    # Assert
    assert response.status_code == 401
    assert response.json()["detail"] == "Credenciales inválidas."


def test_login_returns_a_token_for_valid_credentials():
    # Arrange
    client = build_client()
    payload = {"email": "Jeremy@UPC.edu.pe", "password": VALID_PASSWORD}

    # Act
    response = client.post("/api/v1/auth/login", json=payload)

    # Assert
    assert response.status_code == 200
    body = response.json()
    assert body["access_token"] == "stub-access-token"
    assert body["user"]["id"] == 1
    assert body["user"]["email"] == "jeremy@upc.edu.pe"
