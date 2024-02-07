from typing import List

from fastapi import APIRouter, HTTPException, status
from fastapi.param_functions import Depends

from startup_forge.db.dao.profile_dao import ProfileDAO
from startup_forge.db.dao.community_dao import CommunityDAO
from startup_forge.db.models.users import User, current_active_user
from startup_forge.db.models.profile import Profile
from startup_forge.db.models.community import Post, Comment
from startup_forge.web.api.community.schema import *
from startup_forge.web.error_message import ErrorMessage, CommunityErrorDetails

router = APIRouter()


@router.get("/", response_model=list[PostDTO])
async def get_posts(
    user: User = Depends(current_active_user),
    profile_dao: ProfileDAO = Depends(),
    community_dao: CommunityDAO = Depends(),
) -> list[Post]:
    """
    Retrieve a list of random post object from the database.

    :param user: current user.
    :return: stream of post object from database.
    """
    profile = await profile_dao.get_profile(user.id)
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ErrorMessage.PROFILE_DOES_NOT_EXIST,
        )
    return community_dao.get_posts()


@router.get("/me", response_model=list[PostDTO])
async def get_my_posts(
    user: User = Depends(current_active_user),
    profile_dao: ProfileDAO = Depends(),
    community_dao: CommunityDAO = Depends(),
) -> list[Post]:
    """
    Retrieve a list of random post object from the database.

    :param user: current user.
    :return: stream of post object from database.
    """
    profile = await profile_dao.get_profile(user.id)
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ErrorMessage.PROFILE_DOES_NOT_EXIST,
        )
    return community_dao.get_posts(user.id)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_post(
    post_object: PostInputDTO,
    user: User = Depends(current_active_user),
    profile_dao: ProfileDAO = Depends(),
    community_dao: CommunityDAO = Depends(),
) -> None:
    """
    Creates post in the database.

    :param post_object: new post item.
    :param profile_dao: DAO for profiles.
    """
    profile = await profile_dao.get_profile(user.id)  # get profile
    if not profile:  # check if profile already exists
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ErrorMessage.PROFILE_DOES_NOT_EXIST,
        )
    new_post = await community_dao.create_post(
        user_id=user.id, text=post_object.text, files_urls=post_object.files_urls
    )
    if post_object.post_id:
        post = await community_dao.get_post(post_object.post_id)
        if not post:
            return
        await community_dao.create_repost(post_object.post_id, new_post.id)


@router.patch("/{post_id}")
async def update_post(
    post_id: UUID,
    post_object: PostUpdateDTO,
    user: User = Depends(current_active_user),
    profile_dao: ProfileDAO = Depends(),
    community_dao: CommunityDAO = Depends(),
) -> None:
    """
    Updates post in the database.

    :param post_id: post id.
    :param post_object: post item.
    :param profile_dao: DAO for profiles.
    """
    profile = await profile_dao.get_profile(user.id)  # get profile
    if not profile:  # check if profile already exists
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ErrorMessage.PROFILE_DOES_NOT_EXIST,
        )
    post = await community_dao.get_post(post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=CommunityErrorDetails.POST_NOT_FOUND,
        )
    await community_dao.update_post(post_id, post_object.text)


@router.delete("/{post_id}")
async def delete_post(
    post_id: UUID,
    user: User = Depends(current_active_user),
    profile_dao: ProfileDAO = Depends(),
    community_dao: CommunityDAO = Depends(),
) -> None:
    """
    Updates post in the database.

    :param post_id: post id.
    :param profile_dao: DAO for profiles.
    """
    profile = await profile_dao.get_profile(user.id)  # get profile
    if not profile:  # check if profile already exists
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ErrorMessage.PROFILE_DOES_NOT_EXIST,
        )
    post = await community_dao.get_post(post_id)
    if not post:
        return
    await community_dao.delete_post(post_id)


