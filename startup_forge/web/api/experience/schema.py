from datetime import date
from uuid import UUID
from typing import Optional

from pydantic import BaseModel, ConfigDict

from startup_forge.db.models.options import Industry


class ExperienceDTO(BaseModel):
    """
    DTO for experiences.

    It is returned when accessing experience from the API.
    """

    id: UUID
    user_id: UUID
    company_name: str
    description: Optional[str] = None
    start_date: date
    end_date: Optional[date] = None
    industry: Industry
    model_config = ConfigDict(from_attributes=True)


class ExperienceInputDTO(BaseModel):
    """DTO for creating experience."""

    company_name: str
    description: Optional[str] = None
    start_date: date
    end_date: Optional[date] = None
    industry: Industry


class ExperienceUpdateDTO(BaseModel):
    """DTO for updating experience."""

    company_name: Optional[str] = None
    description: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    industry: Optional[Industry] = None
