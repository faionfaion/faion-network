# Modern Python Examples

Real-world examples demonstrating Python 3.12-3.14 features and best practices.

---

## 1. PEP 695: Type Parameter Syntax (Python 3.12+)

### Generic Classes

```python
# Old way (pre-3.12)
from typing import TypeVar, Generic

T = TypeVar("T")
E = TypeVar("E", bound=Exception)

class Result(Generic[T, E]):
    def __init__(self, value: T | None, error: E | None) -> None:
        self._value = value
        self._error = error

# New way (3.12+)
class Result[T, E: Exception]:
    """A result type that holds either a value or an error."""

    def __init__(self, value: T | None = None, error: E | None = None) -> None:
        self._value = value
        self._error = error

    @property
    def is_ok(self) -> bool:
        return self._error is None

    @property
    def is_err(self) -> bool:
        return self._error is not None

    def unwrap(self) -> T:
        if self._error is not None:
            raise self._error
        assert self._value is not None
        return self._value

    def unwrap_or(self, default: T) -> T:
        if self._error is not None:
            return default
        assert self._value is not None
        return self._value

# Usage
def divide(a: float, b: float) -> Result[float, ValueError]:
    if b == 0:
        return Result(error=ValueError("Division by zero"))
    return Result(value=a / b)

result = divide(10, 2)
if result.is_ok:
    print(result.unwrap())  # 5.0
```

### Generic Functions

```python
# Old way
from typing import TypeVar, Iterable

T = TypeVar("T")

def first(items: Iterable[T]) -> T | None:
    for item in items:
        return item
    return None

# New way (3.12+)
def first[T](items: Iterable[T]) -> T | None:
    """Return the first item from an iterable, or None if empty."""
    for item in items:
        return item
    return None

def chunk[T](items: list[T], size: int) -> list[list[T]]:
    """Split a list into chunks of specified size."""
    return [items[i:i + size] for i in range(0, len(items), size)]

# With constraints
def max_item[T: (int, float, str)](items: list[T]) -> T:
    """Return the maximum item (works with int, float, or str)."""
    return max(items)
```

### Type Aliases

```python
# Old way
from typing import TypeAlias, Callable

Handler: TypeAlias = Callable[[str, int], bool]
JsonValue: TypeAlias = str | int | float | bool | None | list["JsonValue"] | dict[str, "JsonValue"]

# New way (3.12+)
type Handler = Callable[[str, int], bool]
type JsonValue = str | int | float | bool | None | list[JsonValue] | dict[str, JsonValue]

# Generic type aliases
type Vector[T] = list[tuple[T, T]]
type Matrix[T] = list[list[T]]
type Callback[T, R] = Callable[[T], R]

# Usage
def process_vectors(vectors: Vector[float]) -> float:
    return sum(x + y for x, y in vectors)
```

---

## 2. PEP 701: F-String Improvements (Python 3.12+)

### Quote Reuse

```python
# Pre-3.12: Had to alternate quote types
data = {"name": "Alice", "age": 30}
message = f"Hello {data['name']}, you are {data['age']} years old"  # Now works!

# Nested f-strings with same quotes
items = ["apple", "banana", "cherry"]
result = f"Items: {', '.join(f'{item.upper()}' for item in items)}"
# Output: "Items: APPLE, BANANA, CHERRY"
```

### Multiline Expressions

```python
# Complex expressions can span multiple lines
users = [
    {"name": "Alice", "score": 95},
    {"name": "Bob", "score": 87},
    {"name": "Charlie", "score": 92},
]

summary = f"""
Report Summary:
Total users: {len(users)}
Average score: {
    sum(user['score'] for user in users) / len(users)
    if users else 0
:.2f}
Top scorer: {
    max(users, key=lambda u: u['score'])['name']
    if users else 'N/A'
}
"""
```

### Backslashes in Expressions

```python
# Pre-3.12: Backslashes were forbidden
path = "C:\\Users\\Alice\\Documents"
unix_path = f"Unix path: {path.replace('\\', '/')}"  # Now works!

# Multi-line strings in expressions
names = ["Alice", "Bob", "Charlie"]
formatted = f"Names:\n{'\n'.join(f'  - {name}' for name in names)}"
```

