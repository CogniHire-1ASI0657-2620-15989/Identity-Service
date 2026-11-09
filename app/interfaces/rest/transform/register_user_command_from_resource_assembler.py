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
            dni=resource.dni,
            first_name=resource.first_name,
            first_last_name=resource.first_last_name,
            second_last_name=resource.second_last_name,
            email=str(resource.email),
            password=resource.password,
            segment=resource.segment,
            city=resource.city,
            country=resource.country,
        )
