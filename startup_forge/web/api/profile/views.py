from typing import List

from fastapi import APIRouter, HTTPException, status
from fastapi.param_functions import Depends

from startup_forge.db.dao.profile_dao import ProfileDAO
from startup_forge.db.dao.review_dao import ReviewDAO
from startup_forge.db.dao.connection_dao import ConnectionDAO
from startup_forge.db.models.users import User, current_active_user
from startup_forge.db.models.profile import Profile
from startup_forge.db.models.review import Review
from startup_forge.web.api.profile.schema import *
from startup_forge.web.api.review.schema import *
from startup_forge.web.error_message import ErrorMessage, ProfileErrorDetails

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

    :param user: current user.
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

    :param user: current user.
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
        first_name=profile_object.first_name,
        last_name=profile_object.last_name,
        years_of_experience=profile_object.years_of_experience,
        bio=profile_object.bio,
        profile_picture_url=profile_object.profile_picture_url,
        expertises=profile_object.expertises,
        skills=profile_object.skills,
        social_links=profile_object.social_lists,
    )


@router.put("/expertises")
async def record_expertises(
    expertise: ExpertiseDTO,
    user: User = Depends(current_active_user),
    profile_dao: ProfileDAO = Depends(),
) -> None:
    """
    Updates profile in the database.

    :param user: current user.
    :param expertise: expertise object.
    :param profile_dao: DAO for profiles.
    """

    profile = await profile_dao.get_profile(user.id)
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ProfileErrorDetails.PROFILE_DOES_NOT_EXIST,
        )
    await profile_dao.record_expertise(
        user_id=user.id,
        expertise_names=expertise.names,
    )


@router.delete("/expertises")
async def remove_expertises(
    expertise: ExpertiseDTO,
    user: User = Depends(current_active_user),
    profile_dao: ProfileDAO = Depends(),
) -> None:
    """
    Updates profile in the database.

    :param user: current user.
    :param expertise: expertise object.
    :param profile_dao: DAO for profiles.
    """

    profile = await profile_dao.get_profile(user.id)
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ProfileErrorDetails.PROFILE_DOES_NOT_EXIST,
        )
    await profile_dao.remove_expertise(
        user_id=user.id,
        expertise_names=expertise.names,
    )


@router.put("/skills")
async def record_skills(
    skill: SkillDTO,
    user: User = Depends(current_active_user),
    profile_dao: ProfileDAO = Depends(),
) -> None:
    """
    Updates profile in the database.

    :param user: current user.
    :param skill: skill object.
    :param profile_dao: DAO for profiles.
    """

    profile = await profile_dao.get_profile(user.id)
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ProfileErrorDetails.PROFILE_DOES_NOT_EXIST,
        )
    await profile_dao.register_skills(
        user_id=user.id,
        skill_names=skill.names,
    )


@router.delete("/skills")
async def record_skills(
    skill: SkillDTO,
    user: User = Depends(current_active_user),
    profile_dao: ProfileDAO = Depends(),
) -> None:
    """
    Updates profile in the database.

    :param user: current user.
    :param skill: skill object.
    :param profile_dao: DAO for profiles.
    """

    profile = await profile_dao.get_profile(user.id)
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ProfileErrorDetails.PROFILE_DOES_NOT_EXIST,
        )
    await profile_dao.remove_skills(
        user_id=user.id,
        skill_names=skill.names,
    )


@router.put("/socials")
async def register_socials(
    social_link: SocialLinkDTO,
    user: User = Depends(current_active_user),
    profile_dao: ProfileDAO = Depends(),
) -> None:
    """
    Updates profile in the database.

    :param user: current user.
    :param social_link: social_link object.
    :param profile_dao: DAO for profiles.
    """

    profile = await profile_dao.get_profile(user.id)
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ProfileErrorDetails.PROFILE_DOES_NOT_EXIST,
        )
    await profile_dao.register_social_link(
        user_id=user.id,
        social_links=social_link.social_link,
    )


@router.delete("/socials")
async def remove_social(
    social_link: SocialLinkDeleteDTO,
    user: User = Depends(current_active_user),
    profile_dao: ProfileDAO = Depends(),
) -> None:
    """
    Updates profile in the database.

    :param user: current user.
    :param social_link: social_link object.
    :param profile_dao: DAO for profiles.
    """

    profile = await profile_dao.get_profile(user.id)
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ProfileErrorDetails.PROFILE_DOES_NOT_EXIST,
        )
    await profile_dao.register_social_link(
        user_id=user.id,
        platform=social_link.platform,
    )


@router.put("/languages")
async def remove_language(
    language: LanguageDTO,
    user: User = Depends(current_active_user),
    profile_dao: ProfileDAO = Depends(),
) -> None:
    """
    Updates profile in the database.

    :param user: current user.
    :param language: language object.
    :param profile_dao: DAO for profiles.
    """

    profile = await profile_dao.get_profile(user.id)
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ProfileErrorDetails.PROFILE_DOES_NOT_EXIST,
        )
    await profile_dao.register_language(
        user_id=user.id, language_names=language.languages
    )


@router.delete("/languages")
async def remove_language(
    language: LanguageDeleteDTO,
    user: User = Depends(current_active_user),
    profile_dao: ProfileDAO = Depends(),
) -> None:
    """
    Updates profile in the database.

    :param user: current user.
    :param language: language object.
    :param profile_dao: DAO for profiles.
    """

    profile = await profile_dao.get_profile(user.id)
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ProfileErrorDetails.PROFILE_DOES_NOT_EXIST,
        )
    await profile_dao.remove_language(
        user_id=user.id,
        language_name=language.name,
    )


@router.get("/{profile_id}/reviews", response_model=ReviewDTO)
async def get_reviews(
    profile_id: UUID,
    profile_dao: ProfileDAO = Depends(),
    review_dao: ReviewDAO = Depends(),
) -> list[Review] | None:
    """
    Retrieve review objects from the database.

    :param profile_id: profile id.
    :param profile_dao: profile dao.
    :param review_dao: review dao.
    :return: review objects from database.
    """
    profile = await profile_dao.get_profile(user_id=profile_id)
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ProfileErrorDetails.PROFILE_DOES_NOT_EXIST,
        )
    return await review_dao.get_reviews(
        user_id=profile_id,
        role=profile.role,
    )


@router.get("/connections", response_model=list[ProfileDTO])
async def get_requests(
    user: User = Depends(current_active_user),
    user_id: Optional[UUID] = None,
    profile_dao: ProfileDAO = Depends(),
    connection_dao: ConnectionDAO = Depends(),
) -> list[Profile]:
    """
    Retrieve connection objects from the database.

    :param user: current user.
    :param user_id: user id.
    :param profile_dao: DAO for profiles.
    :param connection_dao: DAO for connections.
    :return: profile objects from database.
    """
    profile = await profile_dao.get_profile(user.id)
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ProfileErrorDetails.PROFILE_DOES_NOT_EXIST,
        )
    connections_ids = await connection_dao.get_connections(
        user_id=user.id if not user_id else user_id
    )

    return [
        profile_dao.get_profile(user_id=connection_id)
        for connection_id in connections_ids
    ]
