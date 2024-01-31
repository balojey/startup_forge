from datetime import datetime
from uuid import UUID

from sqlalchemy import ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from sqlalchemy.sql.sqltypes import String, Uuid, DateTime, Text, ARRAY

from startup_forge.db.base import Base
from startup_forge.db.models.base_model import BaseModel
from startup_forge.db.models.options import (
    Role,
    ExpertiseName,
    SkillName,
    LanguageLevel,
    LanguageName,
    Platform,
)


class Profile(Base):
    """Model for profile."""

    __tablename__ = "profile"

    first_name: Mapped[str] = mapped_column(String(length=150))
    last_name: Mapped[str] = mapped_column(String(length=150))
    user_id: Mapped[UUID] = mapped_column(
        Uuid(),
        ForeignKey("user.id", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True,
    )
    role: Mapped[Role] = mapped_column(Enum(Role), default=Role.MENTEE)
    years_of_experience: Mapped[str] = mapped_column(String(length=150), nullable=True)
    bio: Mapped[str] = mapped_column(Text(), nullable=True)
    expertises: Mapped[list[ExpertiseName]] = mapped_column(
        ARRAY(String), nullable=True
    )
    skills: Mapped[list[SkillName]] = mapped_column(ARRAY(String), nullable=True)
    profile_picture_url: Mapped[str] = mapped_column(String(length=100), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    def is_mentee(self) -> bool:
        """Check if profile has a mentee role"""
        return self.role == Role.MENTEE

    def is_mentor(self) -> bool:
        """Check if profile has a mentor role"""
        return self.role == Role.MENTOR


class SocialLink(BaseModel, Base):
    """Model for social links"""

    __tablename__ = "social_link"

    user_id: Mapped[UUID] = mapped_column(
        Uuid(),
        ForeignKey("user.id", ondelete="CASCADE", onupdate="CASCADE"),
    )
    platform: Mapped[Platform] = mapped_column(Enum(Platform))
    link: Mapped[str] = mapped_column(String(length=150))


class Language(BaseModel, Base):
    """Model for languages"""

    __tablename__ = "language"

    user_id: Mapped[UUID] = mapped_column(
        Uuid(),
        ForeignKey("user.id", ondelete="CASCADE", onupdate="CASCADE"),
    )
    name: Mapped[LanguageName] = mapped_column(Enum(LanguageName))
    level: Mapped[LanguageLevel] = mapped_column(Enum(LanguageLevel))
