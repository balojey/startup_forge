from uuid import UUID

from sqlalchemy import ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.sqltypes import Uuid, String, Text, ARRAY

from startup_forge.db.base import Base
from startup_forge.db.models.base_model import BaseModel


class Post(BaseModel, Base):
    """Model for post."""

    __tablename__ = "post"

    user_id: Mapped[UUID] = mapped_column(
        Uuid(), ForeignKey("user.id", ondelete="CASCADE", onupdate="CASCADE")
    )
    text: Mapped[str] = mapped_column(Text(), nullable=True)
    files_urls: Mapped[list[str]] = mapped_column(ARRAY(String), nullable=True)

    comments: Mapped[list["Comment"]] = relationship("Comment", back_populates="post")
    likes: Mapped[list["Like"]] = relationship("Like", back_populates="post")


class Comment(BaseModel, Base):
    """Model for comment."""

    __tablename__ = "comment"

    user_id: Mapped[UUID] = mapped_column(
        Uuid(), ForeignKey("user.id", ondelete="CASCADE", onupdate="CASCADE")
    )
    post_id: Mapped[UUID] = mapped_column(
        Uuid(), ForeignKey("post.id", ondelete="CASCADE", onupdate="CASCADE")
    )
    content: Mapped[str] = mapped_column(Text(), nullable=False)

    post: Mapped["Post"] = relationship("Post", back_populates="comments")


class Like(Base):
    """Model for like."""

    __tablename__ = "like"

    user_id: Mapped[UUID] = mapped_column(
        Uuid(), ForeignKey("user.id", ondelete="CASCADE", onupdate="CASCADE")
    )
    post_id: Mapped[UUID] = mapped_column(
        Uuid(), ForeignKey("post.id", ondelete="CASCADE", onupdate="CASCADE")
    )

    post: Mapped["Post"] = relationship("Post", back_populates="likes")

    PrimaryKeyConstraint(user_id, post_id)


class CommentReply(Base):
    """Model for comment reply."""

    __tablename__ = "comment_reply"

    comment_id: Mapped[UUID] = mapped_column(
        Uuid(), ForeignKey("comment.id", ondelete="CASCADE", onupdate="CASCADE")
    )
    reply_id: Mapped[UUID] = mapped_column(
        Uuid(),
        ForeignKey("comment.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=True,
    )

    PrimaryKeyConstraint(comment_id, reply_id)


class Repost(Base):
    """Model for repost."""

    __tablename__ = "repost"

    post_id: Mapped[UUID] = mapped_column(
        Uuid(), ForeignKey("post.id", ondelete="CASCADE", onupdate="CASCADE")
    )
    repost_id: Mapped[UUID] = mapped_column(
        Uuid(), ForeignKey("post.id", ondelete="CASCADE", onupdate="CASCADE")
    )

    PrimaryKeyConstraint(post_id, repost_id)