### Debug Format with `=`

```python
def calculate_price(base: float, tax_rate: float, discount: float) -> float:
    subtotal = base * (1 - discount)
    tax = subtotal * tax_rate
    total = subtotal + tax

    # Debug output
    print(f"{base=}, {tax_rate=}, {discount=}")
    print(f"{subtotal=:.2f}, {tax=:.2f}, {total=:.2f}")

    return total

# Output:
# base=100.0, tax_rate=0.1, discount=0.15
# subtotal=85.00, tax=8.50, total=93.50
```

---

## 3. Async Patterns with TaskGroup (Python 3.11+)

### Basic TaskGroup

```python
import asyncio
import aiohttp

async def fetch_url(session: aiohttp.ClientSession, url: str) -> dict:
    """Fetch JSON data from a URL."""
    async with session.get(url) as response:
        return await response.json()

async def fetch_all_data() -> dict[str, dict]:
    """Fetch data from multiple APIs concurrently."""
    async with aiohttp.ClientSession() as session:
        async with asyncio.TaskGroup() as tg:
            users_task = tg.create_task(
                fetch_url(session, "https://api.example.com/users")
            )
            products_task = tg.create_task(
                fetch_url(session, "https://api.example.com/products")
            )
            orders_task = tg.create_task(
                fetch_url(session, "https://api.example.com/orders")
            )

    # Tasks are guaranteed to be complete here
    return {
        "users": users_task.result(),
        "products": products_task.result(),
        "orders": orders_task.result(),
    }
```

### Exception Handling with except*

```python
import asyncio

class FetchError(Exception):
    pass

class ValidationError(Exception):
    pass

async def risky_operation(name: str) -> str:
    await asyncio.sleep(0.1)
    if name == "fail_fetch":
        raise FetchError(f"Failed to fetch {name}")
    if name == "fail_validate":
        raise ValidationError(f"Validation failed for {name}")
    return f"Success: {name}"

async def process_all(names: list[str]) -> list[str]:
    """Process all names, handling different exception types."""
    results: list[str] = []

    try:
        async with asyncio.TaskGroup() as tg:
            tasks = [tg.create_task(risky_operation(name)) for name in names]
    except* FetchError as eg:
        # Handle all FetchError exceptions
        for exc in eg.exceptions:
            print(f"Fetch error: {exc}")
    except* ValidationError as eg:
        # Handle all ValidationError exceptions
        for exc in eg.exceptions:
            print(f"Validation error: {exc}")
    else:
        # No exceptions - collect results
        results = [task.result() for task in tasks]

    return results
```

### Rate-Limited Concurrent Requests

```python
import asyncio
import aiohttp
from dataclasses import dataclass

@dataclass
class RateLimiter:
    """Simple rate limiter using semaphore."""
    max_concurrent: int
    _semaphore: asyncio.Semaphore | None = None

    @property
    def semaphore(self) -> asyncio.Semaphore:
        if self._semaphore is None:
            self._semaphore = asyncio.Semaphore(self.max_concurrent)
        return self._semaphore

    async def acquire(self) -> None:
        await self.semaphore.acquire()

    def release(self) -> None:
        self.semaphore.release()

async def fetch_with_limit[T](
    limiter: RateLimiter,
    session: aiohttp.ClientSession,
    url: str,
    transform: Callable[[dict], T],
) -> T:
    """Fetch URL with rate limiting."""
    await limiter.acquire()
    try:
        async with session.get(url) as response:
            data = await response.json()
            return transform(data)
    finally:
        limiter.release()

async def fetch_many_urls(
    urls: list[str],
    max_concurrent: int = 10,
) -> list[dict]:
    """Fetch many URLs with concurrency limit."""
    limiter = RateLimiter(max_concurrent=max_concurrent)

    async with aiohttp.ClientSession() as session:
        async with asyncio.TaskGroup() as tg:
            tasks = [
                tg.create_task(
                    fetch_with_limit(limiter, session, url, lambda x: x)
                )
                for url in urls
            ]

    return [task.result() for task in tasks]
```

### Timeout Context Manager

