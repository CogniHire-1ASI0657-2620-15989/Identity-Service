from abc import ABC, abstractmethod

from app.domain.model.aggregates.user import User
from app.domain.model.value_objects.email_address import EmailAddress


class UserRepository(ABC):

    @abstractmethod
    def find_by_id(self, user_id: int) -> User | None:
        pass

    @abstractmethod
    def find_by_email(self, email: EmailAddress) -> User | None:
        pass

    @abstractmethod
    def save(self, user: User) -> User:
        pass

    @abstractmethod
    def update(self, user: User) -> User:
        pass

    @abstractmethod
    def delete(self, user: User) -> None:
        pass