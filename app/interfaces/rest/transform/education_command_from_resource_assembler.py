from app.domain.model.commands.add_education_command import AddEducationCommand
from app.domain.model.commands.remove_education_command import RemoveEducationCommand
from app.domain.model.commands.update_education_command import UpdateEducationCommand
from app.interfaces.rest.resources.professional_resources import EducationInputResource


class EducationCommandFromResourceAssembler:
    @staticmethod
    def to_add_command(user_id: int, resource: EducationInputResource) -> AddEducationCommand:
        return AddEducationCommand(user_id=user_id, education=resource.model_dump())

    @staticmethod
    def to_update_command(user_id: int, education_id: str, resource: EducationInputResource) -> UpdateEducationCommand:
        return UpdateEducationCommand(user_id=user_id, education_id=education_id, education=resource.model_dump())

    @staticmethod
    def to_remove_command(user_id: int, education_id: str) -> RemoveEducationCommand:
        return RemoveEducationCommand(user_id=user_id, education_id=education_id)
