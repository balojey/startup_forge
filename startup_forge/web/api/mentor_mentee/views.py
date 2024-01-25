from typing import List

from fastapi import APIRouter, HTTPException, status
from fastapi.param_functions import Depends

from startup_forge.db.dao.profile_dao import ProfileDAO
from startup_forge.db.dao.mentor_mentee_dao import MentorMenteeDAO
from startup_forge.db.models.users import User, current_active_user
from startup_forge.db.models.mentor_mentee import MentorMentee
from startup_forge.db.models.profile import Profile
from startup_forge.web.api.mentor_mentee.schema import (
    MentorMenteeDTO,
    MentorMenteeInputDTO,
    MentorMenteeDeleteDTO,
)
from startup_forge.web.api.profile.schema import ProfileDTO
from startup_forge.web.error_message import ErrorMessage
from startup_forge.db.models.options import Role

router = APIRouter()


@router.get("/request", response_model=list[tuple[ProfileDTO, float]])
async def request_matches(
    user: User = Depends(current_active_user),
    mentor_mentee_dao: MentorMenteeDAO = Depends(),
    profile_dao: ProfileDAO = Depends(),
) -> list[tuple[Profile, float]]:
    """
    Retrieve a list of compatible mentors from the database.

    :param user: current user.
    :param profile_dao: DAO for profiles.
    :return: profile object(s) from database.
    """
    profile = await profile_dao.get_profile(user.id)
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ErrorMessage.USER_NOT_ASSOCIATED_WITH_AN_ACTIVE_PROFILE,
        )
    return await mentor_mentee_dao.match_mentees_to_mentors(mentee=profile)


@router.get("/", response_model=MentorMenteeDTO | list[MentorMenteeDTO])
async def get_matches(
    user: User = Depends(current_active_user),
    mentor_mentee_dao: MentorMenteeDAO = Depends(),
    profile_dao: ProfileDAO = Depends(),
) -> MentorMentee | list[MentorMentee]:
    """
    Retrieve mentor_mentee object(s) from the database.

    :param user: current user.
    :param profile_dao: DAO for profiles.
    :return: mentor_mentee object(s) from database.
    """
    profile = await profile_dao.get_profile(user.id)
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ErrorMessage.USER_NOT_ASSOCIATED_WITH_AN_ACTIVE_PROFILE,
        )
    mentor_mentees = await mentor_mentee_dao.get_matches(user.id, role=profile.role)
    if (profile.role == Role.MENTOR and len(mentor_mentees) < 1) or not mentor_mentees:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ErrorMessage.NO_VALID_MENTOR_MENTEE_RECORD,
        )
    return mentor_mentees


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_match(
    mentor_mentee_object: MentorMenteeInputDTO,
    user: User = Depends(current_active_user),
    mentor_mentee_dao: MentorMenteeDAO = Depends(),
    profile_dao: ProfileDAO = Depends(),
) -> None:
    """
    Creates profile in the database.

    :param mentor_mentee_object: new mentor_mentee item.
    :param user: current user.
    :param mentor_mentee_dao: DAO for MentorMentees.
    :param profile_dao: DAO for profiles.
    """
    user_profile = await profile_dao.get_profile(user.id)  # get user profile
    if not user_profile:  # check if profile already exists
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ErrorMessage.USER_NOT_ASSOCIATED_WITH_AN_ACTIVE_PROFILE,
        )
    mentor_profile = await profile_dao.get_profile(
        mentor_mentee_object.mentor_id
    )  # get mentor profile
    if not mentor_profile:  # check if profile already exists
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ErrorMessage.MENTOR_NOT_ASSOCIATED_WITH_AN_ACTIVE_PROFILE,
        )
    if mentor_mentee_dao.get_matches(user.id, user_profile.role):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ErrorMessage.USER_HAS_A_MENTOR_ALREADY,
        )
    await mentor_mentee_dao.create_match(
        user_id=user.id, mentor_id=mentor_mentee_object.mentor_id
    )


@router.delete("/")
async def unmatch(
    mentor_mentee_object: MentorMenteeDeleteDTO,
    user: User = Depends(current_active_user),
    profile_dao: ProfileDAO = Depends(),
    mentor_mentee_dao: MentorMenteeDAO = Depends(),
) -> None:
    """
    Deletes MentorMentee instance in the database.

    :param user: current user.
    :param profile_dao: DAO for profiles.
    :param mentor_mentee_dao: DAO for MentorMentees.
    """
    profile = await profile_dao.get_profile(user.id)  # get profile
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ErrorMessage.PROFILE_DOES_NOT_EXIST,
        )
    if profile.role != Role.MENTEE:
        return
    await mentor_mentee_dao.unmatch(
        user.id,
        mentor_comment=mentor_mentee_object.mentor_comment,
        mentee_comment=mentor_mentee_object.mentee_comment,
    )
