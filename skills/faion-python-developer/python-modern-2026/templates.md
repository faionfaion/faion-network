# Modern Python Templates

Copy-paste templates for modern Python projects (3.12-3.14).

---

## 1. Project Configuration

### pyproject.toml (Complete)

```toml
[project]
name = "my-project"
version = "0.1.0"
description = "Modern Python project"
readme = "README.md"
requires-python = ">=3.12"
license = {text = "MIT"}
authors = [
    {name = "Your Name", email = "you@example.com"}
]
keywords = ["python", "modern"]
classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.12",
    "Programming Language :: Python :: 3.13",
    "Programming Language :: Python :: 3.14",
    "Typing :: Typed",
]

dependencies = [
    "pydantic>=2.0",
    "httpx>=0.27",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0",
    "pytest-asyncio>=0.24",
    "pytest-cov>=5.0",
    "ruff>=0.8",
    "mypy>=1.13",
]

[project.urls]
Homepage = "https://github.com/username/my-project"
Documentation = "https://my-project.readthedocs.io"
Repository = "https://github.com/username/my-project.git"
Issues = "https://github.com/username/my-project/issues"

[project.scripts]
my-cli = "my_project.cli:main"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["src/my_project"]

# Ruff Configuration
[tool.ruff]
line-length = 88
target-version = "py312"
src = ["src", "tests"]

[tool.ruff.lint]
select = [
    "E",      # pycodestyle errors
    "W",      # pycodestyle warnings
    "F",      # pyflakes
    "I",      # isort
    "B",      # flake8-bugbear
    "C4",     # flake8-comprehensions
    "UP",     # pyupgrade
    "N",      # pep8-naming
    "S",      # flake8-bandit
    "T20",    # flake8-print
    "PT",     # flake8-pytest-style
    "RUF",    # Ruff-specific
]
ignore = [
    "S101",   # assert usage (needed for tests)
]

[tool.ruff.lint.per-file-ignores]
"tests/**/*" = ["S101"]

[tool.ruff.format]
quote-style = "double"
indent-style = "space"
docstring-code-format = true

# pytest Configuration
[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["tests"]
addopts = "-ra -q --strict-markers"
markers = [
    "slow: marks tests as slow",
    "integration: marks integration tests",
]

# Coverage Configuration
[tool.coverage.run]
source = ["src"]
branch = true
omit = ["*/tests/*", "*/__init__.py"]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise NotImplementedError",
    "if TYPE_CHECKING:",
]
show_missing = true

# mypy Configuration
[tool.mypy]
python_version = "3.13"
strict = true
warn_return_any = true
warn_unused_ignores = true
disallow_untyped_defs = true
no_implicit_optional = true
show_error_codes = true

[[tool.mypy.overrides]]
module = "tests.*"
disallow_untyped_defs = false
```

### .pre-commit-config.yaml

```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.8.4
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.13.0
    hooks:
      - id: mypy
        additional_dependencies: [pydantic>=2.0]
        args: [--strict]

  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.6.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
```

### .github/workflows/ci.yml

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.12", "3.13", "3.14"]

    steps:
      - uses: actions/checkout@v4

      - name: Install uv
        uses: astral-sh/setup-uv@v4
        with:
          version: "latest"

      - name: Set up Python ${{ matrix.python-version }}
        run: uv python install ${{ matrix.python-version }}

      - name: Install dependencies
        run: uv sync --all-extras

      - name: Lint with Ruff
        run: |
          uv run ruff check .
          uv run ruff format --check .

      - name: Type check with mypy
        run: uv run mypy src/

      - name: Test with pytest
        run: uv run pytest -v --cov=src --cov-report=xml

      - name: Upload coverage
        uses: codecov/codecov-action@v4
        with:
          files: ./coverage.xml
```

---

## 2. Type Patterns

### Generic Class Template

```python
from dataclasses import dataclass
from typing import Iterator

@dataclass
class Container[T]:
    """Generic container with iteration support."""

    items: list[T]

    def __iter__(self) -> Iterator[T]:
        return iter(self.items)

    def __len__(self) -> int:
        return len(self.items)

    def add(self, item: T) -> None:
        self.items.append(item)

    def get(self, index: int) -> T:
        return self.items[index]

    def map[R](self, func: Callable[[T], R]) -> "Container[R]":
        return Container(items=[func(item) for item in self.items])

    def filter(self, predicate: Callable[[T], bool]) -> "Container[T]":
        return Container(items=[item for item in self.items if predicate(item)])
