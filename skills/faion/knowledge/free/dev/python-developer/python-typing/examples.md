# Python Typing Examples

Real-world examples of Python type hints for common patterns.

---

## Table of Contents

1. [Basic Types](#basic-types)
2. [Generic Classes](#generic-classes)
3. [Protocol Examples](#protocol-examples)
4. [TypedDict Examples](#typeddict-examples)
5. [Callable and Decorators](#callable-and-decorators)
6. [Dataclass Examples](#dataclass-examples)
7. [Django Examples](#django-examples)
8. [FastAPI Examples](#fastapi-examples)
9. [Advanced Patterns](#advanced-patterns)

---

## Basic Types

### Variables and Collections

```python
from typing import Any
from collections.abc import Sequence, Mapping, Iterable

# Primitives
name: str = "Alice"
age: int = 30
height: float = 5.9
is_active: bool = True

# Collections (Python 3.9+)
numbers: list[int] = [1, 2, 3]
unique_ids: set[str] = {"a", "b", "c"}
coordinates: tuple[float, float] = (10.5, 20.3)
config: dict[str, Any] = {"debug": True, "port": 8080}

# Immutable tuple with mixed types
record: tuple[int, str, bool] = (1, "test", True)

# Variable-length tuple
scores: tuple[int, ...] = (85, 90, 78, 92)

# Abstract types (preferred for function parameters)
def process_items(items: Iterable[str]) -> list[str]:
    return [item.upper() for item in items]

def lookup(data: Mapping[str, int], key: str) -> int | None:
    return data.get(key)
```

### Functions with Multiple Return Types

```python
from typing import overload

# Using union return
def parse_value(value: str) -> int | float | None:
    try:
        if "." in value:
            return float(value)
        return int(value)
    except ValueError:
        return None

# Using overload for precise typing
@overload
def get_item(index: int) -> str: ...
@overload
def get_item(index: slice) -> list[str]: ...

def get_item(index: int | slice) -> str | list[str]:
    items = ["a", "b", "c", "d"]
    return items[index]

# Usage - type checker knows the exact return type
single: str = get_item(0)
multiple: list[str] = get_item(slice(0, 2))
```

---

## Generic Classes

### Python 3.12+ Generic Syntax

```python
# Simple generic class
class Stack[T]:
    def __init__(self) -> None:
        self._items: list[T] = []

    def push(self, item: T) -> None:
        self._items.append(item)

    def pop(self) -> T:
        return self._items.pop()

    def peek(self) -> T | None:
        return self._items[-1] if self._items else None

    def __len__(self) -> int:
        return len(self._items)

# Usage
int_stack: Stack[int] = Stack()
int_stack.push(1)
int_stack.push(2)
value: int = int_stack.pop()  # Type checker knows this is int

# Generic with bounds
class NumberStack[T: (int, float)]:
    def __init__(self) -> None:
        self._items: list[T] = []

    def push(self, item: T) -> None:
        self._items.append(item)

    def sum(self) -> T:
        return sum(self._items)  # type: ignore[return-value]

# Multiple type parameters
class Pair[K, V]:
    def __init__(self, key: K, value: V) -> None:
        self.key = key
        self.value = value

    def swap(self) -> "Pair[V, K]":
        return Pair(self.value, self.key)

# Generic with upper bound
from collections.abc import Hashable

class Cache[K: Hashable, V]:
    def __init__(self) -> None:
        self._data: dict[K, V] = {}

    def get(self, key: K) -> V | None:
        return self._data.get(key)

    def set(self, key: K, value: V) -> None:
        self._data[key] = value
```

### Repository Pattern

```python
from abc import abstractmethod
from typing import Protocol

class Entity(Protocol):
    id: int

class Repository[T: Entity]:
    """Generic repository for CRUD operations."""

    @abstractmethod
    def get(self, id: int) -> T | None:
        ...

    @abstractmethod
    def list(self, limit: int = 100, offset: int = 0) -> list[T]:
        ...

    @abstractmethod
    def create(self, item: T) -> T:
        ...

    @abstractmethod
    def update(self, item: T) -> T:
        ...

    @abstractmethod
    def delete(self, id: int) -> bool:
        ...


class User:
    def __init__(self, id: int, name: str, email: str) -> None:
        self.id = id
        self.name = name
        self.email = email


class UserRepository(Repository[User]):
    def __init__(self) -> None:
        self._users: dict[int, User] = {}

    def get(self, id: int) -> User | None:
        return self._users.get(id)

    def list(self, limit: int = 100, offset: int = 0) -> list[User]:
        users = list(self._users.values())
        return users[offset:offset + limit]

    def create(self, item: User) -> User:
        self._users[item.id] = item
        return item

    def update(self, item: User) -> User:
        self._users[item.id] = item
        return item

    def delete(self, id: int) -> bool:
        if id in self._users:
            del self._users[id]
            return True
        return False
```

---

## Protocol Examples

### Basic Protocol

```python
from typing import Protocol, runtime_checkable

class Drawable(Protocol):
    """Protocol for objects that can be drawn."""

    def draw(self, canvas: "Canvas") -> None:
        ...


class Circle:
    def __init__(self, x: float, y: float, radius: float) -> None:
        self.x = x
        self.y = y
        self.radius = radius

    def draw(self, canvas: "Canvas") -> None:
        canvas.draw_circle(self.x, self.y, self.radius)


class Rectangle:
    def __init__(self, x: float, y: float, width: float, height: float) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self, canvas: "Canvas") -> None:
        canvas.draw_rectangle(self.x, self.y, self.width, self.height)


def render_all(shapes: list[Drawable], canvas: "Canvas") -> None:
    """Works with any object implementing draw()."""
    for shape in shapes:
        shape.draw(canvas)
```

### Protocol with Properties

```python
from typing import Protocol

class HasName(Protocol):
    @property
    def name(self) -> str:
        ...

class HasId(Protocol):
    @property
    def id(self) -> int:
        ...

class Identifiable(HasId, HasName, Protocol):
    """Combined protocol."""
    pass

class User:
    def __init__(self, id: int, name: str) -> None:
        self._id = id
        self._name = name

    @property
    def id(self) -> int:
        return self._id

    @property
    def name(self) -> str:
        return self._name

def get_display_name(entity: Identifiable) -> str:
    return f"{entity.name} (#{entity.id})"

# Works because User has matching properties
user = User(1, "Alice")
print(get_display_name(user))  # "Alice (#1)"
```

### Generic Protocol

```python
from typing import Protocol

class Comparable[T](Protocol):
    def __lt__(self, other: T) -> bool:
        ...

    def __le__(self, other: T) -> bool:
        ...

    def __gt__(self, other: T) -> bool:
        ...

    def __ge__(self, other: T) -> bool:
        ...

def find_max[T: Comparable[T]](items: list[T]) -> T:
    """Find maximum in a list of comparable items."""
    if not items:
        raise ValueError("Empty list")
    result = items[0]
    for item in items[1:]:
        if item > result:
            result = item
    return result
```

### Runtime Checkable Protocol

```python
from typing import Protocol, runtime_checkable

@runtime_checkable
class Closeable(Protocol):
    def close(self) -> None:
        ...

class FileHandler:
    def __init__(self, path: str) -> None:
        self.path = path
        self._handle: Any = None

    def close(self) -> None:
        if self._handle:
            self._handle.close()

class DatabaseConnection:
    def close(self) -> None:
        print("Closing database connection")

def cleanup(resources: list[Any]) -> None:
    """Close all closeable resources."""
    for resource in resources:
        if isinstance(resource, Closeable):  # Runtime check works!
            resource.close()

# Usage
resources = [FileHandler("test.txt"), DatabaseConnection(), "not closeable"]
cleanup(resources)  # Only closes FileHandler and DatabaseConnection
```

---

## TypedDict Examples

### Basic TypedDict

```python
from typing import TypedDict, NotRequired, Required

class UserData(TypedDict):
    id: int
    email: str
    name: str

def process_user(data: UserData) -> str:
    # Type-safe access
    return f"User {data['name']} <{data['email']}>"

# With optional fields
class UserProfile(TypedDict):
    id: int
    email: str
    name: str
    bio: NotRequired[str]
    avatar_url: NotRequired[str | None]
    followers_count: NotRequired[int]

def render_profile(profile: UserProfile) -> str:
    bio = profile.get("bio", "No bio provided")
    return f"{profile['name']}: {bio}"
```

### Nested TypedDict

```python
from typing import TypedDict, NotRequired

class Address(TypedDict):
    street: str
    city: str
    country: str
    postal_code: NotRequired[str]

class Company(TypedDict):
    name: str
    address: Address

class Employee(TypedDict):
    id: int
    name: str
    email: str
    company: Company
    manager_id: NotRequired[int]

def get_employee_location(employee: Employee) -> str:
    company = employee["company"]
    address = company["address"]
    return f"{address['city']}, {address['country']}"
```

### TypedDict with total=False

```python
from typing import TypedDict, Required

class SearchParams(TypedDict, total=False):
    """Most fields are optional."""
    query: Required[str]  # This one is required
    page: int
    per_page: int
    sort_by: str
    sort_order: str
    filters: dict[str, str]

def search(params: SearchParams) -> list[dict[str, Any]]:
    query = params["query"]  # Safe - it's Required
    page = params.get("page", 1)  # Optional with default
    per_page = params.get("per_page", 20)
    # ... perform search
    return []
```

### API Response TypedDict

```python
from typing import TypedDict, NotRequired, Generic, TypeVar

T = TypeVar("T")

class PaginationMeta(TypedDict):
    page: int
    per_page: int
    total: int
    total_pages: int

class APIError(TypedDict):
    code: str
    message: str
    field: NotRequired[str]

class APIResponse(TypedDict):
    success: bool
    data: NotRequired[dict[str, Any] | list[dict[str, Any]]]
    errors: NotRequired[list[APIError]]
    meta: NotRequired[PaginationMeta]

def handle_response(response: APIResponse) -> None:
    if response["success"]:
        data = response.get("data")
        if data:
            print(f"Got data: {data}")
    else:
        errors = response.get("errors", [])
        for error in errors:
            print(f"Error {error['code']}: {error['message']}")
```

---

## Callable and Decorators

### Basic Callable Types

```python
from collections.abc import Callable, Awaitable

# Simple callback
Callback = Callable[[str], None]

def process_with_callback(data: str, callback: Callback) -> None:
    result = data.upper()
    callback(result)

# Async callback
AsyncCallback = Callable[[str], Awaitable[None]]

async def process_async(data: str, callback: AsyncCallback) -> None:
    result = data.upper()
    await callback(result)

# Multiple arguments
Handler = Callable[[int, str, bool], dict[str, Any]]

def dispatch(handler: Handler, id: int, name: str, active: bool) -> dict[str, Any]:
    return handler(id, name, active)
```

### Decorator with ParamSpec

```python
from typing import ParamSpec, TypeVar
from collections.abc import Callable
from functools import wraps
import time

P = ParamSpec("P")
T = TypeVar("T")

def timed(func: Callable[P, T]) -> Callable[P, T]:
    """Decorator that logs execution time."""
    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"{func.__name__} took {elapsed:.4f}s")
        return result
    return wrapper

@timed
def process_data(items: list[int], multiplier: int = 2) -> list[int]:
    return [item * multiplier for item in items]

# Type checker knows the exact signature is preserved
result: list[int] = process_data([1, 2, 3], multiplier=3)
```

### Decorator Factory

```python
from typing import ParamSpec, TypeVar
from collections.abc import Callable
from functools import wraps

P = ParamSpec("P")
T = TypeVar("T")

def retry(times: int = 3, delay: float = 1.0) -> Callable[[Callable[P, T]], Callable[P, T]]:
    """Retry decorator factory."""
    def decorator(func: Callable[P, T]) -> Callable[P, T]:
        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            last_exception: Exception | None = None
            for attempt in range(times):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < times - 1:
                        time.sleep(delay)
            raise last_exception or RuntimeError("Retry failed")
        return wrapper
    return decorator

@retry(times=3, delay=0.5)
def fetch_data(url: str) -> dict[str, Any]:
    # May fail, will be retried
    response = requests.get(url)
    return response.json()
```

### Adding Arguments with Concatenate

```python
from typing import ParamSpec, TypeVar, Concatenate
from collections.abc import Callable
from functools import wraps

P = ParamSpec("P")
T = TypeVar("T")

class Context:
    def __init__(self, user_id: int) -> None:
        self.user_id = user_id

def with_context(
    func: Callable[Concatenate[Context, P], T]
) -> Callable[P, T]:
    """Automatically inject context as first argument."""
    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        ctx = Context(user_id=get_current_user_id())
        return func(ctx, *args, **kwargs)
    return wrapper

@with_context
def create_post(ctx: Context, title: str, content: str) -> dict[str, Any]:
    return {
        "author_id": ctx.user_id,
        "title": title,
        "content": content,
    }

# Caller doesn't need to pass context
post: dict[str, Any] = create_post("Hello", content="World")
```

### Async Decorator

```python
from typing import ParamSpec, TypeVar
from collections.abc import Callable, Awaitable
from functools import wraps

P = ParamSpec("P")
T = TypeVar("T")

def async_timed(
    func: Callable[P, Awaitable[T]]
) -> Callable[P, Awaitable[T]]:
    """Async decorator that logs execution time."""
    @wraps(func)
    async def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        start = time.perf_counter()
        result = await func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"{func.__name__} took {elapsed:.4f}s")
        return result
    return wrapper

@async_timed
async def fetch_user(user_id: int) -> dict[str, Any]:
    async with aiohttp.ClientSession() as session:
        async with session.get(f"/users/{user_id}") as response:
            return await response.json()
```

---

## Dataclass Examples

### Basic Dataclass

```python
from dataclasses import dataclass, field
from datetime import datetime
from typing import ClassVar

@dataclass
class User:
    id: int
    email: str
    name: str
    is_active: bool = True
    created_at: datetime = field(default_factory=datetime.now)
    tags: list[str] = field(default_factory=list)

    # Class variable (not an instance field)
    _instances: ClassVar[int] = 0

    def __post_init__(self) -> None:
        User._instances += 1

    def full_display(self) -> str:
        status = "active" if self.is_active else "inactive"
        return f"{self.name} <{self.email}> ({status})"
```

### Immutable Dataclass

```python
from dataclasses import dataclass
from typing import Self

@dataclass(frozen=True)
class Point:
    x: float
    y: float

    def distance_to(self, other: Self) -> float:
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5

    def moved(self, dx: float, dy: float) -> Self:
        """Return a new point moved by dx, dy."""
        return Point(self.x + dx, self.y + dy)

@dataclass(frozen=True)
class Rectangle:
    top_left: Point
    bottom_right: Point

    @property
    def width(self) -> float:
        return self.bottom_right.x - self.top_left.x

    @property
    def height(self) -> float:
        return self.bottom_right.y - self.top_left.y

    @property
    def area(self) -> float:
        return self.width * self.height
```

### Dataclass with Slots

```python
from dataclasses import dataclass

@dataclass(slots=True)
class HighPerformanceUser:
    """Uses slots for better memory and performance."""
    id: int
    name: str
    email: str
    score: float = 0.0

# Slots prevent adding arbitrary attributes
user = HighPerformanceUser(1, "Alice", "alice@example.com")
# user.extra = "value"  # Error! Can't add attributes with slots
```

### Generic Dataclass

```python
from dataclasses import dataclass
from typing import Generic, TypeVar

T = TypeVar("T")

@dataclass
class Result(Generic[T]):
    """Generic result wrapper."""
    success: bool
    data: T | None = None
    error: str | None = None

    @classmethod
    def ok(cls, data: T) -> "Result[T]":
        return cls(success=True, data=data)

    @classmethod
    def fail(cls, error: str) -> "Result[T]":
        return cls(success=False, error=error)

# Usage with specific types
def fetch_user(id: int) -> Result[User]:
    try:
        user = get_user_from_db(id)
        return Result.ok(user)
    except NotFoundError:
        return Result.fail(f"User {id} not found")

result: Result[User] = fetch_user(1)
if result.success and result.data:
    print(result.data.name)
```

---

## Django Examples

### Models

```python
from django.db import models
from decimal import Decimal

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self) -> str:
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products"
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name

    def discounted_price(self, discount_percent: float) -> Decimal:
        """Calculate price after discount."""
        discount = Decimal(str(discount_percent)) / Decimal("100")
        return self.price * (1 - discount)

    @classmethod
    def get_active(cls) -> models.QuerySet["Product"]:
        """Return queryset of active products."""
        return cls.objects.filter(is_active=True)
```

### Views

```python
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

# Custom request type for authenticated views
class AuthenticatedHttpRequest(HttpRequest):
    user: User  # Guaranteed to be authenticated User, not AnonymousUser

def product_list(request: HttpRequest) -> JsonResponse:
    """List all active products."""
    products = Product.get_active().select_related("category")
    data = [
        {
            "id": p.id,
            "name": p.name,
            "price": str(p.price),
            "category": p.category.name,
        }
        for p in products
    ]
    return JsonResponse({"products": data})

def product_detail(request: HttpRequest, product_id: int) -> JsonResponse:
    """Get single product details."""
    product = get_object_or_404(Product, id=product_id, is_active=True)
    return JsonResponse({
        "id": product.id,
        "name": product.name,
        "description": product.description,
        "price": str(product.price),
        "category": product.category.name,
    })

@login_required
def create_order(request: AuthenticatedHttpRequest) -> JsonResponse:
    """Create order for authenticated user."""
    user: User = request.user  # Type checker knows this is User, not AnonymousUser
    # ... create order logic
    return JsonResponse({"status": "created"})
```

### Services

```python
from django.db import transaction
from decimal import Decimal

class OrderService:
    """Service for order operations."""

    def __init__(self, user: User) -> None:
        self.user = user

    @transaction.atomic
    def create_order(
        self,
        items: list[dict[str, int | Decimal]],
        shipping_address: str,
    ) -> Order:
        """Create a new order with items."""
        order = Order.objects.create(
            user=self.user,
            shipping_address=shipping_address,
            status="pending",
        )

        total = Decimal("0")
        for item_data in items:
            product = Product.objects.get(id=item_data["product_id"])
            quantity = int(item_data["quantity"])

            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                price=product.price,
            )
            total += product.price * quantity

        order.total = total
        order.save()

        return order

    def get_user_orders(
        self,
        status: str | None = None,
        limit: int = 10,
    ) -> models.QuerySet[Order]:
        """Get orders for the current user."""
        qs = Order.objects.filter(user=self.user)
        if status:
            qs = qs.filter(status=status)
        return qs.order_by("-created_at")[:limit]
```

---

## FastAPI Examples

### Basic Endpoints

```python
from fastapi import FastAPI, HTTPException, Query, Path, Depends
from pydantic import BaseModel, Field, EmailStr
from typing import Annotated

app = FastAPI()

# Request/Response models
class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=100)
    name: str = Field(min_length=1, max_length=100)

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    name: str
    is_active: bool

    model_config = {"from_attributes": True}

class UserListResponse(BaseModel):
    users: list[UserResponse]
    total: int
    page: int
    per_page: int

# Endpoints
@app.post("/users", response_model=UserResponse, status_code=201)
async def create_user(user: UserCreate) -> UserResponse:
    """Create a new user."""
    db_user = await create_user_in_db(user)
    return UserResponse.model_validate(db_user)

@app.get("/users/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: Annotated[int, Path(ge=1, description="User ID")],
) -> UserResponse:
    """Get user by ID."""
    user = await get_user_from_db(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserResponse.model_validate(user)

@app.get("/users", response_model=UserListResponse)
async def list_users(
    page: Annotated[int, Query(ge=1)] = 1,
    per_page: Annotated[int, Query(ge=1, le=100)] = 20,
    active_only: Annotated[bool, Query()] = True,
) -> UserListResponse:
    """List users with pagination."""
    users, total = await list_users_from_db(
        page=page,
        per_page=per_page,
        active_only=active_only,
    )
    return UserListResponse(
        users=[UserResponse.model_validate(u) for u in users],
        total=total,
        page=page,
        per_page=per_page,
    )
```

### Dependencies

```python
from fastapi import Depends, Header, HTTPException
from typing import Annotated

class CurrentUser:
    def __init__(self, id: int, email: str, roles: list[str]) -> None:
        self.id = id
        self.email = email
        self.roles = roles

async def get_current_user(
    authorization: Annotated[str, Header()],
) -> CurrentUser:
    """Dependency to get current authenticated user."""
    token = authorization.replace("Bearer ", "")
    user_data = await verify_token(token)
    if not user_data:
        raise HTTPException(status_code=401, detail="Invalid token")
    return CurrentUser(**user_data)

async def require_admin(
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
) -> CurrentUser:
    """Dependency to require admin role."""
    if "admin" not in current_user.roles:
        raise HTTPException(status_code=403, detail="Admin required")
    return current_user

@app.delete("/users/{user_id}")
async def delete_user(
    user_id: int,
    admin: Annotated[CurrentUser, Depends(require_admin)],
) -> dict[str, str]:
    """Delete user (admin only)."""
    await delete_user_from_db(user_id)
    return {"status": "deleted"}
```

### Pydantic Models with Validation

```python
from pydantic import BaseModel, Field, field_validator, model_validator
from datetime import date
from typing import Self

class ProductCreate(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    description: str = Field(default="", max_length=5000)
    price: float = Field(gt=0)
    discount_price: float | None = Field(default=None, gt=0)
    sku: str = Field(pattern=r"^[A-Z]{3}-\d{6}$")
    available_from: date | None = None
    available_until: date | None = None

    @field_validator("name")
    @classmethod
    def name_must_not_be_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Name cannot be empty or whitespace only")
        return v.strip()

    @model_validator(mode="after")
    def validate_prices(self) -> Self:
        if self.discount_price and self.discount_price >= self.price:
            raise ValueError("Discount price must be less than regular price")
        return self

    @model_validator(mode="after")
    def validate_dates(self) -> Self:
        if (
            self.available_from
            and self.available_until
            and self.available_from > self.available_until
        ):
            raise ValueError("available_from must be before available_until")
        return self
```

---

## Advanced Patterns

### Self Type

```python
from typing import Self

class Builder:
    def __init__(self) -> None:
        self._name: str = ""
        self._age: int = 0

    def with_name(self, name: str) -> Self:
        self._name = name
        return self

    def with_age(self, age: int) -> Self:
        self._age = age
        return self

    def build(self) -> dict[str, str | int]:
        return {"name": self._name, "age": self._age}

# Works correctly with inheritance
class ExtendedBuilder(Builder):
    def __init__(self) -> None:
        super().__init__()
        self._email: str = ""

    def with_email(self, email: str) -> Self:
        self._email = email
        return self

# Method chaining returns correct type
user = ExtendedBuilder().with_name("Alice").with_email("alice@example.com").build()
```

### Literal Types

```python
from typing import Literal

Status = Literal["pending", "active", "inactive", "deleted"]
SortOrder = Literal["asc", "desc"]
HTTPMethod = Literal["GET", "POST", "PUT", "DELETE", "PATCH"]

def set_status(user_id: int, status: Status) -> None:
    # Type checker ensures only valid status values
    ...

def sort_items(
    items: list[int],
    order: SortOrder = "asc"
) -> list[int]:
    reverse = order == "desc"
    return sorted(items, reverse=reverse)

# Type error: "unknown" is not a valid Status
# set_status(1, "unknown")  # Error!
```

### TypeGuard

```python
from typing import TypeGuard, Any

def is_string_list(val: list[Any]) -> TypeGuard[list[str]]:
    """Check if all items in list are strings."""
    return all(isinstance(item, str) for item in val)

def process(data: list[Any]) -> None:
    if is_string_list(data):
        # Type checker knows data is list[str] here
        for item in data:
            print(item.upper())  # .upper() is valid for str
    else:
        print("Not all strings")

def is_user_dict(val: dict[str, Any]) -> TypeGuard[UserData]:
    """Check if dict matches UserData structure."""
    required_keys = {"id", "email", "name"}
    return (
        isinstance(val, dict)
        and required_keys <= val.keys()
        and isinstance(val.get("id"), int)
        and isinstance(val.get("email"), str)
        and isinstance(val.get("name"), str)
    )
```

### Never Type

```python
from typing import Never, NoReturn

def assert_never(value: Never) -> Never:
    """Used for exhaustiveness checking."""
    raise AssertionError(f"Unexpected value: {value}")

Status = Literal["pending", "active", "completed"]

def handle_status(status: Status) -> str:
    match status:
        case "pending":
            return "Waiting..."
        case "active":
            return "In progress"
        case "completed":
            return "Done!"
        case _:
            # If we add a new status, type checker will catch it here
            assert_never(status)

def fail(message: str) -> NoReturn:
    """Function that never returns normally."""
    raise RuntimeError(message)
```

### Final and ClassVar

```python
from typing import Final, ClassVar

class Config:
    # Class constant - cannot be reassigned
    MAX_RETRIES: Final[int] = 3
    API_VERSION: Final[str] = "v2"

    # Class variable - shared across instances
    _instance_count: ClassVar[int] = 0

    def __init__(self, name: str) -> None:
        self.name = name
        Config._instance_count += 1

    @classmethod
    def get_instance_count(cls) -> int:
        return cls._instance_count

# Error: Cannot assign to final attribute
# Config.MAX_RETRIES = 5  # Type error!
```

---

*These examples cover common typing patterns in Python 3.12+. Adjust for earlier versions as needed.*
