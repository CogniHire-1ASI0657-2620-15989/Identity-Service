from app.domain.model.commands.authenticate_user_command import (
    AuthenticateUserCommand,
)
from app.interfaces.rest.resources.login_resource import (
    LoginResource,
)


class AuthenticateUserCommandFromResourceAssembler:

    @staticmethod
    def to_command(
        resource: LoginResource
    ) -> AuthenticateUserCommand:

        return AuthenticateUserCommand(
            email=str(resource.email),
            password=resource.password,
        )