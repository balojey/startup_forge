from datetime import date
from uuid import UUID
from typing import Optional

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.sql import func
from sqlalchemy.ext.asyncio import AsyncSession

from startup_forge.db.dependencies import get_db_session
from startup_forge.db.models.education import Education
from startup_forge.db.models.options import Industry


class EducationDAO:
    """Class for accessing education table."""

    def __init__(self, session: AsyncSession = Depends(get_db_session)):
        self.session = session

    async def record_education(
        self,
        user_id: UUID,
        institution_name: str,
        course_of_study: str,
        start_date: date,
        state: str,
        country: Optional[str] = None,
        end_date: Optional[date] = None,
    ) -> None:
        """
        Add single experience to session.

        :param user_id: id of the user registering the education.
        :param institution_name: name of institution.
        :param course_of_study: course of study.
        :param state: the state in which the institution is located.
        :param start_date: the date the user enrolled in the institution.
        :param end_date: the date the user left the institution.
        :param country: the country in which the institution is located.
        """
        self.session.add(
            Education(
                user_id=user_id,
                institution_name=institution_name,
                course_of_study=course_of_study,
                start_date=start_date,
                end_date=end_date,
                state=state,
                country=country,
            )
        )

    async def update_education(
        self,
        education_id: UUID,
        institution_name: Optional[str] = None,
        course_of_study: Optional[str] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        state: Optional[str] = None,
        country: Optional[str] = None,
    ) -> None:
        """
        Update an education.

        :param education_id: education id.
        :param institution_name: name of institution.
        :param course_of_study: course of study.
        :param state: the state in which the institution is located.
        :param start_date: the date the user enrolled in the institution.
        :param end_date: the date the user left the institution.
        :param country: the country in which the institution is located.
        """

        education = await self.get_education(
            education_id=education_id
        )  # get the education

        # edit education
        education.institution_name = (
            institution_name if institution_name else education.institution_name
        )
        education.course_of_study = (
            course_of_study if course_of_study else education.course_of_study
        )
        education.state = state if state else education.state
        education.country = country if country else education.country
        education.start_date = start_date if start_date else education.start_date
        education.end_date = end_date if end_date else education.end_date

        # save changes
        education.updated_at = func.now()
        self.session.add(education)

    async def get_education(self, education_id: UUID) -> Education | None:
        """
        Get a particular education.

        :param education_id: id of the education.
        :return: an education.
        """
        education = await self.session.execute(
            select(Education).where(Education.id == education_id),
        )

        return education.scalars().first()

    async def get_educations(
        self,
        user_id: UUID,
    ) -> list[Education] | None:
        """
        Get a user's educations.

        :param user_id: id of the user.
        :return: a list of education.
        """
        educations = await self.session.execute(
            select(Education).where(Education.user_id == user_id),
        )

        return list(educations.scalars().fetchall())

    async def delete_education(self, education_id: UUID) -> None:
        """
        Delete a particular education.

        :param education_id: id of the education.
        """
        education = await self.get_education(education_id=education_id)  # get education

        # delete education
        await self.session.delete(education)

    async def delete_educations(self, educations: list[Education]) -> None:
        """
        Delete a educations.

        :param educations: list of the educations.
        """
        for education in educations:
            await self.session.delete(education)  # delete education

    async def filter(
        self,
        institution_name: Optional[str] = None,
    ) -> list[Education] | None:
        """
        Get specific ducation.

        :param institution_name: name of institution.
        :return: Educations.
        """
        query = select(Education)
        if institution_name:
            query = query.where(Education.institution_name == institution_name)
        rows = await self.session.execute(query)
        return list(rows.scalars().fetchall())
