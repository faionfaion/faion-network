# Python Basics Templates

Copy-paste code templates for common Python patterns.

---

## Project Setup

### pyproject.toml (Modern Project)

```toml
[project]
name = "my-project"
version = "0.1.0"
description = "Project description"
readme = "README.md"
requires-python = ">=3.12"
license = {text = "MIT"}
authors = [
    {name = "Your Name", email = "you@example.com"}
]
dependencies = []

[project.optional-dependencies]
dev = [
    "pytest>=8.0",
    "pytest-cov>=5.0",
    "ruff>=0.8",
    "mypy>=1.13",
]

[project.scripts]
my-cli = "my_project.cli:main"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["src/my_project"]

[tool.ruff]
line-length = 88
target-version = "py312"

[tool.ruff.lint]
select = [
    "E",    # pycodestyle errors
    "F",    # pyflakes
    "I",    # isort
    "B",    # flake8-bugbear
    "UP",   # pyupgrade
    "N",    # pep8-naming
    "S",    # flake8-bandit (security)
    "C4",   # flake8-comprehensions
    "PT",   # flake8-pytest-style
]
ignore = ["S101"]  # Allow assert in tests

[tool.ruff.lint.per-file-ignores]
"tests/**/*.py" = ["S101"]

[tool.ruff.format]
quote-style = "double"

[tool.mypy]
python_version = "3.12"
strict = true
warn_return_any = true
warn_unused_ignores = true

[[tool.mypy.overrides]]
module = "tests.*"
disallow_untyped_defs = false

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "-v --cov=src --cov-report=term-missing"
```

### Project Structure

```
my-project/
├── pyproject.toml
├── uv.lock
├── README.md
├── .gitignore
├── .python-version
├── src/
│   └── my_project/
│       ├── __init__.py
│       ├── main.py
│       ├── config.py
│       ├── models/
│       │   ├── __init__.py
│       │   └── user.py
│       ├── services/
│       │   ├── __init__.py
│       │   └── user_service.py
│       └── utils/
│           ├── __init__.py
│           └── helpers.py
└── tests/
    ├── __init__.py
    ├── conftest.py
    ├── test_main.py
    └── test_services/
        └── test_user_service.py
```

### .gitignore

```gitignore
# Virtual environments
.venv/
venv/
ENV/

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python

# Distribution
build/
dist/
*.egg-info/
*.egg

# IDE
.idea/
.vscode/
*.swp
*.swo

# Testing
.pytest_cache/
.coverage
htmlcov/

# Type checking
.mypy_cache/

# Environment
.env
.env.local
*.local

# Logs
*.log
logs/

# OS
.DS_Store
Thumbs.db
```

---

## Functions

### Function with Full Type Hints

```python
from typing import Any

def process_data(
    items: list[dict[str, Any]],
    *,
    filter_key: str | None = None,
    transform: bool = False,
) -> list[dict[str, Any]]:
    """
    Process a list of data items.

    Args:
        items: List of dictionaries to process.
        filter_key: Optional key to filter items (keep only items with this key).
        transform: Whether to apply transformation.

    Returns:
        Processed list of dictionaries.

    Raises:
        ValueError: If items is empty.

    Examples:
        >>> process_data([{"a": 1}, {"b": 2}])
        [{'a': 1}, {'b': 2}]
        >>> process_data([{"a": 1}, {"b": 2}], filter_key="a")
        [{'a': 1}]
    """
    if not items:
        raise ValueError("Items cannot be empty")

    result = items

    if filter_key:
        result = [item for item in result if filter_key in item]

    if transform:
        result = [_transform_item(item) for item in result]

    return result


def _transform_item(item: dict[str, Any]) -> dict[str, Any]:
    """Transform a single item (private helper)."""
    return {k: str(v).upper() for k, v in item.items()}
```

### Generic Function (Python 3.12+)

```python
def first[T](items: list[T], default: T | None = None) -> T | None:
    """
    Return first item from list or default if empty.

    Args:
        items: List to get first item from.
        default: Value to return if list is empty.

    Returns:
        First item or default value.
    """
    return items[0] if items else default


def group_by[T, K](items: list[T], key_fn: Callable[[T], K]) -> dict[K, list[T]]:
    """
    Group items by a key function.

    Args:
        items: Items to group.
        key_fn: Function to extract grouping key.

    Returns:
        Dictionary mapping keys to lists of items.
    """
    result: dict[K, list[T]] = {}
    for item in items:
        key = key_fn(item)
        if key not in result:
            result[key] = []
        result[key].append(item)
    return result
```

---

## Decorators

### Timer Decorator

