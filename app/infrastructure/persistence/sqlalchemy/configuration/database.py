import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import (
    declarative_base,
    sessionmaker,
)


load_dotenv()


DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg://postgre:12345678@localhost:5432/identity_db"
)


engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
)


SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


Base = declarative_base()


def initialize_database() -> None:
    Base.metadata.create_all(bind=engine)

    columns = {
        "target_position": "VARCHAR(150)",
        "expected_city": "VARCHAR(100)",
        "expected_country": "VARCHAR(100)",
        "work_modality": "VARCHAR(20)",
        "hard_skills": "JSON NOT NULL DEFAULT '[]'",
        "soft_skills": "JSON NOT NULL DEFAULT '[]'",
        "education": "JSON NOT NULL DEFAULT '[]'",
        "experience": "JSON NOT NULL DEFAULT '[]'",
        "languages": "JSON NOT NULL DEFAULT '[]'",
        "professional_summary": "VARCHAR(2000)",
    }

    with engine.begin() as connection:
        for name, definition in columns.items():
            connection.execute(
                text(
                    f"ALTER TABLE users ADD COLUMN IF NOT EXISTS "
                    f"{name} {definition}"
                )
            )


def get_db():
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()