from datetime import date
from uuid import UUID
from typing import Optional

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.sql import func
from sqlalchemy.ext.asyncio import AsyncSession

from startup_forge.db.dependencies import get_db_session
from startup_forge.db.models.connection import Connection, ConnectionRequest
from startup_forge.db.models.options import ConnectionRequestStatus


class EducationDAO:
    """Class for accessing education table."""

    def __init__(self, session: AsyncSession = Depends(get_db_session)):
        self.session = session

    async def make_request(
        self,
        user_id: UUID,
        request_to_id: UUID,
    ) -> None:
        """
        Add single experience to session.

        :param user_id: id of the user registering the education.
        :param request_to_id: id of user recieving the request.
        """
        request = self.get_request(request_from=user_id, request_to=request_to_id)
        if request:
            request.status = ConnectionRequestStatus.PENDING
            self.session.add(request)
            return
        self.session.add(
            ConnectionRequest(
                request_from=user_id,
                request_to=request_to_id,
            )
        )

    async def get_request(
        self,
        request_from: UUID,
        request_to: UUID,
    ) -> ConnectionRequest | None:
        """
        Get a stream of connection requests education.

        :param user_id: id of the user.
        :return: stream of connection_request.
        """
        request = await self.session.execute(
            select(ConnectionRequest).where(
                ConnectionRequest.request_to == request_to
                and ConnectionRequest.request_from == request_from
            ),
        )

        return request.scalars().first()

    async def get_requests(
        self,
        user_id: UUID,
    ) -> list[ConnectionRequest] | None:
        """
        Get a stream of connection requests education.

        :param user_id: id of the user.
        :return: stream of connection_request.
        """
        requests = await self.session.execute(
            select(ConnectionRequest).where(ConnectionRequest.request_to == user_id),
        )

        return list(requests.scalars().fetchall())

    async def accept_request(self, request_from: UUID, request_to: UUID) -> None:
        """
        Change the status of a connect_request to ACCEPTED.

        :param request_from: id of the user who sent the request.
        :param request_to: id of the user who recieved the request.
        """
        result = await self.session.execute(
            select(ConnectionRequest).where(
                ConnectionRequest.request_from == request_from
                and ConnectionRequest.request_to == request_to
            ),
        )

        request = result.scalars().first()

        # change request status to accepted
        request.status = ConnectionRequestStatus.ACCEPTED

        # save the changes
        self.session.add(request)

        # create the connection
        self.session.add(
            Connection(
                request_from=request_from,
                request_to=request_to,
            )
        )

    async def reject_request(self, request_from: UUID, request_to: UUID) -> None:
        """
        Change the status of a connect_request to REJECTED.

        :param request_from: id of the user who sent the request.
        :param request_to: id of the user who recieved the request.
        """
        result = await self.session.execute(
            select(ConnectionRequest).where(
                ConnectionRequest.request_from == request_from
                and ConnectionRequest.request_to == request_to
            ),
        )

        request = result.scalars().first()

        # change request status to rejected
        request.status = ConnectionRequestStatus.REJECTED

        # save the changes
        self.session.add(request)

    async def get_connections(
        self,
        user_id: UUID,
    ) -> list[UUID] | None:
        """
        Get a stream of connections.

        :param user_id: id of the user.
        :return: stream of connection.
        """
        requests = await self.session.execute(
            select(ConnectionRequest).where(
                ConnectionRequest.request_to == user_id
                or ConnectionRequest.request_from == user_id
            ),
        )

        connections = list(requests.scalars().fetchall())

        connections_ids = [connection.request_from for connection in connections]
        connections_ids.extend([connection.request_to for connection in connections])
        connections_ids = list(set(connections))
        return connections_ids
