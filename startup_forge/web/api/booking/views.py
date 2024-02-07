from typing import Optional

from fastapi import APIRouter, HTTPException, status
from fastapi.param_functions import Depends

from startup_forge.db.dao.profile_dao import ProfileDAO
from startup_forge.db.dao.booking_dao import BookingDAO
from startup_forge.db.models.users import User, current_active_user
from startup_forge.db.models.booking import Booking, BookingActivity, TimeSlot
from startup_forge.web.api.booking.schema import *
from startup_forge.web.error_message import BookingErrorDetails, ProfileErrorDetails
from startup_forge.db.models.options import Role

router = APIRouter()


@router.get("/timeslots", response_model=list[TimeSlotDTO])
async def get_time_slots(
    user: User = Depends(current_active_user),
    user_id: Optional[UUID] = None,
    profile_dao: ProfileDAO = Depends(),
    booking_dao: BookingDAO = Depends(),
) -> list[TimeSlot]:
    """
    Retrieve time_slot objects from the database.

    :param user: current user.
    :param user_id: user id.
    :return: profile object from database.
    """
    profile = await profile_dao.get_profile(user.id)  # get profile
    if not profile:  # check if profile already exists
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ProfileErrorDetails.PROFILE_ALREADY_EXISTS,
        )
    if profile.role != Role.MENTOR:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ProfileErrorDetails.PROFILE_ROLE_NOT_MENTOR,
        )
    await booking_dao.get_time_slots(user_id=user.id if not user_id else user_id)


@router.post("/timeslots", status_code=status.HTTP_201_CREATED)
async def create_timeslot(
    time_slot_object: TimeSlotDTO,
    user: User = Depends(current_active_user),
    profile_dao: ProfileDAO = Depends(),
    booking_dao: BookingDAO = Depends(),
) -> None:
    """
    Creates timeslot in the database.

    :param user: current user.
    :param time_slot_object: new time_slot item.
    :param profile_dao: DAO for profiles.
    :param booking_dao: DAO for bookings.
    """
    profile = await profile_dao.get_profile(user.id)  # get profile
    if not profile:  # check if profile already exists
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ProfileErrorDetails.PROFILE_ALREADY_EXISTS,
        )
    if profile.role != Role.MENTOR:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ProfileErrorDetails.PROFILE_ROLE_NOT_MENTOR,
        )
    time_slot = await booking_dao.get_time_slot(
        user_id=user.id,
        day=time_slot_object.day,
        start_time=time_slot_object.start_time,
        end_time=time_slot_object.end_time,
    )
    if time_slot:
        return
    await booking_dao.create_time_slot(
        user_id=user.id,
        day=time_slot_object.day,
        start_time=time_slot_object.start_time,
        end_time=time_slot_object.end_time,
    )


@router.patch("/timeslots/{time_slot_id}", status_code=status.HTTP_201_CREATED)
async def update_timeslot(
    time_slot_object: TimeSlotDTO,
    time_slot_id: UUID,
    user: User = Depends(current_active_user),
    profile_dao: ProfileDAO = Depends(),
    booking_dao: BookingDAO = Depends(),
) -> None:
    """
    Updates timeslot in the database.

    :param user: current user.
    :param time_slot_id: time_slot id.
    :param time_slot_object: new time_slot item.
    :param profile_dao: DAO for profiles.
    :param booking_dao: DAO for bookings.
    """
    profile = await profile_dao.get_profile(user.id)  # get profile
    if not profile:  # check if profile already exists
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ProfileErrorDetails.PROFILE_DOES_NOT_EXIST,
        )
    if profile.role != Role.MENTOR:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ProfileErrorDetails.PROFILE_ROLE_NOT_MENTOR,
        )
    time_slot = await booking_dao.get_time_slot_by_id(time_slot_id=time_slot_id)
    if not time_slot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=BookingErrorDetails.TIME_SLOT_NOT_FOUND,
        )
    if user.id != time_slot.user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=ProfileErrorDetails.UNAUTHORIZED,
        )
    await booking_dao.update_time_slot(
        time_slot_id=time_slot_id,
        day=time_slot_object.day,
        start_time=time_slot_object.start_time,
        end_time=time_slot_object.end_time,
    )


@router.delete("/timeslots/{time_slot_id}", status_code=status.HTTP_201_CREATED)
async def delete_timeslot(
    time_slot_id: UUID,
    user: User = Depends(current_active_user),
    profile_dao: ProfileDAO = Depends(),
    booking_dao: BookingDAO = Depends(),
) -> None:
    """
    Updates timeslot in the database.

    :param user: current user.
    :param time_slot_id: time_slot id.
    :param profile_dao: DAO for profiles.
    :param booking_dao: DAO for bookings.
    """
    profile = await profile_dao.get_profile(user.id)  # get profile
    if not profile:  # check if profile already exists
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ProfileErrorDetails.PROFILE_DOES_NOT_EXIST,
        )
    if profile.role != Role.MENTOR:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ProfileErrorDetails.PROFILE_ROLE_NOT_MENTOR,
        )
    time_slot = await booking_dao.get_time_slot_by_id(time_slot_id=time_slot_id)
    if not time_slot:
        return
    if user.id != time_slot.user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=ProfileErrorDetails.UNAUTHORIZED,
        )
    await booking_dao.delete_time_slot(
        time_slot_id=time_slot_id,
    )


