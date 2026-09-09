from dataclasses import dataclass


@dataclass(frozen=True)
class GetCurrentProfileQuery:
    user_id: int