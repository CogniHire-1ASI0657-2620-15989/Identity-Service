from abc import ABC, abstractmethod

from app.domain.model.aggregates.user import User
from app.domain.model.queries.get_current_profile_query import (
    GetCurrentProfileQuery,
)
from app.domain.model.queries.get_user_by_email_query import (
    GetUserByEmailQuery,
)
from app.domain.model.queries.get_user_by_id_query import (
    GetUserByIdQuery,
)


class ProfileQueryService(ABC):

    @abstractmethod
    def handle_get_by_id(
        self,
        query: GetUserByIdQuery
    ) -> User | None:
        pass

    @abstractmethod
    def handle_get_by_email(
        self,
        query: GetUserByEmailQuery
    ) -> User | None:
        pass

    @abstractmethod
    def handle_get_current_profile(
        self,
        query: GetCurrentProfileQuery
    ) -> User | None:
        pass