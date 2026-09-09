from app.domain.model.aggregates.user import User

from app.domain.model.queries.get_user_by_id_query import (
    GetUserByIdQuery,
)
from app.domain.model.queries.get_user_by_email_query import (
    GetUserByEmailQuery,
)
from app.domain.model.queries.get_current_profile_query import (
    GetCurrentProfileQuery,
)

from app.domain.model.value_objects.email_address import EmailAddress

from app.domain.repositories.user_repository import UserRepository

from app.domain.services.profile_query_service import (
    ProfileQueryService,
)


class DefaultProfileQueryService(ProfileQueryService):

    def __init__(
        self,
        user_repository: UserRepository,
    ):
        self._user_repository = user_repository

    def handle_get_by_id(
        self,
        query: GetUserByIdQuery
    ) -> User | None:

        return self._user_repository.find_by_id(
            query.user_id
        )

    def handle_get_by_email(
        self,
        query: GetUserByEmailQuery
    ) -> User | None:

        email = EmailAddress(
            query.email
        )

        return self._user_repository.find_by_email(
            email
        )

    def handle_get_current_profile(
        self,
        query: GetCurrentProfileQuery
    ) -> User | None:

        return self._user_repository.find_by_id(
            query.user_id
        )