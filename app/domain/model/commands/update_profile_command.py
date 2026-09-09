from dataclasses import dataclass


@dataclass(frozen=True)
class UpdateProfileCommand:
    user_id: int
    name: str | None = None
    email: str | None = None
    segment: str | None = None
    city: str | None = None
    country: str | None = None
    target_position: str | None = None
    expected_city: str | None = None
    expected_country: str | None = None
    work_modality: str | None = None
    hard_skills: list[dict] | None = None
    soft_skills: list[dict] | None = None
    education: list[dict] | None = None
    experience: list[dict] | None = None
    languages: list[dict] | None = None
    professional_summary: str | None = None