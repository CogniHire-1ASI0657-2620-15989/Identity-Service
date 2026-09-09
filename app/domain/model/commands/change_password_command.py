from dataclasses import dataclass


@dataclass(frozen=True)
class ChangePasswordCommand:
    user_id: int
    current_password: str
    new_password: str