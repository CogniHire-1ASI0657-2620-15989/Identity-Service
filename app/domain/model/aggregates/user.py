from datetime import datetime, timezone

from app.domain.model.value_objects.email_address import EmailAddress
from app.domain.model.value_objects.person_name import PersonName
from app.domain.model.value_objects.user_segment import UserSegment
from app.domain.model.value_objects.location import Location


class User:
    def __init__(
        self,
        user_id: int | None,
        name: PersonName,
        email: EmailAddress,
        password_hash: str,
        segment: UserSegment,
        location: Location | None = None,
        target_position: str | None = None,
        expected_city: str | None = None,
        expected_country: str | None = None,
        work_modality: str | None = None,
        hard_skills: list[dict] | None = None,
        soft_skills: list[dict] | None = None,
        education: list[dict] | None = None,
        experience: list[dict] | None = None,
        languages: list[dict] | None = None,
        professional_summary: str | None = None,
        created_at: datetime | None = None,
    ):
        if not password_hash:
            raise ValueError("El password hash no puede estar vacío.")

        self._id = user_id
        self._name = name
        self._email = email
        self._password_hash = password_hash
        self._segment = segment
        self._location = location
        self._target_position = target_position
        self._expected_city = expected_city
        self._expected_country = expected_country
        self._work_modality = work_modality
        self._hard_skills = hard_skills or []
        self._soft_skills = soft_skills or []
        self._education = education or []
        self._experience = experience or []
        self._languages = languages or []
        self._professional_summary = professional_summary
        self._created_at = created_at or datetime.now(timezone.utc)

    @property
    def id(self) -> int | None:
        return self._id

    @property
    def name(self) -> PersonName:
        return self._name

    @property
    def email(self) -> EmailAddress:
        return self._email

    @property
    def password_hash(self) -> str:
        return self._password_hash

    @property
    def segment(self) -> UserSegment:
        return self._segment

    @property
    def location(self) -> Location | None:
        return self._location

    @property
    def created_at(self) -> datetime:
        return self._created_at

    @property
    def target_position(self) -> str | None:
        return self._target_position

    @property
    def expected_city(self) -> str | None:
        return self._expected_city

    @property
    def expected_country(self) -> str | None:
        return self._expected_country

    @property
    def work_modality(self) -> str | None:
        return self._work_modality

    @property
    def hard_skills(self) -> list[dict]:
        return self._hard_skills

    @property
    def soft_skills(self) -> list[dict]:
        return self._soft_skills

    @property
    def education(self) -> list[dict]:
        return self._education

    @property
    def experience(self) -> list[dict]:
        return self._experience

    @property
    def languages(self) -> list[dict]:
        return self._languages

    @property
    def professional_summary(self) -> str | None:
        return self._professional_summary

    def change_name(self, name: PersonName) -> None:
        self._name = name

    def change_email(self, email: EmailAddress) -> None:
        self._email = email

    def change_segment(self, segment: UserSegment) -> None:
        self._segment = segment

    def change_location(self, location: Location) -> None:
        self._location = location

    def change_password(self, password_hash: str) -> None:
        if not password_hash:
            raise ValueError("El password hash no puede estar vacío.")

        self._password_hash = password_hash

    def update_job_profile(self, **fields) -> None:
        for field, value in fields.items():
            if value is not None and hasattr(self, f"_{field}"):
                setattr(self, f"_{field}", value)

    def skills(self, skill_type: str) -> list[dict]:
        if skill_type not in ("hard", "soft"):
            raise ValueError("El tipo de habilidad debe ser hard o soft.")
        return self._hard_skills if skill_type == "hard" else self._soft_skills

    def add_skill(self, skill_type: str, skill: dict) -> None:
        skills = self.skills(skill_type)
        if any(item["name"].lower() == skill["name"].lower() for item in skills):
            raise ValueError("La habilidad ya existe.")
        skills.append(skill)

    def update_skill(self, skill_type: str, name: str, skill: dict) -> None:
        skills = self.skills(skill_type)
        for index, item in enumerate(skills):
            if item["name"].lower() == name.lower():
                skills[index] = skill
                return
        raise ValueError("La habilidad no existe.")

    def remove_skill(self, skill_type: str, name: str) -> None:
        skills = self.skills(skill_type)
        for index, item in enumerate(skills):
            if item["name"].lower() == name.lower():
                skills.pop(index)
                return
        raise ValueError("La habilidad no existe.")