```python
import asyncio

async def fetch_with_timeout(url: str, timeout_seconds: float = 5.0) -> dict:
    """Fetch URL with timeout."""
    try:
        async with asyncio.timeout(timeout_seconds):
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    return await response.json()
    except asyncio.TimeoutError:
        raise TimeoutError(f"Request to {url} timed out after {timeout_seconds}s")

async def fetch_with_retry(
    url: str,
    max_retries: int = 3,
    timeout_seconds: float = 5.0,
) -> dict:
    """Fetch URL with retry logic and timeout."""
    last_error: Exception | None = None

    for attempt in range(max_retries):
        try:
            return await fetch_with_timeout(url, timeout_seconds)
        except (TimeoutError, aiohttp.ClientError) as e:
            last_error = e
            wait_time = 2 ** attempt  # Exponential backoff
            await asyncio.sleep(wait_time)

    raise last_error or RuntimeError("Max retries exceeded")
```

---

## 4. TypeIs and ReadOnly (Python 3.13+)

### TypeIs for Type Narrowing

```python
from typing import TypeIs, TypedDict

class User(TypedDict):
    id: int
    name: str
    email: str

class Admin(User):
    permissions: list[str]

def is_admin(user: User) -> TypeIs[Admin]:
    """Check if user is an admin."""
    return "permissions" in user

def process_user(user: User) -> None:
    """Process user based on type."""
    if is_admin(user):
        # Type checker knows user is Admin here
        print(f"Admin {user['name']} has permissions: {user['permissions']}")
    else:
        print(f"Regular user: {user['name']}")

# More examples
def is_string_list(val: list[object]) -> TypeIs[list[str]]:
    """Check if all items in list are strings."""
    return all(isinstance(item, str) for item in val)

def process_items(items: list[object]) -> None:
    if is_string_list(items):
        # Type checker knows items is list[str]
        joined = ", ".join(items)
        print(f"Strings: {joined}")
    else:
        print(f"Mixed types: {items}")
```

### ReadOnly for Immutable Fields

```python
from typing import ReadOnly, TypedDict, Required

class Config(TypedDict):
    """Application configuration with immutable fields."""
    app_name: ReadOnly[str]
    version: ReadOnly[str]
    debug: bool
    log_level: str

def update_config(config: Config, debug: bool, log_level: str) -> Config:
    """Update mutable config fields."""
    # These are allowed
    config["debug"] = debug
    config["log_level"] = log_level

    # These would cause type errors:
    # config["app_name"] = "new name"  # Error: ReadOnly
    # config["version"] = "2.0"  # Error: ReadOnly

    return config

class ImmutablePoint(TypedDict):
    """Completely immutable point."""
    x: ReadOnly[float]
    y: ReadOnly[float]

# Usage
config: Config = {
    "app_name": "MyApp",
    "version": "1.0.0",
    "debug": False,
    "log_level": "INFO",
}
```

---

## 5. Free-Threaded Python (Python 3.13+)

### CPU-Bound Parallelism

```python
# Run with: python3.13t -X gil=0
import sys
import threading
from concurrent.futures import ThreadPoolExecutor
import time

def check_free_threading() -> bool:
    """Check if running in free-threaded mode."""
    return not sys._is_gil_enabled()

def cpu_intensive_task(data: list[int]) -> int:
    """CPU-bound computation that benefits from parallelism."""
    return sum(x * x for x in data)

def parallel_compute(
    data_chunks: list[list[int]],
    max_workers: int = 4,
) -> list[int]:
    """Process data chunks in parallel."""
    if check_free_threading():
        print("Running in free-threaded mode - true parallelism!")
    else:
        print("Running with GIL - sequential threading")

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        results = list(executor.map(cpu_intensive_task, data_chunks))

    return results

def benchmark_threading() -> None:
    """Benchmark free-threading performance."""
    # Prepare data
    chunk_size = 1_000_000
    num_chunks = 4
    data = [list(range(i * chunk_size, (i + 1) * chunk_size)) for i in range(num_chunks)]

    # Single-threaded
    start = time.perf_counter()
    single_result = [cpu_intensive_task(chunk) for chunk in data]
    single_time = time.perf_counter() - start

    # Multi-threaded
    start = time.perf_counter()
    multi_result = parallel_compute(data, max_workers=4)
    multi_time = time.perf_counter() - start

    print(f"Single-threaded: {single_time:.3f}s")
    print(f"Multi-threaded:  {multi_time:.3f}s")
    print(f"Speedup: {single_time / multi_time:.2f}x")

if __name__ == "__main__":
    benchmark_threading()
```

