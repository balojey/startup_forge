from datetime import date
from uuid import UUID
from typing import List, Optional

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.sql import func
from sqlalchemy.ext.asyncio import AsyncSession

from startup_forge.db.dependencies import get_db_session
from startup_forge.db.models.experience import Experience
from startup_forge.db.models.options import Role, Industry


class ExperienceDAO:
    """Class for accessing experience table."""

    def __init__(self, session: AsyncSession = Depends(get_db_session)):
        self.session = session

    async def create_experience(
        self,
        user_id: UUID,
        company_name: str,
        start_date: date,
        industry: Industry,
        description: Optional[str] = None,
        end_date: Optional[date] = None,
    ) -> None:
        """
        Add single experience to session.

        :param user_id: id of the user registering the experience.
        :param company_name: name of company.
        :param description: what the company is about.
        :param start_date: the date the company was started.
        :param end_date: the date the company ended.
        :param industry: the industry in which the company thrived.
        """
        self.session.add(
            Experience(
                user_id=user_id,
                company_name=company_name,
                description=description,
                start_date=start_date,
                end_date=end_date,
                industry=industry,
            )
        )

    async def get_experiences(self, user_id: UUID) -> list[Experience] | None:
        """
        Get a stream of experience.

        :param user_id: id of the user.
        :return: stream of experience.
        """
        profile = await self.session.execute(
            select(Experience).where(Experience.user_id == user_id),
        )

        return list(profile.scalars().fetchall())

    async def get_experience(self, experience_id: UUID) -> Experience | None:
        """
        Get a particular experience.

        :param experience_id: id of the experience.
        :return: an experience.
        """
        profile = await self.session.execute(
            select(Experience).where(Experience.id == experience_id),
        )

        return profile.scalars().first()

    async def update_experience(
        self,
        experience_id: UUID,
        company_name: Optional[str] = None,
        description: Optional[str] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        industry: Optional[Industry] = None,
    ) -> None:
        """
        Update a specific experience

        :param experience_id: id of the experience.
        :param company_name: name of company.
        :param description: what the company is about.
        :param start_date: the date the company was started.
        :param end_date: the date the company ended.
        :param industry: the industry in which the company thrived.
        """
        experience = await self.get_experience(
            experience_id=experience_id
        )  # get experience

        # edit experience
        experience.company_name = (
            company_name if company_name else experience.company_name
        )
        experience.description = description if description else experience.description
        experience.start_date = start_date if start_date else experience.start_date
        experience.end_date = end_date if end_date else experience.end_date
        experience.industry = industry if industry else experience.industry

        # save experience
        experience.updated_at = func.now()
        self.session.add(experience)

    async def delete_experience(self, experience_id: UUID) -> None:
        """
        Delete a particular experience.

        :param experience_id: id of the experience.
        """
        experience = await self.get_experience(
            experience_id=experience_id
        )  # get experience

        # delete experience
        await self.session.delete(experience)

    async def delete_experiences(self, experiences: list[Experience]) -> None:
        """
        Delete a experiences.

        :param experiences: list of the experiences.
        """
        for experience in experiences:
            await self.session.delete(experience)  # delete experience

    async def filter(
        self,
        company_name: Optional[str] = None,
    ) -> list[Experience] | None:
        """
        Get specific experience.

        :param company_name: name of company.
        :return: experiences.
        """
        query = select(Experience)
        if company_name:
            query = query.where(Experience.company_name == company_name)
        rows = await self.session.execute(query)
        return list(rows.scalars().fetchall())
