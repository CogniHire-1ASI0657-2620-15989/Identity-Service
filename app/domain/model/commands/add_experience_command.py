from dataclasses import dataclass


@dataclass(frozen=True)
class AddExperienceCommand:
    user_id: int
    experience: dict
