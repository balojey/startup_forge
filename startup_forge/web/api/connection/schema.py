from datetime import datetime
from uuid import UUID
from typing import Optional

from pydantic import BaseModel, ConfigDict

from startup_forge.db.models.options import ConnectionRequestStatus


class ConnectionRequestDTO(BaseModel):
    """
    DTO for connection requests.

    It is returned when accessing connection_request from the API.
    """

    request_from: UUID
    request_to: UUID
    requested_at: datetime
    status: ConnectionRequestStatus
    model_config = ConfigDict(from_attributes=True)


class ConnectionDTO(BaseModel):
    """
    DTO for connection connection.

    It is returned when accessing connection from the API.
    """

    request_from: UUID
    request_to: UUID
    accepted_at: datetime
    model_config = ConfigDict(from_attributes=True)
