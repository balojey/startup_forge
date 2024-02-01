from datetime import date
from uuid import UUID
from typing import Optional

from pydantic import BaseModel, ConfigDict


class EducationInputDTO(BaseModel):
    """DTO for creating education."""

    institution_name: str
    course_of_study: str
    start_date: date
    end_date: Optional[str]
    state: str
    country: str


class EducationUpdateDTO(EducationInputDTO):
    """DTO for updating profile."""

    pass


class EducationDTO(EducationInputDTO):
    """
    DTO for education.

    It is returned when accessing education from the API.
    """

    id: UUID
    model_config = ConfigDict(from_attributes=True)
