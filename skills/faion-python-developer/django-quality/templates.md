# Django Quality Templates

Copy-paste configurations for Django code quality tools.

## Ruff Configuration (Replaces Black, isort, Flake8)

```toml
# pyproject.toml

[tool.ruff]
target-version = "py312"
line-length = 88
exclude = [
    ".git",
    ".mypy_cache",
    ".ruff_cache",
    ".venv",
    "__pycache__",
    "migrations",
    "node_modules",
]

[tool.ruff.lint]
select = [
    "E",      # pycodestyle errors
    "W",      # pycodestyle warnings
    "F",      # Pyflakes
    "I",      # isort
    "B",      # flake8-bugbear
    "C4",     # flake8-comprehensions
    "UP",     # pyupgrade
    "ARG",    # flake8-unused-arguments
    "SIM",    # flake8-simplify
    "TCH",    # flake8-type-checking
    "PTH",    # flake8-use-pathlib
    "ERA",    # eradicate (commented-out code)
    "PL",     # Pylint
    "RUF",    # Ruff-specific rules
]
ignore = [
    "E501",   # Line too long (handled by formatter)
    "B008",   # Do not perform function calls in argument defaults (needed for DI)
    "B904",   # Allow raise without from (common in Django)
    "PLR0913", # Too many arguments
    "PLR2004", # Magic value comparison
]

[tool.ruff.lint.per-file-ignores]
"tests/**/*.py" = [
    "ARG",    # Unused arguments in tests (fixtures)
    "PLR2004", # Magic values in tests
]
"**/migrations/*.py" = [
    "E501",   # Line too long in migrations
]

[tool.ruff.lint.isort]
known-first-party = ["myproject", "apps"]
known-third-party = ["django", "rest_framework"]
section-order = [
    "future",
    "standard-library",
    "django",
    "third-party",
    "first-party",
    "local-folder",
]

[tool.ruff.lint.isort.sections]
"django" = ["django", "rest_framework"]

[tool.ruff.format]
quote-style = "double"
indent-style = "space"
skip-magic-trailing-comma = false
line-ending = "auto"
```

## mypy Configuration

```toml
# pyproject.toml

[tool.mypy]
python_version = "3.12"
plugins = ["mypy_django_plugin.main", "mypy_drf_plugin.main"]
strict = true
warn_return_any = true
warn_unused_ignores = true
disallow_untyped_defs = true
disallow_incomplete_defs = true
check_untyped_defs = true
disallow_untyped_decorators = true
no_implicit_optional = true
warn_redundant_casts = true
warn_unused_configs = true
show_error_codes = true
show_column_numbers = true

# Per-module overrides
[[tool.mypy.overrides]]
module = "*.migrations.*"
ignore_errors = true

[[tool.mypy.overrides]]
module = [
    "celery.*",
    "kombu.*",
    "redis.*",
]
ignore_missing_imports = true

[tool.django-stubs]
django_settings_module = "config.settings"
```

## Pre-commit Configuration

```yaml
# .pre-commit-config.yaml

default_language_version:
  python: python3.12

repos:
  # Ruff - linting and formatting
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.9.2
    hooks:
      - id: ruff
        args: [--fix, --exit-non-zero-on-fix]
      - id: ruff-format

  # mypy - type checking
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.14.1
    hooks:
      - id: mypy
        additional_dependencies:
          - django-stubs[compatible-mypy]
          - djangorestframework-stubs[compatible-mypy]
          - types-requests
        args: [--config-file=pyproject.toml]

  # Security checks
  - repo: https://github.com/PyCQA/bandit
    rev: 1.8.2
    hooks:
      - id: bandit
        args: [-c, pyproject.toml]
        additional_dependencies: ["bandit[toml]"]

  # Django checks
  - repo: local
    hooks:
      - id: django-check
        name: Django system checks
        entry: python manage.py check
        language: system
        types: [python]
        pass_filenames: false

  # pytest
  - repo: local
    hooks:
      - id: pytest
        name: pytest
        entry: pytest --tb=short -q
        language: system
        types: [python]
        pass_filenames: false
        stages: [pre-push]
```

## pytest Configuration

```toml
# pyproject.toml

[tool.pytest.ini_options]
DJANGO_SETTINGS_MODULE = "config.settings.test"
python_files = ["test_*.py", "*_test.py"]
addopts = [
    "--strict-markers",
    "--strict-config",
    "-ra",
    "--tb=short",
    "--cov=apps",
    "--cov-report=term-missing:skip-covered",
    "--cov-report=html",
    "--cov-fail-under=80",
]
filterwarnings = [
    "error",
    "ignore::DeprecationWarning",
    "ignore::django.utils.deprecation.RemovedInDjango60Warning",
]
markers = [
    "slow: marks tests as slow",
    "integration: marks tests as integration tests",
]
```

