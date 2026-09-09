from abc import ABC, abstractmethod

from app.domain.model.aggregates.user import User
from app.domain.model.commands.change_password_command import (
    ChangePasswordCommand,
)
from app.domain.model.commands.update_profile_command import (
    UpdateProfileCommand,
)


class ProfileCommandService(ABC):

    @abstractmethod
    def handle_update_profile(
        self,
        command: UpdateProfileCommand
    ) -> User:
        pass

    @abstractmethod
    def handle_change_password(
        self,
        command: ChangePasswordCommand
    ) -> User:
        pass