@router.post("/{post_id}", status_code=status.HTTP_201_CREATED)
async def create_comment(
    post_id: UUID,
    comment_object: CommentInputDTO,
    user: User = Depends(current_active_user),
    profile_dao: ProfileDAO = Depends(),
    community_dao: CommunityDAO = Depends(),
) -> None:
    """
    Creates comment in the database.

    :param post_id: post id.
    :param comment_object: new comment item.
    :param profile_dao: DAO for profiles.
    """
    profile = await profile_dao.get_profile(user.id)  # get profile
    if not profile:  # check if profile already exists
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ErrorMessage.PROFILE_DOES_NOT_EXIST,
        )
    post = await community_dao.get_post(post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=CommunityErrorDetails.POST_NOT_FOUND,
        )
    new_comment = await community_dao.create_comment(
        user_id=user.id,
        text=comment_object.content,
        post_id=post_id,
    )
    if comment_object.comment_id:
        comment = await community_dao.get_comment(comment_object.comment_id)
        if not comment:
            return
        await community_dao.create_reply(comment_object.comment_id, new_comment.id)


@router.patch("/comments/{comment_id}")
async def update_comment(
    comment_id: UUID,
    comment_object: CommentUpdateDTO,
    user: User = Depends(current_active_user),
    profile_dao: ProfileDAO = Depends(),
    community_dao: CommunityDAO = Depends(),
) -> None:
    """
    Updates comment in the database.

    :param comment_id: comment id.
    :param comment_object: comment item.
    :param profile_dao: DAO for profiles.
    """
    profile = await profile_dao.get_profile(user.id)  # get profile
    if not profile:  # check if profile already exists
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ErrorMessage.PROFILE_DOES_NOT_EXIST,
        )
    comment = await community_dao.get_comment(comment_id)
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=CommunityErrorDetails.COMMENT_NOT_FOUND,
        )
    await community_dao.update_comment(comment_id, comment_object.content)


@router.delete("/comments/{comment_id}")
async def delete_comment(
    comment_id: UUID,
    user: User = Depends(current_active_user),
    profile_dao: ProfileDAO = Depends(),
    community_dao: CommunityDAO = Depends(),
) -> None:
    """
    Deletes comment in the database.

    :param comment_id: comment id.
    :param profile_dao: DAO for profiles.
    """
    profile = await profile_dao.get_profile(user.id)  # get profile
    if not profile:  # check if profile already exists
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ErrorMessage.PROFILE_DOES_NOT_EXIST,
        )
    comment = await community_dao.get_comment(comment_id)
    if not comment:
        return
    await community_dao.delete_comment(comment_id)


@router.get("/comments", response_model=list[CommentDTO])
async def get_comments(
    post_id: UUID,
    user: User = Depends(current_active_user),
    profile_dao: ProfileDAO = Depends(),
    community_dao: CommunityDAO = Depends(),
) -> list[Comment]:
    """
    Retrieve a list of random post object from the database.

    :param post_id: post id.
    :param user: current user.
    :return: stream of post object from database.
    """
    profile = await profile_dao.get_profile(user.id)
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ErrorMessage.PROFILE_DOES_NOT_EXIST,
        )
    if post_id:
        post = await community_dao.get_post(post_id)
        if not post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=CommunityErrorDetails.POST_NOT_FOUND,
            )
        return await community_dao.get_comments(post_id)
    return await community_dao.get_my_comments(user.id)


@router.post("/{post_id}/likes", status_code=status.HTTP_201_CREATED)
async def like_unlike(
    post_id: UUID,
    user: User = Depends(current_active_user),
    profile_dao: ProfileDAO = Depends(),
    community_dao: CommunityDAO = Depends(),
) -> None:
    """
    Creates comment in the database.

    :param post_id: post id.
    :param comment_object: new comment item.
    :param profile_dao: DAO for profiles.
    """
    profile = await profile_dao.get_profile(user.id)  # get profile
    if not profile:  # check if profile already exists
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ErrorMessage.PROFILE_DOES_NOT_EXIST,
        )
    post = await community_dao.get_post(post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=CommunityErrorDetails.POST_NOT_FOUND,
        )
    await community_dao.like_unlike(post_id, user.id)
