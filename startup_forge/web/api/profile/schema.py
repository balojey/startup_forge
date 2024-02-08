from uuid import UUID
from typing import Optional, List, Tuple

from pydantic import BaseModel, ConfigDict, HttpUrl

from startup_forge.db.models.options import (
    Role,
    ExpertiseName,
    SkillName,
    Platform,
    LanguageLevel,
    LanguageName,
)


class ProfileDTO(BaseModel):
    """
    DTO for profiles.

    It is returned when accessing profile from the API.
    """

    user_id: UUID
    first_name: str
    last_name: str
    role: Role
    years_of_experienc: Optional[str]
    bio: Optional[str]
    expertises: Optional[Tuple[ExpertiseName]]
    skills: Optional[Tuple[SkillName]]
    profile_picture_url: Optional[HttpUrl]
    languages: Optional[List[Tuple[LanguageName, LanguageLevel]]]
    social_lists: Optional[List[Tuple[Platform, HttpUrl]]]

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
    years_of_experience: Optional[str] = None
    bio: Optional[str] = None
    expertises: Optional[Tuple[ExpertiseName]] = None
    skills: Optional[Tuple[SkillName]] = None
    profile_picture_url: Optional[HttpUrl] = None
    languages: (
        Optional[List[Tuple[LanguageName, LanguageLevel]]]
        | Optional[Tuple[LanguageName, LanguageLevel]]
    ) = None
    social_lists: (
        Optional[List[Tuple[Platform, HttpUrl]]] | Optional[Tuple[Platform, HttpUrl]]
    ) = None


class ExpertiseDTO(BaseModel):
    """DTO for expertise."""

    names: list[ExpertiseName] | ExpertiseName


class SkillDTO(BaseModel):
    """DTO for skill."""

    names: list[SkillName] | SkillName


class SocialLinkDTO(BaseModel):
    """DTO for social link."""

    social_link: List[Tuple[Platform, HttpUrl]] | Tuple[Platform, HttpUrl]


class SocialLinkDeleteDTO(BaseModel):
    """DTO for deleting social link."""

    platform: Platform


class LanguageDTO(BaseModel):
    """DTO for language."""

    languages: List[Tuple[LanguageName, LanguageLevel]] | Tuple[LanguageName, LanguageLevel]


class LanguageDeleteDTO(BaseModel):
    """DTO for deleting language."""

    name: LanguageName
