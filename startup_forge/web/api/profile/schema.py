from uuid import UUID
from typing import Optional

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
    expertises: Optional[list[ExpertiseName]]
    Skills: Optional[list[SkillName]]
    profile_picture_url: Optional[HttpUrl]
    languages: list[list[LanguageName, LanguageLevel]]
    social_lists: list[list[Platform, HttpUrl]]
    model_config = ConfigDict(from_attributes=True)


class ProfileInputDTO(BaseModel):
    """DTO for creating profile."""

    first_name: str
    last_name: str
    role: Role


# class MentorProfileInputDTO(BaseModel):
#     """DTO for updating new mentor profile"""

#     years_of_experience: Optional[str]
#     bio: Optional[str]
#     linkedin_url: Optional[HttpUrl]


class ProfileUpdateDTO(BaseModel):
    """DTO for updating profile."""

    first_name: Optional[str] = None
    last_name: Optional[str] = None
    years_of_experience: Optional[str] = None
    bio: Optional[str] = None
    expertises: Optional[list[ExpertiseName]] = None
    Skills: Optional[list[SkillName]] = None
    profile_picture_url: Optional[HttpUrl] = None
    languages: list[list[LanguageName, LanguageLevel]] | list[
        LanguageName, LanguageLevel
    ] = None
    social_lists: list[list[Platform, HttpUrl]] | list[Platform, HttpUrl] = None


class ExpertiseDTO(BaseModel):
    """DTO for expertise."""

    names: list[ExpertiseName] | ExpertiseName


class SkillDTO(BaseModel):
    """DTO for skill."""

    names: list[SkillName] | SkillName


class SocialLinkDTO(BaseModel):
    """DTO for social link."""

    social_link: list[list[Platform, HttpUrl]] | list[Platform, HttpUrl]


class SocialLinkDeleteDTO(BaseModel):
    """DTO for deleting social link."""

    platform: Platform


class LanguageDTO(BaseModel):
    """DTO for language."""

    languages: list[list[LanguageName, LanguageLevel]] | list[
        LanguageName, LanguageLevel
    ]


class LanguageDeleteDTO(BaseModel):
    """DTO for deleting language."""

    name: LanguageName