```python
import functools
import time
from typing import Callable, ParamSpec, TypeVar

P = ParamSpec("P")
R = TypeVar("R")


def timer(func: Callable[P, R]) -> Callable[P, R]:
    """Measure and log function execution time."""
    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"{func.__name__} executed in {elapsed:.4f}s")
        return result
    return wrapper


# Usage
@timer
def slow_function() -> None:
    time.sleep(1)
```

### Retry Decorator

```python
import functools
import time
from typing import Callable, ParamSpec, TypeVar

P = ParamSpec("P")
R = TypeVar("R")


def retry(
    max_attempts: int = 3,
    delay: float = 1.0,
    exceptions: tuple[type[Exception], ...] = (Exception,),
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """
    Retry decorator with configurable attempts and delay.

    Args:
        max_attempts: Maximum retry attempts.
        delay: Delay between retries in seconds.
        exceptions: Exception types to catch and retry.
    """
    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            last_exception: Exception | None = None
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt < max_attempts - 1:
                        time.sleep(delay)
            if last_exception:
                raise last_exception
            raise RuntimeError("Unexpected state in retry")
        return wrapper
    return decorator


# Usage
@retry(max_attempts=3, delay=0.5, exceptions=(ConnectionError, TimeoutError))
def fetch_data(url: str) -> dict:
    ...
```

### Cache Decorator (Simple)

```python
import functools
from typing import Callable, ParamSpec, TypeVar

P = ParamSpec("P")
R = TypeVar("R")


def cache(func: Callable[P, R]) -> Callable[P, R]:
    """Simple unbounded cache decorator."""
    _cache: dict = {}

    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        key = (args, tuple(sorted(kwargs.items())))
        if key not in _cache:
            _cache[key] = func(*args, **kwargs)
        return _cache[key]

    wrapper.cache_clear = lambda: _cache.clear()  # type: ignore
    return wrapper


# Or use built-in (recommended)
from functools import lru_cache, cache

@lru_cache(maxsize=128)
def expensive_computation(n: int) -> int:
    ...

@cache  # Unbounded cache (Python 3.9+)
def another_computation(n: int) -> int:
    ...
```

### Validate Decorator

```python
import functools
from typing import Callable, ParamSpec, TypeVar

P = ParamSpec("P")
R = TypeVar("R")


def validate_positive(*param_names: str) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """Validate that specified parameters are positive."""
    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            # Get parameter names from function signature
            import inspect
            sig = inspect.signature(func)
            params = list(sig.parameters.keys())

            # Check positional args
            for i, arg in enumerate(args):
                if i < len(params) and params[i] in param_names:
                    if arg <= 0:
                        raise ValueError(f"{params[i]} must be positive, got {arg}")

            # Check keyword args
            for name in param_names:
                if name in kwargs and kwargs[name] <= 0:
                    raise ValueError(f"{name} must be positive, got {kwargs[name]}")

            return func(*args, **kwargs)
        return wrapper
    return decorator


# Usage
@validate_positive("amount", "quantity")
def process_order(amount: float, quantity: int) -> float:
    return amount * quantity
```

---

## Classes

### Dataclass Template

```python
from dataclasses import dataclass, field
from datetime import datetime
from typing import ClassVar


@dataclass(slots=True)
class User:
    """User entity with auto-generated methods."""

    id: int
    email: str
    name: str
    is_active: bool = True
    created_at: datetime = field(default_factory=datetime.now)
    tags: list[str] = field(default_factory=list)

    # Class variable (not an instance attribute)
    _registry: ClassVar[dict[int, "User"]] = {}

    def __post_init__(self) -> None:
        """Validate and register after initialization."""
        if not self.email or "@" not in self.email:
            raise ValueError(f"Invalid email: {self.email}")
        User._registry[self.id] = self

    @classmethod
    def get(cls, user_id: int) -> "User | None":
        """Get user by ID from registry."""
        return cls._registry.get(user_id)

    @classmethod
    def all(cls) -> list["User"]:
        """Get all registered users."""
        return list(cls._registry.values())

    def activate(self) -> None:
        """Activate user."""
        self.is_active = True

    def deactivate(self) -> None:
        """Deactivate user."""
        self.is_active = False
```

### Protocol Template

```python
from typing import Protocol, runtime_checkable


@runtime_checkable
class Repository[T](Protocol):
    """Generic repository protocol."""

    def get(self, id: int) -> T | None:
        """Get entity by ID."""
        ...

    def list(self) -> list[T]:
        """List all entities."""
        ...

    def create(self, entity: T) -> T:
        """Create new entity."""
        ...

    def update(self, entity: T) -> T:
        """Update existing entity."""
        ...

    def delete(self, id: int) -> bool:
        """Delete entity by ID."""
        ...


# Implementation
class UserRepository:
    """In-memory user repository."""

    def __init__(self) -> None:
        self._users: dict[int, User] = {}
        self._counter = 0

    def get(self, id: int) -> User | None:
        return self._users.get(id)

    def list(self) -> list[User]:
        return list(self._users.values())

    def create(self, entity: User) -> User:
        self._counter += 1
        entity.id = self._counter
        self._users[entity.id] = entity
        return entity

    def update(self, entity: User) -> User:
        self._users[entity.id] = entity
        return entity

    def delete(self, id: int) -> bool:
        if id in self._users:
            del self._users[id]
            return True
        return False


# Usage with Protocol type hint
def process_users(repo: Repository[User]) -> None:
    for user in repo.list():
        print(user)
```

