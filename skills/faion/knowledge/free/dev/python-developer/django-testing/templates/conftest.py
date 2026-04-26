"""
Shared fixtures: api_client, authed_client, staff_client, factory registration, db autouse.
Add to tests/conftest.py.
"""

import pytest
from pytest_factoryboy import register
from rest_framework.test import APIClient

# ─── Factory registration ────────────────────────────────────────────────────
# Register creates both `model` (instance) and `model_factory` fixtures
# from tests/factories.py
#
# Example factories to register (adjust to your project):
# from tests.factories import UserFactory, OrganizationFactory, OrderFactory
# register(OrganizationFactory)  # → organization, organization_factory
# register(UserFactory)           # → user, user_factory
# register(OrderFactory)          # → order, order_factory


# ─── Database autouse (optional) ─────────────────────────────────────────────
# Uncomment to grant DB access to ALL tests without @pytest.mark.django_db
# Use only if the vast majority of tests need DB access.
#
# @pytest.fixture(autouse=True)
# def enable_db_access_for_all_tests(db):
#     pass


# ─── API client fixtures ──────────────────────────────────────────────────────

@pytest.fixture
def api_client() -> APIClient:
    """Unauthenticated DRF API client."""
    return APIClient()


@pytest.fixture
def authed_client(user) -> APIClient:
    """
    Authenticated client for the auto-created `user` fixture.
    Requires UserFactory to be registered above.
    """
    client = APIClient()
    client.force_authenticate(user=user)
    return client


@pytest.fixture
def staff_client(user_factory) -> APIClient:
    """
    Authenticated client for a staff user.
    Requires UserFactory to be registered with a `staff` Trait.
    """
    staff_user = user_factory(is_staff=True)
    client = APIClient()
    client.force_authenticate(user=staff_user)
    return client


@pytest.fixture
def admin_client_drf(user_factory) -> APIClient:
    """
    Authenticated client for a superuser (Django admin).
    """
    admin_user = user_factory(is_staff=True, is_superuser=True)
    client = APIClient()
    client.force_authenticate(user=admin_user)
    return client


# ─── Utility fixtures ─────────────────────────────────────────────────────────

@pytest.fixture
def authed_client_for(user_factory):
    """
    Factory fixture: returns a function that creates an authed client for any user.

    Usage:
        def test_foo(authed_client_for, user_factory):
            client = authed_client_for(user_factory(is_staff=True))
    """
    def _make(user) -> APIClient:
        client = APIClient()
        client.force_authenticate(user=user)
        return client
    return _make