```

### Result Type Template

```python
from dataclasses import dataclass
from typing import Callable, NoReturn

@dataclass(frozen=True)
class Ok[T]:
    """Success result."""
    value: T

@dataclass(frozen=True)
class Err[E]:
    """Error result."""
    error: E

type Result[T, E] = Ok[T] | Err[E]

def unwrap[T, E](result: Result[T, E]) -> T:
    """Unwrap result or raise error."""
    match result:
        case Ok(value):
            return value
        case Err(error):
            raise ValueError(f"Called unwrap on Err: {error}")

def unwrap_or[T, E](result: Result[T, E], default: T) -> T:
    """Unwrap result or return default."""
    match result:
        case Ok(value):
            return value
        case Err(_):
            return default

def map_result[T, U, E](
    result: Result[T, E],
    func: Callable[[T], U],
) -> Result[U, E]:
    """Map function over Ok value."""
    match result:
        case Ok(value):
            return Ok(func(value))
        case Err(error):
            return Err(error)
```

### Protocol Template

```python
from typing import Protocol, runtime_checkable

@runtime_checkable
class Identifiable(Protocol):
    """Protocol for objects with an ID."""
    @property
    def id(self) -> int: ...

@runtime_checkable
class Serializable(Protocol):
    """Protocol for serializable objects."""
    def to_dict(self) -> dict[str, object]: ...

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> "Serializable": ...

@runtime_checkable
class Repository[T: Identifiable](Protocol):
    """Generic repository protocol."""
    async def get(self, id: int) -> T | None: ...
    async def save(self, entity: T) -> T: ...
    async def delete(self, id: int) -> bool: ...
    async def list(self, skip: int = 0, limit: int = 100) -> list[T]: ...
```

### TypedDict Template

```python
from typing import TypedDict, ReadOnly, Required, NotRequired

class UserCreate(TypedDict):
    """User creation payload."""
    name: Required[str]
    email: Required[str]
    age: NotRequired[int]

class UserResponse(TypedDict):
    """User API response."""
    id: ReadOnly[int]
    name: str
    email: str
    created_at: ReadOnly[str]

class PaginatedResponse[T](TypedDict):
    """Paginated API response."""
    items: list[T]
    total: int
    page: int
    page_size: int
    has_next: bool
```

---

## 3. Async Patterns

### TaskGroup Service Template

```python
import asyncio
from dataclasses import dataclass
from typing import Callable, Awaitable

@dataclass
class AsyncService:
    """Service with concurrent operations."""

    async def fetch_all[T](
        self,
        urls: list[str],
        fetcher: Callable[[str], Awaitable[T]],
    ) -> list[T]:
        """Fetch multiple URLs concurrently."""
        async with asyncio.TaskGroup() as tg:
            tasks = [tg.create_task(fetcher(url)) for url in urls]
        return [task.result() for task in tasks]

    async def process_batch[T, R](
        self,
        items: list[T],
        processor: Callable[[T], Awaitable[R]],
        max_concurrent: int = 10,
    ) -> list[R]:
        """Process items with concurrency limit."""
        semaphore = asyncio.Semaphore(max_concurrent)

        async def bounded_process(item: T) -> R:
            async with semaphore:
                return await processor(item)

        async with asyncio.TaskGroup() as tg:
            tasks = [tg.create_task(bounded_process(item)) for item in items]
        return [task.result() for task in tasks]
```

### Async Context Manager Template

```python
from contextlib import asynccontextmanager
from typing import AsyncIterator
from dataclasses import dataclass

@dataclass
class Connection:
    """Async connection wrapper."""
    host: str
    connected: bool = False

    async def connect(self) -> None:
        # Simulate connection
        await asyncio.sleep(0.01)
        self.connected = True

    async def disconnect(self) -> None:
        # Simulate disconnection
        await asyncio.sleep(0.01)
        self.connected = False

