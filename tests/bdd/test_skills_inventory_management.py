from pathlib import Path

from pytest_bdd import given, parsers, scenarios, then, when

from app.dependencies import get_token_service
from conftest import create_user

scenarios(str(Path(__file__).parent / "features" / "skills_inventory_management.feature"))


@given(parsers.re(r'an authenticated user who already has the skill "(?P<skill>[^"]+)" registered'))
def user_with_skill(db, ctx, skill):
    ctx.user = create_user(db, hard_skills=[{"name": skill, "level": "advanced"}])
    ctx.headers = {"Authorization": f"Bearer {get_token_service().generate(ctx.user)}"}


@when(parsers.re(r'a POST request is sent to "(?P<path>[^"]+)" with skill name "(?P<name>[^"]+)" and level "(?P<level>[^"]+)"'),
      target_fixture="response")
def add_skill(client, ctx, path, name, level):
    return client.post(path, json={"name": name, "level": level}, headers=ctx.headers)


@then("the response body contains the updated profile including the new skill")
def skill_added(response):
    assert {"name": "Python", "level": "advanced"} in response.json()["hard_skills"]


@then("the response body contains the profile without the specified skill")
def skill_removed(response):
    assert all(skill["name"] != "Python" for skill in response.json()["hard_skills"])
