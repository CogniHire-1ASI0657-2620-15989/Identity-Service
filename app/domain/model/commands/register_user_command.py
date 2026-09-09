from dataclasses import dataclass


@dataclass(frozen=True)
class RegisterUserCommand:
    name: str
    email: str
    password: str
    segment: str
    city: str | None = None
    country: str | None = None