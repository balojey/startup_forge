from uuid import UUID
from typing import List

from fastapi import APIRouter, HTTPException, status
from fastapi.param_functions import Depends

from startup_forge.db.dao.profile_dao import ProfileDAO
from startup_forge.db.dao.connection_dao import ConnectionDAO
from startup_forge.db.models.users import User, current_active_user
from startup_forge.db.models.connection import Connection, ConnectionRequest
from startup_forge.web.api.connection.schema import *
from startup_forge.web.error_message import ProfileErrorDetails, ConnectionErrorDetails

router = APIRouter()


@router.get("/requests", response_model=list[ConnectionRequestDTO])
async def get_requests(
    user: User = Depends(current_active_user),
    profile_dao: ProfileDAO = Depends(),
    connection_dao: ConnectionDAO = Depends(),
) -> list[ConnectionRequest]:
    """
    Retrieve a profile object from the database.

    :param user: current user.
    :param profile_dao: DAO for profiles.
    :param connection_dao: DAO for connections.
    :return: profile object from database.
    """
    profile = await profile_dao.get_profile(user.id)
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ProfileErrorDetails.PROFILE_DOES_NOT_EXIST,
        )
    return await connection_dao.get_requests(user_id=user.id)


@router.post("/requests/{profile_id}", status_code=status.HTTP_201_CREATED)
async def send_request(
    profile_id: UUID,
    user: User = Depends(current_active_user),
    profile_dao: ProfileDAO = Depends(),
    connection_dao: ConnectionDAO = Depends(),
) -> None:
    """
    Send a connection request.

    :param user: current user.
    :param profile_id: profile id.
    :param profile_dao: DAO for profiles.
    :param connection_dao: DAO for connections.
    """
    request_from = await profile_dao.get_profile(user.id)  # get profile
    request_to = await profile_dao.get_profile(profile_id)
    if not request_from or not request_to:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ProfileErrorDetails.PROFILE_DOES_NOT_EXIST,
        )
    await connection_dao.make_request(
        user_id=request_from.user_id,
        request_to_id=request_to.user_id,
    )


@router.patch(
    "/requests/{request_from}/{requestt_to}/accept", status_code=status.HTTP_201_CREATED
)
async def accept_request(
    request_from: UUID,
    request_to: UUID,
    user: User = Depends(current_active_user),
    profile_dao: ProfileDAO = Depends(),
    connection_dao: ConnectionDAO = Depends(),
) -> None:
    """
    Send a connection request.

    :param user: current user.
    :param request_from: id of the user who sent the request.
    :param request_to: id of the user who recieved the request.
    :param profile_dao: DAO for profiles.
    :param connection_dao: DAO for connections.
    """
    profile = await profile_dao.get_profile(user.id)  # get profile
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ProfileErrorDetails.PROFILE_DOES_NOT_EXIST,
        )
    connection_request = await connection_dao.get_request(
        request_from=request_from, request_to=request_to
    )
    if not connection_request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ConnectionErrorDetails.NO_SUCH_CONNECTION_REQUEST,
        )
    if profile.id != request_to:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=ProfileErrorDetails.UNAUTHORIZED,
        )
    await connection_dao.accept_request(
        request_from=request_from, request_to=request_to
    )


@router.patch(
    "/requests/{request_from}/{requestt_to}/accept", status_code=status.HTTP_201_CREATED
)
async def reject_request(
    request_from: UUID,
    request_to: UUID,
    user: User = Depends(current_active_user),
    profile_dao: ProfileDAO = Depends(),
    connection_dao: ConnectionDAO = Depends(),
) -> None:
    """
    Reject a connection request.

    :param user: current user.
    :param request_from: id of the user who sent the request.
    :param request_to: id of the user who recieved the request.
    :param profile_dao: DAO for profiles.
    :param connection_dao: DAO for connections.
    """
    profile = await profile_dao.get_profile(user.id)  # get profile
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ProfileErrorDetails.PROFILE_DOES_NOT_EXIST,
        )
    connection_request = await connection_dao.get_request(
        request_from=request_from, request_to=request_to
    )
    if not connection_request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ConnectionErrorDetails.NO_SUCH_CONNECTION_REQUEST,
        )
    if profile.id != request_to:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=ProfileErrorDetails.UNAUTHORIZED,
        )
    await connection_dao.reject_request(
        request_from=request_from, request_to=request_to
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
