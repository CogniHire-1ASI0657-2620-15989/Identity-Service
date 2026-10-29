from abc import ABC, abstractmethod

from app.domain.model.aggregates.user import User
from app.domain.model.commands.change_password_command import (
    ChangePasswordCommand,
)
from app.domain.model.commands.update_profile_command import (
    UpdateProfileCommand,
)
from app.domain.model.commands.add_education_command import AddEducationCommand
from app.domain.model.commands.update_education_command import UpdateEducationCommand
from app.domain.model.commands.remove_education_command import RemoveEducationCommand


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

    @abstractmethod
    def handle_ensure_verified_hard_skill(self, user_id: int, skill_name: str) -> User:
        pass

    @abstractmethod
    def handle_add_education(self, command: AddEducationCommand) -> User:
        pass

    @abstractmethod
    def handle_update_education(self, command: UpdateEducationCommand) -> User:
        pass

    @abstractmethod
    def handle_remove_education(self, command: RemoveEducationCommand) -> User:
        pass
