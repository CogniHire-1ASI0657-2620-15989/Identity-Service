from pathlib import Path

from pytest_bdd import scenarios, then, when

from app.dependencies import get_token_service
from conftest import EMAIL, PASSWORD

scenarios(str(Path(__file__).parent / "features" / "user_authentication_login.feature"))


@when('a POST request is sent to "/api/v1/auth/login" with the correct credentials', target_fixture="response")
def login_ok(client):
    return client.post("/api/v1/auth/login", json={"email": EMAIL, "password": PASSWORD})


@when('a POST request is sent to "/api/v1/auth/login" with an invalid password', target_fixture="response")
def login_bad(client):
    return client.post("/api/v1/auth/login", json={"email": EMAIL, "password": "ClaveIncorrecta999"})


@then("the response body contains a valid bearer access token")
def bearer_token(response):
    body = response.json()
    assert body["token_type"].lower() == "bearer"
    assert get_token_service().decode(body["access_token"])["sub"] == str(body["user"]["id"])
