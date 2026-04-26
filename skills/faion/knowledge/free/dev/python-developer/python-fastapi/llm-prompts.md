# LLM Prompts for FastAPI Development

Prompts for code generation, debugging, and refactoring FastAPI applications.

## New Project Setup

### Create FastAPI Project Structure

```
Create a FastAPI project structure with:

Tech stack:
- FastAPI 0.115+
- Pydantic v2 with pydantic-settings
- SQLAlchemy 2.0 async with asyncpg
- Alembic for migrations
- pytest-asyncio for testing
- uv as package manager

Requirements:
1. app/main.py with lifespan events
2. app/config.py with Pydantic Settings
3. app/db/engine.py with async engine and session factory
4. app/models/base.py with UUID and timestamp mixins
5. app/schemas/base.py with default ConfigDict
6. app/dependencies.py with get_db and auth dependencies
7. Dockerfile with multi-stage build
8. docker-compose.yml with postgres

Follow these patterns:
- expire_on_commit=False for async sessions
- Type aliases for dependencies (DBSession, CurrentUser)
- Yield dependencies for cleanup
- ORJSONResponse for performance
```

### Add Resource CRUD

```
Add a complete CRUD resource for {Resource} to my FastAPI app.

Resource fields:
- name: str (required, 1-100 chars)
- description: str (optional)
- status: enum (active, inactive)
- owner_id: UUID (foreign key to users)

Generate:
1. app/models/{resource}.py - SQLAlchemy model
2. app/schemas/{resource}.py - Create, Update, Response schemas
3. app/services/{resource}.py - Business logic layer
4. app/routers/{resource}.py - API endpoints
5. tests/test_{resource}.py - Test cases

Requirements:
- Pagination on list endpoint
- Owner-only update/delete
- Proper error handling (404, 403)
- Async throughout
```

## Authentication

### JWT Authentication Setup

```
Implement JWT authentication for my FastAPI app.

Requirements:
1. OAuth2 password flow with token endpoint
2. Access token with 30 min expiry
3. Refresh token with 7 day expiry
4. get_current_user dependency
5. get_current_active_user dependency
6. Secure password hashing with bcrypt

Generate:
- app/routers/auth.py with /token and /refresh endpoints
- app/utils/security.py with password hashing and JWT functions
- Update app/dependencies.py with auth dependencies
- tests/test_auth.py with login/logout tests

Use python-jose for JWT and passlib for hashing.
```

### Add API Key Authentication

```
Add API key authentication as an alternative to JWT.

Requirements:
1. API keys stored in database with hash
2. X-API-Key header authentication
3. Scopes/permissions per API key
4. Rate limiting per API key
5. API key management endpoints (admin only)

Generate:
- app/models/api_key.py
- app/schemas/api_key.py
- app/dependencies.py - get_api_key dependency
- app/routers/api_keys.py - CRUD for API keys
```

## Database Operations

### Add Pagination and Filtering

```
Implement advanced pagination and filtering for my FastAPI list endpoints.

Requirements:
1. Cursor-based pagination (better for large datasets)
2. Flexible filtering (field=value, field__gte=value)
3. Sorting (sort_by, order)
4. Search across multiple fields
5. Reusable dependency

Generate:
- app/schemas/pagination.py with PaginationParams
- app/utils/filtering.py with filter builder
- app/dependencies.py with get_pagination dependency
- Update service layer to accept these params

Example usage:
GET /api/v1/items?status=active&created_at__gte=2024-01-01&sort_by=name&cursor=xxx
```

### Add Soft Delete

```
Implement soft delete pattern for my SQLAlchemy models.

Requirements:
1. deleted_at timestamp column (null = not deleted)
2. Automatic filtering in queries
3. Restore capability
4. Permanent delete option
5. Cascade to related models

Update:
- app/models/base.py - SoftDeleteMixin
- Service layer - respect soft delete in queries
- Add /restore and /permanent-delete endpoints
```

### Add Database Migrations

```
Set up Alembic for async SQLAlchemy migrations.

Requirements:
1. alembic/env.py configured for async
2. Auto-import all models
3. Migration script template
4. CI pipeline for migration check

Generate:
- alembic.ini
- alembic/env.py (async version)
- alembic/script.py.mako
- Example migration

Include commands for:
- alembic revision --autogenerate -m "message"
- alembic upgrade head
- alembic downgrade -1
```

## Performance

### Add Caching Layer

```
Implement Redis caching for my FastAPI app.

Requirements:
1. Cache decorator for service functions
2. Automatic cache invalidation on update/delete
3. Configurable TTL per endpoint
4. Cache key generation from function args
5. Redis connection in lifespan

Generate:
- app/cache/redis.py - Redis client setup
- app/cache/decorators.py - @cached decorator
- Update lifespan to init/close Redis
- Example usage in service layer

Use redis-py with async support.
```

