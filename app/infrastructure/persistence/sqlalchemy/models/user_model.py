from datetime import datetime

from sqlalchemy import DateTime, Integer, JSON, String
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.persistence.sqlalchemy.configuration.database import Base


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    email: Mapped[str] = mapped_column(
        String(256),
        unique=True,
        nullable=False,
        index=True,
    )

    password_hash: Mapped[str] = mapped_column(
        String(512),
        nullable=False,
    )

    segment: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    city: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    country: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    target_position: Mapped[str | None] = mapped_column(String(150), nullable=True)
    expected_city: Mapped[str | None] = mapped_column(String(100), nullable=True)
    expected_country: Mapped[str | None] = mapped_column(String(100), nullable=True)
    work_modality: Mapped[str | None] = mapped_column(String(20), nullable=True)
    hard_skills: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    soft_skills: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    education: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    experience: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    languages: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    professional_summary: Mapped[str | None] = mapped_column(String(2000), nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
    )