from dataclasses import dataclass


@dataclass(frozen=True)
class AddEducationCommand:
    user_id: int
    education: dict
