from abc import ABC, abstractmethod
from typing import Any

from app.domain.model.aggregates.user import User
from app.domain.model.commands.authenticate_user_command import (
    AuthenticateUserCommand,
)
from app.domain.model.commands.register_user_command import (
    RegisterUserCommand,
)


class AuthCommandService(ABC):

    @abstractmethod
    def handle_register(
        self,
        command: RegisterUserCommand
    ) -> User:
        pass

    @abstractmethod
    def handle_authenticate(
        self,
        command: AuthenticateUserCommand
    ) -> Any:
        pass