# Monolith Architecture Templates

Copy-paste configurations and code templates for monolith applications.

## Directory Structure Templates

### Python/Django Modular Monolith

```
project_name/
    manage.py
    pyproject.toml

    config/
        __init__.py
        settings/
            __init__.py
            base.py
            local.py
            production.py
            test.py
        urls.py
        wsgi.py
        asgi.py

    modules/
        __init__.py

        users/
            __init__.py          # Public API exports
            public/
                __init__.py
                api.py           # Public functions
                events.py        # Domain events
                types.py         # DTOs
            internal/
                __init__.py
                models.py
                services.py
                repository.py
                selectors.py
            migrations/
            tests/
                __init__.py
                test_services.py
                test_api.py
                conftest.py

        orders/
            __init__.py
            public/
            internal/
            migrations/
            tests/

    shared/
        __init__.py
        exceptions.py
        utils.py
        middleware.py

    api/
        __init__.py
        v1/
            __init__.py
            urls.py
            views/
            serializers/

    infrastructure/
        __init__.py
        cache.py
        email.py
        storage.py
```

### Python/FastAPI Vertical Slices

```
app/
    main.py
    pyproject.toml

    config/
        __init__.py
        settings.py
        database.py
        dependencies.py

    features/
        __init__.py

        users/
            __init__.py
            router.py
            models.py
            schemas.py
            service.py
            repository.py
            tests/

        products/
            __init__.py
            router.py
            models.py
            schemas.py
            service.py
            repository.py
            tests/

    shared/
        __init__.py
        base_model.py
        exceptions.py
        security.py
```

### Node.js/TypeScript Modular

```
src/
    index.ts
    app.ts

    config/
        index.ts
        database.ts
        env.ts

    modules/
        users/
            index.ts              # Public exports
            user.controller.ts
            user.service.ts
            user.repository.ts
            user.model.ts
            user.dto.ts
            user.routes.ts
            __tests__/

        orders/
            index.ts
            order.controller.ts
            order.service.ts
            order.repository.ts
            order.model.ts
            order.dto.ts
            order.routes.ts
            __tests__/

    shared/
        index.ts
        middleware/
        exceptions/
        utils/

    infrastructure/
        database/
        cache/
        queue/
```

### Go Modular Monolith

```
cmd/
    server/
        main.go

internal/
    config/
        config.go
        env.go

    modules/
        users/
            handler.go
            service.go
            repository.go
            model.go
            dto.go
            routes.go

        orders/
            handler.go
            service.go
            repository.go
            model.go
            dto.go
            routes.go

    shared/
        middleware/
        errors/
        utils/

    infrastructure/
        database/
        cache/
        queue/

pkg/
    # Public packages (if any)

migrations/
    001_create_users.sql
    002_create_orders.sql
```

---

## Configuration Templates

### Django Settings (base.py)

```python
# config/settings/base.py
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = os.environ.get('SECRET_KEY', 'change-me-in-production')

DEBUG = False

ALLOWED_HOSTS = []

# Application definition
INSTALLED_APPS = [
    # Django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third party
    'rest_framework',
    'corsheaders',
    'django_extensions',

    # Local modules
    'modules.users',
    'modules.orders',
    'modules.payments',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'shared.middleware.RequestLoggingMiddleware',
]

ROOT_URLCONF = 'config.urls'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME', 'app'),
        'USER': os.environ.get('DB_USER', 'postgres'),
        'PASSWORD': os.environ.get('DB_PASSWORD', ''),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '5432'),
        'CONN_MAX_AGE': 60,
        'OPTIONS': {
            'connect_timeout': 10,
        },
    }
}

# Cache
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': os.environ.get('REDIS_URL', 'redis://localhost:6379/0'),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        },
    }
}

# REST Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/hour',
        'user': '1000/hour',
    },
}

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'json': {
            '()': 'pythonjsonlogger.jsonlogger.JsonFormatter',
            'format': '%(asctime)s %(levelname)s %(name)s %(message)s',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'json',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'WARNING',
            'propagate': False,
        },
        'modules': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}
```

### FastAPI Configuration

