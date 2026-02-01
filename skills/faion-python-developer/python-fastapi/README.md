# FastAPI Development Guide

Modern FastAPI patterns for production-grade async APIs with Pydantic v2 and SQLAlchemy 2.0.

## Project Structure

```
project/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app, lifespan, middleware
│   ├── config.py            # Pydantic Settings
│   ├── dependencies.py      # Shared DI (db, auth, etc.)
│   │
│   ├── routers/             # API routes by domain
│   │   ├── __init__.py
│   │   ├── users.py
│   │   └── orders.py
│   │
│   ├── schemas/             # Pydantic models (request/response)
│   │   ├── __init__.py
│   │   ├── base.py          # Base schema with ConfigDict
│   │   ├── users.py
│   │   └── orders.py
│   │
│   ├── models/              # SQLAlchemy ORM models
│   │   ├── __init__.py
│   │   ├── base.py          # Base model with common fields
│   │   └── user.py
│   │
│   ├── services/            # Business logic layer
│   │   ├── __init__.py
│   │   └── users.py
│   │
│   └── db/
│       ├── __init__.py
│       ├── engine.py        # Async engine + session factory
│       └── repositories/    # Data access layer (optional)
│
├── tests/
│   ├── conftest.py          # Fixtures (async client, db)
│   ├── test_users.py
│   └── factories/           # Model factories
│
├── alembic/                 # Migrations
│   ├── env.py
│   └── versions/
│
├── pyproject.toml           # uv/poetry config
├── Dockerfile
├── docker-compose.yml
└── .env.example
```

## Key Principles

1. **Type hints everywhere** - Pydantic validates, FastAPI documents
2. **Async by default** - Use async/await for all I/O
3. **Dependency injection** - Clean, testable code via `Depends()`
4. **Schema-first** - Pydantic models define API contracts
5. **Separation of concerns** - Routes → Services → Repositories

## Dependency Injection Patterns

### Lifecycle Levels

| Level | Use Case | Example |
|-------|----------|---------|
| Per-request | DB sessions, auth | `Depends(get_db)` |
| Router-level | Shared concerns | `dependencies=[Depends(verify_api_key)]` |
| App lifespan | Singletons | Kafka producer, Redis pool |

### Dependency Graph

```
get_current_user
    ├── get_db (AsyncSession)
    └── oauth2_scheme (token)
            └── JWT decode
                    └── user lookup
```

FastAPI resolves dependencies top-down, caches per-request, injects into endpoints.

### Type Aliases for Clean Signatures

```python
from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

DBSession = Annotated[AsyncSession, Depends(get_db)]
CurrentUser = Annotated[User, Depends(get_current_active_user)]

@router.get("/me")
async def get_me(user: CurrentUser) -> UserResponse:
    return user
```

### Yield Dependencies (Cleanup)

```python
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
```

Yield runs teardown after response is sent - perfect for connections, spans.

## Async/Await Best Practices

### When to Use Async

| Operation | Use Async? | Why |
|-----------|------------|-----|
| Database queries | Yes | I/O bound |
| HTTP requests | Yes | Network I/O |
| File reads | Yes | Disk I/O |
| JWT parsing | No | CPU-light, no I/O |
| Password hashing | No | CPU-bound |

### Avoid Blocking the Event Loop

```python
# BAD - blocks event loop
import requests
response = requests.get(url)

# GOOD - async HTTP client
import httpx
async with httpx.AsyncClient() as client:
    response = await client.get(url)

# BAD - sync file read
with open("file.txt") as f:
    data = f.read()

# GOOD - async file read
import aiofiles
async with aiofiles.open("file.txt") as f:
    data = await f.read()
```

### Concurrency Patterns

```python
import asyncio

# Parallel execution
results = await asyncio.gather(
    fetch_user(user_id),
    fetch_orders(user_id),
    fetch_notifications(user_id),
)

# With error handling
results = await asyncio.gather(
    *tasks,
    return_exceptions=True,  # Don't fail all if one fails
)

# Semaphore for rate limiting
semaphore = asyncio.Semaphore(10)
async with semaphore:
    await external_api_call()
```

### Background Tasks

```python
from fastapi import BackgroundTasks

@router.post("/orders")
async def create_order(
    order: OrderCreate,
    background_tasks: BackgroundTasks,
) -> OrderResponse:
    order = await order_service.create(order)
    background_tasks.add_task(send_confirmation_email, order)
    return order
```

## SQLAlchemy 2.0 Async Integration

