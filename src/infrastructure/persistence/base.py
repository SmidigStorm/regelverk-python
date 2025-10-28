"""
SQLAlchemy declarative base for ORM models.

All ORM models should inherit from Base.
"""
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Base class for all ORM models."""
    pass
