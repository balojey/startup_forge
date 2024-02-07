from datetime import date, time
from uuid import UUID
from typing import Optional

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.sql import func
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import HttpUrl

from startup_forge.db.dependencies import get_db_session
from startup_forge.db.models.community import Post, Comment, CommentReply, Repost, Like
from startup_forge.db.models.options import Day, BookingStatus, BookingStatus2, Role


class CommunityDAO:
    """Class for accessing community table."""

    def __init__(self, session: AsyncSession = Depends(get_db_session)):
        self.session = session

    async def create_post(
        self,
        user_id: UUID,
        text: Optional[str] = None,
        files_urls: Optional[list[HttpUrl]] = None,
    ) -> Post:
        """
        Add single post to session.

        :param user_id: id of the user registering the time_slot.
        :param text: post's textual content.
        :param files_urls: urls of files.
        :return: a post.
        """
        post = Post(
            user_id=user_id,
            text=text,
            files_urls=files_urls,
        )
        self.session.add(post)
        return post

    async def create_repost(
        self, post_id: UUID, repost_id: Optional[UUID] = None
    ) -> None:
        """
        Add single repost to session.

        :param post_id: original post's id.
        :param repost_id: repost's id.
        """
        self.session.add(
            Repost(
                post_id=post_id,
                repost_id=repost_id,
            )
        )

    async def update_post(self, post_id: UUID, text: str) -> None:
        """
        Add single repost to session.

        :param post_id: original post's id.
        :param repost_id: repost's id.
        """
        post = await self.get_post(post_id=post_id)
        post.text = text

        # save
        post.updated_at = func.now()
        self.session.add(post)

    async def get_post(
        self,
        post_id: UUID,
    ) -> Post | None:
        """
        Get a post.

        :param post_id: original post's id.
        :return: a post.
        """
        post = await self.session.execute(select(Post).where(Post.id == post_id))

        return post.scalars().first()

    async def get_posts(
        self,
        user_id: Optional[UUID] = None,
    ) -> list[Post] | None:
        """
        Get a posts.

        :param user_id: user's id.
        :return: a stream of post.
        """
        posts = (
            await self.session.execute(select(Post))
            if not user_id
            else await self.session.execute(select(Post).where(Post.user_id == user_id))
        )

        return list(posts.scalars().fetchall())

    async def delete_post(
        self,
        post_id: UUID,
    ) -> None:
        """
        Delete a post.

        :param post_id: original post's id.
        """
        post = await self.get_post(post_id=post_id)

        await self.session.delete(post)

    async def create_comment(
        self,
        user_id: UUID,
        content: str,
        post_id: UUID,
    ) -> Comment:
        """
        Add single comment to session.

        :param user_id: id of the user registering the time_slot.
        :param content: comments's content.
        :return: a comment.
        """
        comment = Comment(
            user_id=user_id,
            content=content,
            post_id=post_id,
        )
        self.session.add(comment)
        return comment

    async def create_reply(
        self, comment_id: UUID, reply_id: Optional[UUID] = None
    ) -> None:
        """
        Add single comment_reply to session.

        :param comment_id: original comment's id.
        :param reply_id: reply's id.
        """
        self.session.add(
            CommentReply(
                comment_id=comment_id,
                reply_id=reply_id,
            )
        )

    async def update_comment(self, comment_id: UUID, content: str) -> None:
        """
        Update a comment.

        :param comment_id: original post's id.
        :param content: comment's content.
        """
        comment = await self.get_comment(comment_id=comment_id)
        comment.content = content

        # save
        comment.updated_at = func.now()
        self.session.add(comment)

    async def get_comment(
        self,
        comment_id: UUID,
    ) -> Comment | None:
        """
        Get a comment.

        :param comment_id: original comment's id.
        :return: a comment.
        """
        comment = await self.session.execute(
            select(Comment).where(Comment.id == comment_id)
        )

        return comment.scalars().first()

    async def get_comments(
        self,
        post_id: UUID,
    ) -> list[Comment] | None:
        """
        Get a comments.

        :param post_id: original post's id.
        :return: a stream of comments.
        """
        comments = await self.session.execute(
            select(Comment).where(Comment.post_id == post_id)
        )

        return list(comments.scalars().fetchall())

    async def get_my_comments(
        self,
        user_id: UUID,
    ) -> list[Comment] | None:
        """
        Get a comments.

        :param user_id: user's id.
        :return: a stream of comments.
        """
        comments = await self.session.execute(
            select(Comment).where(Comment.user_id == user_id)
        )

        return list(comments.scalars().fetchall())

    async def delete_comment(
        self,
        comment_id: UUID,
    ) -> None:
        """
        Delete a comment.

        :param comment_id: original comment's id.
        """
        comment = await self.get_comment(comment_id=comment_id)

        await self.session.delete(comment)

    async def like_unlike(self, post_id: UUID, user_id: UUID) -> None:
        """
        Like and unlike a comment

        :param post_id: original post id.
        :param user_id: user's id.
        """
        like = await self.get_like(post_id=post_id, user_id=user_id)
        if like:
            await self.session.delete(like)  # unlike
            return
        self.session.add(
            Like(
                post_id=post_id,
                user_id=user_id,
            )
        )

    async def get_like(self, post_id: UUID, user_id: UUID) -> Like | None:
        """
        Get a like

        :param post_id: original post id.
        :param user_id: user's id.
        :return: a like.
        """

        like = await self.session.execute(
            select(Like).where(Like.post_id == post_id and Like.user_id == user_id)
        )

        return like.scalars().first()
