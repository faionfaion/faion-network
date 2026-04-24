# Python Web Frameworks - Project Templates

**Copy-paste project structures and boilerplate for Django, FastAPI, and Flask.**

---

## Django Project Template

### Directory Structure

```
project/
|-- config/                    # Django settings
|   |-- __init__.py
|   |-- settings/
|   |   |-- __init__.py
|   |   |-- base.py           # Common settings
|   |   |-- development.py    # Dev overrides
|   |   |-- production.py     # Prod overrides
|   |-- urls.py
|   |-- wsgi.py
|   |-- asgi.py
|
|-- apps/
|   |-- __init__.py
|   |-- users/
|   |   |-- __init__.py
|   |   |-- models.py
|   |   |-- views.py
|   |   |-- serializers.py
|   |   |-- services.py       # Business logic
|   |   |-- admin.py
|   |   |-- urls.py
|   |   |-- tests/
|   |   |   |-- __init__.py
|   |   |   |-- test_models.py
|   |   |   |-- test_views.py
|   |   |   |-- test_services.py
|   |   |-- migrations/
|   |
|   |-- core/                  # Shared utilities
|       |-- __init__.py
|       |-- models.py          # Base models
|       |-- permissions.py
|       |-- pagination.py
|
|-- manage.py
|-- pyproject.toml
|-- requirements/
|   |-- base.txt
|   |-- development.txt
|   |-- production.txt
|-- pytest.ini
|-- .env.example
|-- docker-compose.yml
|-- Dockerfile
```

### Settings Template

```python
# config/settings/base.py
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = os.environ.get('SECRET_KEY', 'change-me-in-production')

DEBUG = False

ALLOWED_HOSTS = []

# Application definition
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    'rest_framework',
    'corsheaders',
]

LOCAL_APPS = [
    'apps.core',
    'apps.users',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'
ASGI_APPLICATION = 'config.asgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME', 'app'),
        'USER': os.environ.get('DB_USER', 'postgres'),
        'PASSWORD': os.environ.get('DB_PASSWORD', 'postgres'),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

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
}
```

```python
# config/settings/development.py
from .base import *

DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

CORS_ALLOW_ALL_ORIGINS = True
```

```python
# config/settings/production.py
from .base import *
import os

DEBUG = False

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')

# Security settings
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

CORS_ALLOWED_ORIGINS = os.environ.get('CORS_ORIGINS', '').split(',')
```

### Base Model Template

```python
# apps/core/models.py
import uuid
from django.db import models


class BaseModel(models.Model):
    """Abstract base model with common fields."""
    uid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
```

### URLs Template

```python
# config/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include([
        path('users/', include('apps.users.urls')),
    ])),
]
```

### pyproject.toml

```toml
[project]
name = "myproject"
version = "0.1.0"
description = "Django API project"
requires-python = ">=3.11"

dependencies = [
    "django>=5.0",
    "djangorestframework>=3.14",
    "django-cors-headers>=4.3",
    "djangorestframework-simplejwt>=5.3",
    "psycopg[binary]>=3.1",
    "python-dotenv>=1.0",
    "gunicorn>=21.0",
    "uvicorn>=0.27",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0",
    "pytest-django>=4.7",
    "pytest-cov>=4.1",
    "factory-boy>=3.3",
    "ruff>=0.2",
    "mypy>=1.8",
    "django-stubs>=4.2",
]

[tool.pytest.ini_options]
DJANGO_SETTINGS_MODULE = "config.settings.development"
python_files = ["test_*.py"]
addopts = "-v --tb=short"

[tool.ruff]
line-length = 100
target-version = "py311"

[tool.mypy]
plugins = ["mypy_django_plugin.main"]
strict = true
```

### Docker Template

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements/production.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

# Run with gunicorn
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "4"]
```

```yaml
# docker-compose.yml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DJANGO_SETTINGS_MODULE=config.settings.production
      - SECRET_KEY=${SECRET_KEY}
      - DB_HOST=db
      - DB_NAME=app
      - DB_USER=postgres
      - DB_PASSWORD=postgres
    depends_on:
      - db

  db:
    image: postgres:16-alpine
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      - POSTGRES_DB=app
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres

volumes:
  postgres_data:
