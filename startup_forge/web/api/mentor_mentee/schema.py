from datetime import datetime
from uuid import UUID
from typing import Optional

from pydantic import BaseModel, ConfigDict

from startup_forge.db.models.options import Role


class MentorMenteeDTO(BaseModel):
    """
    DTO for mentor_mentee.

    It is returned when accessing mentor_mentee from the API.
    """

    mentor_id: UUID
    mentee_id: UUID
    start_date: datetime
    model_config = ConfigDict(from_attributes=True)


class MentorMenteeInputDTO(BaseModel):
    """DTO for creating mentor_mentee instance."""

    mentor_id: UUID


class MentorMenteeDeleteDTO(BaseModel):
    """DTO for deleting mentor_mentee instance."""

    mentor_comment: Optional[str] = None
    mentee_comment: Optional[str] = None
