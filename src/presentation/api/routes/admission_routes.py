"""
Admission API routes.

Endpoints for admission evaluation and management.
"""
from fastapi import APIRouter

router = APIRouter(
    prefix="/api/v1/admission",
    tags=["admission"],
)


@router.get("/")
async def get_admission_info() -> dict[str, str]:
    """Placeholder endpoint for admission API."""
    return {"message": "Admission API"}
