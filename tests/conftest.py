"""
Shared pytest fixtures for all tests.

This file provides common test fixtures and configuration used across
unit, integration, and e2e tests.
"""
import pytest


@pytest.fixture
def sample_fixture() -> str:
    """Example fixture - will be replaced with real fixtures as needed."""
    return "test"
