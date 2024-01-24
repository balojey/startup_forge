from datetime import datetime
from uuid import UUID

from sqlalchemy import PrimaryKeyConstraint, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from sqlalchemy.sql.sqltypes import String, Uuid, DateTime

from startup_forge.db.base import Base


class MentorMentee(Base):
    """Model for mentor and mentee relationship"""

    __tablename__ = "mentor_mentee"

    mentor_id: Mapped[UUID] = mapped_column(Uuid(), nullable=False)
    mentee_id: Mapped[UUID] = mapped_column(Uuid(), nullable=False)
    start_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=func.now()
    )

    PrimaryKeyConstraint(mentor_id, mentee_id)
    UniqueConstraint(mentor_id, mentee_id)
