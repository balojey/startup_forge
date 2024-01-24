from datetime import datetime
from uuid import UUID

from sqlalchemy import ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from sqlalchemy.sql.sqltypes import String, Uuid, DateTime, Text

from startup_forge.db.base import Base
from startup_forge.db.models.base_model import BaseModel
from startup_forge.db.models.options import Role


class MentorMenteeHistory(BaseModel, Base):
    """Model for keeping the history of mentors and mentees relationship"""

    __tablename__ = "mentor_mentee_history"

    mentor_id: Mapped[UUID] = mapped_column(
        Uuid(), ForeignKey("user.id"), nullable=False
    )
    mentee_id: Mapped[UUID] = mapped_column(
        Uuid(), ForeignKey("user.id"), nullable=False
    )
    start_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    end_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=func.now()
    )
    mentee_comment: Mapped[str] = mapped_column(Text(), nullable=True)
    mentor_comment: Mapped[str] = mapped_column(Text(), nullable=True)
    triggered_by: Mapped[Role] = mapped_column(Enum(Role), nullable=False)
