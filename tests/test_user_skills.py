import pytest

from app.domain.model.aggregates.user import User
from app.domain.model.value_objects.email_address import EmailAddress
from app.domain.model.value_objects.person_name import PersonName
from app.domain.model.value_objects.user_segment import UserSegment


def build_user() -> User:
    return User(
        user_id=1,
        name=PersonName("Jeremy Quijada"),
        email=EmailAddress("jeremy@upc.edu.pe"),
        password_hash="$2b$12$hashedvalue",
        segment=UserSegment.INTERN,
        hard_skills=[{"name": "Python"}],
    )


def test_add_skill_rejects_duplicates_ignoring_case():
    # Arrange
    user = build_user()
    duplicated_skill = {"name": "python"}

    # Act / Assert
    with pytest.raises(ValueError, match="La habilidad ya existe."):
        user.add_skill("hard", duplicated_skill)


def test_remove_skill_deletes_the_matching_entry():
    # Arrange
    user = build_user()

    # Act
    user.remove_skill("hard", "PYTHON")

    # Assert
    assert user.hard_skills == []


def test_remove_skill_fails_when_the_skill_is_absent():
    # Arrange
    user = build_user()
    missing_skill = "Java"

    # Act / Assert
    with pytest.raises(ValueError, match="La habilidad no existe."):
        user.remove_skill("hard", missing_skill)
