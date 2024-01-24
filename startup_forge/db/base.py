from sqlalchemy.orm import DeclarativeBase

from startup_forge.db.meta import meta


class Base(DeclarativeBase):
    """Base for all models."""

    metadata = meta
