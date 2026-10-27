from dataclasses import dataclass


@dataclass(frozen=True)
class UpdateEducationCommand:
    user_id: int
    education_id: str
    education: dict
