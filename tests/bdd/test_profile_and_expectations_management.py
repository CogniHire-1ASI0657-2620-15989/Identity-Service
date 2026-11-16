from pathlib import Path

from pytest_bdd import parsers, scenarios, then, when

scenarios(str(Path(__file__).parent / "features" / "profile_and_expectations_management.feature"))

PROFILE = {"target_position": "Backend Developer", "expected_city": "Lima", "expected_country": "Perú",
           "work_modality": "hibrido", "professional_summary": "Desarrollador especializado en APIs REST."}


@when('a PUT request is sent to "/api/v1/profile/me" with valid profile details and expected role', target_fixture="response")
@when('a PUT request is sent to "/api/v1/profile/me" with profile updates', target_fixture="response")
def update_profile(client, ctx):
    return client.put("/api/v1/profile/me", json=PROFILE, headers=ctx.headers)


@then("the response body contains the updated user profile data")
def updated_profile(response):
    body = response.json()
    assert all(body[key] == value for key, value in PROFILE.items())


@then("the response body indicates missing or invalid token")
def missing_token(response):
    assert "token" in str(response.json()["detail"]).lower()


@when(parsers.re(r'a POST request is sent to "(?P<path>[^"]+)" with position "(?P<position>[^"]+)" at company '
                 r'"(?P<company>[^"]+)" from "(?P<start>[^"]+)" to "(?P<end>[^"]+)"'), target_fixture="response")
def add_experience(client, ctx, path, position, company, start, end):
    payload = {"position": position, "company": company, "start_date": start, "end_date": end}
    return client.post(path, json=payload, headers=ctx.headers)


@then(parsers.re(r'the response body contains the experience "(?P<position>[^"]+)" at "(?P<company>[^"]+)"'))
def experience_added(response, position, company):
    assert any(item["position"] == position and item["company"] == company
               for item in response.json()["experience"])