## Django Settings Templates

### Base Settings

```python
# config/settings/base.py
import environ
from pathlib import Path

env = environ.Env()

BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Read .env file
environ.Env.read_env(BASE_DIR / ".env")

# Security
SECRET_KEY = env("SECRET_KEY")
DEBUG = env.bool("DEBUG", default=False)
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=[])

# Application definition
DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

THIRD_PARTY_APPS = [
    "rest_framework",
    "corsheaders",
    "django_filters",
]

LOCAL_APPS = [
    "apps.users",
    "apps.core",
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# Middleware
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django_structlog.middlewares.RequestMiddleware",
]

# Database
DATABASES = {
    "default": env.db("DATABASE_URL", default="sqlite:///db.sqlite3")
}
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Cache
CACHES = {
    "default": env.cache("CACHE_URL", default="locmemcache://")
}

# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Logging (structured)
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "json": {
            "()": "pythonjsonlogger.jsonlogger.JsonFormatter",
            "format": "%(asctime)s %(levelname)s %(name)s %(message)s",
        },
        "verbose": {
            "format": "{levelname} {asctime} {module} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": env("DJANGO_LOG_LEVEL", default="INFO"),
            "propagate": False,
        },
        "django.db.backends": {
            "level": "WARNING",
        },
    },
}
```

### Development Settings

```python
# config/settings/development.py
from .base import *  # noqa: F401, F403

DEBUG = True
ALLOWED_HOSTS = ["localhost", "127.0.0.1", "0.0.0.0"]

# Debug Toolbar
INSTALLED_APPS += ["debug_toolbar"]
MIDDLEWARE.insert(0, "debug_toolbar.middleware.DebugToolbarMiddleware")
INTERNAL_IPS = ["127.0.0.1"]

# Debug Toolbar settings
DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TOOLBAR_CALLBACK": lambda request: DEBUG,
    "SHOW_COLLAPSED": True,
}

# Email backend
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# CORS
CORS_ALLOW_ALL_ORIGINS = True

# Logging - more verbose in development
LOGGING["handlers"]["console"]["formatter"] = "verbose"
LOGGING["root"]["level"] = "DEBUG"
```

### Production Settings

```python
# config/settings/production.py
from .base import *  # noqa: F401, F403

DEBUG = False

# Security settings
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"

# HSTS
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Content Security Policy (Django 6.0+)
MIDDLEWARE.insert(1, "django.middleware.csp.ContentSecurityPolicyMiddleware")
CONTENT_SECURITY_POLICY = {
    "default-src": ["'self'"],
    "script-src": ["'self'"],
    "style-src": ["'self'", "'unsafe-inline'"],
    "img-src": ["'self'", "data:", "https:"],
    "font-src": ["'self'", "https://fonts.gstatic.com"],
    "connect-src": ["'self'"],
    "frame-ancestors": ["'none'"],
    "form-action": ["'self'"],
}

# Logging - JSON format for production
LOGGING["handlers"]["console"]["formatter"] = "json"

# Sentry
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.celery import CeleryIntegration
from sentry_sdk.integrations.redis import RedisIntegration

sentry_sdk.init(
    dsn=env("SENTRY_DSN"),
    integrations=[
        DjangoIntegration(),
        CeleryIntegration(),
        RedisIntegration(),
    ],
    traces_sample_rate=0.1,
    profiles_sample_rate=0.1,
    send_default_pii=False,
    environment=env("ENVIRONMENT", default="production"),
)
```

### Test Settings

```python
# config/settings/test.py
from .base import *  # noqa: F401, F403

DEBUG = False

# Use faster password hasher in tests
PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]

# Use in-memory SQLite for faster tests
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

# Use local memory cache
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
    }
}

# Disable migrations for faster tests
class DisableMigrations:
    def __contains__(self, item):
        return True

    def __getitem__(self, item):
        return None


MIGRATION_MODULES = DisableMigrations()

# Email backend
EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
```

## Environment Variables Template

```bash
# .env.example

# Django
SECRET_KEY=your-secret-key-here
DEBUG=false
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DATABASE_URL=postgres://user:pass@localhost:5432/dbname

# Cache
CACHE_URL=redis://localhost:6379/0

# Celery
CELERY_BROKER_URL=redis://localhost:6379/1

# Email
EMAIL_URL=smtp://user:pass@smtp.example.com:587
DEFAULT_FROM_EMAIL=noreply@example.com

# Sentry
SENTRY_DSN=https://xxx@sentry.io/xxx
ENVIRONMENT=development

# AWS (if using S3)
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_STORAGE_BUCKET_NAME=
AWS_S3_REGION_NAME=
```

