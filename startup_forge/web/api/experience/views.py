from uuid import UUID
from typing import List, Optional

from fastapi import APIRouter, HTTPException, status
from fastapi.param_functions import Depends

from startup_forge.db.dao.experience_dao import ExperienceDAO
from startup_forge.db.dao.profile_dao import ProfileDAO
from startup_forge.db.models.users import User, current_active_user
from startup_forge.db.models.experience import Experience
from startup_forge.web.api.experience.schema import (
    ExperienceDTO,
    ExperienceInputDTO,
    ExperienceUpdateDTO,
)
from startup_forge.db.models.options import Industry
from startup_forge.web.error_message import ErrorMessage

router = APIRouter()


@router.get("/", response_model=list[ExperienceDTO])
async def get_experiences(
    user_id: Optional[str] = None,
    user: User = Depends(current_active_user),
    experience_dao: ExperienceDAO = Depends(),
) -> list[Experience]:
    """
    Retrieve a list of experience objects from the database.

    :param user: current user.
    :param experience: experience's data access model instance.
    :return: list of experience object from database.
    """
    if user_id:
        u_id = user_id
    else:
        u_id = user.id
    experiences = await experience_dao.get_experiences(u_id)
    if len(experiences) < 1:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ErrorMessage.EXPERIENCES_NOT_FOUND,
        )
    return experiences


@router.get("/{experience_id}", response_model=ExperienceDTO)
async def get_experience(
    experience_id: UUID,
    experience_dao: ExperienceDAO = Depends(),
) -> Experience:
    """
    Retrieve an experience object from the database.

    :param experience_id: id of the experience.
    :param user: current user.
    :param experience: experience's data access model instance.
    :return: an experience object from database.
    """
    experience = await experience_dao.get_experience(experience_id=experience_id)
    if not experience:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ErrorMessage.EXPERIENCE_NOT_FOUND,
        )
    return experience


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_experience(
    experience_object: ExperienceInputDTO,
    user: User = Depends(current_active_user),
    experience_dao: ExperienceDAO = Depends(),
    profile_dao: ProfileDAO = Depends(),
) -> None:
    """
    Creates experience in the database.

    :param experience_object: new experience item.
    :param user: current user.
    :param experience_dao: DAO for experiences.
    """
    profile = await profile_dao.get_profile(user.id)
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ErrorMessage.USER_NOT_ASSOCIATED_WITH_AN_ACTIVE_PROFILE,
        )
    await experience_dao.create_experience(
        user_id=user.id,
        company_name=experience_object.company_name,
        start_date=experience_object.start_date,
        industry=experience_object.industry,
        description=experience_object.description,
        end_date=experience_object.end_date,
    )


@router.patch("/{experience_id}")
async def update_experience(
    experience_id: UUID,
    experience_object: ExperienceUpdateDTO,
    user: User = Depends(current_active_user),
    experience_dao: ExperienceDAO = Depends(),
) -> None:
    """
    Updates experience in the database.

    :param experience_id: id of the experience
    :param experience_object: profile item.
    :param user: current user.
    :param experience_dao: DAO for experiences.
    """
    experience = await experience_dao.get_experience(
        experience_id=experience_id
    )  # get experience
    if not experience:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ErrorMessage.EXPERIENCE_DOES_NOT_EXIST,
        )
    if user.id != experience.user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=ErrorMessage.UNAUTHORIZED,
        )
    await experience_dao.update_profile(
        company_name=experience_object.company_name,
        start_date=experience_object.start_date,
        industry=experience_object.industry,
        description=experience_object.description,
        end_date=experience_object.end_date,
    )


@router.delete("/{experience_id}")
async def delete_experience(
    experience_id: UUID,
    user: User = Depends(current_active_user),
    experience_dao: ExperienceDAO = Depends(),
) -> None:
    """
    Deletes an experience in the database.

    :param experience_id: id of the experience
    :param user: current user.
    :param experience_dao: DAO for experiences.
    """
    experience = await experience_dao.get_experience(
        experience_id=experience_id
    )  # get experience
    if not experience:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ErrorMessage.EXPERIENCE_DOES_NOT_EXIST,
        )
    if user.id != experience.user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=ErrorMessage.UNAUTHORIZED,
        )
    await experience_dao.delete_experience(experience_id=experience_id)


@router.delete("/")
async def delete_experiences(
    user: User = Depends(current_active_user),
    experience_dao: ExperienceDAO = Depends(),
) -> None:
    """
    Delete experiences in the database.

    :param user: current user.
    :param experience_dao: DAO for experiences.
    """
    experiences = await experience_dao.get_experiences(
        user_id=user.id
    )  # get experiences
    if not experiences:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ErrorMessage.EXPERIENCES_NOT_FOUND,
        )
    await experience_dao.delete_experiences(experiences=experiences)


@router.get("/industries", response_model=list[ExperienceDTO])
async def get_industries(
    user_id: Optional[str] = None,
    user: User = Depends(current_active_user),
    experience_dao: ExperienceDAO = Depends(),
) -> list[Industry]:
    """
    Retrieve a list of industry objects from the database.

    :param user: current user.
    :return: list of industry object from database.
    """
    if user_id:
        u_id = user_id
    else:
        u_id = user.id
    experiences = await experience_dao.get_experiences(u_id)
    if len(experiences) < 1:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ErrorMessage.EXPERIENCES_NOT_FOUND,
        )
    return [experience.industry for experience in experiences]


@router.get("/", response_model=list[ExperienceDTO])
async def get_current_experiences(
    user_id: Optional[str] = None,
    user: User = Depends(current_active_user),
    experience_dao: ExperienceDAO = Depends(),
) -> list[Experience]:
    """
    Retrieve a list of experience objects from the database.

    :param user: current user.
    :param experience: experience's data access model instance.
    :return: list of experience object from database.
    """
    if user_id:
        u_id = user_id
    else:
        u_id = user.id
    experiences = await experience_dao.get_experiences(u_id)
    if len(experiences) < 1:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ErrorMessage.EXPERIENCES_NOT_FOUND,
        )
    return [experience for experience in experiences if experience.end_date != None]