```python
# config/settings.py
from functools import lru_cache
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Application
    app_name: str = "My App"
    debug: bool = False
    environment: str = "production"

    # Database
    database_url: str = "postgresql://localhost/app"
    database_pool_size: int = 5
    database_max_overflow: int = 10

    # Redis
    redis_url: str = "redis://localhost:6379/0"

    # Security
    secret_key: str
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7

    # CORS
    cors_origins: list[str] = ["http://localhost:3000"]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

@lru_cache()
def get_settings() -> Settings:
    return Settings()

# config/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from config.settings import get_settings

settings = get_settings()

engine = create_engine(
    settings.database_url,
    pool_size=settings.database_pool_size,
    max_overflow=settings.database_max_overflow,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

---

## Docker Templates

### Dockerfile (Python)

```dockerfile
# Dockerfile
FROM python:3.12-slim as builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt

# Production image
FROM python:3.12-slim

WORKDIR /app

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN useradd -m -u 1000 app

# Copy wheels and install
COPY --from=builder /app/wheels /wheels
RUN pip install --no-cache /wheels/*

# Copy application
COPY --chown=app:app . .

USER app

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"

EXPOSE 8000

CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "4"]
```

### Docker Compose (Development)

```yaml
# docker-compose.yml
version: '3.8'

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    environment:
      - DEBUG=true
      - DATABASE_URL=postgresql://postgres:postgres@db:5432/app
      - REDIS_URL=redis://redis:6379/0
      - SECRET_KEY=dev-secret-key
    volumes:
      - .:/app
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_started
    command: python manage.py runserver 0.0.0.0:8000

  db:
    image: postgres:16
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres
      - POSTGRES_DB=app
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

  celery:
    build: .
    command: celery -A config worker -l info
    environment:
      - DATABASE_URL=postgresql://postgres:postgres@db:5432/app
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - db
      - redis
    volumes:
      - .:/app

  celery-beat:
    build: .
    command: celery -A config beat -l info
    environment:
      - DATABASE_URL=postgresql://postgres:postgres@db:5432/app
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - db
      - redis

volumes:
  postgres_data:
  redis_data:
```

### Docker Compose (Production)

```yaml
# docker-compose.prod.yml
version: '3.8'

services:
  app:
    image: ${IMAGE_NAME}:${IMAGE_TAG}
    deploy:
      replicas: 3
      update_config:
        parallelism: 1
        delay: 10s
        failure_action: rollback
      restart_policy:
        condition: on-failure
        max_attempts: 3
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - REDIS_URL=${REDIS_URL}
      - SECRET_KEY=${SECRET_KEY}
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    logging:
      driver: json-file
      options:
        max-size: "10m"
        max-file: "3"

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./ssl:/etc/nginx/ssl:ro
    depends_on:
      - app
```

---

## Nginx Configuration

### Basic Reverse Proxy

```nginx
# nginx.conf
upstream app {
    server app:8000;
    keepalive 32;
}

server {
    listen 80;
    server_name example.com;

    # Redirect HTTP to HTTPS
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl http2;
    server_name example.com;

    ssl_certificate /etc/nginx/ssl/cert.pem;
    ssl_certificate_key /etc/nginx/ssl/key.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256;
    ssl_prefer_server_ciphers off;

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;

    # Gzip compression
    gzip on;
    gzip_vary on;
    gzip_proxied any;
    gzip_comp_level 6;
    gzip_types text/plain text/css text/xml application/json application/javascript;

    # Static files
    location /static/ {
        alias /app/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    # Media files
    location /media/ {
        alias /app/media/;
        expires 7d;
    }

    # Health check (no logging)
    location /health {
        access_log off;
        proxy_pass http://app;
    }

    # API
    location / {
        proxy_pass http://app;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header Connection "";

        # Timeouts
        proxy_connect_timeout 30s;
        proxy_send_timeout 30s;
        proxy_read_timeout 30s;

        # Buffering
        proxy_buffering on;
        proxy_buffer_size 4k;
        proxy_buffers 8 4k;
    }
}
```

### Load Balancer Configuration

```nginx
# nginx-lb.conf
upstream app_cluster {
    least_conn;  # Load balancing method

    server app1:8000 weight=5;
    server app2:8000 weight=5;
    server app3:8000 weight=5;

    keepalive 64;
}

server {
    listen 80;

    location / {
        proxy_pass http://app_cluster;
        proxy_http_version 1.1;
        proxy_set_header Connection "";

        # Health checks
        proxy_next_upstream error timeout http_502 http_503 http_504;
        proxy_next_upstream_tries 3;
    }

    # Health check endpoint (for load balancer itself)
    location /nginx-health {
        access_log off;
        return 200 "healthy\n";
        add_header Content-Type text/plain;
    }
}
```

---

## Database Migration Templates

### Alembic Configuration

```python
# alembic/env.py
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
import os

config = context.config

# Override sqlalchemy.url from environment
config.set_main_option('sqlalchemy.url', os.environ.get('DATABASE_URL'))

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Import all models for autogenerate
from app.features.users.models import User
from app.features.orders.models import Order
from app.shared.base_model import Base

target_metadata = Base.metadata

def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
```

### Migration Example

```python
# alembic/versions/001_create_users.py
"""create users table

Revision ID: 001
Create Date: 2025-01-25
"""
from alembic import op
import sqlalchemy as sa

revision = '001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.UUID(), primary_key=True),
        sa.Column('email', sa.String(255), unique=True, nullable=False),
        sa.Column('password_hash', sa.String(255), nullable=False),
        sa.Column('is_active', sa.Boolean(), default=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), onupdate=sa.func.now()),
    )

    op.create_index('idx_users_email', 'users', ['email'])

def downgrade():
    op.drop_index('idx_users_email')
    op.drop_table('users')
```

---

## CI/CD Templates

### GitHub Actions

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

env:
  PYTHON_VERSION: "3.12"
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  test:
    runs-on: ubuntu-latest

    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_USER: test
          POSTGRES_PASSWORD: test
          POSTGRES_DB: test
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432

      redis:
        image: redis:7
        ports:
          - 6379:6379

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ env.PYTHON_VERSION }}
          cache: pip

      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install -r requirements-dev.txt

      - name: Lint
        run: |
          ruff check .
          ruff format --check .

      - name: Type check
        run: mypy .

      - name: Run tests
        env:
          DATABASE_URL: postgresql://test:test@localhost:5432/test
          REDIS_URL: redis://localhost:6379/0
          SECRET_KEY: test-secret-key
        run: |
          pytest --cov=. --cov-report=xml

      - name: Upload coverage
        uses: codecov/codecov-action@v4
        with:
          file: ./coverage.xml

  build:
    needs: test
    runs-on: ubuntu-latest
    if: github.event_name == 'push'

    permissions:
      contents: read
      packages: write

    steps:
      - uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Log in to registry
        uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
          tags: |
            type=ref,event=branch
            type=sha,prefix=

      - name: Build and push
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max

  deploy:
    needs: build
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    environment: production

    steps:
      - name: Deploy to production
        run: |
          # Add deployment script here
          echo "Deploying to production..."
```

---

## Health Check Templates

### FastAPI Health Check

```python
# api/health.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from redis import Redis
from config.database import get_db
from config.cache import get_redis

router = APIRouter()

@router.get("/health")
async def health():
    """Basic liveness check."""
    return {"status": "healthy"}

@router.get("/health/ready")
async def readiness(
    db: Session = Depends(get_db),
    redis: Redis = Depends(get_redis)
):
    """Readiness check with dependency verification."""
    checks = {}

    # Database check
    try:
        db.execute("SELECT 1")
        checks["database"] = "healthy"
    except Exception as e:
        checks["database"] = f"unhealthy: {str(e)}"

    # Redis check
    try:
        redis.ping()
        checks["redis"] = "healthy"
    except Exception as e:
        checks["redis"] = f"unhealthy: {str(e)}"

    # Overall status
    all_healthy = all(v == "healthy" for v in checks.values())

    return {
        "status": "healthy" if all_healthy else "unhealthy",
        "checks": checks
    }

@router.get("/health/live")
async def liveness():
    """Kubernetes liveness probe."""
    return {"status": "alive"}
```

### Django Health Check

```python
# shared/health.py
from django.http import JsonResponse
from django.db import connection
from django.core.cache import cache
import redis

def health(request):
    """Basic health check."""
    return JsonResponse({"status": "healthy"})

def readiness(request):
    """Readiness check with dependencies."""
    checks = {}

    # Database
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        checks["database"] = "healthy"
    except Exception as e:
        checks["database"] = f"unhealthy: {str(e)}"

    # Cache/Redis
    try:
        cache.set("health_check", "ok", timeout=1)
        if cache.get("health_check") == "ok":
            checks["cache"] = "healthy"
        else:
            checks["cache"] = "unhealthy: cache read failed"
    except Exception as e:
        checks["cache"] = f"unhealthy: {str(e)}"

    all_healthy = all(v == "healthy" for v in checks.values())

    return JsonResponse({
        "status": "healthy" if all_healthy else "unhealthy",
        "checks": checks
    }, status=200 if all_healthy else 503)
```

---

## Logging Templates

### Structured Logging Setup

```python
# shared/logging.py
import logging
import structlog
from pythonjsonlogger import jsonlogger

def configure_logging(debug: bool = False):
    """Configure structured logging for production."""

    # Configure structlog
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.processors.JSONRenderer() if not debug else structlog.dev.ConsoleRenderer(),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(
            logging.DEBUG if debug else logging.INFO
        ),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=True,
    )

    # Configure standard library logging
    handler = logging.StreamHandler()
    handler.setFormatter(jsonlogger.JsonFormatter(
        '%(asctime)s %(levelname)s %(name)s %(message)s'
    ))

    logging.basicConfig(
        level=logging.DEBUG if debug else logging.INFO,
        handlers=[handler]
    )

# Usage
logger = structlog.get_logger()

logger.info(
    "order_created",
    order_id="ord_123",
    user_id="usr_456",
    total=99.99
)
```

---

## Module Public API Template

```python
# modules/users/__init__.py
"""
Users module - manages user accounts and authentication.

Public API:
- create_user(email, password) -> UserDTO
- get_user(user_id) -> UserDTO
- authenticate(email, password) -> TokenDTO
- UserCreated event

Do not import from internal/ directly.
"""

from modules.users.public.api import (
    create_user,
    get_user,
    get_user_by_email,
    authenticate,
    update_user,
    delete_user,
)
from modules.users.public.events import (
    UserCreated,
    UserUpdated,
    UserDeleted,
)
from modules.users.public.types import (
    UserDTO,
    TokenDTO,
    CreateUserInput,
    UpdateUserInput,
)

__all__ = [
    # Functions
    "create_user",
    "get_user",
    "get_user_by_email",
    "authenticate",
    "update_user",
    "delete_user",
    # Events
    "UserCreated",
    "UserUpdated",
    "UserDeleted",
    # Types
    "UserDTO",
    "TokenDTO",
    "CreateUserInput",
    "UpdateUserInput",
]
```

```python
# modules/users/public/api.py
"""Public API for users module."""

from modules.users.internal.services import UserService
from modules.users.public.types import UserDTO, CreateUserInput

_service = UserService()

def create_user(input: CreateUserInput) -> UserDTO:
    """Create a new user account."""
    return _service.create_user(input)

def get_user(user_id: str) -> UserDTO:
    """Get user by ID."""
    return _service.get_user(user_id)

def get_user_by_email(email: str) -> UserDTO | None:
    """Get user by email address."""
    return _service.get_user_by_email(email)
```

```python
# modules/users/public/types.py
"""Public types for users module."""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass(frozen=True)
class UserDTO:
    """User data transfer object."""
    id: str
    email: str
    name: Optional[str]
    created_at: datetime
    is_active: bool

@dataclass(frozen=True)
class CreateUserInput:
    """Input for creating a user."""
    email: str
    password: str
    name: Optional[str] = None

@dataclass(frozen=True)
class TokenDTO:
    """Authentication token."""
    access_token: str
    refresh_token: str
    expires_in: int
```

```python
# modules/users/public/events.py
"""Domain events for users module."""

from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True)
class UserCreated:
    """Emitted when a new user is created."""
    user_id: str
    email: str
    timestamp: datetime

@dataclass(frozen=True)
class UserUpdated:
    """Emitted when user data is updated."""
    user_id: str
    changes: dict
    timestamp: datetime

@dataclass(frozen=True)
class UserDeleted:
    """Emitted when a user is deleted."""
    user_id: str
    timestamp: datetime
```
