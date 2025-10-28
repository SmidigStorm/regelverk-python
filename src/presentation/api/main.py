"""
FastAPI application entry point.

Main application setup with middleware, routes, and configuration.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.infrastructure.config import settings
from src.presentation.api.routes import admission_routes, quota_routes, student_routes

# Create FastAPI application
app = FastAPI(
    title="Norwegian Admission Rules API",
    description="API for Norwegian higher education admission rules system",
    version="0.1.0",
    debug=settings.DEBUG,
)

# CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Health check endpoint
@app.get("/health", tags=["health"])
async def health_check() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "ok"}


# Include routers
app.include_router(admission_routes.router)
app.include_router(student_routes.router)
app.include_router(quota_routes.router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "src.presentation.api.main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.DEBUG,
    )
