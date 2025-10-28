"""
Dependency injection for FastAPI routes.

Provides dependencies for database sessions and use cases.
"""
from src.infrastructure.persistence import get_db_session

# Re-export for convenience
__all__ = ["get_db_session"]
