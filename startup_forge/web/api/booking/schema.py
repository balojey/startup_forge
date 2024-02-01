from datetime import time, date
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from startup_forge.db.models.options import Day, BookingStatus2


class TimeSlotDTO(BaseModel):
    """
    DTO for time_slot.

    It is returned when accessing time_slot from the API.
    """

    day: Day
    start_time: time
    end_time: time
    model_config = ConfigDict(from_attributes=True)


class BookingInputDTO(BaseModel):
    """DTO for creating a booking"""

    date: date


class BookingInputDTO(BookingInputDTO):
    """DTO for updating a booking"""

    pass


class BookingDTO(BookingInputDTO):
    """
    DTO for booking.

    It is returned when accessing booking from the API.
    """

    day: Day
    user_id: UUID
    time_slot_id: UUID
    model_config = ConfigDict(from_attributes=True)


class BookingStatusDTO(BaseModel):
    """DTO for updating a booking's status"""

    status: BookingStatus2
