# tests/conftest.py — reusable Django + DRF + baker fixtures.
import datetime as dt

import pytest
from model_bakery import baker
from rest_framework.test import APIClient


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user(db):
    return baker.make("users.User", is_active=True)


@pytest.fixture
def staff_user(db):
    return baker.make("users.User", is_active=True, is_staff=True)


@pytest.fixture
def authed_client(api_client, user):
    api_client.force_authenticate(user=user)
    return api_client


@pytest.fixture(autouse=True)
def _reset_outbound_email(settings):
    settings.EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"


@pytest.fixture
def freeze_now(monkeypatch):
    """Freeze django.utils.timezone.now to a fixed instant."""
    from django.utils import timezone

    fixed = dt.datetime(2026, 1, 1, 12, 0, tzinfo=dt.timezone.utc)
    monkeypatch.setattr(timezone, "now", lambda: fixed)
    return fixed
