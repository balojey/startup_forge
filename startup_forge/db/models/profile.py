from uuid import UUID

from sqlalchemy import ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql.sqltypes import String, Uuid

from startup_forge.db.base import Base
from startup_forge.db.models.options import Role


class Profile(Base):
    """Model for profile."""

    __tablename__ = "profile"

    first_name: Mapped[str] = mapped_column(String(length=150))
    last_name: Mapped[str] = mapped_column(String(length=150))
    user_id: Mapped[UUID] = mapped_column(
        Uuid(), ForeignKey("user.id"), primary_key=True
    )
    role: Mapped[Role] = mapped_column(Enum(Role), default=Role.MENTEE)
