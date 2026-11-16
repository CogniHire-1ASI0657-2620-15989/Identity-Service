from pathlib import Path

from pytest_bdd import given, parsers, scenarios, then, when

from app.domain.model.value_objects.email_address import EmailAddress
from app.infrastructure.persistence.sqlalchemy.repositories.sqlalchemy_user_repository import SQLAlchemyUserRepository
from conftest import PASSWORD, create_user

scenarios(str(Path(__file__).parent / "features" / "user_registration.feature"))

# El registro valida identidad contra RENIEC: el DNI y los nombres deben coincidir con FakeReniecIdentityVerifier.
PAYLOAD = {
    "dni": "46027896",
    "first_name": "Ana",
    "first_last_name": "Perez",
    "second_last_name": "Gomez",
    "password": PASSWORD,
    "segment": "trabajador",
    "city": "Lima",
    "country": "Perú",
}


@given(parsers.re(r'the email "(?P<email>[^"]+)" is not registered in the system'))
def email_not_registered(email):
    pass  # la base de datos de cada escenario arranca vacía


@given(parsers.re(r'the email "(?P<email>[^"]+)" is already registered in the system'))
def email_registered(db, email):
    create_user(db, email)


@when("a POST request is sent to \"/api/v1/auth/register\" with valid registration details", target_fixture="response")
@when("a POST request is sent to \"/api/v1/auth/register\" with the duplicate email", target_fixture="response")
def register(client):
    return client.post("/api/v1/auth/register", json={**PAYLOAD, "email": "ana.perez@example.com"})


@then("the response body contains an access token and user profile information")
def token_and_profile(response):
    body = response.json()
    assert body["access_token"]
    assert body["user"]["email"] == "ana.perez@example.com" and body["user"]["id"]


@when('a POST request is sent to "/api/v1/auth/register" with a DNI whose names do not match RENIEC',
      target_fixture="response")
def register_with_mismatched_identity(client):
    return client.post("/api/v1/auth/register",
                       json={**PAYLOAD, "first_name": "Maria", "email": "ana.perez@example.com"})


@then(parsers.re(r'no user account is created for "(?P<email>[^"]+)"'))
def no_account(db, email):
    assert SQLAlchemyUserRepository(db).find_by_email(EmailAddress(email)) is None
