from app.domain.model.commands.update_profile_command import (
    UpdateProfileCommand,
)
from app.interfaces.rest.resources.update_profile_resource import (
    UpdateProfileResource,
)


class UpdateProfileCommandFromResourceAssembler:

    @staticmethod
    def to_command(
        user_id: int,
        resource: UpdateProfileResource,
    ) -> UpdateProfileCommand:

        return UpdateProfileCommand(
            user_id=user_id,
            name=resource.name,
            email=(
                str(resource.email)
                if resource.email is not None
                else None
            ),
            segment=resource.segment,
            city=resource.city,
            country=resource.country,
            target_position=resource.target_position,
            expected_city=resource.expected_city,
            expected_country=resource.expected_country,
            work_modality=resource.work_modality,
            hard_skills=(
                [skill.model_dump() for skill in resource.hard_skills]
                if resource.hard_skills is not None
                else None
            ),
            soft_skills=(
                [skill.model_dump() for skill in resource.soft_skills]
                if resource.soft_skills is not None
                else None
            ),
            education=(
                [item.model_dump() for item in resource.education]
                if resource.education is not None
                else None
            ),
            experience=(
                [item.model_dump() for item in resource.experience]
                if resource.experience is not None
                else None
            ),
            languages=(
                [item.model_dump() for item in resource.languages]
                if resource.languages is not None
                else None
            ),
            professional_summary=resource.professional_summary,
        )