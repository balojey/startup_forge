from uuid import UUID
from typing import Optional

from pydantic import BaseModel, ConfigDict

from startup_forge.db.models.options import Role


class ProfileDTO(BaseModel):
    """
    DTO for profiles.

    It is returned when accessing profile from the API.
    """

    user_id: UUID
    first_name: str
    last_name: str
    role: Role
    model_config = ConfigDict(from_attributes=True)


class ProfileInputDTO(BaseModel):
    """DTO for creating profile."""

    first_name: str
    last_name: str
    role: Role


class ProfileUpdateDTO(BaseModel):
    """DTO for updating profile."""

    first_name: Optional[str] = None
    last_name: Optional[str] = None
    role: Optional[Role] = None