```

---

## FastAPI Project Template

### Directory Structure

```
project/
|-- app/
|   |-- __init__.py
|   |-- main.py               # FastAPI app
|   |-- config.py             # Settings
|   |-- dependencies.py       # DI dependencies
|   |
|   |-- routers/
|   |   |-- __init__.py
|   |   |-- users.py
|   |   |-- auth.py
|   |   |-- health.py
|   |
|   |-- schemas/
|   |   |-- __init__.py
|   |   |-- users.py
|   |   |-- auth.py
|   |   |-- common.py
|   |
|   |-- models/
|   |   |-- __init__.py
|   |   |-- base.py
|   |   |-- users.py
|   |
|   |-- services/
|   |   |-- __init__.py
|   |   |-- users.py
|   |   |-- auth.py
|   |
|   |-- db/
|   |   |-- __init__.py
|   |   |-- database.py
|   |   |-- session.py
|   |
|   |-- core/
|       |-- __init__.py
|       |-- security.py
|       |-- exceptions.py
|
|-- tests/
|   |-- __init__.py
|   |-- conftest.py
|   |-- test_users.py
|   |-- test_auth.py
|
|-- alembic/
|   |-- versions/
|   |-- env.py
|-- alembic.ini
|-- pyproject.toml
|-- .env.example
|-- docker-compose.yml
|-- Dockerfile
```

### Main Application Template

```python
# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.config import settings
from app.routers import users, auth, health
from app.db.database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    await init_db()
    yield


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description=settings.DESCRIPTION,
    lifespan=lifespan,
    docs_url="/api/docs" if settings.DEBUG else None,
    redoc_url="/api/redoc" if settings.DEBUG else None,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router, tags=["health"])
app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(users.router, prefix="/api/v1/users", tags=["users"])
```

### Config Template

```python
# app/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings."""
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )

    # Project
    PROJECT_NAME: str = "My API"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "FastAPI application"
    DEBUG: bool = False

    # Database
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/app"

    # Security
    SECRET_KEY: str = "change-me-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ALGORITHM: str = "HS256"

    # CORS
    CORS_ORIGINS: list[str] = ["http://localhost:3000"]


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
```

### Database Template

```python
# app/db/database.py
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

from app.config import settings

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    future=True,
)

async_session = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

Base = declarative_base()


async def init_db():
    """Initialize database."""
    async with engine.begin() as conn:
        # Only for development - use Alembic migrations in production
        if settings.DEBUG:
            await conn.run_sync(Base.metadata.create_all)
```

```python
# app/db/session.py
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import async_session


async def get_db() -> AsyncSession:
    """Database session dependency."""
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
```

### Base Model Template

```python
# app/models/base.py
from datetime import datetime
from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.orm import declared_attr

from app.db.database import Base


class BaseModel(Base):
    """Abstract base model."""
    __abstract__ = True

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower() + 's'
```

### Dependencies Template

```python
# app/dependencies.py
from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.models.users import User
from app.services import auth as auth_service

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/token")


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> User:
    """Get current authenticated user."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    user = await auth_service.get_user_from_token(db, token)
    if not user:
        raise credentials_exception
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user",
        )
    return user


# Type aliases
CurrentUser = Annotated[User, Depends(get_current_user)]
DBSession = Annotated[AsyncSession, Depends(get_db)]
```

### pyproject.toml

```toml
[project]
name = "myproject"
version = "0.1.0"
description = "FastAPI application"
requires-python = ">=3.11"

dependencies = [
    "fastapi>=0.109",
    "uvicorn[standard]>=0.27",
    "pydantic>=2.5",
    "pydantic-settings>=2.1",
    "sqlalchemy[asyncio]>=2.0",
    "asyncpg>=0.29",
    "alembic>=1.13",
    "python-jose[cryptography]>=3.3",
    "passlib[bcrypt]>=1.7",
    "python-multipart>=0.0.6",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0",
    "pytest-asyncio>=0.23",
    "httpx>=0.26",
    "pytest-cov>=4.1",
    "ruff>=0.2",
    "mypy>=1.8",
]

[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["tests"]
addopts = "-v --tb=short"

[tool.ruff]
line-length = 100
target-version = "py311"

[tool.mypy]
python_version = "3.11"
strict = true
```

### Docker Template

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY pyproject.toml .
RUN pip install --no-cache-dir .

# Copy application
COPY . .

# Run with uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
```

```yaml
# docker-compose.yml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql+asyncpg://postgres:postgres@db:5432/app
      - SECRET_KEY=${SECRET_KEY}
      - DEBUG=false
    depends_on:
      - db

  db:
    image: postgres:16-alpine
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      - POSTGRES_DB=app
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres

volumes:
  postgres_data:
```

---

## Flask Project Template

### Directory Structure

```
project/
|-- app/
|   |-- __init__.py           # Application factory
|   |-- extensions.py         # Flask extensions
|   |
|   |-- users/
|   |   |-- __init__.py
|   |   |-- models.py
|   |   |-- views.py
|   |   |-- services.py
|   |   |-- schemas.py
|   |
|   |-- auth/
|   |   |-- __init__.py
|   |   |-- views.py
|   |   |-- utils.py
|   |
|   |-- core/
|       |-- __init__.py
|       |-- models.py
|       |-- errors.py
|
|-- config.py
|-- migrations/
|-- tests/
|   |-- __init__.py
|   |-- conftest.py
|   |-- test_users.py
|
|-- pyproject.toml
|-- .env.example
|-- docker-compose.yml
|-- Dockerfile
```

### Application Factory Template

```python
# app/__init__.py
from flask import Flask
from app.extensions import db, migrate, jwt
from app.core.errors import register_error_handlers


def create_app(config_name='development'):
    """Application factory."""
    app = Flask(__name__)

    # Load config
    app.config.from_object(f'config.{config_name.capitalize()}Config')

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # Register error handlers
    register_error_handlers(app)

    # Register blueprints
    from app.users import bp as users_bp
    from app.auth import bp as auth_bp

    app.register_blueprint(users_bp, url_prefix='/api/v1/users')
    app.register_blueprint(auth_bp, url_prefix='/api/v1/auth')

    # Health check
    @app.route('/health')
    def health():
        return {'status': 'healthy'}

    return app
```

### Extensions Template

```python
# app/extensions.py
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
```

### Config Template

```python
# config.py
import os
from datetime import timedelta


class BaseConfig:
    """Base configuration."""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'jwt-secret-key')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)


class DevelopmentConfig(BaseConfig):
    """Development configuration."""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        'sqlite:///dev.db'
    )


class ProductionConfig(BaseConfig):
    """Production configuration."""
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')


class TestingConfig(BaseConfig):
    """Testing configuration."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
