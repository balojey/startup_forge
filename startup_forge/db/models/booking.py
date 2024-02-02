from datetime import time
from uuid import UUID

from sqlalchemy import ForeignKey, Enum, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.sqltypes import Uuid, Time, Date

from startup_forge.db.base import Base
from startup_forge.db.models.base_model import BaseModel
from startup_forge.db.models.options import Day, BookingStatus


class TimeSlot(BaseModel, Base):
    """Model for time slot."""

    __tablename__ = "time_slot"

    user_id: Mapped[UUID] = mapped_column(
        Uuid(), ForeignKey("user.id", ondelete="CASCADE", onupdate="CASCADE")
    )
    day: Mapped[Day] = mapped_column(Enum(Day), nullable=False)
    start_time: Mapped[time] = mapped_column(Time(timezone=True), nullable=False)
    end_time: Mapped[time] = mapped_column(Time(timezone=True), nullable=False)

    bookings: Mapped[list["Booking"]] = relationship(
        "Booking", back_populates="time_slot"
    )

    UniqueConstraint(user_id, day, start_time, end_time)


class Booking(BaseModel, Base):
    """Model for booking."""

    __tablename__ = "booking"

    user_id: Mapped[UUID] = mapped_column(
        Uuid(), ForeignKey("user.id", ondelete="CASCADE", onupdate="CASCADE")
    )
    time_slot_id: Mapped[UUID] = mapped_column(
        Uuid(), ForeignKey("time_slot.id", ondelete="CASCADE", onupdate="CASCADE")
    )
    date: Mapped[date] = mapped_column(Date(), nullable=False)

    time_slot: Mapped[TimeSlot] = relationship("TimeSlot", back_populates="booking")
    booking_activity: Mapped["BookingActivity"] = relationship(
        "BookingActivity", back_populates="booking"
    )

    UniqueConstraint(user_id, time_slot_id, date)


class BookingActivity(Base):
    """Model for booking activity."""

    __tablename__ = "booking_activity"

    mentor_activity: Mapped[BookingStatus] = mapped_column(Enum(BookingStatus))
    mentee_activity: Mapped[BookingStatus] = mapped_column(
        Enum(BookingStatus), nullable=True
    )
    booking_id: Mapped[UUID] = mapped_column(
        Uuid(),
        ForeignKey("booking.id", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True,
    )

    booking: Mapped[Booking] = relationship(
        "Booking", back_populates="booking_activity"
    )
