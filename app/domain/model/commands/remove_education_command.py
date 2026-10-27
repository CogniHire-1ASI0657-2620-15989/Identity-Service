from dataclasses import dataclass


@dataclass(frozen=True)
class RemoveEducationCommand:
    user_id: int
    education_id: str
