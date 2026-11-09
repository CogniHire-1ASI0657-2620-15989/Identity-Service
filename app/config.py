import os
import re
from dataclasses import dataclass
from functools import lru_cache


@dataclass(frozen=True)
class Settings:
    internal_api_key: str
    database_schema: str
    decolecta_base_url: str
    decolecta_api_key: str
    decolecta_timeout_seconds: float


@lru_cache
def get_settings() -> Settings:
    internal_api_key = os.getenv("INTERNAL_API_KEY", "").strip()
    if not internal_api_key:
        raise RuntimeError("Missing required configuration: INTERNAL_API_KEY")

    decolecta_base_url = os.getenv("DECOLECTA_BASE_URL", "").strip().rstrip("/")
    decolecta_api_key = os.getenv("DECOLECTA_API_KEY", "").strip()
    if not decolecta_base_url or not decolecta_api_key:
        raise RuntimeError("Missing required configuration: DECOLECTA_BASE_URL, DECOLECTA_API_KEY")
    try:
        decolecta_timeout_seconds = float(os.getenv("DECOLECTA_TIMEOUT_SECONDS", "3"))
    except ValueError as exc:
        raise RuntimeError("DECOLECTA_TIMEOUT_SECONDS must be a positive number.") from exc
    if decolecta_timeout_seconds <= 0:
        raise RuntimeError("DECOLECTA_TIMEOUT_SECONDS must be a positive number.")

    database_schema = os.getenv("DATABASE_SCHEMA", "identity").strip()
    if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", database_schema):
        raise RuntimeError("DATABASE_SCHEMA must be a valid PostgreSQL identifier.")

    return Settings(
        internal_api_key=internal_api_key,
        database_schema=database_schema,
        decolecta_base_url=decolecta_base_url,
        decolecta_api_key=decolecta_api_key,
        decolecta_timeout_seconds=decolecta_timeout_seconds,
    )
