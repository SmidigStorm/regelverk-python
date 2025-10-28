"""
Quota API routes.

Endpoints for quota management.
"""
from fastapi import APIRouter

router = APIRouter(
    prefix="/api/v1/quotas",
    tags=["quotas"],
)


@router.get("/")
async def get_quotas_info() -> dict[str, str]:
    """Placeholder endpoint for quotas API."""
    return {"message": "Quota API"}
