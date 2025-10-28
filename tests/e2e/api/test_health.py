"""
E2E tests for health and placeholder endpoints.

Tests the FastAPI application startup and basic endpoint functionality.
"""
from fastapi.testclient import TestClient

from src.presentation.api.main import app

client = TestClient(app)


def test_health_endpoint_returns_ok() -> None:
    """Test that health endpoint returns 200 OK."""
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_admission_placeholder_endpoint() -> None:
    """Test admission placeholder endpoint."""
    response = client.get("/api/v1/admission/")

    assert response.status_code == 200
    assert response.json() == {"message": "Admission API"}


def test_students_placeholder_endpoint() -> None:
    """Test students placeholder endpoint."""
    response = client.get("/api/v1/students/")

    assert response.status_code == 200
    assert response.json() == {"message": "Student API"}


def test_quotas_placeholder_endpoint() -> None:
    """Test quotas placeholder endpoint."""
    response = client.get("/api/v1/quotas/")

    assert response.status_code == 200
    assert response.json() == {"message": "Quota API"}


def test_cors_headers_present() -> None:
    """Test that CORS headers are configured."""
    response = client.options(
        "/health",
        headers={
            "Origin": "http://localhost:5173",
            "Access-Control-Request-Method": "GET",
        },
    )

    assert response.status_code == 200
    assert "access-control-allow-origin" in response.headers
