from typing import List

from fastapi import APIRouter, HTTPException, status
from fastapi.param_functions import Depends

from startup_forge.db.dao.review_dao import ReviewDAO
from startup_forge.db.dao.profile_dao import ProfileDAO
from startup_forge.db.models.users import User, current_active_user
from startup_forge.db.models.review import Review
from startup_forge.web.api.review.schema import *
from startup_forge.web.error_message import ProfileErrorDetails, ReviewErrorDetails

router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_review(
    review_object: ReviewInputDTO,
    user: User = Depends(current_active_user),
    profile_dao: ProfileDAO = Depends(),
    review_dao: ReviewDAO = Depends(),
) -> None:
    """
    Creates review in the database.

    :param review_object: new review item.
    :param user: current user.
    :param profile_dao: profile dao.
    :param review_dao: review dao.
    """
    profile = await profile_dao.get_profile(user_id=user.id)  # get profile
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ProfileErrorDetails.PROFILE_DOES_NOT_EXIST,
        )
    await review_dao.record_review(
        user_id=user.id,
        mentor_id=review_object.mentor_id,
        content=review_object.content,
    )


@router.patch("/{review_id}", status_code=status.HTTP_201_CREATED)
async def update_review(
    review_object: ReviewUpdateDTO,
    review_id: UUID,
    user: User = Depends(current_active_user),
    profile_dao: ProfileDAO = Depends(),
    review_dao: ReviewDAO = Depends(),
) -> None:
    """
    Creates review in the database.

    :param review_object: new review item.
    :param review_id: review id.
    :param user: current user.
    :param profile_dao: profile dao.
    :param review_dao: review dao.
    """
    profile = await profile_dao.get_profile(user_id=user.id)  # get profile
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ProfileErrorDetails.PROFILE_DOES_NOT_EXIST,
        )
    review = await review_dao.get_review(review_id=review_id)
    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ReviewErrorDetails.REVIEW_DOES_NOT_EXIST,
        )
    if review.user_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=ProfileErrorDetails.UNAUTHORIZED,
        )
    await review_dao.update_review(
        review_id=review.id,
        content=review_object.content,
    )


@router.delete("/{review_id}")
async def delete_education(
    review_id: UUID,
    user: User = Depends(current_active_user),
    review_dao: ReviewDAO = Depends(),
    profile_dao: ProfileDAO = Depends(),
) -> None:
    """
    Deletes a review object in the database.

    :param review_id: review id.
    :param user: current user.
    :param review_dao: review dao.
    :param profile_dao: DAO for profiles.
    """
    profile = await profile_dao.get_profile(user.id)  # get profile
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ProfileErrorDetails.PROFILE_DOES_NOT_EXIST,
        )
    review = await review_dao.get_review(review_id=review_id)
    if not review:
        return
    if user.id != review.mentee_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=ProfileErrorDetails.UNAUTHORIZED,
        )
    await review_dao.delete_review(
        review_id=review_id,
    )
