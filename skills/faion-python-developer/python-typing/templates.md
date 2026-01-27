# Python Typing Templates

Copy-paste typing patterns for common scenarios.

---

## Configuration Templates

### mypy Configuration (pyproject.toml)

```toml
[tool.mypy]
python_version = "3.12"
strict = true
warn_return_any = true
warn_unused_ignores = true
disallow_untyped_defs = true
disallow_incomplete_defs = true
no_implicit_optional = true
check_untyped_defs = true
warn_redundant_casts = true
warn_unused_configs = true
show_error_codes = true

# Per-module overrides
[[tool.mypy.overrides]]
module = "tests.*"
disallow_untyped_defs = false
disallow_incomplete_defs = false

[[tool.mypy.overrides]]
module = "migrations.*"
ignore_errors = true

[[tool.mypy.overrides]]
module = [
    "third_party_lib.*",
    "untyped_dependency.*",
]
ignore_missing_imports = true
```

### Pyright Configuration (pyproject.toml)

```toml
[tool.pyright]
pythonVersion = "3.12"
typeCheckingMode = "strict"
reportMissingImports = true
reportMissingTypeStubs = false
reportUnusedImport = true
reportUnusedVariable = true
reportUnusedFunction = true
reportOptionalMemberAccess = true
reportOptionalSubscript = true
reportPrivateUsage = true
```

### Django + mypy Configuration

```toml
[tool.mypy]
python_version = "3.12"
strict = true
plugins = ["mypy_django_plugin.main"]

[tool.mypy.plugins.django-stubs]
django_settings_module = "myproject.settings"

[[tool.mypy.overrides]]
module = "*.migrations.*"
ignore_errors = true
```

---

## Function Templates

### Basic Function

```python
def function_name(
    param1: str,
    param2: int,
    *,
    optional_param: str | None = None,
    flag: bool = False,
) -> ReturnType:
    """Description.

    Args:
        param1: Description.
        param2: Description.
        optional_param: Description.
        flag: Description.

    Returns:
        Description.
    """
    ...
```

### Async Function

```python
async def async_function(
    param: str,
    *,
    timeout: float = 30.0,
) -> ResultType:
    """Async operation description."""
    ...
```

### Generator Function

```python
from collections.abc import Generator

def generate_items(
    source: list[T],
    batch_size: int = 10,
) -> Generator[list[T], None, None]:
    """Yield items in batches."""
    for i in range(0, len(source), batch_size):
        yield source[i:i + batch_size]
```

### Async Generator

```python
from collections.abc import AsyncGenerator

async def async_generate_items(
    source: list[T],
) -> AsyncGenerator[T, None]:
    """Async yield items."""
    for item in source:
        yield item
        await asyncio.sleep(0)
```

---

## Class Templates

### Basic Class

```python
class ClassName:
    """Class description."""

    def __init__(
        self,
        param1: str,
        param2: int,
        *,
        optional: str | None = None,
    ) -> None:
        self.param1 = param1
        self.param2 = param2
        self.optional = optional

    def method(self, arg: str) -> ReturnType:
        """Method description."""
        ...

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ClassName":
        """Create instance from dictionary."""
        return cls(
            param1=data["param1"],
            param2=data["param2"],
            optional=data.get("optional"),
        )

    @staticmethod
    def utility_method(value: str) -> str:
        """Static utility method."""
        return value.strip()
```

### Generic Class (Python 3.12+)

```python
class Container[T]:
    """Generic container class."""

    def __init__(self, value: T) -> None:
        self._value = value

    @property
    def value(self) -> T:
        return self._value

    def map[U](self, func: Callable[[T], U]) -> "Container[U]":
        """Apply function to value."""
        return Container(func(self._value))
```

### Generic Class (Pre-3.12)

```python
from typing import TypeVar, Generic

T = TypeVar("T")

class Container(Generic[T]):
    """Generic container class."""

    def __init__(self, value: T) -> None:
        self._value = value

    @property
    def value(self) -> T:
        return self._value
```