```

### Base Model Template

```python
# app/core/models.py
from datetime import datetime
from app.extensions import db


class BaseModel(db.Model):
    """Abstract base model."""
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )
```

### Error Handlers Template

```python
# app/core/errors.py
from flask import jsonify
from werkzeug.exceptions import HTTPException


def register_error_handlers(app):
    """Register application error handlers."""

    @app.errorhandler(HTTPException)
    def handle_http_exception(error):
        return jsonify({
            'error': error.name,
            'message': error.description,
        }), error.code

    @app.errorhandler(Exception)
    def handle_exception(error):
        app.logger.error(f'Unhandled exception: {error}')
        return jsonify({
            'error': 'Internal Server Error',
            'message': 'An unexpected error occurred',
        }), 500
```

### Blueprint Template

```python
# app/users/__init__.py
from flask import Blueprint

bp = Blueprint('users', __name__)

from app.users import views  # noqa
```

```python
# app/users/views.py
from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.users import bp
from app.users import services
from app.users.schemas import UserSchema, CreateUserSchema


@bp.route('/', methods=['GET'])
@jwt_required()
def list_users():
    """List all users."""
    users = services.get_all_users()
    return jsonify(UserSchema(many=True).dump(users))


@bp.route('/', methods=['POST'])
@jwt_required()
def create_user():
    """Create a new user."""
    schema = CreateUserSchema()
    errors = schema.validate(request.json)
    if errors:
        return jsonify({'errors': errors}), 400

    data = schema.load(request.json)
    user = services.create_user(**data)
    return jsonify(UserSchema().dump(user)), 201


@bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """Get current user."""
    user_id = get_jwt_identity()
    user = services.get_user_by_id(user_id)
    return jsonify(UserSchema().dump(user))
```

### pyproject.toml

```toml
[project]
name = "myproject"
version = "0.1.0"
description = "Flask application"
requires-python = ">=3.11"

dependencies = [
    "flask>=3.0",
    "flask-sqlalchemy>=3.1",
    "flask-migrate>=4.0",
    "flask-jwt-extended>=4.6",
    "marshmallow>=3.20",
    "psycopg2-binary>=2.9",
    "python-dotenv>=1.0",
    "gunicorn>=21.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0",
    "pytest-cov>=4.1",
    "ruff>=0.2",
    "mypy>=1.8",
]

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "-v --tb=short"

[tool.ruff]
line-length = 100
target-version = "py311"
```

### Docker Template

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY pyproject.toml .
RUN pip install --no-cache-dir .

# Copy application
COPY . .

# Run with gunicorn
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "app:create_app()"]
```

---

## Quick Start Commands

### Django

```bash
# Create new project
mkdir myproject && cd myproject
python -m venv .venv && source .venv/bin/activate
pip install django djangorestframework
django-admin startproject config .
python manage.py startapp users
mv users apps/

# Development
python manage.py runserver

# Production
gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 4
```

### FastAPI

```bash
# Create new project
mkdir myproject && cd myproject
python -m venv .venv && source .venv/bin/activate
pip install fastapi uvicorn sqlalchemy asyncpg alembic

# Development
uvicorn app.main:app --reload

# Production
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Flask

```bash
# Create new project
mkdir myproject && cd myproject
python -m venv .venv && source .venv/bin/activate
pip install flask flask-sqlalchemy flask-migrate

# Development
flask run --debug

# Production
gunicorn -w 4 -b 0.0.0.0:8000 "app:create_app()"
```

---

## Environment Variables Template

```bash
# .env.example

# Application
SECRET_KEY=your-secret-key-change-in-production
DEBUG=false

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/dbname

# JWT (FastAPI/Flask)
JWT_SECRET_KEY=your-jwt-secret-key
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS
CORS_ORIGINS=http://localhost:3000,https://example.com

# Django specific
DJANGO_SETTINGS_MODULE=config.settings.production
ALLOWED_HOSTS=example.com,api.example.com
```

---

*Python Web Frameworks Templates v1.0*
*Django | FastAPI | Flask*
