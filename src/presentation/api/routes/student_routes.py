"""
Student API routes.

Endpoints for student management.
"""
from fastapi import APIRouter

router = APIRouter(
    prefix="/api/v1/students",
    tags=["students"],
)


@router.get("/")
async def get_students_info() -> dict[str, str]:
    """Placeholder endpoint for students API."""
    return {"message": "Student API"}
