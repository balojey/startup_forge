from datetime import datetime
from uuid import UUID

from sqlalchemy import ForeignKey, Enum, PrimaryKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from sqlalchemy.sql.sqltypes import Uuid, DateTime

from startup_forge.db.base import Base
from startup_forge.db.models.options import ConnectionRequestStatus


class ConnectionRequest(Base):
    """Model for connection request."""

    __tablename__ = "connection_request"

    request_from: Mapped[UUID] = mapped_column(
        Uuid(), ForeignKey("user.id", ondelete="CASCADE", onupdate="CASCADE")
    )
    request_to: Mapped[UUID] = mapped_column(
        Uuid(), ForeignKey("user.id", ondelete="CASCADE", onupdate="CASCADE")
    )
    requested_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=func.now()
    )
    status: Mapped[ConnectionRequestStatus] = mapped_column(
        Enum(ConnectionRequestStatus), default=ConnectionRequestStatus.PENDING
    )

    PrimaryKeyConstraint(request_from, request_to)


class Connection(Base):
    """Model for connection."""

    __tablename__ = "connection"

    request_from: Mapped[UUID] = mapped_column(
        Uuid(), ForeignKey("user.id", ondelete="CASCADE", onupdate="CASCADE")
    )
    request_to: Mapped[UUID] = mapped_column(
        Uuid(), ForeignKey("user.id", ondelete="CASCADE", onupdate="CASCADE")
    )
    accepted_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=func.now()
    )

    PrimaryKeyConstraint(request_from, request_to)