### Context Manager Class

```python
from typing import Any


class DatabaseConnection:
    """Database connection as context manager."""

    def __init__(self, connection_string: str) -> None:
        self.connection_string = connection_string
        self._connection: Any = None

    def __enter__(self) -> "DatabaseConnection":
        """Open connection on enter."""
        self._connection = self._create_connection()
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: Any,
    ) -> bool:
        """Close connection on exit."""
        if self._connection:
            self._connection.close()
        return False  # Don't suppress exceptions

    def _create_connection(self) -> Any:
        """Create actual connection."""
        # Implementation here
        return None

    def execute(self, query: str) -> list[dict]:
        """Execute query."""
        if not self._connection:
            raise RuntimeError("Not connected")
        # Implementation here
        return []


# Usage
with DatabaseConnection("postgresql://localhost/db") as db:
    results = db.execute("SELECT * FROM users")
```

### Context Manager with contextlib

```python
from contextlib import contextmanager
from typing import Generator


@contextmanager
def timer(name: str = "Block") -> Generator[dict[str, float], None, None]:
    """Context manager for timing code blocks."""
    import time

    stats: dict[str, float] = {"start": 0, "elapsed": 0}
    stats["start"] = time.perf_counter()

    try:
        yield stats
    finally:
        stats["elapsed"] = time.perf_counter() - stats["start"]
        print(f"{name} took {stats['elapsed']:.4f}s")


# Usage
with timer("Processing"):
    # Your code here
    result = sum(range(1_000_000))


@contextmanager
def temporary_directory() -> Generator[Path, None, None]:
    """Create and cleanup temporary directory."""
    import shutil
    import tempfile
    from pathlib import Path

    temp_dir = Path(tempfile.mkdtemp())
    try:
        yield temp_dir
    finally:
        shutil.rmtree(temp_dir)


# Usage
with temporary_directory() as temp_dir:
    file_path = temp_dir / "test.txt"
    file_path.write_text("Hello")
```

---

## Error Handling

### Exception Hierarchy

```python
class AppError(Exception):
    """Base exception for application."""

    def __init__(self, message: str, code: str | None = None) -> None:
        self.message = message
        self.code = code
        super().__init__(message)


class ValidationError(AppError):
    """Raised when validation fails."""

    def __init__(self, field: str, message: str) -> None:
        self.field = field
        super().__init__(f"Validation error on '{field}': {message}", "VALIDATION_ERROR")


class NotFoundError(AppError):
    """Raised when resource not found."""

    def __init__(self, resource: str, identifier: Any) -> None:
        self.resource = resource
        self.identifier = identifier
        super().__init__(f"{resource} not found: {identifier}", "NOT_FOUND")


class AuthenticationError(AppError):
    """Raised when authentication fails."""

    def __init__(self, message: str = "Authentication failed") -> None:
        super().__init__(message, "AUTH_ERROR")


class AuthorizationError(AppError):
    """Raised when authorization fails."""

    def __init__(self, action: str, resource: str) -> None:
        super().__init__(
            f"Not authorized to {action} on {resource}",
            "AUTHORIZATION_ERROR"
        )
```

### Error Handler Template

```python
import logging
from typing import Any

logger = logging.getLogger(__name__)


def handle_operation(
    operation: Callable[[], T],
    *,
    on_error: T | None = None,
    log_error: bool = True,
    reraise: bool = False,
) -> T | None:
    """
    Execute operation with standardized error handling.

    Args:
        operation: Callable to execute.
        on_error: Value to return on error.
        log_error: Whether to log errors.
        reraise: Whether to re-raise after handling.

    Returns:
        Operation result or on_error value.
    """
    try:
        return operation()
    except Exception as e:
        if log_error:
            logger.exception(f"Operation failed: {e}")
        if reraise:
            raise
        return on_error


# Usage
result = handle_operation(
    lambda: risky_operation(),
    on_error=default_value,
    log_error=True,
)
```

---

## File I/O

### Read/Write JSON

