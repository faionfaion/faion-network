# Python FastAPI

## Summary

**One-sentence:** FastAPI production patterns with Pydantic v2 + SQLAlchemy 2 async + thin routes + per-task AsyncSession.

**One-paragraph:** FastAPI production patterns with Pydantic v2 and SQLAlchemy 2 async. Routes are thin: validate input via Pydantic schema → call service → return response model. One AsyncSession per asyncio task — never share across asyncio.gather siblings. Background tasks via FastAPI BackgroundTasks for short work only (<100ms); route longer jobs to Celery/Arq/Taskiq. Snapshot openapi.json per PR to catch schema drift.

**Ефективно для:** інженера, який будує або еволюціонує FastAPI-сервіс — закриває петлю між Pydantic-валідацією, SQLAlchemy-сесіями та чіткими роутами без бізнес-логіки.

## Applies If (ALL must hold)

- New async REST API project where I/O concurrency dominates.
- Adding endpoints to an existing FastAPI project (one vertical slice at a time).
- Migrating Flask/Django REST to FastAPI vertical slices.
- Wiring openapi.json snapshot tests into CI.

## Skip If (ANY kills it)

- Synchronous CPU-bound workloads — use Celery + Flask/Django.
- Tight CRUD-only apps that fit a Django admin — FastAPI's flexibility is overkill.
- GraphQL endpoints — use Strawberry or Ariadne instead.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Python 3.12+ interpreter | binary | uv install |
| FastAPI 0.115+ installed | package | uv add fastapi |
| Pydantic v2 + SQLAlchemy 2 async drivers | package | uv add pydantic 'sqlalchemy[asyncio]' asyncpg |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `free/dev/python-developer/python-async` | Async fundamentals (TaskGroup, asyncio.timeout, no blocking calls). |
| `free/dev/python-developer/python-type-hints` | Pydantic v2 relies on accurate type hints. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 13 rules: thin routes, Pydantic v2 in/out, one AsyncSession per task, BackgroundTasks <100ms only, Depends injection, openapi snapshot, lifespan not on_event, Base/Create/Update/Response quartet, Annotated dependency aliases, services return ORM, flush+refresh never commit, no sync I/O in async, docs guarded in prod. | ~2000 |
| `content/02-output-contract.xml` | essential | Shape: routers/ + services/ + schemas/ + models/ + dependencies.py + main.py. Forbidden: business logic in routes, dict in/out, shared AsyncSession across gather siblings. | ~900 |
| `content/03-failure-modes.xml` | essential | 9 antipatterns: shared session across gather, fat route, BackgroundTasks for slow work, openapi drift, deprecated on_event, one-schema-fits-all, sync I/O in an async route, unguarded /docs in production. | ~1300 |
| `content/04-procedure.xml` | medium | 8 steps: bootstrap the async stack → lifespan + dependency aliases → schema quartet → service function → wire route → register dependencies → snapshot openapi → audit blocking calls → CI gate. | ~1000 |
| `content/06-decision-tree.xml` | essential | Tree: stack in scope? then what is being written — lifespan / schema / route / service / post-response work / fan-out — each to a rule id. | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scaffold-vertical-slice` | sonnet | schema + service + route + test triplet with judgement. |
| `audit-openapi-drift` | haiku | Diff openapi.json against snapshot. |

## Templates

| File | Purpose |
|------|---------|
| `templates/router.py` | Thin FastAPI router: Depends() for session, Pydantic schema in/out, calls service. |
| `templates/service.py` | Service function skeleton: AsyncSession dependency, returns Pydantic response model. |
| `templates/schemas.py` | Pydantic v2 quartet: <Entity>Base/Create/Update/Response + paginated list response. |
| `templates/main.py` | App entry: asynccontextmanager lifespan, CORS, router includes, docs gated on settings.debug. |
| `templates/dependencies.py` | get_db + get_current_user with the DBSession / CurrentUser Annotated aliases. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-python-fastapi.py` | Check that routes only call services (no ORM in routes), and openapi.json matches snapshot. | Pre-commit and CI. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[python-async]]
- [[python-type-hints]]
- [[python-pytest-async]]
- [[error-handling]] — the RFC 7807 envelope this app's exception handler returns.
- [[django-api]] — the DRF/Ninja counterpart when the project is Django rather than FastAPI.

## Decision tree

The tree at content/06-decision-tree.xml decides BackgroundTasks vs job queue, Depends scope, and fan-out strategy inside a request. Walk it before adding any new endpoint or background job.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/router.py`

```python
"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import ItemIn, ItemOut
from .service import create_item
from .deps import get_session

router = APIRouter()


@router.post("/items", response_model=ItemOut, status_code=201)
async def create_item_endpoint(
    payload: ItemIn,
    session: AsyncSession = Depends(get_session),
) -> ItemOut:
    return await create_item(session, payload)
```

### `templates/service.py`

```python
"""

from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import ItemIn, ItemOut


async def create_item(session: AsyncSession, payload: ItemIn) -> ItemOut:
    # ORM logic lives here; route stays thin.
    return ItemOut(id=1, name=payload.name)
```

### `templates/schemas.py`

```python
"""
Pydantic v2 schema hierarchy for User resource.
Copy and adapt for other resources: rename User → YourResource.
"""
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field, ConfigDict


class UserBase(BaseModel):
    email: EmailStr
    name: str = Field(..., min_length=1, max_length=100)


class UserCreate(UserBase):
    """Request schema for user creation. Includes password (not in response)."""
    password: str = Field(..., min_length=8, max_length=100)


class UserUpdate(BaseModel):
    """Request schema for partial update (PATCH). All fields optional."""
    email: EmailStr | None = None
    name: str | None = Field(None, min_length=1, max_length=100)


class UserResponse(UserBase):
    """Response schema. Excludes password. from_attributes for ORM serialization."""
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    is_active: bool
    created_at: datetime


class UserListResponse(BaseModel):
    """Paginated user list response."""
    items: list[UserResponse]
    total: int
    page: int
    size: int
    pages: int
```

### `templates/main.py`

```python
"""
FastAPI application entry point.
Adjust imports, router includes, and middleware to your project structure.
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.db.database import init_db, close_db
from app.routers import users  # add more routers here


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize resources on startup, release on shutdown."""
    await init_db()
    yield
    await close_db()


app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    description="Production API",
    lifespan=lifespan,
    docs_url="/docs" if settings.debug else None,
    redoc_url="/redoc" if settings.debug else None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router, prefix="/api/v1/users", tags=["users"])


@app.get("/health")
async def health_check() -> dict:
    return {"status": "healthy", "version": "1.0.0"}
```

### `templates/dependencies.py`

```python
"""
Shared FastAPI dependencies: DB session, current user, type aliases.
Import DBSession and CurrentUser in route functions instead of raw Depends().
"""
from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from jose import jwt, JWTError

from app.config import settings
from app.db.database import async_session
from app.models.user import User
from app.services import users as user_service

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")


async def get_db() -> AsyncSession:  # type: ignore[return]
    """Yields an async DB session; commits on success, rolls back on error."""
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.jwt_secret,
                             algorithms=[settings.jwt_algorithm])
        user_id: str | None = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = await user_service.get_user_by_id(db, user_id)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
) -> User:
    if not current_user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Inactive user")
    return current_user


# Use these aliases in route function signatures
DBSession = Annotated[AsyncSession, Depends(get_db)]
CurrentUser = Annotated[User, Depends(get_current_active_user)]
```