@asynccontextmanager
async def get_connection(host: str) -> AsyncIterator[Connection]:
    """Async context manager for database connection."""
    conn = Connection(host=host)
    try:
        await conn.connect()
        yield conn
    finally:
        await conn.disconnect()

# Usage
async def main() -> None:
    async with get_connection("localhost") as conn:
        assert conn.connected
        # Use connection
```

### Retry Decorator Template

```python
import asyncio
from functools import wraps
from typing import Callable, TypeVar, ParamSpec

P = ParamSpec("P")
R = TypeVar("R")

def async_retry(
    max_retries: int = 3,
    delay: float = 1.0,
    backoff: float = 2.0,
    exceptions: tuple[type[Exception], ...] = (Exception,),
) -> Callable[[Callable[P, Awaitable[R]]], Callable[P, Awaitable[R]]]:
    """Decorator for async retry with exponential backoff."""

    def decorator(func: Callable[P, Awaitable[R]]) -> Callable[P, Awaitable[R]]:
        @wraps(func)
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            last_exception: Exception | None = None
            current_delay = delay

            for attempt in range(max_retries + 1):
                try:
                    return await func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt < max_retries:
                        await asyncio.sleep(current_delay)
                        current_delay *= backoff

            assert last_exception is not None
            raise last_exception

        return wrapper

    return decorator

# Usage
@async_retry(max_retries=3, delay=0.5, exceptions=(TimeoutError, ConnectionError))
async def fetch_data(url: str) -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.get(url, timeout=5.0)
        return response.json()
```

---

## 4. Testing Templates

### conftest.py Template

```python
import asyncio
from collections.abc import AsyncIterator, Iterator
from typing import Any

import pytest
import pytest_asyncio

# Event loop fixture (for session-scoped async fixtures)
@pytest.fixture(scope="session")
def event_loop() -> Iterator[asyncio.AbstractEventLoop]:
    """Create event loop for session."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()

# Async database fixture
@pytest_asyncio.fixture
async def db_session() -> AsyncIterator[Any]:
    """Provide database session with cleanup."""
    # Setup
    session = await create_session()
    yield session
    # Cleanup
    await session.rollback()
    await session.close()

# HTTP client fixture
@pytest_asyncio.fixture
async def http_client() -> AsyncIterator[httpx.AsyncClient]:
    """Provide HTTP client."""
    async with httpx.AsyncClient() as client:
        yield client

# Test data fixtures
@pytest.fixture
def sample_user() -> dict[str, Any]:
    """Provide sample user data."""
    return {
        "id": 1,
        "name": "Test User",
        "email": "test@example.com",
    }

@pytest.fixture
def sample_users() -> list[dict[str, Any]]:
    """Provide multiple sample users."""
    return [
        {"id": i, "name": f"User {i}", "email": f"user{i}@example.com"}
        for i in range(1, 6)
    ]
```

### Async Test Template

```python
import pytest
from unittest.mock import AsyncMock, patch

@pytest.mark.asyncio
class TestUserService:
    """Tests for UserService."""

    async def test_get_user_success(
        self,
        user_service: UserService,
        sample_user: dict,
    ) -> None:
        """Test successful user retrieval."""
        user_service.repository.get = AsyncMock(return_value=sample_user)

        result = await user_service.get_user(1)

        assert result == sample_user
        user_service.repository.get.assert_called_once_with(1)

    async def test_get_user_not_found(
        self,
        user_service: UserService,
    ) -> None:
        """Test user not found."""
        user_service.repository.get = AsyncMock(return_value=None)

        with pytest.raises(UserNotFoundError):
            await user_service.get_user(999)

    @pytest.mark.parametrize(
        "user_id,expected_name",
        [
            (1, "Alice"),
            (2, "Bob"),
            (3, "Charlie"),
        ],
    )
    async def test_get_user_names(
        self,
        user_service: UserService,
        user_id: int,
        expected_name: str,
    ) -> None:
        """Test getting different users."""
        user_service.repository.get = AsyncMock(
            return_value={"id": user_id, "name": expected_name}
        )

        result = await user_service.get_user(user_id)

        assert result["name"] == expected_name
```

### Integration Test Template

```python
import pytest
from httpx import AsyncClient
from fastapi import status

@pytest.mark.integration
@pytest.mark.asyncio
class TestUserAPI:
    """Integration tests for User API."""

    async def test_create_user(
        self,
        client: AsyncClient,
        sample_user: dict,
    ) -> None:
        """Test user creation endpoint."""
        response = await client.post(
            "/api/users",
            json=sample_user,
        )

        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["name"] == sample_user["name"]
        assert "id" in data

    async def test_get_user(
        self,
        client: AsyncClient,
        created_user: dict,
    ) -> None:
        """Test get user endpoint."""
        response = await client.get(f"/api/users/{created_user['id']}")

        assert response.status_code == status.HTTP_200_OK
        assert response.json()["id"] == created_user["id"]

    async def test_list_users_pagination(
        self,
        client: AsyncClient,
    ) -> None:
        """Test users list pagination."""
        response = await client.get("/api/users?page=1&page_size=10")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "items" in data
        assert "total" in data
        assert len(data["items"]) <= 10
```

---

## 5. FastAPI Templates

### FastAPI App Template

```python
from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel

# Lifespan management
@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Manage application lifespan."""
    # Startup
    await startup_tasks()
    yield
    # Shutdown
    await shutdown_tasks()