### Dataclass Template

```python
from dataclasses import dataclass, field
from datetime import datetime
from typing import ClassVar

@dataclass
class EntityName:
    """Entity description."""

    id: int
    name: str
    created_at: datetime = field(default_factory=datetime.now)
    tags: list[str] = field(default_factory=list)
    is_active: bool = True

    # Class variable
    _cache: ClassVar[dict[int, "EntityName"]] = {}

    def __post_init__(self) -> None:
        """Post-initialization processing."""
        EntityName._cache[self.id] = self
```

### Frozen Dataclass

```python
from dataclasses import dataclass
from typing import Self

@dataclass(frozen=True)
class ImmutableEntity:
    """Immutable entity."""

    id: int
    name: str

    def with_name(self, name: str) -> Self:
        """Return copy with new name."""
        return ImmutableEntity(id=self.id, name=name)
```

### Dataclass with Slots

```python
from dataclasses import dataclass

@dataclass(slots=True)
class HighPerformanceEntity:
    """Memory-efficient entity."""

    id: int
    name: str
    value: float
```

---

## Protocol Templates

### Basic Protocol

```python
from typing import Protocol

class ProtocolName(Protocol):
    """Protocol description."""

    def method(self, param: str) -> ReturnType:
        """Method that implementing classes must have."""
        ...
```

### Protocol with Properties

```python
from typing import Protocol

class HasIdentity(Protocol):
    """Protocol for identifiable objects."""

    @property
    def id(self) -> int:
        ...

    @property
    def name(self) -> str:
        ...
```

### Generic Protocol

```python
from typing import Protocol

class Repository[T](Protocol):
    """Generic repository protocol."""

    def get(self, id: int) -> T | None:
        ...

    def list(self) -> list[T]:
        ...

    def create(self, item: T) -> T:
        ...

    def delete(self, id: int) -> bool:
        ...
```

### Runtime Checkable Protocol

```python
from typing import Protocol, runtime_checkable

@runtime_checkable
class Closeable(Protocol):
    """Protocol for closeable resources."""

    def close(self) -> None:
        ...

# Usage
if isinstance(resource, Closeable):
    resource.close()
```

### Callback Protocol

```python
from typing import Protocol

class EventHandler(Protocol):
    """Protocol for event handlers."""

    def __call__(self, event: Event, *, context: Context | None = None) -> None:
        ...
```

---

## TypedDict Templates

### Basic TypedDict

```python
from typing import TypedDict

class EntityData(TypedDict):
    """Data structure description."""

    id: int
    name: str
    email: str
```

### TypedDict with Optional Fields

```python
from typing import TypedDict, NotRequired

class EntityData(TypedDict):
    """Data structure with optional fields."""

    id: int
    name: str
    email: NotRequired[str]
    metadata: NotRequired[dict[str, Any]]
```

### TypedDict with Required in total=False

```python
from typing import TypedDict, Required

class SearchParams(TypedDict, total=False):
    """Search parameters - most optional."""

    query: Required[str]  # This one is required
    page: int
    per_page: int
    sort_by: str
    filters: dict[str, str]
```

### Nested TypedDict

```python
from typing import TypedDict, NotRequired

class Address(TypedDict):
    street: str
    city: str
    country: str
    postal_code: NotRequired[str]

class Person(TypedDict):
    name: str
    email: str
    address: Address
```

### API Response TypedDict

```python
from typing import TypedDict, NotRequired

class PaginationMeta(TypedDict):
    page: int
    per_page: int
    total: int
    total_pages: int

class APIError(TypedDict):
    code: str
    message: str
    field: NotRequired[str]

class APIResponse[T](TypedDict):
    success: bool
    data: NotRequired[T]
    errors: NotRequired[list[APIError]]
    meta: NotRequired[PaginationMeta]
```

---

## Callable Templates

### Basic Callable Types