### Thread-Safe Data Structures

```python
import threading
from collections.abc import Iterator
from dataclasses import dataclass, field

@dataclass
class ThreadSafeCounter:
    """Thread-safe counter using Lock."""
    _value: int = 0
    _lock: threading.Lock = field(default_factory=threading.Lock)

    def increment(self, amount: int = 1) -> int:
        with self._lock:
            self._value += amount
            return self._value

    def decrement(self, amount: int = 1) -> int:
        with self._lock:
            self._value -= amount
            return self._value

    @property
    def value(self) -> int:
        with self._lock:
            return self._value

@dataclass
class ThreadSafeQueue[T]:
    """Thread-safe queue implementation."""
    _items: list[T] = field(default_factory=list)
    _lock: threading.Lock = field(default_factory=threading.Lock)
    _not_empty: threading.Condition = field(init=False)

    def __post_init__(self) -> None:
        self._not_empty = threading.Condition(self._lock)

    def put(self, item: T) -> None:
        with self._not_empty:
            self._items.append(item)
            self._not_empty.notify()

    def get(self, timeout: float | None = None) -> T:
        with self._not_empty:
            while not self._items:
                if not self._not_empty.wait(timeout):
                    raise TimeoutError("Queue get timed out")
            return self._items.pop(0)

    def __len__(self) -> int:
        with self._lock:
            return len(self._items)
```

---

## 6. Template Strings (Python 3.14)

### Basic Template Strings

```python
# t-strings return Template objects, not strings
name = "Alice"
greeting = t"Hello, {name}!"  # Template object

# Access template parts
print(greeting.strings)  # ("Hello, ", "!")
print(greeting.interpolations)  # (Interpolation(value="Alice", ...),)

# Convert to string
print(str(greeting))  # "Hello, Alice!"
```

### SQL-Safe Templates

```python
from string import Template
import sqlite3

def sql_escape(value: str) -> str:
    """Escape SQL special characters."""
    return value.replace("'", "''")

class SQLTemplate:
    """SQL-safe template processor."""

    def __init__(self, template: Template) -> None:
        self.template = template

    def render(self) -> str:
        """Render template with SQL-escaped values."""
        parts = []
        for i, s in enumerate(self.template.strings):
            parts.append(s)
            if i < len(self.template.interpolations):
                interp = self.template.interpolations[i]
                escaped = sql_escape(str(interp.value))
                parts.append(f"'{escaped}'")
        return "".join(parts)

# Usage
user_input = "O'Brien"  # Potentially dangerous input
query = t"SELECT * FROM users WHERE name = {user_input}"
safe_query = SQLTemplate(query).render()
# Result: "SELECT * FROM users WHERE name = 'O''Brien'"
```

### HTML-Safe Templates

```python
import html

class HTMLTemplate:
    """HTML-safe template processor."""

    def __init__(self, template: Template) -> None:
        self.template = template

    def render(self) -> str:
        """Render template with HTML-escaped values."""
        parts = []
        for i, s in enumerate(self.template.strings):
            parts.append(s)
            if i < len(self.template.interpolations):
                interp = self.template.interpolations[i]
                escaped = html.escape(str(interp.value))
                parts.append(escaped)
        return "".join(parts)

# Usage
user_content = "<script>alert('XSS')</script>"
html_output = t"<p>User says: {user_content}</p>"
safe_html = HTMLTemplate(html_output).render()
# Result: "<p>User says: &lt;script&gt;alert('XSS')&lt;/script&gt;</p>"
```

---

## 7. Modern pytest Patterns

### Async Test Fixtures

