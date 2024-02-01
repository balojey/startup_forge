from datetime import date
from uuid import UUID
from typing import Optional

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.sql import func
from sqlalchemy.ext.asyncio import AsyncSession

from startup_forge.db.dependencies import get_db_session
from startup_forge.db.models.review import Review
from startup_forge.db.models.options import Role


class ReviewDAO:
    """Class for accessing review table."""

    def __init__(self, session: AsyncSession = Depends(get_db_session)):
        self.session = session

    async def record_review(self, user_id: UUID, mentor_id: UUID, content: str) -> None:
        """
        Add single review to session.

        :param user_id: id of the user.
        :param mentor_id: id of mentor to be reviewed.
        :param content: content of review.
        """
        self.session.add(
            Review(
                user_id=user_id,
                mentor_id=mentor_id,
                content=content,
            )
        )

    async def update_review(self, review_id: UUID, content: str) -> None:
        """
        Update an review.

        :param review_id: review id.
        :param content: content of review.
        """

        review = await self.get_review(review_id=review_id)  # get the review

        # edit review
        review.content = content if content else review.content

        # save changes
        review.updated_at = func.now()
        self.session.add(review)

    async def get_review(self, review_id: UUID) -> Review | None:
        """
        Get a particular review.

        :param review_id: id of the review.
        :return: a review.
        """
        review = await self.session.execute(
            select(Review).where(Review.id == review_id),
        )

        return review.scalars().first()

    async def get_reviews(self, user_id: UUID, role: Role) -> Review | None:
        """
        Get a particular review.

        :param review_id: id of the review.
        :param role: role of user.
        :return: a review.
        """
        review = (
            await self.session.execute(
                select(Review).where(Review.user_id == user_id),
            )
            if role == Role.MENTEE
            else await self.session.execute(
                select(Review).where(Review.mentor_id == user_id),
            )
        )

        return list(review.scalars().fetchall())

    async def delete_review(self, review_id: UUID) -> None:
        """
        Delete a particular review.

        :param review_id: id of the review.
        """
        review = await self.get_review(review_id=review_id)  # get review

        # delete review
        await self.session.delete(review)

    async def delete_reviews(self, reviews: list[Review]) -> None:
        """
        Delete a reviews.

        :param reviews: list of the reviews.
        """
        for review in reviews:
            await self.session.delete(review)  # delete review

    async def filter(
        self,
        content: Optional[str] = None,
    ) -> list[Review] | None:
        """
        Get specific review.

        :param content: content of review.
        :return: a list of Review.
        """
        query = select(Review)
        if content:
            query = query.where(content in Review.content)
        rows = await self.session.execute(query)
        return list(rows.scalars().fetchall())