```python
from collections.abc import Callable

# Simple callback
Callback = Callable[[str], None]

# With multiple args
Handler = Callable[[int, str, bool], dict[str, Any]]

# Returning None
VoidCallback = Callable[[], None]

# Async callback
from collections.abc import Awaitable
AsyncCallback = Callable[[str], Awaitable[None]]
```

### Decorator Template (Preserving Signature)

```python
from typing import ParamSpec, TypeVar
from collections.abc import Callable
from functools import wraps

P = ParamSpec("P")
T = TypeVar("T")

def decorator_name(func: Callable[P, T]) -> Callable[P, T]:
    """Decorator description."""
    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        # Pre-processing
        result = func(*args, **kwargs)
        # Post-processing
        return result
    return wrapper
```

### Decorator Factory Template

```python
from typing import ParamSpec, TypeVar
from collections.abc import Callable
from functools import wraps

P = ParamSpec("P")
T = TypeVar("T")

def decorator_factory(
    param1: str,
    param2: int = 10,
) -> Callable[[Callable[P, T]], Callable[P, T]]:
    """Decorator factory description."""
    def decorator(func: Callable[P, T]) -> Callable[P, T]:
        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            # Use param1, param2
            return func(*args, **kwargs)
        return wrapper
    return decorator
```

### Async Decorator Template

```python
from typing import ParamSpec, TypeVar
from collections.abc import Callable, Awaitable
from functools import wraps

P = ParamSpec("P")
T = TypeVar("T")

def async_decorator(
    func: Callable[P, Awaitable[T]]
) -> Callable[P, Awaitable[T]]:
    """Async decorator description."""
    @wraps(func)
    async def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        # Pre-processing
        result = await func(*args, **kwargs)
        # Post-processing
        return result
    return wrapper
```

### Decorator Adding Arguments

```python
from typing import ParamSpec, TypeVar, Concatenate
from collections.abc import Callable
from functools import wraps

P = ParamSpec("P")
T = TypeVar("T")

def with_context(
    func: Callable[Concatenate[Context, P], T]
) -> Callable[P, T]:
    """Inject context as first argument."""
    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        ctx = get_context()
        return func(ctx, *args, **kwargs)
    return wrapper
```

---

## Django Templates

### Model Method Types

```python
from django.db import models
from decimal import Decimal

class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def discounted_price(self, discount: float) -> Decimal:
        """Calculate discounted price."""
        return self.price * (1 - Decimal(str(discount)))

    @classmethod
    def get_active(cls) -> models.QuerySet["Product"]:
        """Return active products queryset."""
        return cls.objects.filter(is_active=True)
```

### View Function Types

```python
from django.http import HttpRequest, HttpResponse, JsonResponse

def view_name(request: HttpRequest) -> HttpResponse:
    """View description."""
    ...
    return HttpResponse("OK")

def json_view(request: HttpRequest) -> JsonResponse:
    """JSON view description."""
    data = {"key": "value"}
    return JsonResponse(data)
```

### Authenticated View Types

```python
from django.http import HttpRequest
from django.contrib.auth.models import User

class AuthenticatedHttpRequest(HttpRequest):
    user: User

def authenticated_view(request: AuthenticatedHttpRequest) -> JsonResponse:
    """View requiring authentication."""
    user_id: int = request.user.id
    ...
```

---

## FastAPI Templates

### Pydantic Model

```python
from pydantic import BaseModel, Field, EmailStr

class EntityCreate(BaseModel):
    """Request model for creating entity."""

    name: str = Field(min_length=1, max_length=100)
    email: EmailStr
    age: int = Field(ge=0, le=150)

class EntityResponse(BaseModel):
    """Response model for entity."""

    id: int
    name: str
    email: str
    is_active: bool

    model_config = {"from_attributes": True}
```

### Endpoint Template

