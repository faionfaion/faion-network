# FastAPI Templates

Copy-ready templates for common FastAPI patterns.

## Router Template

```python
# app/routers/{resource}.py
from uuid import UUID
from fastapi import APIRouter, HTTPException, Query, status

from app.dependencies import DBSession, CurrentUser
from app.schemas.{resource} import (
    {Resource}Create,
    {Resource}Update,
    {Resource}Response,
    {Resource}ListResponse,
)
from app.services import {resource} as {resource}_service

router = APIRouter()


@router.get("", response_model={Resource}ListResponse)
async def list_{resources}(
    db: DBSession,
    current_user: CurrentUser,
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
):
    """List {resources} with pagination."""
    items, total = await {resource}_service.get_list(db, page=page, size=size)
    return {Resource}ListResponse(items=items, total=total, page=page, size=size)


@router.post("", response_model={Resource}Response, status_code=status.HTTP_201_CREATED)
async def create_{resource}(
    db: DBSession,
    current_user: CurrentUser,
    data: {Resource}Create,
):
    """Create a new {resource}."""
    return await {resource}_service.create(db, data)


@router.get("/{{{resource}_id}}", response_model={Resource}Response)
async def get_{resource}(
    db: DBSession,
    current_user: CurrentUser,
    {resource}_id: UUID,
):
    """Get {resource} by ID."""
    item = await {resource}_service.get_by_id(db, {resource}_id)
    if not item:
        raise HTTPException(status_code=404, detail="{Resource} not found")
    return item


@router.patch("/{{{resource}_id}}", response_model={Resource}Response)
async def update_{resource}(
    db: DBSession,
    current_user: CurrentUser,
    {resource}_id: UUID,
    data: {Resource}Update,
):
    """Update {resource} fields."""
    item = await {resource}_service.update(db, {resource}_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="{Resource} not found")
    return item


@router.delete("/{{{resource}_id}}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_{resource}(
    db: DBSession,
    current_user: CurrentUser,
    {resource}_id: UUID,
):
    """Delete {resource}."""
    if not await {resource}_service.delete(db, {resource}_id):
        raise HTTPException(status_code=404, detail="{Resource} not found")
```

## Schema Templates

### Base Schema

```python
# app/schemas/base.py
from pydantic import BaseModel, ConfigDict


class BaseSchema(BaseModel):
    """Base schema with default config."""

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        extra="forbid",
        str_strip_whitespace=True,
    )
```

### Resource Schemas

```python
# app/schemas/{resource}.py
from datetime import datetime
from uuid import UUID
from pydantic import Field

from app.schemas.base import BaseSchema


class {Resource}Base(BaseSchema):
    """Shared fields."""
    name: str = Field(..., min_length=1, max_length=100)
    description: str | None = None


class {Resource}Create({Resource}Base):
    """Create request - required fields."""
    pass


class {Resource}Update(BaseSchema):
    """Update request - all optional."""
    name: str | None = Field(None, min_length=1, max_length=100)
    description: str | None = None


class {Resource}Response({Resource}Base):
    """Response - includes id, timestamps."""
    id: UUID
    created_at: datetime
    updated_at: datetime


class {Resource}ListResponse(BaseSchema):
    """Paginated list response."""
    items: list[{Resource}Response]
    total: int
    page: int
    size: int

    @property
    def pages(self) -> int:
        return (self.total + self.size - 1) // self.size
```

### With Validators

```python
# app/schemas/users.py
from pydantic import EmailStr, Field, field_validator, model_validator

from app.schemas.base import BaseSchema


class UserCreate(BaseSchema):
    email: EmailStr
    name: str = Field(..., min_length=1, max_length=100)
    password: str = Field(..., min_length=8, max_length=100)
    password_confirm: str

    @field_validator("password")
    @classmethod
    def validate_password_strength(cls, v: str) -> str:
        if not any(c.isupper() for c in v):
            raise ValueError("Must contain uppercase letter")
        if not any(c.islower() for c in v):
            raise ValueError("Must contain lowercase letter")
        if not any(c.isdigit() for c in v):
            raise ValueError("Must contain digit")
        return v

    @model_validator(mode="after")
    def validate_passwords_match(self) -> "UserCreate":
        if self.password != self.password_confirm:
            raise ValueError("Passwords do not match")
        return self
```

### With Computed Fields

```python
from pydantic import computed_field


class UserResponse(BaseSchema):
    id: UUID
    first_name: str
    last_name: str
    email: EmailStr

    @computed_field
    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"
```

## Service Template

