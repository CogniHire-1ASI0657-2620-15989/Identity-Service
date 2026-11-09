from dataclasses import dataclass


@dataclass(frozen=True)
class RegisterUserCommand:
    dni: str
    first_name: str
    first_last_name: str
    second_last_name: str
    email: str
    password: str
    segment: str
    city: str | None = None
    country: str | None = None
