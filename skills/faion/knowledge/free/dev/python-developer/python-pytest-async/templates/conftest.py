"""
purpose: Async fixtures: async_client, app_client (FastAPI via ASGITransport), async database fixture.
consumes: 01-core-rules.xml
produces: code
depends-on: content/01-core-rules.xml
token-budget-impact: small
"""

import pytest
from pytest_factoryboy import register


# Register your factories here:
# from tests.factories import UserFactory
# register(UserFactory)


@pytest.fixture
def api_client():
    """DRF APIClient (override per project)."""
    from rest_framework.test import APIClient

    return APIClient()


@pytest.fixture
def authed_client(api_client, user):
    api_client.force_authenticate(user=user)
    return api_client


@pytest.fixture
def staff_client(api_client, user_factory):
    staff_user = user_factory(is_staff=True)
    api_client.force_authenticate(user=staff_user)
    return api_client
