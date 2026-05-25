"""
purpose: config/settings/test.py — Django settings overrides for fast pytest runs.
consumes: config/settings/base.py.
produces: in-memory SQLite, MD5 hasher, locmem email, eager Celery.
depends-on: base settings module.
token-budget-impact: ~180 tokens.
"""

from .base import *  # noqa: F401,F403

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

# ~200x faster than the production bcrypt hasher.
PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]

EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"

# Run Celery tasks synchronously inside the test process.
CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_EAGER_PROPAGATES = True

# locmem cache — never hit Redis from tests.
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
    }
}

# MEDIA_ROOT is overridden per-test via an autouse fixture (see conftest.py).
DEBUG = False
ALLOWED_HOSTS = ["*"]
