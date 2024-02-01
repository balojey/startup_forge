from typing import List

from fastapi import APIRouter, HTTPException, status
from fastapi.param_functions import Depends

from startup_forge.db.dao.profile_dao import ProfileDAO
from startup_forge.db.models.users import User, current_active_user
from startup_forge.db.models.profile import Profile
from startup_forge.web.api.profile.schema import (
    ProfileDTO,
    ProfileInputDTO,
    ProfileUpdateDTO,
)
from startup_forge.web.error_message import ErrorMessage

router = APIRouter()


@router.get("/", response_model=ProfileDTO)
async def get_profile(
    user: User = Depends(current_active_user),
    profile_dao: ProfileDAO = Depends(),
) -> Profile:
    """
    Retrieve a profile object from the database.

    :param user: current user.
    :return: profile object from database.
    """
    profile = await profile_dao.get_profile(user.id)
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ErrorMessage.PROFILE_DOES_NOT_EXIST,
        )
    return profile


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_profile(
    profile_object: ProfileInputDTO,
    user: User = Depends(current_active_user),
    profile_dao: ProfileDAO = Depends(),
) -> None:
    """
    Creates profile in the database.

    :param profile_object: new profile item.
    :param profile_dao: DAO for profiles.
    """
    profile = await profile_dao.get_profile(user.id)  # get profile
    if profile:  # check if profile already exists
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=ErrorMessage.PROFILE_ALREADY_EXISTS,
        )
    await profile_dao.create_profile(
        user_id=user.id,
        role=profile_object.role,
        first_name=profile_object.first_name,
        last_name=profile_object.last_name,
    )


@router.patch("/")
async def update_profile(
    profile_object: ProfileUpdateDTO,
    user: User = Depends(current_active_user),
    profile_dao: ProfileDAO = Depends(),
) -> None:
    """
    Updates profile in the database.

    :param profile_object: profile item.
    :param profile_dao: DAO for profiles.
    """
    profile = await profile_dao.get_profile(user.id)  # get profile
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ErrorMessage.PROFILE_DOES_NOT_EXIST,
        )
    await profile_dao.update_profile(
        user_id=user.id,
        role=profile_object.role,
        first_name=profile_object.first_name,
        last_name=profile_object.last_name,
    )