app = FastAPI(
    title="My API",
    version="0.1.0",
    lifespan=lifespan,
)

# Pydantic models
class UserCreate(BaseModel):
    name: str
    email: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: str

    model_config = {"from_attributes": True}

# Dependency injection
async def get_db() -> AsyncIterator[Database]:
    db = Database()
    try:
        await db.connect()
        yield db
    finally:
        await db.disconnect()

# Endpoints
@app.post("/users", response_model=UserResponse, status_code=201)
async def create_user(
    user: UserCreate,
    db: Database = Depends(get_db),
) -> UserResponse:
    """Create a new user."""
    result = await db.users.create(user.model_dump())
    return UserResponse.model_validate(result)

@app.get("/users/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    db: Database = Depends(get_db),
) -> UserResponse:
    """Get user by ID."""
    user = await db.users.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserResponse.model_validate(user)
```

### Pydantic Model Templates

```python
from datetime import datetime
from pydantic import BaseModel, Field, EmailStr, ConfigDict

class BaseEntity(BaseModel):
    """Base entity with common fields."""
    model_config = ConfigDict(from_attributes=True)

class UserBase(BaseModel):
    """Base user fields."""
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr

class UserCreate(UserBase):
    """User creation payload."""
    password: str = Field(..., min_length=8)

class UserUpdate(BaseModel):
    """User update payload (all fields optional)."""
    name: str | None = Field(None, min_length=1, max_length=100)
    email: EmailStr | None = None

class UserResponse(UserBase, BaseEntity):
    """User API response."""
    id: int
    created_at: datetime
    updated_at: datetime | None = None

class PaginatedResponse[T](BaseModel):
    """Generic paginated response."""
    items: list[T]
    total: int
    page: int = Field(..., ge=1)
    page_size: int = Field(..., ge=1, le=100)

    @property
    def has_next(self) -> bool:
        return self.page * self.page_size < self.total
```

---

## 6. Utility Templates

### Logging Setup Template

```python
import logging
import sys
from typing import Any

def setup_logging(
    level: int = logging.INFO,
    format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
) -> None:
    """Configure application logging."""
    logging.basicConfig(
        level=level,
        format=format,
        handlers=[
            logging.StreamHandler(sys.stdout),
        ],
    )

    # Suppress noisy loggers
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)

def get_logger(name: str) -> logging.Logger:
    """Get configured logger."""
    return logging.getLogger(name)

# Structured logging helper
def log_context(logger: logging.Logger, **context: Any) -> None:
    """Log with structured context."""
    logger.info("Context: %s", context)
```

### Environment Configuration Template

```python
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """Application settings from environment."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # App
    app_name: str = "my-app"
    debug: bool = False
    environment: str = "development"

    # Database
    database_url: str = "sqlite+aiosqlite:///./app.db"

    # API
    api_prefix: str = "/api/v1"
    cors_origins: list[str] = ["http://localhost:3000"]

    # Auth
    secret_key: str
    access_token_expire_minutes: int = 30

@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
```

---

*Templates v2.0 - Modern Python 2026*
