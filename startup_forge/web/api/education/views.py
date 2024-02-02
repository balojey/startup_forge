from typing import List

from fastapi import APIRouter, HTTPException, status
from fastapi.param_functions import Depends

from startup_forge.db.dao.education_dao import EducationDAO
from startup_forge.db.dao.profile_dao import ProfileDAO
from startup_forge.db.models.users import User, current_active_user
from startup_forge.db.models.education import Education
from startup_forge.web.api.education.schema import *
from startup_forge.web.error_message import EducationErrorDetails, ProfileErrorDetails

router = APIRouter()


@router.get("/", response_model=EducationDTO)
async def get_educations(
    user: User = Depends(current_active_user),
    education_id: Optional[UUID] = None,
    user_id: Optional[UUID] = None,
    profile_dao: ProfileDAO = Depends(),
    education_dao: EducationDAO = Depends(),
) -> list[Education] | None:
    """
    Retrieve a education objects from the database.

    :param user: current user.
    :param education_id: education id.
    :param user_id: a user id.
    :param profile_dao: profile dao.
    :param education_dao: education dao.
    :return: education objects from database.
    """
    profile = await profile_dao.get_profile(user_id=user.id)
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ProfileErrorDetails.PROFILE_DOES_NOT_EXIST,
        )
    if education_id:
        return await education_dao.get_education(
            education_id=education_id,
        )
    return await education_dao.get_educations(
        user_id=user.id if not user_id else user_id
    )


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_education(
    education_object: EducationInputDTO,
    user: User = Depends(current_active_user),
    education_dao: EducationDAO = Depends(),
    profile_dao: ProfileDAO = Depends(),
) -> None:
    """
    Creates eduction in the database.

    :param education_object: new education item.
    :param user: current user.
    :param education_dao: education dao.
    :param profile_dao: DAO for profiles.
    """
    profile = await profile_dao.get_profile(user.id)  # get profile
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ProfileErrorDetails.PROFILE_DOES_NOT_EXIST,
        )
    await education_dao.record_education(
        user_id=user.id,
        institution_name=education_object.institution_name,
        course_of_study=education_object.course_of_study,
        start_date=education_object.start_date,
        state=education_object.state,
        country=education_object.country,
        end_date=education_object.end_date,
    )


@router.patch("/{education_id}")
async def update_education(
    education_id: UUID,
    education_object: EducationUpdateDTO,
    user: User = Depends(current_active_user),
    education_dao: EducationDAO = Depends(),
    profile_dao: ProfileDAO = Depends(),
) -> None:
    """
    Updates eduction in the database.

    :param education_id: education id.
    :param education_object: new education item.
    :param user: current user.
    :param education_dao: education dao.
    :param profile_dao: DAO for profiles.
    """
    profile = await profile_dao.get_profile(user.id)  # get profile
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ProfileErrorDetails.PROFILE_DOES_NOT_EXIST,
        )
    if not await education_dao.get_education(education_id=education_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=EducationErrorDetails.EDUCATION_DOES_NOT_EXIST,
        )
    await education_dao.update_education(
        institution_name=education_object.institution_name,
        course_of_study=education_object.course_of_study,
        start_date=education_object.start_date,
        state=education_object.state,
        country=education_object.country,
        end_date=education_object.end_date,
    )


@router.delete("/{education_id}")
async def delete_education(
    education_id: UUID,
    user: User = Depends(current_active_user),
    education_dao: EducationDAO = Depends(),
    profile_dao: ProfileDAO = Depends(),
) -> None:
    """
    Deletes an eduction object in the database.

    :param education_id: education id.
    :param user: current user.
    :param education_dao: education dao.
    :param profile_dao: DAO for profiles.
    """
    profile = await profile_dao.get_profile(user.id)  # get profile
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ProfileErrorDetails.PROFILE_DOES_NOT_EXIST,
        )
    await education_dao.delete_education(
        education_id=education_id,
    )