```python
from fastapi import FastAPI, HTTPException, Query, Path
from typing import Annotated

app = FastAPI()

@app.get("/entities/{entity_id}", response_model=EntityResponse)
async def get_entity(
    entity_id: Annotated[int, Path(ge=1, description="Entity ID")],
) -> EntityResponse:
    """Get entity by ID."""
    entity = await get_entity_from_db(entity_id)
    if not entity:
        raise HTTPException(status_code=404, detail="Not found")
    return EntityResponse.model_validate(entity)

@app.get("/entities", response_model=list[EntityResponse])
async def list_entities(
    page: Annotated[int, Query(ge=1)] = 1,
    per_page: Annotated[int, Query(ge=1, le=100)] = 20,
    active_only: Annotated[bool, Query()] = True,
) -> list[EntityResponse]:
    """List entities with pagination."""
    entities = await list_entities_from_db(page, per_page, active_only)
    return [EntityResponse.model_validate(e) for e in entities]
```

### Dependency Template

```python
from fastapi import Depends, Header, HTTPException
from typing import Annotated

async def get_current_user(
    authorization: Annotated[str, Header()],
) -> User:
    """Dependency to get current user from token."""
    token = authorization.replace("Bearer ", "")
    user = await verify_token(token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    return user

CurrentUser = Annotated[User, Depends(get_current_user)]

@app.get("/me")
async def get_me(user: CurrentUser) -> UserResponse:
    """Get current user."""
    return UserResponse.model_validate(user)
```

---

## Type Alias Templates

### Simple Aliases (Python 3.12+)

```python
# Simple alias
type UserId = int
type Email = str

# Generic alias
type ListOrSet[T] = list[T] | set[T]

# Callable alias
type Handler[T] = Callable[[Request], T]

# Recursive alias
type JSON = dict[str, "JSON"] | list["JSON"] | str | int | float | bool | None
```

### Simple Aliases (Pre-3.12)

```python
from typing import TypeAlias

UserId: TypeAlias = int
Email: TypeAlias = str
JSON: TypeAlias = dict[str, Any] | list[Any] | str | int | float | bool | None
```

---

## Overload Templates

### Method Overloading

```python
from typing import overload

@overload
def process(value: str) -> str: ...
@overload
def process(value: int) -> int: ...
@overload
def process(value: list[str]) -> list[str]: ...

def process(value: str | int | list[str]) -> str | int | list[str]:
    """Process various types."""
    if isinstance(value, str):
        return value.upper()
    elif isinstance(value, int):
        return value * 2
    else:
        return [v.upper() for v in value]
```

### Overload with Optional Return

```python
from typing import overload, Literal

@overload
def get_item(key: str, default: None = None) -> str | None: ...
@overload
def get_item(key: str, default: str) -> str: ...

def get_item(key: str, default: str | None = None) -> str | None:
    """Get item with optional default."""
    value = _storage.get(key)
    if value is None:
        return default
    return value
```

---

## Utility Templates

### TypeGuard

```python
from typing import TypeGuard, Any

def is_string_list(value: list[Any]) -> TypeGuard[list[str]]:
    """Check if all items are strings."""
    return all(isinstance(item, str) for item in value)

# Usage
def process(data: list[Any]) -> None:
    if is_string_list(data):
        # data is now list[str]
        for item in data:
            print(item.upper())
```

### Literal Types

```python
from typing import Literal

Status = Literal["pending", "active", "completed", "failed"]
SortOrder = Literal["asc", "desc"]
HTTPMethod = Literal["GET", "POST", "PUT", "DELETE", "PATCH"]

def set_status(item_id: int, status: Status) -> None:
    """Set item status."""
    ...
```

### Final and ClassVar

```python
from typing import Final, ClassVar

class Config:
    # Constant - cannot be reassigned
    MAX_RETRIES: Final[int] = 3

    # Class variable - shared across instances
    _instance_count: ClassVar[int] = 0

    def __init__(self) -> None:
        Config._instance_count += 1
```

### Self Type

```python
from typing import Self

class Builder:
    def with_name(self, name: str) -> Self:
        self._name = name
        return self

    def with_value(self, value: int) -> Self:
        self._value = value
        return self
```

---

*Copy and adapt these templates for your specific use cases.*
