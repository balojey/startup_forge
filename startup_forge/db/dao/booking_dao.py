from datetime import date, time
from uuid import UUID
from typing import Optional

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.sql import func
from sqlalchemy.ext.asyncio import AsyncSession

from startup_forge.db.dependencies import get_db_session
from startup_forge.db.models.booking import TimeSlot, Booking, BookingActivity
from startup_forge.db.models.options import Day, BookingStatus, BookingStatus2, Role


class BookingDAO:
    """Class for accessing education table."""

    def __init__(self, session: AsyncSession = Depends(get_db_session)):
        self.session = session

    async def create_time_slot(
        self,
        user_id: UUID,
        day: Day,
        start_time: time,
        end_time: time,
    ) -> None:
        """
        Add single time_slot to session.

        :param user_id: id of the user registering the time_slot.
        :param day: day of the week.
        :param start_time: start time.
        :param end_time: end time.
        """
        self.session.add(
            TimeSlot(
                user_id=user_id,
                day=day,
                start_time=start_time,
                end_time=end_time,
            )
        )

    async def get_time_slot(
        self,
        user_id: UUID,
        day: Day,
        start_time: time,
        end_time: time,
    ) -> TimeSlot | None:
        """
        Get a stream of connection requests education.

        :param user_id: id of the user.
        :param day: day of the week.
        :param start_time: start time.
        :param end_time: end time.
        :return: a TimeSlot.
        """
        result = await self.session.execute(
            select(TimeSlot).where(
                TimeSlot.user_id == user_id
                and TimeSlot.start_time == start_time
                and TimeSlot.end_time == end_time
                and TimeSlot.day == day
            ),
        )

        return result.scalars().first()

    async def get_time_slots(
        self,
        user_id: UUID,
    ) -> TimeSlot | None:
        """
        Get a stream of connection requests education.

        :param user_id: id of the user.
        :return: a stream of TimeSlot.
        """
        results = await self.session.execute(
            select(TimeSlot).where(TimeSlot.user_id == user_id),
        )

        return list(results.scalars().fetchall())

    async def update_time_slot(
        self,
        time_slot_id: UUID,
        day: Day,
        start_time: time,
        end_time: time,
    ) -> TimeSlot | None:
        """
        Get a stream of connection requests education.

        :param time_slot_id: id of the time_slot.
        :param day: day of the week.
        :param start_time: start time.
        :param end_time: end time.
        :return: a TimeSlot.
        """
        time_slot = await self.get_time_slot_by_id(time_slot_id=time_slot_id)

        # edit time_slot
        time_slot.day = day if day else time_slot.day
        time_slot.start_time = start_time if start_time else time_slot.start_time
        time_slot.end_time = end_time if end_time else time_slot.end_time

        # save
        time_slot.updated_at = func.now()
        self.session.add(time_slot)

    async def get_time_slot_by_id(
        self,
        time_slot_id: UUID,
    ) -> TimeSlot | None:
        """
        Get a time_slot.

        :param time_slot_id: id of the time_slot.
        :return: a time_slot.
        """
        request = await self.session.execute(
            select(TimeSlot).where(TimeSlot.id == time_slot_id),
        )

        return request.scalars().first()

    async def delete_time_slot(
        self,
        time_slot_id: UUID,
    ) -> TimeSlot | None:
        """
        Delete a time_slot.

        :param time_slot_id: id of the time_slot.
        """
        time_slot = await self.get_time_slot_by_id(time_slot_id=time_slot_id)
        await self.session.delete(time_slot)

    async def create_booking(
        self,
        user_id: UUID,
        time_slot_id: UUID,
        date: date,
    ) -> None:
        """
        Create a booking.

        :param user_id: id of the user.
        :param time_slot_id: id of the time_slot.
        :param date: date of booking.
        """
        await self.session.add(
            Booking(
                user_id=user_id,
                time_slot_id=time_slot_id,
                date=date,
            )
        )

    async def update_booking(
        self,
        booking_id: UUID,
        date: date,
        user_role: Role,
    ) -> None:
        """
        Update a booking.

        :param booking_id: id of the booking.
        :param date: date of booking.
        """
        booking = await self.get_booking_by_id(booking_id=booking_id)

        if date == booking.date:
            return
        # edit booking
        booking.date = date if date else booking.date
        if user_role == Role.MENTEE:
            booking.booking_activity.mentee_activity = BookingStatus.RESCHEDULED
        else:
            booking.booking_activity.mentor_activity = BookingStatus.RESCHEDULED

        # save
        booking.updated_at = func.now()
        self.session.add(booking)

    async def get_booking_by_id(
        self,
        booking_id: UUID,
    ) -> Booking | None:
        """
        Get a booking by id.

        :param booking_id: id of the booking.
        :return: a booking.
        """
        booking = await self.session.execute(
            select(Booking).where(Booking.id == booking_id)
        )
        return booking.scalars().first()

    async def get_booking(
        self,
        user_id: UUID,
        time_slot_id: UUID,
        date: date,
    ) -> Booking | None:
        """
        Get a booking.

        :param user_id: user id.
        :param time_slot_id: id of the time_slot.
        :param date: date.
        :return: a booking.
        """
        booking = await self.session.execute(
            select(Booking).where(
                Booking.user_id == user_id
                and Booking.time_slot_id == time_slot_id
                and Booking.date == date
            )
        )
        return booking.scalars().first()

    async def available(
        self,
        time_slot_id: UUID,
        date: date,
    ) -> Booking | None:
        """
        Get a booking.

        :param time_slot_id: id of the time_slot.
        :param date: date.
        :return: a booking.
        """
        results = await self.session.execute(
            select(Booking).where(
                Booking.time_slot_id == time_slot_id and Booking.date == date
            )
        )
        if results.scalars().fetchall().count() == 3:
            return False
        return True

    async def get_bookings(
        self,
        user_id: UUID,
    ) -> list[Booking] | None:
        """
        Get a bookings.

        :param user_id: id of the user.
        :return: a bookings.
        """
        booking = await self.session.execute(
            select(Booking).where(
                Booking.user_id == user_id or Booking.time_slot.user_id == user_id
            )
        )
        return list(booking.scalars().fetchall())

    async def delete_booking(
        self,
        booking_id: UUID,
    ) -> None:
        """
        Delete a booking.

        :param booking_id: id of the booking.
        """
        booking = await self.get_booking_by_id(booking_id=booking_id)
        await self.session.delete(booking)

    async def update_booking_status(
        self, booking_id: UUID, role: Role, status: BookingStatus2
    ) -> None:
        """
        Update a booking.

        :param booking_id: id of the booking.
        :param role: user role.
        :param status: booking status.
        """
        booking = await self.get_booking_by_id(booking_id=booking_id)

        # edit status
        if role == Role.MENTEE:
            booking.booking_activity.mentee_activity = status
        else:
            booking.booking_activity.mentor_activity = status

        # save
        booking.updated_at = func.now()
        self.session.add(booking)

    async def get_sessions(self, user_id: UUID) -> None:
        """
        Get the total number of completed sessions.

        :param user_id: id of the user.
        :return: total number of completed sessions.
        """
        bookings = await self.session.execute(
            select(Booking).where(
                (Booking.user_id == user_id or Booking.time_slot.user_id == user_id)
                and (
                    Booking.booking_activity.mentor_activity == BookingStatus2.COMPLETED
                    or Booking.booking_activity.mentee_activity
                    == BookingStatus2.COMPLETED
                )
            )
        )

        return bookings.scalars().fetchall().count()

    async def get_available_sessions(
        self, user_id: UUID
    ) -> list[tuple[Day, date, time]]:
        """
        Get mentor's available sessions.

        :param user_id: id of the user.
        :return: tuples of available days, dates and times.
        """
