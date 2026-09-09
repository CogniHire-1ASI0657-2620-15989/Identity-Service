from app.domain.model.commands.change_password_command import (
    ChangePasswordCommand,
)
from app.interfaces.rest.resources.change_password_resource import (
    ChangePasswordResource,
)


class ChangePasswordCommandFromResourceAssembler:

    @staticmethod
    def to_command(
        user_id: int,
        resource: ChangePasswordResource,
    ) -> ChangePasswordCommand:

        return ChangePasswordCommand(
            user_id=user_id,
            current_password=resource.current_password,
            new_password=resource.new_password,
        )