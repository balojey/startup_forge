from datetime import date
from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql.sqltypes import String, Uuid, Date

from startup_forge.db.base import Base
from startup_forge.db.models.base_model import BaseModel


class Education(BaseModel, Base):
    """Model for education."""

    __tablename__ = "education"

    user_id: Mapped[UUID] = mapped_column(
        Uuid(),
        ForeignKey("user.id", ondelete="CASCADE", onupdate="CASCADE"),
    )
    institution_name: Mapped[str] = mapped_column(String(length=150))
    course_of_study: Mapped[str] = mapped_column(String(length=150))
    start_date: Mapped[date] = mapped_column(Date())
    end_date: Mapped[date] = mapped_column(Date(), nullable=True)
    state: Mapped[str] = mapped_column(String(length=150))
    country: Mapped[str] = mapped_column(String(length=150))