```python
import json
from pathlib import Path
from typing import Any


def read_json(path: Path) -> dict[str, Any]:
    """Read JSON file."""
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict[str, Any], indent: int = 2) -> None:
    """Write JSON file."""
    path.write_text(
        json.dumps(data, indent=indent, ensure_ascii=False),
        encoding="utf-8"
    )


def update_json(path: Path, updates: dict[str, Any]) -> dict[str, Any]:
    """Update JSON file with new values."""
    data = read_json(path) if path.exists() else {}
    data.update(updates)
    write_json(path, data)
    return data
```

### Process Large Files

```python
from pathlib import Path
from typing import Generator, Iterator


def read_lines(path: Path) -> Generator[str, None, None]:
    """Read file line by line (memory efficient)."""
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            yield line.rstrip("\n")


def read_chunks(path: Path, chunk_size: int = 8192) -> Generator[str, None, None]:
    """Read file in chunks."""
    with open(path, "r", encoding="utf-8") as f:
        while chunk := f.read(chunk_size):
            yield chunk


def process_csv(path: Path) -> Generator[dict[str, str], None, None]:
    """Process CSV file row by row."""
    import csv

    with open(path, "r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            yield row


def write_lines(path: Path, lines: Iterator[str]) -> int:
    """Write lines to file, return count."""
    count = 0
    with open(path, "w", encoding="utf-8") as f:
        for line in lines:
            f.write(line + "\n")
            count += 1
    return count
```

---

## Testing

### pytest Conftest

```python
# tests/conftest.py
import pytest
from pathlib import Path


@pytest.fixture
def sample_data() -> dict[str, Any]:
    """Provide sample test data."""
    return {
        "users": [
            {"id": 1, "name": "Alice"},
            {"id": 2, "name": "Bob"},
        ]
    }


@pytest.fixture
def temp_dir(tmp_path: Path) -> Path:
    """Provide temporary directory for tests."""
    return tmp_path


@pytest.fixture
def mock_config(monkeypatch: pytest.MonkeyPatch) -> None:
    """Set up mock configuration."""
    monkeypatch.setenv("DEBUG", "true")
    monkeypatch.setenv("API_KEY", "test-key")


@pytest.fixture(scope="session")
def database():
    """Session-scoped database fixture."""
    db = create_test_database()
    yield db
    db.cleanup()
```

### Test File Template

```python
# tests/test_example.py
import pytest
from my_project.services import UserService


class TestUserService:
    """Tests for UserService."""

    def test_create_user(self) -> None:
        """Test user creation."""
        service = UserService()
        user = service.create(name="Alice", email="alice@example.com")

        assert user.id is not None
        assert user.name == "Alice"
        assert user.email == "alice@example.com"

    def test_create_user_invalid_email(self) -> None:
        """Test user creation with invalid email."""
        service = UserService()

        with pytest.raises(ValidationError) as exc_info:
            service.create(name="Alice", email="invalid")

        assert exc_info.value.field == "email"

    @pytest.mark.parametrize(
        "name,email,expected",
        [
            ("Alice", "alice@example.com", True),
            ("Bob", "bob@test.org", True),
            ("", "test@example.com", False),
        ],
    )
    def test_validate_user(
        self,
        name: str,
        email: str,
        expected: bool,
    ) -> None:
        """Test user validation with various inputs."""
        service = UserService()
        result = service.validate(name=name, email=email)
        assert result == expected
```

---

## Logging

### Logging Setup

```python
import logging
import sys
from pathlib import Path


def setup_logging(
    level: int = logging.INFO,
    log_file: Path | None = None,
    format_string: str | None = None,
) -> None:
    """
    Configure application logging.

    Args:
        level: Logging level.
        log_file: Optional file to write logs to.
        format_string: Custom format string.
    """
    if format_string is None:
        format_string = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    handlers: list[logging.Handler] = [
        logging.StreamHandler(sys.stdout),
    ]

    if log_file:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        handlers.append(logging.FileHandler(log_file))

    logging.basicConfig(
        level=level,
        format=format_string,
        handlers=handlers,
    )


# Usage
setup_logging(
    level=logging.DEBUG,
    log_file=Path("logs/app.log"),
)

logger = logging.getLogger(__name__)
logger.info("Application started")
```

---

## CLI

### Basic CLI with argparse

```python
import argparse
import sys
from pathlib import Path


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="My CLI Application",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "input",
        type=Path,
        help="Input file path",
    )

    parser.add_argument(
        "-o", "--output",
        type=Path,
        default=Path("output.txt"),
        help="Output file path (default: output.txt)",
    )

    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose output",
    )

    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 1.0.0",
    )

    args = parser.parse_args()

    if args.verbose:
        print(f"Processing {args.input}...")

    try:
        process_file(args.input, args.output)
        return 0
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
```

---

*Python Basics Templates v2.0*
*Last updated: 2026-01-25*
