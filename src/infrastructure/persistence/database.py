"""
Database engine and session management.

Provides SQLAlchemy engine, session factory, and FastAPI dependency for database sessions.
"""
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from src.infrastructure.config import settings

# Create engine with SQLAlchemy 2.0 style
engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    future=True,
)

# Session factory
SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)


def get_db_session() -> Generator[Session, None, None]:
    """
    FastAPI dependency for database sessions.

    Yields a database session and ensures it's closed after use.
    """
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
