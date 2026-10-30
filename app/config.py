import os
import re
from dataclasses import dataclass
from functools import lru_cache


@dataclass(frozen=True)
class Settings:
    internal_api_key: str
    database_schema: str


@lru_cache
def get_settings() -> Settings:
    internal_api_key = os.getenv("INTERNAL_API_KEY", "").strip()
    if not internal_api_key:
        raise RuntimeError("Missing required configuration: INTERNAL_API_KEY")

    database_schema = os.getenv("DATABASE_SCHEMA", "identity").strip()
    if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", database_schema):
        raise RuntimeError("DATABASE_SCHEMA must be a valid PostgreSQL identifier.")

    return Settings(internal_api_key=internal_api_key, database_schema=database_schema)
