from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True)
class ReniecIdentity:
    first_name: str
    first_last_name: str
    second_last_name: str
    document_number: str


class ReniecIdentityNotFound(ValueError):
    """The DNI has no identity record in the configured provider."""


class ReniecIdentityUnavailable(RuntimeError):
    """The identity provider cannot be used safely at this time."""


class ReniecIdentityVerifier(ABC):
    @abstractmethod
    def find_by_dni(self, dni: str) -> ReniecIdentity:
        pass
