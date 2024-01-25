from uuid import UUID
from typing import List, Optional

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import func

from startup_forge.db.dependencies import get_db_session
from startup_forge.db.models.profile import Profile
from startup_forge.db.models.options import Role


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
        role: Optional[Role] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
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
        profile.role = role if role else profile.role
        profile.first_name = first_name if first_name else profile.first_name
        profile.last_name = last_name if last_name else profile.last_name
        profile.updated_at = func.now()

        # save profile
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
