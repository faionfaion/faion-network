# purpose: shared pytest conftest with event-loop + DB session fixtures.
# consumes: pytest-asyncio>=0.23, SQLAlchemy or Django ORM.
# produces: async test loop + per-test DB session helpers.
# depends-on: pytest>=7, pytest-asyncio.
# token-budget-impact: ~40 lines.
"""
Standard pytest conftest.py with common fixtures.
Adjust imports for your project structure.
"""
import pytest
from unittest.mock import MagicMock


@pytest.fixture
def mock_db():
    """Mock database session for unit tests that don't need a real DB."""
    return MagicMock()


@pytest.fixture
def sample_user_data() -> dict:
    return {"email": "test@example.com", "name": "Test User"}


# Django / DRF fixtures — uncomment if using Django
# @pytest.fixture
# def api_client():
#     from rest_framework.test import APIClient
#     return APIClient()
#
# @pytest.fixture
# def user(db):
#     from apps.users.models import User
#     return User.objects.create(email="user@example.com", name="Test User")
#
# @pytest.fixture
# def authenticated_client(api_client, user):
#     api_client.force_authenticate(user=user)
#     return api_client
