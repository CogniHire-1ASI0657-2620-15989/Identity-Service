from abc import ABC, abstractmethod

from app.domain.model.aggregates.user import User


class TokenService(ABC):

    @abstractmethod
    def generate(self, user: User) -> str:
        pass

    @abstractmethod
    def decode(self, token: str) -> dict:
        pass