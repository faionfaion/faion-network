"""
purpose: Shared pytest fixtures: api_client, authed_client, staff_client, factory registration.
consumes: 01-core-rules.xml
produces: code
depends-on: content/01-core-rules.xml
token-budget-impact: small
"""

import datetime as dt

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


# --- model_bakery alternative -------------------------------------------------
# Projects that chose baker over factory_boy (rule r4) drop the register() calls
# above and use these instead. Pick ONE path per project, never both.
#
# from model_bakery import baker
#
# @pytest.fixture
# def user(db):
#     return baker.make("users.User", is_active=True)
#
# @pytest.fixture
# def staff_user(db):
#     return baker.make("users.User", is_active=True, is_staff=True)


@pytest.fixture(autouse=True)
def _capture_outbound_email(settings):
    """Mail never leaves the process, in any test, without opting out."""
    settings.EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"


@pytest.fixture
def freeze_now(monkeypatch):
    """Freeze django.utils.timezone.now to a fixed instant."""
    from django.utils import timezone

    fixed = dt.datetime(2026, 1, 1, 12, 0, tzinfo=dt.timezone.utc)
    monkeypatch.setattr(timezone, "now", lambda: fixed)
    return fixed
