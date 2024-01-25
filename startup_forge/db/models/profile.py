from datetime import datetime
from uuid import UUID

from sqlalchemy import ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from sqlalchemy.sql.sqltypes import String, Uuid, DateTime

from startup_forge.db.base import Base
from startup_forge.db.models.options import Role


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