## Django Debug Toolbar Configuration

```python
# config/settings/development.py

# Only add Debug Toolbar in development
if DEBUG:
    INSTALLED_APPS += ["debug_toolbar"]
    MIDDLEWARE.insert(0, "debug_toolbar.middleware.DebugToolbarMiddleware")

    # Show toolbar for these IPs
    INTERNAL_IPS = ["127.0.0.1"]

    # Docker support
    import socket
    hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
    INTERNAL_IPS += [".".join(ip.split(".")[:-1] + ["1"]) for ip in ips]

    DEBUG_TOOLBAR_CONFIG = {
        "DISABLE_PANELS": [
            "debug_toolbar.panels.redirects.RedirectsPanel",
            "debug_toolbar.panels.profiling.ProfilingPanel",
        ],
        "SHOW_TEMPLATE_CONTEXT": True,
        "SHOW_TOOLBAR_CALLBACK": lambda request: DEBUG and not request.is_ajax(),
        "SHOW_COLLAPSED": True,
        "SQL_WARNING_THRESHOLD": 100,  # ms
    }

    DEBUG_TOOLBAR_PANELS = [
        "debug_toolbar.panels.history.HistoryPanel",
        "debug_toolbar.panels.versions.VersionsPanel",
        "debug_toolbar.panels.timer.TimerPanel",
        "debug_toolbar.panels.settings.SettingsPanel",
        "debug_toolbar.panels.headers.HeadersPanel",
        "debug_toolbar.panels.request.RequestPanel",
        "debug_toolbar.panels.sql.SQLPanel",
        "debug_toolbar.panels.staticfiles.StaticFilesPanel",
        "debug_toolbar.panels.templates.TemplatesPanel",
        "debug_toolbar.panels.cache.CachePanel",
        "debug_toolbar.panels.signals.SignalsPanel",
        "debug_toolbar.panels.logging.LoggingPanel",
    ]
```

## Structured Logging Configuration

```python
# config/settings/base.py

import structlog

# Structlog configuration
structlog.configure(
    processors=[
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
    ],
    logger_factory=structlog.stdlib.LoggerFactory(),
    cache_logger_on_first_use=True,
)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "json": {
            "()": structlog.stdlib.ProcessorFormatter,
            "processor": structlog.processors.JSONRenderer(),
        },
        "console": {
            "()": structlog.stdlib.ProcessorFormatter,
            "processor": structlog.dev.ConsoleRenderer(),
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "console" if DEBUG else "json",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
        "django.db.backends": {
            "handlers": ["console"],
            "level": "WARNING",
            "propagate": False,
        },
        "django.request": {
            "handlers": ["console"],
            "level": "ERROR",
            "propagate": False,
        },
        "celery": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
    },
}
```

## Bandit Security Configuration

```toml
# pyproject.toml

[tool.bandit]
exclude_dirs = ["tests", "migrations", ".venv"]
skips = [
    "B101",  # assert_used - OK in tests
    "B104",  # hardcoded_bind_all_interfaces - handled by deployment
]

[tool.bandit.assert_used]
skips = ["**/test_*.py", "**/tests.py"]
```

## Coverage Configuration

```toml
# pyproject.toml

[tool.coverage.run]
source = ["apps"]
branch = true
omit = [
    "*/migrations/*",
    "*/tests/*",
    "*/__init__.py",
    "*/admin.py",
]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise AssertionError",
    "raise NotImplementedError",
    "if __name__ == .__main__.:",
    "if TYPE_CHECKING:",
    "if settings.DEBUG:",
    "@abstractmethod",
]
fail_under = 80
show_missing = true
skip_covered = true

[tool.coverage.html]
directory = "htmlcov"
```

## Makefile for Common Tasks

```makefile
# Makefile

.PHONY: help install lint format test migrate run clean

help:
	@echo "Available commands:"
	@echo "  install    - Install dependencies"
	@echo "  lint       - Run linters"
	@echo "  format     - Format code"
	@echo "  test       - Run tests"
	@echo "  migrate    - Run migrations"
	@echo "  run        - Run development server"
	@echo "  clean      - Clean cache files"

install:
	pip install -r requirements/development.txt
	pre-commit install

lint:
	ruff check .
	mypy .
	python manage.py check

format:
	ruff check --fix .
	ruff format .

test:
	pytest

test-cov:
	pytest --cov --cov-report=html

migrate:
	python manage.py makemigrations
	python manage.py migrate

run:
	python manage.py runserver

shell:
	python manage.py shell_plus

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .mypy_cache .pytest_cache .ruff_cache htmlcov .coverage

check-deploy:
	python manage.py check --deploy
```
