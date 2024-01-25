from uuid import UUID
from typing import List, Optional

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import func

from startup_forge.db.dependencies import get_db_session
from startup_forge.db.models.profile import Profile
from startup_forge.db.dao.profile_dao import ProfileDAO
from startup_forge.db.models.mentor_mentee import MentorMentee
from startup_forge.db.models.mentor_mentee_history import MentorMenteeHistory
from startup_forge.db.models.experience import Experience
from startup_forge.db.models.options import Role, RelatedIndustry


class MentorMenteeDAO:
    """Class for accessing profile table."""

    def __init__(self, session: AsyncSession = Depends(get_db_session)):
        self.session = session

    async def create_match(self, user_id: UUID, mentor_id: UUID) -> None:
        """
        Match a mentee to a mentor.

        :param user_id: id of the user initiating the match.
        :param mentor_id: profile id of the mentor.
        """
        self.session.add(MentorMentee(mentee_id=user_id, mentor_id=mentor_id))

    async def unmatch(
        self,
        user_id: UUID,
        mentor_comment: Optional[str] = None,
        mentee_comment: Optional[str] = None,
    ) -> None:
        """
        Unmatch a mentee from it's mentor

        :param user_id: id of the profile.
        """
        result = await self.session.execute(
            select(MentorMentee).where(MentorMentee.mentee_id == user_id)
        )
        match = result.scalars().first()
        mentor_mentee_history = MentorMenteeHistory(
            mentor_id=match.mentor_id,
            mentee_id=match.mentee_id,
            start_date=match.start_date,
            mentor_comment=mentor_comment,
            mentee_comment=mentee_comment,
            triggered_by=Role.MENTEE,
        )
        await self.session.delete(match)
        self.session.add(mentor_mentee_history)

    async def get_matches(self, user_id: UUID, role: Role) -> list[MentorMentee]:
        """
        Get mentor_mentees instances related to of a specific user

        :param user_id: id of the current user.
        :return: MentorMentee instance.
        """
        if role == Role.MENTEE:
            mentor_mentee = await self.session.execute(
                select(MentorMentee).where(MentorMentee.mentee_id == user_id)
            )
            return mentor_mentee.scalars().first()
        mentor_mentees = await self.session.execute(
            select(MentorMentee).where(MentorMentee.mentor_id == user_id)
        )
        return list(mentor_mentees.scalars().fetchall())

    async def match_mentees_to_mentors(
        self, mentee: Profile
    ) -> list[tuple[Profile, float]]:
        """
        Get compatible mentors for a mentee

        :param mentee: profile of mentee
        :return: list of tuple comprised of the profile data and a compatibility percentage
        """
        mentors = await self.session.execute(
            select(Profile).where(Profile.role == Role.MENTOR)
        )  # get all mentors
        mentors = list(mentors.scalars().fetchall())

        # Calculate compatibility percentage based on industry match
        matches: list[tuple[Profile, float]] = []

        mentee_experiences = await self.session.execute(
            select(Experience).where(
                Experience.user_id == mentee.user_id and Experience.end_date == None
            )
        )
        mentee_experiences = mentee_experiences.scalars().fetchall()

        for mentor in mentors:
            mentor_experiences = await self.session.execute(
                select(Experience).where(Experience.user_id == mentor.user_id)
            )
            mentor_experiences = list(mentor_experiences.scalars().fetchall())

            common_industries = set(exp.industry for exp in mentor_experiences) & set(
                mentee_exp.industry for mentee_exp in mentee_experiences
            )

            related_industries = []
            related_industries.extend(
                RelatedIndustry[mentor_exp.industry.name]
                for mentor_exp in mentor_experiences
            )
            related_industries = set(related_industries[0])

            mentee_related_industries = []
            mentee_related_industries.extend(
                RelatedIndustry[mentee_exp.industry.name]
                for mentee_exp in mentee_experiences
            )
            common_related_industries = related_industries & set(
                mentee_related_industries[0]
            )

            compatibility = (
                len(common_industries) + len(common_related_industries)
            ) / (len(mentee_experiences) * 2)
            matches.append((mentor, compatibility))

        return matches