### Add Background Task Processing

```
Implement background task processing with async patterns.

For simple tasks:
- Use FastAPI BackgroundTasks

For complex tasks:
- Add Celery/ARQ integration
- Task retry with exponential backoff
- Task status tracking
- Dead letter queue

Generate:
- app/tasks/worker.py - ARQ worker setup
- app/tasks/email.py - Email task example
- app/tasks/reports.py - Long-running report task
- app/dependencies.py - enqueue_task dependency
```

## Testing

### Generate Test Suite

```
Generate comprehensive tests for my FastAPI app.

Requirements:
1. tests/conftest.py with async fixtures
2. Test database isolation (SQLite in-memory)
3. Authenticated client fixture
4. Factory fixtures for models
5. Test coverage for:
   - All CRUD operations
   - Authentication flows
   - Error cases (401, 403, 404)
   - Pagination
   - Validation errors

Use:
- pytest-asyncio
- httpx.AsyncClient
- Factory Boy (async)
```

### Add Integration Tests

```
Add integration tests for my FastAPI app with real database.

Requirements:
1. Use testcontainers for PostgreSQL
2. Run migrations before tests
3. Test database transactions
4. Test concurrent requests
5. Test WebSocket endpoints

Generate:
- tests/integration/conftest.py
- tests/integration/test_db_transactions.py
- tests/integration/test_concurrency.py
```

## Refactoring

### Convert Sync to Async

```
Convert my synchronous FastAPI code to fully async.

Current issues:
- Using sync SQLAlchemy (Session, not AsyncSession)
- Using requests instead of httpx
- Blocking file I/O
- Sync password hashing in async routes

Refactor to:
1. Replace Session with AsyncSession
2. Replace requests with httpx.AsyncClient
3. Use aiofiles for file operations
4. Move CPU-bound work to thread pool

Show before/after for each file.
```

### Extract Service Layer

```
Refactor my FastAPI app to add a service layer.

Current state:
- Business logic in route handlers
- Direct database access in routes
- Validation mixed with logic

Target state:
- Routes only handle HTTP (request/response)
- Services contain business logic
- Repositories handle data access (optional)

Refactor:
- Extract business logic to app/services/
- Keep routes thin
- Add proper error handling in services
```

### Add Dependency Injection

```
Refactor my FastAPI app to use proper dependency injection.

Current issues:
- Global database session
- Hardcoded configuration
- Direct instantiation of services

Target:
1. Database session via Depends(get_db)
2. Settings via Depends(get_settings)
3. Services via Depends(get_service)
4. Easy to mock in tests

Update:
- app/dependencies.py with all dependencies
- Type aliases for common patterns
- Router-level dependencies where appropriate
```

## Debugging

### Fix Async Performance Issues

```
My FastAPI app has performance issues. Help me identify and fix them.

Symptoms:
- High response times
- Event loop blocking
- Memory growing over time

Check for:
1. Sync I/O in async routes (requests, file open)
2. N+1 query problems
3. Missing connection pool limits
4. Lazy loading in async context
5. Memory leaks in dependencies

Provide:
- Diagnostic queries/code
- Specific fixes for each issue
- Performance testing approach
```

### Debug Database Connection Issues

```
My FastAPI app has intermittent database connection errors.

Error messages:
- "connection pool exhausted"
- "connection reset by peer"
- "SSL connection has been closed unexpectedly"

Check:
1. Pool size vs concurrent requests
2. Connection leak (missing close/commit)
3. Long-running transactions
4. Health check configuration
5. SSL/TLS settings

Provide:
- Diagnostic logging
- Pool configuration recommendations
- Connection lifecycle best practices
```

## Quick Snippets

### Pagination Dependency

```
Create a reusable pagination dependency:
- page: int (default 1, min 1)
- size: int (default 20, min 1, max 100)
- Returns PaginationParams dataclass
- Calculates offset internally
```

### Error Handler

```
Create a global exception handler for my FastAPI app:
- HTTPException - return as-is
- ValidationError - format nicely
- SQLAlchemyError - log and return 500
- Generic Exception - log full traceback, return 500
- Include request_id in all responses
```

### Rate Limiter

```
Create a rate limiting dependency:
- Redis-based sliding window
- Configurable limits per endpoint
- Different limits for auth/anon users
- Return X-RateLimit-* headers
- 429 response when exceeded
```

### Request Logging

```
Create a middleware for request/response logging:
- Log request method, path, duration
- Log response status code
- Include request_id
- Exclude health check endpoints
- Structured JSON logging
```
