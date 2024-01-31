from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql.sqltypes import Uuid, Text

from startup_forge.db.base import Base
from startup_forge.db.models.base_model import BaseModel


class Review(BaseModel, Base):
    """Model for review."""

    __tablename__ = "review"

    mentee_id: Mapped[UUID] = mapped_column(
        Uuid(),
        ForeignKey("user.id", ondelete="CASCADE", onupdate="CASCADE"),
    )
    mentor_id: Mapped[UUID] = mapped_column(
        Uuid(),
        ForeignKey("user.id", ondelete="CASCADE", onupdate="CASCADE"),
    )
    content: Mapped[str] = mapped_column(Text())
