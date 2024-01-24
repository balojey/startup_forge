from datetime import date
from uuid import UUID

from sqlalchemy import Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql.sqltypes import String, Uuid, Text, Date

from startup_forge.db.base import Base
from startup_forge.db.models.base_model import BaseModel
from startup_forge.db.models.options import Industry


class Experience(BaseModel, Base):
    """Model for experience."""

    __tablename__ = "experience"

    user_id: Mapped[UUID] = mapped_column(Uuid(), ForeignKey("user.id"))
    company_name: Mapped[str] = mapped_column(String(), nullable=False)
    description: Mapped[str] = mapped_column(Text(), nullable=True)
    start_date: Mapped[date] = mapped_column(Date(), nullable=False)
    end_date: Mapped[date] = mapped_column(Date(), nullable=True)
    industry: Mapped[Industry] = mapped_column(Enum(Industry), nullable=False)
