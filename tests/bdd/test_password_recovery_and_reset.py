from pathlib import Path

from pytest_bdd import given, scenarios, then, when

from app.application.internal.command_services.password_recovery_service import PasswordRecoveryService
from app.infrastructure.persistence.sqlalchemy.repositories.sqlalchemy_user_repository import SQLAlchemyUserRepository
from app.infrastructure.security.bcrypt_password_hasher import BcryptPasswordHasher
from conftest import EMAIL, create_user

scenarios(str(Path(__file__).parent / "features" / "password_recovery_and_reset.feature"))


@given("a valid password recovery token for the user")
def valid_recovery_token(db, ctx):
    ctx.user = create_user(db)
    service = PasswordRecoveryService(db, SQLAlchemyUserRepository(db), BcryptPasswordHasher())
    ctx.token = service.request_recovery(EMAIL)


@when('a POST request is sent to "/api/v1/auth/password-recovery" with the email', target_fixture="response")
def request_recovery(client):
    return client.post("/api/v1/auth/password-recovery", json={"email": EMAIL})


@when('a POST request is sent to "/api/v1/auth/password-reset" with the token and new password', target_fixture="response")
def reset_password(client, ctx):
    return client.post("/api/v1/auth/password-reset", json={"token": ctx.token, "new_password": "NuevaClave456"})


@then("the response body indicates that a recovery token has been generated")
def token_generated(response):
    assert response.json()["token"]
