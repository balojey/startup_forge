from datetime import datetime
from uuid import UUID
from typing import Optional

from pydantic import BaseModel, ConfigDict, HttpUrl


class PostDTO(BaseModel):
    """
    DTO for profiles.

    It is returned when accessing profile from the API.
    """

    id: UUID
    user_id: UUID
    text: Optional[str]
    files_urls: Optional[HttpUrl]
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)


class PostInputDTO(BaseModel):
    """DTO for creating post."""

    text: Optional[str]
    files_urls: Optional[HttpUrl]
    post_id: Optional[UUID] = None


class PostUpdateDTO(BaseModel):
    """DTO for updating post."""

    text: Optional[str]
    files_urls: Optional[HttpUrl]


class CommentDTO(BaseModel):
    """
    DTO for comment.

    It is returned when accessing comment from the API.
    """

    id: UUID
    user_id: UUID
    content: Optional[str]
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)


class CommentInputDTO(BaseModel):
    """DTO for creating comment."""

    content: str
    comment_id: Optional[UUID] = None


class CommentUpdateDTO(CommentInputDTO):
    """DTO for updating comment."""

    pass
