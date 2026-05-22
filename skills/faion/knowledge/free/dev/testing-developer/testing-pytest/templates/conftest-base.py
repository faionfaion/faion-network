# purpose: TBD-template-header
# consumes: input from methodology
# produces: output artefact
# depends-on: 01-core-rules.xml
# token-budget-impact: small

"""
Base conftest.py — adapt for your project stack.
Provides: db session, API client, user factory, settings override.
"""
import pytest


# ---- Settings override (Django example) ----

@pytest.fixture(scope="session")
def django_db_setup():
    """Use a test database. Override DB settings if needed."""
    pass  # pytest-django handles this automatically


# ---- Database transaction isolation ----

@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    """Allow DB access in all tests without @pytest.mark.django_db."""
    pass


# ---- API client ----

@pytest.fixture
def api_client():
    """Django REST Framework test client. Swap for httpx.AsyncClient for FastAPI."""
    from rest_framework.test import APIClient
    return APIClient()


@pytest.fixture
def auth_client(api_client, make_user):
    """Pre-authenticated API client."""
    user = make_user()
    api_client.force_authenticate(user=user)
    return api_client


# ---- User factory ----

@pytest.fixture
def make_user(db):
    """Factory fixture for creating User instances."""
    from django.contrib.auth import get_user_model
    User = get_user_model()
    created = []

    def factory(email="user@example.com", password="testpass123", role="user", **kwargs):
        user = User.objects.create_user(email=email, password=password, **kwargs)
        created.append(user)
        return user

    yield factory

    # Cleanup (optional — db fixture rolls back automatically in most setups)
    for user in created:
        user.delete()


# ---- Environment/settings override ----

@pytest.fixture(autouse=True)
def override_settings(settings):
    """Override settings for tests. Uses pytest-django's settings fixture."""
    settings.EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
    settings.CELERY_TASK_ALWAYS_EAGER = True
    settings.CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        }
    }


# ---- Async client (FastAPI/ASGI) ----

# @pytest.fixture
# async def async_client():
#     from httpx import AsyncClient, ASGITransport
#     from myapp.main import app
#     async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
#         yield client
