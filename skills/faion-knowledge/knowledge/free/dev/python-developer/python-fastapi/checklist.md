# FastAPI Project Checklist

Use this checklist when starting or auditing a FastAPI project.

## Project Setup

### Dependencies

- [ ] FastAPI 0.115+
- [ ] Pydantic 2.x (pydantic-settings for config)
- [ ] SQLAlchemy 2.0+ with asyncpg/aiosqlite
- [ ] Alembic for migrations
- [ ] httpx for async HTTP
- [ ] pytest-asyncio for testing
- [ ] uvicorn[standard] for ASGI

### Package Manager

- [ ] uv (recommended) or poetry
- [ ] pyproject.toml configured
- [ ] Lock file committed

### Project Structure

- [ ] `app/main.py` - FastAPI instance
- [ ] `app/config.py` - Pydantic Settings
- [ ] `app/dependencies.py` - Shared DI
- [ ] `app/routers/` - API routes
- [ ] `app/schemas/` - Pydantic models
- [ ] `app/models/` - SQLAlchemy models
- [ ] `app/services/` - Business logic
- [ ] `app/db/` - Database engine, session
- [ ] `tests/` - Test suite

## Configuration

### Settings Class

- [ ] Inherits from `BaseSettings`
- [ ] Uses `SettingsConfigDict` for .env
- [ ] Sensitive values typed (SecretStr)
- [ ] Cached with `@lru_cache`
- [ ] All env vars documented

### Environment Files

- [ ] `.env.example` with all vars (no secrets)
- [ ] `.env` in `.gitignore`
- [ ] Different envs: dev, staging, prod

## Application Setup

### Lifespan Events

- [ ] `@asynccontextmanager` lifespan
- [ ] Database init on startup
- [ ] Connection pool warmup
- [ ] Clean shutdown

### Middleware

- [ ] CORS configured (restrictive in prod)
- [ ] Trusted host middleware (prod)
- [ ] Request ID middleware
- [ ] Timing/logging middleware

### Routers

- [ ] Versioned prefixes (`/api/v1/`)
- [ ] Logical tags for OpenAPI
- [ ] Dependencies at router level
- [ ] Type aliases for common deps

## Database

### SQLAlchemy Setup

- [ ] Async engine created
- [ ] `async_sessionmaker` configured
- [ ] `expire_on_commit=False`
- [ ] Pool size tuned for concurrency

### Models

- [ ] Base model with common fields
- [ ] UUID primary keys (recommended)
- [ ] Timestamps: created_at, updated_at
- [ ] Soft delete if needed
- [ ] Write-only relationships for async

### Migrations

- [ ] Alembic initialized
- [ ] `alembic/env.py` configured for async
- [ ] Auto-generate working
- [ ] Migration in CI pipeline

## Schemas (Pydantic)

### Base Schema

- [ ] `ConfigDict` with defaults
- [ ] `from_attributes=True`
- [ ] `extra="forbid"`
- [ ] `str_strip_whitespace=True`

### Schema Patterns

- [ ] Create schema (required fields)
- [ ] Update schema (optional fields)
- [ ] Response schema (id, timestamps)
- [ ] List response (pagination)

### Validation

- [ ] Field validators where needed
- [ ] Model validators for cross-field
- [ ] Custom error messages
- [ ] Computed fields for derived data

## Authentication

### JWT Setup

- [ ] Secure secret key (32+ bytes)
- [ ] Short expiry (15-30 min)
- [ ] Refresh token flow
- [ ] Proper error responses

### OAuth2

- [ ] `OAuth2PasswordBearer` configured
- [ ] Token endpoint
- [ ] `get_current_user` dependency
- [ ] `get_current_active_user` dependency

### Security

- [ ] Password hashing (bcrypt/argon2)
- [ ] Rate limiting on auth endpoints
- [ ] Account lockout after failed attempts
- [ ] Secure headers

## API Design

### Endpoints

- [ ] RESTful conventions
- [ ] Proper HTTP status codes
- [ ] Consistent response format
- [ ] Pagination on list endpoints
- [ ] Filtering and sorting

### Error Handling

- [ ] Custom exception handlers
- [ ] Consistent error schema
- [ ] Detailed errors in dev only
- [ ] Logged for monitoring

### Documentation

- [ ] OpenAPI enabled (dev only in prod)
- [ ] Endpoint descriptions
- [ ] Request/response examples
- [ ] Tags organized logically

## Testing

### Setup

- [ ] pytest-asyncio configured
- [ ] Test database (SQLite or testcontainers)
- [ ] AsyncClient fixture
- [ ] Factory fixtures (Factory Boy)

### Coverage

- [ ] Unit tests for services
- [ ] Integration tests for endpoints
- [ ] Auth flow tested
- [ ] Error cases tested
- [ ] Pagination tested

### CI

- [ ] Tests run on PR
- [ ] Coverage reporting
- [ ] Linting (ruff)
- [ ] Type checking (mypy)

## Deployment

### Docker

- [ ] Multi-stage Dockerfile
- [ ] Non-root user
- [ ] Health check endpoint
- [ ] Proper signal handling

### Production

- [ ] Uvicorn with workers
- [ ] Gunicorn if needed
- [ ] HTTPS only
- [ ] Secrets via env vars
- [ ] Logging configured

### Monitoring

- [ ] Health endpoint (`/health`)
- [ ] Readiness endpoint
- [ ] Structured logging
- [ ] Error tracking (Sentry)
- [ ] Metrics (Prometheus)

## Performance

### Optimization

- [ ] ORJSONResponse for speed
- [ ] Connection pooling tuned
- [ ] Eager loading for relationships
- [ ] Caching where appropriate
- [ ] Background tasks for heavy work

### Async

- [ ] No sync I/O in async routes
- [ ] httpx for HTTP calls
- [ ] aiofiles for file I/O
- [ ] Proper semaphores for rate limiting

## Quick Reference

### Minimum Viable Setup

```bash
# Create project
mkdir my-api && cd my-api
uv init
uv add fastapi uvicorn[standard] pydantic-settings

# Run
uvicorn app.main:app --reload
```

### Essential Dependencies

```toml
[project]
dependencies = [
    "fastapi>=0.115.0",
    "uvicorn[standard]>=0.32.0",
    "pydantic>=2.10.0",
    "pydantic-settings>=2.6.0",
    "sqlalchemy[asyncio]>=2.0.0",
    "asyncpg>=0.30.0",
    "alembic>=1.14.0",
    "httpx>=0.28.0",
    "python-jose[cryptography]>=3.3.0",
    "passlib[bcrypt]>=1.7.4",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0.0",
    "pytest-asyncio>=0.24.0",
    "ruff>=0.8.0",
    "mypy>=1.13.0",
]
```
