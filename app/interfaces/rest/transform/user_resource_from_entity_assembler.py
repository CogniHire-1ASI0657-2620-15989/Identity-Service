from app.domain.model.aggregates.user import User
from app.interfaces.rest.resources.user_resource import (
    UserResource,
)


class UserResourceFromEntityAssembler:

    @staticmethod
    def to_resource(
        user: User
    ) -> UserResource:

        return UserResource(
            id=user.id,
            name=user.name.value,
            email=user.email.value,
            segment=user.segment.value,
            city=(
                user.location.city
                if user.location
                else None
            ),
            country=(
                user.location.country
                if user.location
                else None
            ),
            target_position=user.target_position,
            expected_city=user.expected_city,
            expected_country=user.expected_country,
            work_modality=user.work_modality,
            hard_skills=user.hard_skills,
            soft_skills=user.soft_skills,
            education=user.education,
            experience=user.experience,
            languages=user.languages,
            professional_summary=user.professional_summary,
            created_at=user.created_at,
        )