```python
import pytest
import pytest_asyncio
import asyncio
from dataclasses import dataclass

@dataclass
class DatabaseConnection:
    """Mock database connection."""
    connected: bool = False

    async def connect(self) -> None:
        await asyncio.sleep(0.01)  # Simulate connection
        self.connected = True

    async def disconnect(self) -> None:
        await asyncio.sleep(0.01)
        self.connected = False

    async def execute(self, query: str) -> list[dict]:
        if not self.connected:
            raise RuntimeError("Not connected")
        return [{"id": 1, "name": "Test"}]

@pytest_asyncio.fixture
async def db_connection() -> AsyncIterator[DatabaseConnection]:
    """Async fixture with cleanup."""
    conn = DatabaseConnection()
    await conn.connect()
    yield conn
    await conn.disconnect()

@pytest.mark.asyncio
async def test_database_query(db_connection: DatabaseConnection) -> None:
    """Test database operations."""
    assert db_connection.connected
    results = await db_connection.execute("SELECT * FROM users")
    assert len(results) == 1
    assert results[0]["name"] == "Test"
```

### Parametrized Async Tests

```python
import pytest

@pytest.mark.asyncio
@pytest.mark.parametrize(
    "input_value,expected",
    [
        (1, 1),
        (2, 4),
        (3, 9),
        (4, 16),
    ],
)
async def test_async_square(input_value: int, expected: int) -> None:
    """Parametrized async test."""
    async def async_square(n: int) -> int:
        await asyncio.sleep(0.001)
        return n * n

    result = await async_square(input_value)
    assert result == expected
```

### Mock Async Functions

```python
from unittest.mock import AsyncMock, patch
import pytest

class ExternalService:
    async def fetch_data(self, id: int) -> dict:
        # Real implementation would make HTTP request
        pass

@pytest.mark.asyncio
async def test_with_mock() -> None:
    """Test with mocked async function."""
    service = ExternalService()
    service.fetch_data = AsyncMock(return_value={"id": 1, "data": "test"})

    result = await service.fetch_data(1)

    assert result["id"] == 1
    service.fetch_data.assert_called_once_with(1)

@pytest.mark.asyncio
async def test_with_patch() -> None:
    """Test with patched async function."""
    with patch.object(
        ExternalService,
        "fetch_data",
        new_callable=AsyncMock,
        return_value={"id": 2, "data": "patched"},
    ):
        service = ExternalService()
        result = await service.fetch_data(2)

        assert result["data"] == "patched"
```

---

## 8. Protocol-Based Design

```python
from typing import Protocol, runtime_checkable
from dataclasses import dataclass

@runtime_checkable
class Serializable(Protocol):
    """Protocol for objects that can be serialized."""

    def to_dict(self) -> dict: ...
    def to_json(self) -> str: ...

@runtime_checkable
class Repository[T](Protocol):
    """Protocol for repository pattern."""

    async def get(self, id: int) -> T | None: ...
    async def save(self, item: T) -> T: ...
    async def delete(self, id: int) -> bool: ...
    async def list(self, limit: int = 100) -> list[T]: ...

@dataclass
class User:
    id: int
    name: str
    email: str

    def to_dict(self) -> dict:
        return {"id": self.id, "name": self.name, "email": self.email}

    def to_json(self) -> str:
        import json
        return json.dumps(self.to_dict())

class InMemoryUserRepository:
    """In-memory implementation of Repository protocol."""

    def __init__(self) -> None:
        self._users: dict[int, User] = {}
        self._next_id = 1

    async def get(self, id: int) -> User | None:
        return self._users.get(id)

    async def save(self, user: User) -> User:
        if user.id == 0:
            user.id = self._next_id
            self._next_id += 1
        self._users[user.id] = user
        return user

    async def delete(self, id: int) -> bool:
        if id in self._users:
            del self._users[id]
            return True
        return False

    async def list(self, limit: int = 100) -> list[User]:
        return list(self._users.values())[:limit]

# Type checking works
def process_serializable(item: Serializable) -> str:
    return item.to_json()

user = User(id=1, name="Alice", email="alice@example.com")
assert isinstance(user, Serializable)  # Runtime check works
json_str = process_serializable(user)  # Type-safe
```

---

*Examples v2.0 - Modern Python 2026*
