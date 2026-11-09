from app.domain.model.commands.add_experience_command import AddExperienceCommand
from app.interfaces.rest.resources.professional_resources import ExperienceInputResource


class ExperienceCommandFromResourceAssembler:
    @staticmethod
    def to_add_command(user_id: int, resource: ExperienceInputResource) -> AddExperienceCommand:
        return AddExperienceCommand(user_id=user_id, experience=resource.model_dump())