### Engine and Session Factory

```python
# app/db/engine.py
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
)
from app.config import settings

async_engine = create_async_engine(
    settings.database_url,
    pool_size=settings.db_pool_size,
    max_overflow=settings.db_max_overflow,
    echo=settings.debug,
)

async_session = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,  # Avoid lazy loading issues
)
```

### Session Per Task Rule

```python
# CRITICAL: One AsyncSession per asyncio task
# Never share across concurrent tasks

# BAD - sharing session
session = await get_session()
await asyncio.gather(
    query_users(session),  # Concurrent access!
    query_orders(session),
)

# GOOD - session per task
async def query_with_session(query_func):
    async with async_session() as session:
        return await query_func(session)

await asyncio.gather(
    query_with_session(query_users),
    query_with_session(query_orders),
)
```

### Eager Loading (Avoid N+1)

```python
from sqlalchemy.orm import selectinload, joinedload

# Eager load relationships
result = await db.execute(
    select(User)
    .options(selectinload(User.orders))  # One-to-many
    .options(joinedload(User.profile))   # One-to-one
    .where(User.id == user_id)
)
user = result.scalar_one_or_none()
```

### Write-Only Relationships (Async Safe)

```python
from sqlalchemy.orm import WriteOnlyMapped, relationship

class User(Base):
    # Async-compatible relationship
    orders: WriteOnlyMapped[list["Order"]] = relationship(
        back_populates="user",
        lazy="write_only",
    )

# Usage
await db.execute(user.orders.select())
```

## Pydantic v2 Patterns

### Base Schema with Defaults

```python
from pydantic import BaseModel, ConfigDict

class BaseSchema(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,      # ORM mode
        populate_by_name=True,     # Allow aliases
        extra="forbid",            # Fail on unknown fields
        str_strip_whitespace=True, # Auto-strip strings
    )
```

### Field Validators

```python
from pydantic import field_validator, model_validator

class UserCreate(BaseSchema):
    email: EmailStr
    password: str

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        if not any(c.isupper() for c in v):
            raise ValueError("Password must contain uppercase")
        return v

    @model_validator(mode="after")
    def validate_model(self) -> "UserCreate":
        # Cross-field validation
        return self
```

### Computed Fields

```python
from pydantic import computed_field

class UserResponse(BaseSchema):
    first_name: str
    last_name: str

    @computed_field
    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"
```

### Request/Response Patterns

```python
# Create - required fields
class UserCreate(BaseSchema):
    email: EmailStr
    name: str

# Update - all optional (PATCH)
class UserUpdate(BaseSchema):
    email: EmailStr | None = None
    name: str | None = None

# Response - includes id, timestamps
class UserResponse(BaseSchema):
    id: UUID
    email: EmailStr
    name: str
    created_at: datetime

# List response with pagination
class UserListResponse(BaseSchema):
    items: list[UserResponse]
    total: int
    page: int
    size: int
    pages: int
```

## Performance Tuning

| Area | Recommendation |
|------|----------------|
| DB pool | `pool_size = concurrency / 2`, `max_overflow = same` |
| HTTP timeouts | 0.5-1.0s for internal, 5s for external |
| Response serialization | Use `ORJSONResponse` for speed |
| Startup warmup | Pre-populate caches in lifespan |
| Lazy loading | Disable with `expire_on_commit=False` |

## Resources

### Official Documentation

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pydantic v2 Documentation](https://docs.pydantic.dev/)
- [SQLAlchemy 2.0 Async](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html)
- [Full Stack FastAPI Template](https://github.com/fastapi/full-stack-fastapi-template)

### Community Resources

- [FastAPI Best Practices](https://github.com/zhanymkanov/fastapi-best-practices)
- [Neon: Async Product API Guide](https://neon.com/guides/fastapi-async)

### Related Skill Files

- [templates.md](templates.md) - Copy-ready templates
- [examples.md](examples.md) - Complete API examples
- [checklist.md](checklist.md) - Project setup checklist
- [llm-prompts.md](llm-prompts.md) - Prompts for FastAPI development


## Agent Selection

| Task | Model | Rationale |
|------|-------|----------|
| Analyze and assess | sonnet | Evaluation and planning |
| Execute implementation | haiku | Apply established patterns |
| Review and validate | sonnet | Quality assurance |
| Strategic decision | opus | Novel scenarios |
| Optimize and refine | haiku | Performance tuning |
| Document approach | haiku | Create documentation |

