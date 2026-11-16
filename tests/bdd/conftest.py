"""Soporte común de los tests BDD (ningún archivo de app/ se modifica).

El microservicio se prueba por su API HTTP real con las capas reales
(servicios, repositorio SQLAlchemy, bcrypt y JWT). Solo se sustituye
PostgreSQL por SQLite en memoria, así que únicamente hacen falta los .feature.
Aquí viven también los steps que comparten varios features.
"""
import os
from datetime import timezone
from types import SimpleNamespace

os.environ["INTERNAL_API_KEY"] = "test-key"  # la app ahora lo exige al importarse y en cada petición
os.environ["DATABASE_URL"] = "sqlite://"  # antes de importar app: evita cualquier conexión a PostgreSQL
os.environ.setdefault("DECOLECTA_BASE_URL", "http://decolecta.test")  # get_settings() lo exige al importar
os.environ.setdefault("DECOLECTA_API_KEY", "test-decolecta-key")
os.environ.setdefault("JWT_SECRET_KEY", "bdd-test-secret-key-with-32-bytes!!")  # evita InsecureKeyLengthWarning

import pytest
from fastapi.testclient import TestClient
from pytest_bdd import given, parsers, then, when
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.application.ports.reniec_identity_verifier import (
    ReniecIdentity,
    ReniecIdentityNotFound,
    ReniecIdentityVerifier,
)
from app.dependencies import get_db, get_reniec_identity_verifier, get_token_service
from app.domain.model.aggregates.user import User
from app.domain.model.value_objects.email_address import EmailAddress
from app.domain.model.value_objects.person_name import PersonName
from app.domain.model.value_objects.user_segment import UserSegment
from app.infrastructure.persistence.sqlalchemy.configuration.database import Base
from app.infrastructure.persistence.sqlalchemy.models import password_reset_token_model, user_model  # noqa: F401
from app.infrastructure.persistence.sqlalchemy.models.password_reset_token_model import PasswordResetTokenModel
from app.infrastructure.persistence.sqlalchemy.repositories.sqlalchemy_user_repository import SQLAlchemyUserRepository
from app.infrastructure.security.bcrypt_password_hasher import BcryptPasswordHasher
from app.main import app

EMAIL = "ana.perez@example.com"
PASSWORD = "ClaveSegura123"


@event.listens_for(PasswordResetTokenModel, "load")
def _utc_after_sqlite(target, _context):
    # SQLite devuelve fechas sin zona horaria; PostgreSQL las devuelve con zona.
    for field in ("expires_at", "used_at"):
        value = getattr(target, field)
        if value is not None and value.tzinfo is None:
            setattr(target, field, value.replace(tzinfo=timezone.utc))


# Identidad que "RENIEC" devuelve para el DNI de prueba. Nunca se llama a Decolecta real.
RENIEC_REGISTRY = {"46027896": ReniecIdentity("ANA LUCIA", "PEREZ", "GOMEZ", "46027896")}


class FakeReniecIdentityVerifier(ReniecIdentityVerifier):
    """Doble de prueba del puerto ReniecIdentityVerifier (ACL hacia Decolecta)."""

    def find_by_dni(self, dni: str) -> ReniecIdentity:
        try:
            return RENIEC_REGISTRY[dni]
        except KeyError as exc:
            raise ReniecIdentityNotFound(dni) from exc


@pytest.fixture
def db():
    engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    Base.metadata.create_all(engine)
    session = sessionmaker(bind=engine, autoflush=False)()
    yield session
    session.close()
    engine.dispose()


@pytest.fixture
def client(db):
    app.dependency_overrides[get_db] = lambda: db
    app.dependency_overrides[get_reniec_identity_verifier] = FakeReniecIdentityVerifier
    yield TestClient(app, headers={"X-Internal-Api-Key": "test-key"})  # sin "with": no se ejecuta el startup que crearía tablas en PostgreSQL
    app.dependency_overrides.clear()


@pytest.fixture
def ctx():
    """Estado compartido entre los steps de un escenario."""
    return SimpleNamespace(headers={}, user=None)


def create_user(db, email=EMAIL, password=PASSWORD, **profile) -> User:
    user = User(None, PersonName("Ana Perez"), EmailAddress(email), BcryptPasswordHasher().hash(password),
                UserSegment.WORKER, **profile)
    return SQLAlchemyUserRepository(db).save(user)


# ---------- Given compartidos ----------
@given(parsers.re(r'a registered user with email "(?P<email>[^"]+)" and password "(?P<password>[^"]+)"'))
def registered_user_with_password(db, ctx, email, password):
    ctx.user = create_user(db, email, password)


@given(parsers.re(r'a registered user with email "(?P<email>[^"]+)"$'))
def registered_user(db, ctx, email):
    ctx.user = create_user(db, email)


@given("an authenticated user with a valid bearer token")
def authenticated_user(db, ctx):
    ctx.user = create_user(db)
    ctx.headers = {"Authorization": f"Bearer {get_token_service().generate(ctx.user)}"}


@given("an unauthenticated user")
def unauthenticated_user(ctx):
    ctx.headers = {}


# ---------- When / Then compartidos ----------
@when(parsers.re(r'a (?P<method>[A-Z]+) request is sent to "(?P<path>[^"]+)"$'), target_fixture="response")
def send_request(client, ctx, method, path):
    return client.request(method, path, headers=ctx.headers)


@then(parsers.re(r"the response status is (?P<code>\d+) .+"))
def status_is(response, code):
    assert response.status_code == int(code), response.text


@then(parsers.re(r'the response body contains the message "(?P<message>[^"]+)"'))
def message_is(response, message):
    assert message in str(response.json().get("detail"))
