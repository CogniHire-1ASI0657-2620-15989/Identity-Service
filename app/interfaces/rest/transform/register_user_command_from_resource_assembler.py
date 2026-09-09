from app.domain.model.commands.register_user_command import (
    RegisterUserCommand,
)
from app.interfaces.rest.resources.register_user_resource import (
    RegisterUserResource,
)


class RegisterUserCommandFromResourceAssembler:

    @staticmethod
    def to_command(
        resource: RegisterUserResource
    ) -> RegisterUserCommand:

        return RegisterUserCommand(
            name=resource.name,
            email=str(resource.email),
            password=resource.password,
            segment=resource.segment,
            city=resource.city,
            country=resource.country,
        )