```python
# app/services/{resource}.py
from uuid import UUID
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.{resource} import {Resource}
from app.schemas.{resource} import {Resource}Create, {Resource}Update


async def get_by_id(db: AsyncSession, id: UUID) -> {Resource} | None:
    """Get {resource} by ID."""
    result = await db.execute(select({Resource}).where({Resource}.id == id))
    return result.scalar_one_or_none()


async def get_list(
    db: AsyncSession,
    *,
    page: int = 1,
    size: int = 20,
) -> tuple[list[{Resource}], int]:
    """Get paginated {resources}."""
    # Count
    count_result = await db.execute(select(func.count({Resource}.id)))
    total = count_result.scalar_one()

    # Fetch
    offset = (page - 1) * size
    result = await db.execute(
        select({Resource})
        .order_by({Resource}.created_at.desc())
        .offset(offset)
        .limit(size)
    )
    items = list(result.scalars().all())

    return items, total


async def create(db: AsyncSession, data: {Resource}Create) -> {Resource}:
    """Create new {resource}."""
    item = {Resource}(**data.model_dump())
    db.add(item)
    await db.flush()
    await db.refresh(item)
    return item


async def update(
    db: AsyncSession,
    id: UUID,
    data: {Resource}Update,
) -> {Resource} | None:
    """Update {resource} fields."""
    item = await get_by_id(db, id)
    if not item:
        return None

    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(item, field, value)

    await db.flush()
    await db.refresh(item)
    return item


async def delete(db: AsyncSession, id: UUID) -> bool:
    """Delete {resource}."""
    item = await get_by_id(db, id)
    if not item:
        return False
    await db.delete(item)
    return True
```

## Model Template

```python
# app/models/{resource}.py
from sqlalchemy import String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, UUIDMixin, TimestampMixin


class {Resource}(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "{resources}"

    name: Mapped[str] = mapped_column(String(100))
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Foreign key example
    # owner_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"))
    # owner: Mapped["User"] = relationship(back_populates="{resources}")
```

## Dependency Template

```python
# app/dependencies.py
from typing import Annotated, AsyncGenerator
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from jose import jwt, JWTError

from app.config import settings
from app.db.engine import async_session
from app.models.user import User
from app.services import users as user_service

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Database session dependency with auto-commit/rollback."""
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
    """Decode JWT and return user."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token,
            settings.secret_key.get_secret_value(),
            algorithms=[settings.algorithm],
        )
        user_id: str | None = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = await user_service.get_by_id(db, user_id)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    user: Annotated[User, Depends(get_current_user)],
) -> User:
    """Ensure user is active."""
    if not user.is_active:
        raise HTTPException(status_code=403, detail="Inactive user")
    return user


# Type aliases for clean signatures
DBSession = Annotated[AsyncSession, Depends(get_db)]
CurrentUser = Annotated[User, Depends(get_current_active_user)]
OptionalUser = Annotated[User | None, Depends(get_current_user)]
```

## Config Template

```python
# app/config.py
from functools import lru_cache
from pydantic import SecretStr, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings from environment."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # Application
    app_name: str = "FastAPI App"
    debug: bool = False
    environment: str = "development"

    # Database
    database_url: str
    db_pool_size: int = 5
    db_max_overflow: int = 10

    # Redis (optional)
    redis_url: str = "redis://localhost:6379"

    # Auth
    secret_key: SecretStr
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # CORS
    cors_origins: list[str] = ["http://localhost:3000"]

    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, v):
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",")]
        return v


@lru_cache
def get_settings() -> Settings:
    """Cached settings instance."""
    return Settings()


settings = get_settings()
```

## Test Fixtures Template

```python
# tests/conftest.py
import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from app.main import app
from app.models.base import Base
from app.dependencies import get_db

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

test_engine = create_async_engine(TEST_DATABASE_URL, echo=False)
test_session = async_sessionmaker(bind=test_engine, expire_on_commit=False)


@pytest.fixture(scope="function")
async def db():
    """Create fresh database for each test."""
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with test_session() as session:
        yield session

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def client(db):
    """HTTP client with test database."""
    async def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:
        yield client

    app.dependency_overrides.clear()


@pytest.fixture
async def auth_client(client, db):
    """Authenticated HTTP client."""
    # Create test user
    from app.services import users as user_service
    from app.schemas.users import UserCreate

    user = await user_service.create(db, UserCreate(
        email="test@example.com",
        name="Test User",
        password="Password123",
    ))
    await db.commit()

    # Get token
    response = await client.post("/api/v1/auth/token", data={
        "username": "test@example.com",
        "password": "Password123",
    })
    token = response.json()["access_token"]

    client.headers["Authorization"] = f"Bearer {token}"
    yield client, user
```

## Dockerfile Template

```dockerfile
# Dockerfile
FROM python:3.12-slim as builder

WORKDIR /app

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies
RUN uv sync --frozen --no-dev

# Production stage
FROM python:3.12-slim

WORKDIR /app

# Create non-root user
RUN useradd -m -u 1000 app

# Copy virtual environment
COPY --from=builder /app/.venv /app/.venv

# Copy application
COPY app ./app

# Set environment
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1

USER app

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import httpx; httpx.get('http://localhost:8000/health')"

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Docker Compose Template

```yaml
# docker-compose.yml
services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql+asyncpg://postgres:postgres@db/app
      - SECRET_KEY=${SECRET_KEY}
      - DEBUG=true
    depends_on:
      db:
        condition: service_healthy
    volumes:
      - ./app:/app/app  # Dev only

  db:
    image: postgres:16-alpine
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres
      - POSTGRES_DB=app
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      timeout: 5s
      retries: 5

volumes:
  postgres_data:
```
