from uuid import UUID
from typing import List, Optional

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import func
from pydantic import HttpUrl

from startup_forge.db.dependencies import get_db_session
from startup_forge.db.models.profile import Profile
from startup_forge.db.models.options import (
    Role,
    LanguageLevel,
    LanguageName,
    Platform,
    SkillName,
    ExpertiseName,
)


class ProfileDAO:
    """Class for accessing profile table."""

    def __init__(self, session: AsyncSession = Depends(get_db_session)):
        self.session = session

    async def create_profile(
        self,
        user_id: UUID,
        role: Role,
        first_name: str,
        last_name: str,
        years_of_experience: Optional[str] = None,
        bio: Optional[str] = None,
    ) -> None:
        """
        Add single profile to session.

        :param user_id: id of the user initiating the profile.
        :param role: role of the user.
        :param first_name: first name of the user.
        :param last_name: last name of the user.
        """
        self.session.add(
            Profile(
                user_id=user_id,
                role=role,
                first_name=first_name,
                last_name=last_name,
                years_of_experience=years_of_experience,
                bio=bio,
            )
        )

    async def get_profile(self, user_id: UUID) -> Profile:
        """
        Get a profile.

        :param user_id: id of the profile.
        :return: a profile.
        """
        profile = await self.session.execute(
            select(Profile).where(Profile.user_id == user_id),
        )

        return profile.scalars().first()

    async def update_profile(
        self,
        user_id: UUID,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        years_of_experience: Optional[str] = None,
        bio: Optional[str] = None,
        profile_picture_url: Optional[str] = None,
        expertises: Optional[list[ExpertiseName]] = None,
        skills: Optional[list[SkillName]] = None,
        languages: Optional[list[list[LanguageName, LanguageLevel]]] = None,
        social_links: Optional[list[list[Platform, HttpUrl]]] = None,
    ) -> None:
        """
        Update a specific profile

        :param user_id: id of the profile owner.
        :param role: role of the user.
        :param first_name: first name of the user.
        :param last_name: last name of the user.
        """
        profile = await self.get_profile(user_id=user_id)  # get the profile

        # edit profile
        profile.first_name = first_name if first_name else profile.first_name
        profile.last_name = last_name if last_name else profile.last_name
        profile.years_of_experience = (
            years_of_experience if years_of_experience else profile.years_of_experience
        )
        profile.bio = bio if bio else profile.bio
        profile.profile_picture_url = (
            profile_picture_url if profile_picture_url else profile.profile_picture_url
        )
        profile.expertises = (
            profile.expertises.extend(expertises) if expertises else profile.expertises
        )
        profile.skills = profile.skills.extend(skills) if skills else profile.skills
        profile.languages = (
            profile.languages.extend(languages) if languages else profile.languages
        )
        profile.social_links = (
            profile.social_links.extend(social_links)
            if social_links
            else profile.social_links
        )

        # remove duplicates
        profile.expertises = list(set(profile.expertises))
        profile.skills = list(set(profile.skills))
        profile.languages = list(set(profile.languages))
        profile.social_links = list(set(profile.social_links))

        # save changes
        profile.updated_at = func.now()
        self.session.add(profile)

    async def register_expertise(
        self,
        user_id: UUID,
        expertise_names: list[ExpertiseName] | ExpertiseName,
    ) -> None:
        """
        Register an expertise

        :param user_id: id of the profile owner.
        :param expertise_names: expertise name.
        """
        profile = await self.get_profile(user_id=user_id)  # get the profile

        # edit profile
        profile.expertises = (
            profile.expertises.append(expertise_names)
            if type(expertise_names) == "str"
            else profile.expertises.extend(expertise_names)
        )

        # remove duplicates
        profile.expertises = list(set(profile.expertises))

        # save profile
        profile.updated_at = func.now()
        self.session.add(profile)

    async def remove_expertise(
        self,
        user_id: UUID,
        expertise_names: list[ExpertiseName] | ExpertiseName,
    ) -> None:
        """
        Register an expertise

        :param user_id: id of the profile owner.
        :param expertise_names: expertise name.
        """
        profile = await self.get_profile(user_id=user_id)  # get the profile

        # edit profile
        for expertise in profile.expertises:
            if expertise == expertise_names or expertise in expertise_names:
                profile.expertises.remove(expertise)

        # save profile
        profile.updated_at = func.now()
        self.session.add(profile)

    async def register_skill(
        self,
        user_id: UUID,
        skill_names: list[SkillName] | SkillName,
    ) -> None:
        """
        Register a skill

        :param user_id: id of the profile owner.
        :param skill_names: skill names.
        """
        profile = await self.get_profile(user_id=user_id)  # get the profile

        # edit profile
        profile.skills = (
            profile.skills.append(skill_names)
            if type(skill_names) == "str"
            else profile.skills.extend(skill_names)
        )

        # remove duplicates
        profile.skills = list(set(profile.skills))

        # save profile
        profile.updated_at = func.now()
        self.session.add(profile)

    async def remove_expertise(
        self,
        user_id: UUID,
        skill_names: list[SkillName] | SkillName,
    ) -> None:
        """
        Register an skill

        :param user_id: id of the profile owner.
        :param skill_names: skill name.
        """
        profile = await self.get_profile(user_id=user_id)  # get the profile

        # edit profile
        for skill in profile.skills:
            if skill == skill_names or skill in skill_names:
                profile.skills.remove(skill)

        # save profile
        profile.updated_at = func.now()
        self.session.add(profile)

    async def register_language(
        self,
        user_id: UUID,
        language_names: list[list[LanguageName, LanguageLevel]]
        | list[LanguageName, LanguageLevel],
    ) -> None:
        """
        Register a language

        :param user_id: id of the profile owner.
        :param language_names: language names.
        """
        profile = await self.get_profile(user_id=user_id)  # get the profile

        # edit profile
        profile.languages = (
            profile.languages.append(language_names)
            if type(language_names[0]) == LanguageName
            else profile.languages.extend(language_names)
        )

        # remove duplicates
        profile.languages = list(set(profile.languages))

        # save profile
        profile.updated_at = func.now()
        self.session.add(profile)

    async def remove_language(
        self,
        user_id: UUID,
        language_name: LanguageName,
    ) -> None:
        """
        Remove a language

        :param user_id: id of the profile owner.
        :param language_name: skill name.
        """
        profile = await self.get_profile(user_id=user_id)  # get the profile

        # edit profile
        for language in profile.languages:
            if language[0] == language_name:
                profile.languages.remove(language)

        # save profile
        profile.updated_at = func.now()
        self.session.add(profile)

    async def register_social_link(
        self,
        user_id: UUID,
        social_links: list[list[Platform, HttpUrl]],
    ) -> None:
        """
        Register a social link

        :param user_id: id of the profile owner.
        :param social_links: social links.
        """
        profile = await self.get_profile(user_id=user_id)  # get the profile

        # edit profile
        profile.social_links = (
            profile.social_links.append(social_links)
            if type(social_links[0]) == Platform
            else profile.social_links.extend(social_links)
        )

        # remove duplicates
        profile.social_links = list(set(profile.social_links))

        # save profile
        profile.updated_at = func.now()
        self.session.add(profile)

    async def remove_language(
        self,
        user_id: UUID,
        language_name: LanguageName,
    ) -> None:
        """
        Remove a language

        :param user_id: id of the profile owner.
        :param language_name: skill name.
        """
        profile = await self.get_profile(user_id=user_id)  # get the profile

        # edit profile
        for language in profile.languages:
            if language[0] == language_name:
                profile.languages.remove(language)

        # save profile
        profile.updated_at = func.now()
        self.session.add(profile)

    async def filter(
        self,
        first_name: Optional[str] = None,
    ) -> List[Profile]:
        """
        Get specific profile.

        :param first_name: first name of the user.
        :return: profiles.
        """
        query = select(Profile)
        if first_name:
            query = query.where(Profile.first_name == first_name)
        rows = await self.session.execute(query)
        return list(rows.scalars().fetchall())