@router.post("/timeslots/{time_slot_id}/bookings", status_code=status.HTTP_201_CREATED)
async def book(
    time_slot_id: UUID,
    booking_object: BookingInputDTO,
    user: User = Depends(current_active_user),
    profile_dao: ProfileDAO = Depends(),
    booking_dao: BookingDAO = Depends(),
) -> None:
    """
    Create a booking in the database.

    :param user: current user.
    :param time_slot_id: time_slot id.
    :param booking_object: booking object.
    :param profile_dao: DAO for profiles.
    :param booking_dao: DAO for bookings.
    """
    profile = await profile_dao.get_profile(user.id)  # get profile
    if not profile:  # check if profile already exists
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ProfileErrorDetails.PROFILE_DOES_NOT_EXIST,
        )
    if profile.role != Role.MENTEE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ProfileErrorDetails.PROFILE_ROLE_NOT_MENTEE,
        )
    time_slot = await booking_dao.get_time_slot_by_id(time_slot_id=time_slot_id)
    if not time_slot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=BookingErrorDetails.INVALID_TIME_SLOT,
        )
    booking = await booking_dao.get_booking(
        user_id=user.id,
        time_slot_id=time_slot_id,
        date=booking_object.date,
    )
    if booking:
        return
    if booking_dao.available(time_slot_id=time_slot_id, date=booking_object.date):
        await booking_dao.create_booking(
            user_id=user.id,
            time_slot_id=time_slot_id,
            date=booking_object.date,
        )
        return
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=BookingErrorDetails.TIMESLOT_OCCUPIED_FOR_THE_SPECIFIED_DATE,
    )


@router.patch("/bookings/{booking_id}")
async def update_booking(
    booking_id: UUID,
    booking_object: BookingUpdateDTO,
    user: User = Depends(current_active_user),
    profile_dao: ProfileDAO = Depends(),
    booking_dao: BookingDAO = Depends(),
) -> None:
    """
    Update a booking in the database.

    :param user: current user.
    :param booking_id: booking id.
    :param booking_object: booking object.
    :param profile_dao: DAO for profiles.
    :param booking_dao: DAO for bookings.
    """
    profile = await profile_dao.get_profile(user.id)  # get profile
    if not profile:  # check if profile already exists
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ProfileErrorDetails.PROFILE_DOES_NOT_EXIST,
        )
    booking = await booking_dao.get_booking_by_id(
        booking_id=booking_id,
    )
    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=BookingErrorDetails.BOOKING_NOT_FOUND,
        )
    if booking.user_id != user.id or booking.time_slot.user_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=BookingErrorDetails.BOOKING_NOT_MADE_BY_CURRENT_USER,
        )
    # check date availability
    if not await booking_dao.available(booking.time_slot_id, booking_object.date):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=BookingErrorDetails.TIMESLOT_OCCUPIED_FOR_THE_SPECIFIED_DATE,
        )
    await booking_dao.update_booking(booking.id, booking_object.date, profile.role)


@router.get("/bookings")
async def get_bookings(
    user: User = Depends(current_active_user),
    profile_dao: ProfileDAO = Depends(),
    booking_dao: BookingDAO = Depends(),
) -> list[BookingDTO] | None:
    """
    Get bookings.

    :param user: current user.
    :param profile_dao: DAO for profiles.
    :param booking_dao: DAO for bookings.
    """
    profile = await profile_dao.get_profile(user.id)  # get profile
    if not profile:  # check if profile already exists
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ProfileErrorDetails.PROFILE_DOES_NOT_EXIST,
        )
    return await booking_dao.get_bookings(
        user_id=user.id,
    )


@router.patch("/bookings/{booking_id}/status")
async def change_booking_status(
    booking_id: UUID,
    booking_status_object: BookingStatusDTO,
    user: User = Depends(current_active_user),
    profile_dao: ProfileDAO = Depends(),
    booking_dao: BookingDAO = Depends(),
) -> None:
    """
    Update booking's status.

    :param booking_id: booking id.
    :param booking_status_object: booking status object.
    :param user: current user.
    :param profile_dao: DAO for profiles.
    :param booking_dao: DAO for bookings.
    """
    profile = await profile_dao.get_profile(user.id)  # get profile
    if not profile:  # check if profile already exists
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ProfileErrorDetails.PROFILE_DOES_NOT_EXIST,
        )
    booking = await booking_dao.get_booking_by_id(
        booking_id=booking_id,
    )
    if booking.user_id != user.id or booking.time_slot.user_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=BookingErrorDetails.BOOKING_NOT_MADE_BY_CURRENT_USER,
        )
    await booking_dao.update_booking_status(
        booking.id, profile.role, booking_status_object.status
    )


@router.get("/sessions/")
async def sessions(
    user_id: Optional[UUID] = None,
    user: User = Depends(current_active_user),
    profile_dao: ProfileDAO = Depends(),
    booking_dao: BookingDAO = Depends(),
) -> int | None:
    """
    Get sessions.

    :param user_id: user id.
    :param user: current user.
    :param profile_dao: DAO for profiles.
    :param booking_dao: DAO for bookings.
    """
    profile = await profile_dao.get_profile(
        user.id if not user_id else user_id
    )  # get profile
    if not profile:  # check if profile already exists
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ProfileErrorDetails.PROFILE_DOES_NOT_EXIST,
        )
    return await booking_dao.get_sessions(profile.user_id)
