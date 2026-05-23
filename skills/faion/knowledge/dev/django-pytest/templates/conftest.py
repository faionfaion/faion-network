# purpose: pytest-django conftest with db + factories + APIClient.
# consumes: project repo; see the methodology AGENTS.md for input contract.
# produces: the working artifact described above; placement: Place at tests/conftest.py.
# depends-on: the tooling pinned in the methodology's AGENTS.md.
# token-budget-impact: zero — local-only template; build/CI time is the only cost.
"""
Minimal root conftest.py for Django + pytest projects.
Copy to tests/conftest.py, add project-specific fixtures as needed.
"""
import socket
import pytest
from rest_framework.test import APIClient


@pytest.fixture
def api_client() -> APIClient:
    """Unauthenticated DRF API test client."""
    return APIClient()


@pytest.fixture
def user(db):
    """Basic test user. Replace UserFactory with your factory."""
    from apps.users.tests.factories import UserFactory
    return UserFactory()


@pytest.fixture
def auth_client(api_client, user) -> APIClient:
    """API client authenticated as the default test user."""
    api_client.force_authenticate(user=user)
    return api_client


@pytest.fixture(autouse=True)
def _disable_external_calls(monkeypatch):
    """Block real network calls in all tests. Fail loudly instead of timing out."""
    def guard(*args, **kwargs):
        raise RuntimeError(
            "Network access in tests is forbidden. Mock the dependency."
        )
    monkeypatch.setattr(socket, "create_connection", guard)
