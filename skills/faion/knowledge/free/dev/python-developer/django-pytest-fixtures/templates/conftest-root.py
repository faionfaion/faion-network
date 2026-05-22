"""
purpose: root conftest.py — API client fixtures + autouse settings overrides.
consumes: factory registrations from tests/factories/.
produces: api_client, authenticated_client, admin_client, autouse media_root fixtures.
depends-on: pytest-django, factory-boy, pytest-factoryboy, rest_framework.
token-budget-impact: ~260 tokens.
"""

from __future__ import annotations

from collections.abc import Iterator
from pathlib import Path

import pytest
from rest_framework.test import APIClient


@pytest.fixture
def api_client() -> APIClient:
    """Unauthenticated DRF client. Per-test scope (default)."""
    return APIClient()


@pytest.fixture
def authenticated_client(api_client: APIClient, user) -> Iterator[APIClient]:
    """DRF client authenticated as `user` via force_authenticate; cleaned up after each test."""
    api_client.force_authenticate(user=user)
    yield api_client
    api_client.force_authenticate(user=None)


@pytest.fixture
def admin_client(api_client: APIClient, admin_user) -> Iterator[APIClient]:
    """DRF client authenticated as admin user."""
    api_client.force_authenticate(user=admin_user)
    yield api_client
    api_client.force_authenticate(user=None)


@pytest.fixture(autouse=True)
def media_root(tmp_path: Path, settings) -> Path:
    """Per-test MEDIA_ROOT so file uploads do not pollute the repo."""
    settings.MEDIA_ROOT = str(tmp_path / "media")
    Path(settings.MEDIA_ROOT).mkdir(parents=True, exist_ok=True)
    return tmp_path / "media"
