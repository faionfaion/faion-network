# Python Basics Examples

Real-world Python code examples covering fundamentals.

---

## 1. Data Structures

### List Operations and Comprehensions

```python
# Basic list operations
numbers = [1, 2, 3, 4, 5]
numbers.append(6)           # [1, 2, 3, 4, 5, 6]
numbers.extend([7, 8])      # [1, 2, 3, 4, 5, 6, 7, 8]
numbers.insert(0, 0)        # [0, 1, 2, 3, 4, 5, 6, 7, 8]
popped = numbers.pop()      # 8, list is now [0, 1, 2, 3, 4, 5, 6, 7]

# Slicing
items = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
first_three = items[:3]     # [0, 1, 2]
last_three = items[-3:]     # [7, 8, 9]
every_other = items[::2]    # [0, 2, 4, 6, 8]
reversed_list = items[::-1] # [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]

# List comprehensions
squares = [x**2 for x in range(10)]
# [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]

evens = [x for x in range(20) if x % 2 == 0]
# [0, 2, 4, 6, 8, 10, 12, 14, 16, 18]

# Nested comprehension - flatten 2D list
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
flat = [num for row in matrix for num in row]
# [1, 2, 3, 4, 5, 6, 7, 8, 9]

# Comprehension with transformation
names = ["alice", "bob", "charlie"]
capitalized = [name.capitalize() for name in names]
# ["Alice", "Bob", "Charlie"]
```

### Dictionary Operations

```python
# Basic dict operations
user = {"name": "Alice", "age": 30, "city": "NYC"}
name = user["name"]                    # "Alice"
country = user.get("country", "USA")   # "USA" (default)

# Dict comprehension
squares_dict = {x: x**2 for x in range(5)}
# {0: 0, 1: 1, 2: 4, 3: 9, 4: 16}

# Invert a dict
original = {"a": 1, "b": 2, "c": 3}
inverted = {v: k for k, v in original.items()}
# {1: "a", 2: "b", 3: "c"}

# Merge dicts (Python 3.9+)
defaults = {"theme": "light", "lang": "en"}
overrides = {"theme": "dark"}
config = defaults | overrides
# {"theme": "dark", "lang": "en"}

# defaultdict for automatic defaults
from collections import defaultdict

word_counts = defaultdict(int)
for word in ["apple", "banana", "apple", "cherry", "apple"]:
    word_counts[word] += 1
# defaultdict(int, {"apple": 3, "banana": 1, "cherry": 1})

# Group items by key
from collections import defaultdict

students = [
    {"name": "Alice", "grade": "A"},
    {"name": "Bob", "grade": "B"},
    {"name": "Charlie", "grade": "A"},
]

by_grade = defaultdict(list)
for student in students:
    by_grade[student["grade"]].append(student["name"])
# {"A": ["Alice", "Charlie"], "B": ["Bob"]}

# Counter for counting
from collections import Counter

text = "mississippi"
letter_counts = Counter(text)
# Counter({"i": 4, "s": 4, "p": 2, "m": 1})

most_common = letter_counts.most_common(2)
# [("i", 4), ("s", 4)]
```

### Set Operations

```python
# Basic set operations
a = {1, 2, 3, 4, 5}
b = {4, 5, 6, 7, 8}

union = a | b           # {1, 2, 3, 4, 5, 6, 7, 8}
intersection = a & b    # {4, 5}
difference = a - b      # {1, 2, 3}
symmetric = a ^ b       # {1, 2, 3, 6, 7, 8}

# Membership test (O(1) vs O(n) for list)
valid_ids = {1001, 1002, 1003, 1004, 1005}
is_valid = 1003 in valid_ids  # True, very fast

# Remove duplicates while preserving order
items = [1, 3, 2, 1, 4, 2, 5, 3]
unique = list(dict.fromkeys(items))
# [1, 3, 2, 4, 5]

# Set comprehension
text = "hello world"
unique_chars = {char for char in text if char.isalpha()}
# {"h", "e", "l", "o", "w", "r", "d"}
```

---

## 2. Control Flow

### Pattern Matching (Python 3.10+)

```python
def handle_command(command: list[str]) -> str:
    match command:
        case ["quit"] | ["exit"]:
            return "Goodbye!"
        case ["hello", name]:
            return f"Hello, {name}!"
        case ["add", *numbers]:
            total = sum(int(n) for n in numbers)
            return f"Sum: {total}"
        case ["search", query] if len(query) >= 3:
            return f"Searching for: {query}"
        case ["search", query]:
            return "Query too short (min 3 chars)"
        case _:
            return "Unknown command"

# Usage
print(handle_command(["hello", "Alice"]))   # "Hello, Alice!"
print(handle_command(["add", "1", "2", "3"]))  # "Sum: 6"
print(handle_command(["quit"]))             # "Goodbye!"
```

### Pattern Matching with Classes

```python
from dataclasses import dataclass

@dataclass
class Point:
    x: int
    y: int

@dataclass
class Circle:
    center: Point
    radius: float

@dataclass
class Rectangle:
    top_left: Point
    width: float
    height: float

def describe_shape(shape) -> str:
    match shape:
        case Circle(center=Point(x=0, y=0), radius=r):
            return f"Circle at origin with radius {r}"
        case Circle(center=c, radius=r):
            return f"Circle at ({c.x}, {c.y}) with radius {r}"
        case Rectangle(width=w, height=h) if w == h:
            return f"Square with side {w}"
        case Rectangle(width=w, height=h):
            return f"Rectangle {w}x{h}"
        case _:
            return "Unknown shape"

# Usage
print(describe_shape(Circle(Point(0, 0), 5)))  # "Circle at origin with radius 5"
print(describe_shape(Rectangle(Point(0, 0), 10, 10)))  # "Square with side 10"
```

### Walrus Operator

```python
# Check and use length
if (n := len(data)) > 10:
    print(f"Processing {n} items")

# In while loops
while (line := file.readline()):
    process(line)

# In comprehensions
results = [
    processed
    for item in items
    if (processed := expensive_operation(item)) is not None
]

# Simplify regex matching
import re

if (match := re.search(r"(\d+)", text)):
    number = int(match.group(1))
```

---

## 3. Functions

### Type Hints and Defaults

```python
from typing import Any

def greet(
    name: str,
    greeting: str = "Hello",
    *,  # Keyword-only after this
    punctuation: str = "!",
    uppercase: bool = False,
) -> str:
    """
    Create a greeting message.

    Args:
        name: Person to greet
        greeting: Greeting word
        punctuation: End punctuation
        uppercase: Convert to uppercase

    Returns:
        Formatted greeting string

    Examples:
        >>> greet("Alice")
        'Hello, Alice!'
        >>> greet("Bob", "Hi", uppercase=True)
        'HI, BOB!'
    """
    message = f"{greeting}, {name}{punctuation}"
    return message.upper() if uppercase else message

# Usage
print(greet("Alice"))                           # "Hello, Alice!"
print(greet("Bob", "Hi", punctuation="?"))      # "Hi, Bob?"
print(greet("Charlie", uppercase=True))         # "HELLO, CHARLIE!"
```

### Generic Functions (Python 3.12+)

```python
def first[T](items: list[T]) -> T | None:
    """Return first item or None if empty."""
    return items[0] if items else None

def merge_dicts[K, V](d1: dict[K, V], d2: dict[K, V]) -> dict[K, V]:
    """Merge two dicts, second wins on conflicts."""
    return d1 | d2

# Usage
first([1, 2, 3])        # 1
first(["a", "b"])       # "a"
first([])               # None
```

### Decorators

```python
import functools
import time
from typing import Callable, ParamSpec, TypeVar

P = ParamSpec("P")
R = TypeVar("R")

def timer(func: Callable[P, R]) -> Callable[P, R]:
    """Measure function execution time."""
    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"{func.__name__} took {elapsed:.4f}s")
        return result
    return wrapper

def retry(max_attempts: int = 3, delay: float = 1.0):
    """Retry decorator with configurable attempts."""
    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            last_exception = None
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_attempts - 1:
                        time.sleep(delay)
            raise last_exception
        return wrapper
    return decorator

def cache_result(func: Callable[P, R]) -> Callable[P, R]:
    """Simple cache decorator (see also @functools.lru_cache)."""
    cache: dict = {}

    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        key = (args, tuple(sorted(kwargs.items())))
        if key not in cache:
            cache[key] = func(*args, **kwargs)
        return cache[key]
    return wrapper

# Usage
@timer
@retry(max_attempts=3, delay=0.5)
def fetch_data(url: str) -> dict:
    """Fetch data with timing and retry."""
    import urllib.request
    with urllib.request.urlopen(url) as response:
        return response.read()

# Built-in caching
from functools import lru_cache

@lru_cache(maxsize=128)
def fibonacci(n: int) -> int:
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)
```

### Closures and Factories

```python
def make_multiplier(factor: float):
    """Factory function that creates multiplier functions."""
    def multiplier(x: float) -> float:
        return x * factor
    return multiplier

double = make_multiplier(2)
triple = make_multiplier(3)

print(double(5))   # 10
print(triple(5))   # 15

# Counter factory
def make_counter(start: int = 0):
    """Create a counter with persistent state."""
    count = start

    def counter() -> int:
        nonlocal count
        count += 1
        return count

    return counter

counter = make_counter()
print(counter())  # 1
print(counter())  # 2
print(counter())  # 3
```

---

## 4. Classes and OOP

### Modern Dataclass

```python
from dataclasses import dataclass, field
from typing import ClassVar

@dataclass(slots=True)
class User:
    """User with automatic __init__, __repr__, __eq__."""
    id: int
    name: str
    email: str
    is_active: bool = True
    tags: list[str] = field(default_factory=list)

    # Class variable (not an instance field)
    _instances: ClassVar[dict[int, "User"]] = {}

    def __post_init__(self) -> None:
        """Run after __init__ for validation/registration."""
        User._instances[self.id] = self

    def activate(self) -> None:
        self.is_active = True

    def deactivate(self) -> None:
        self.is_active = False

    @classmethod
    def get_by_id(cls, user_id: int) -> "User | None":
        return cls._instances.get(user_id)

# Usage
user = User(1, "Alice", "alice@example.com")
print(user)  # User(id=1, name='Alice', email='alice@example.com', is_active=True, tags=[])
```

### Protocol (Structural Subtyping)

```python
from typing import Protocol, runtime_checkable

@runtime_checkable
class Sendable(Protocol):
    """Protocol for objects that can send messages."""
    def send(self, message: str) -> bool: ...

class EmailClient:
    def send(self, message: str) -> bool:
        print(f"Email: {message}")
        return True

class SlackClient:
    def send(self, message: str) -> bool:
        print(f"Slack: {message}")
        return True

class SMSClient:
    def send(self, message: str) -> bool:
        print(f"SMS: {message}")
        return True

def notify_all(clients: list[Sendable], message: str) -> list[bool]:
    """Send message via all clients."""
    return [client.send(message) for client in clients]

# Works with any object having send() method
clients: list[Sendable] = [EmailClient(), SlackClient(), SMSClient()]
notify_all(clients, "Hello, World!")

# Runtime check
assert isinstance(EmailClient(), Sendable)
```

### Context Manager Class

```python
from typing import Any

class Timer:
    """Context manager for timing code blocks."""

    def __init__(self, name: str = "Block") -> None:
        self.name = name
        self.start: float = 0
        self.elapsed: float = 0

    def __enter__(self) -> "Timer":
        import time
        self.start = time.perf_counter()
        return self

    def __exit__(
        self,
        exc_type: type | None,
        exc_val: Exception | None,
        exc_tb: Any,
    ) -> bool:
        import time
        self.elapsed = time.perf_counter() - self.start
        print(f"{self.name} took {self.elapsed:.4f}s")
        return False  # Don't suppress exceptions

# Usage
with Timer("Processing"):
    result = sum(range(1_000_000))
# Output: Processing took 0.0234s
```

### Property and Computed Attributes

```python
from dataclasses import dataclass

@dataclass
class Rectangle:
    width: float
    height: float

    @property
    def area(self) -> float:
        """Computed property for area."""
        return self.width * self.height

    @property
    def perimeter(self) -> float:
        """Computed property for perimeter."""
        return 2 * (self.width + self.height)

    @property
    def is_square(self) -> bool:
        """Check if rectangle is a square."""
        return self.width == self.height

class Temperature:
    """Temperature with Celsius/Fahrenheit conversion."""

    def __init__(self, celsius: float = 0) -> None:
        self._celsius = celsius

    @property
    def celsius(self) -> float:
        return self._celsius

    @celsius.setter
    def celsius(self, value: float) -> None:
        if value < -273.15:
            raise ValueError("Temperature below absolute zero")
        self._celsius = value

    @property
    def fahrenheit(self) -> float:
        return self._celsius * 9/5 + 32

    @fahrenheit.setter
    def fahrenheit(self, value: float) -> None:
        self.celsius = (value - 32) * 5/9

# Usage
temp = Temperature(25)
print(temp.fahrenheit)  # 77.0
temp.fahrenheit = 100
print(temp.celsius)     # 37.78
```

---

## 5. Error Handling

### Proper Exception Handling

```python
import logging
from typing import Any

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fetch_user_data(user_id: int) -> dict[str, Any]:
    """Fetch user data with proper error handling."""
    try:
        # Narrow try block - only wrap what can fail
        response = api_client.get(f"/users/{user_id}")
        response.raise_for_status()
    except ConnectionError as e:
        logger.error(f"Network error fetching user {user_id}: {e}")
        raise  # Re-raise after logging
    except HTTPError as e:
        if e.response.status_code == 404:
            logger.warning(f"User {user_id} not found")
            raise UserNotFoundError(user_id) from e  # Chain exceptions
        raise
    else:
        # Runs only if no exception
        logger.info(f"Successfully fetched user {user_id}")
        return response.json()
    finally:
        # Always runs - cleanup
        logger.debug(f"Completed fetch attempt for user {user_id}")
```

### Custom Exception Hierarchy

```python
class AppError(Exception):
    """Base exception for application errors."""
    pass

class ValidationError(AppError):
    """Raised when validation fails."""
    def __init__(self, field: str, message: str) -> None:
        self.field = field
        self.message = message
        super().__init__(f"{field}: {message}")

class NotFoundError(AppError):
    """Raised when resource not found."""
    def __init__(self, resource: str, id: Any) -> None:
        self.resource = resource
        self.id = id
        super().__init__(f"{resource} with id {id} not found")

class AuthenticationError(AppError):
    """Raised when authentication fails."""
    pass

# Usage
def get_user(user_id: int) -> User:
    user = db.users.get(user_id)
    if user is None:
        raise NotFoundError("User", user_id)
    return user

def create_user(data: dict) -> User:
    if not data.get("email"):
        raise ValidationError("email", "Email is required")
    if "@" not in data["email"]:
        raise ValidationError("email", "Invalid email format")
    return db.users.create(data)
```

### Context Manager for Error Handling

```python
from contextlib import contextmanager
from typing import Generator

@contextmanager
def handle_api_errors() -> Generator[None, None, None]:
    """Context manager for standardized API error handling."""
    try:
        yield
    except ConnectionError:
        raise APIError("Network connection failed")
    except TimeoutError:
        raise APIError("Request timed out")
    except ValueError as e:
        raise APIError(f"Invalid response: {e}")

# Usage
with handle_api_errors():
    response = api.fetch_data()
```

---

## 6. File I/O

### Modern File Operations with pathlib

```python
from pathlib import Path
import json

# Path operations
base = Path("/home/user/project")
config_path = base / "config" / "settings.json"
data_dir = base / "data"

# Create directories
data_dir.mkdir(parents=True, exist_ok=True)

# Check existence
if config_path.exists():
    # Read JSON
    config = json.loads(config_path.read_text(encoding="utf-8"))
else:
    # Write JSON
    config = {"debug": True, "version": "1.0"}
    config_path.write_text(
        json.dumps(config, indent=2),
        encoding="utf-8"
    )

# Find files
python_files = list(base.rglob("*.py"))
print(f"Found {len(python_files)} Python files")

# File info
for file in base.glob("*.txt"):
    print(f"{file.name}: {file.stat().st_size} bytes")
```

### Processing Large Files

```python
from pathlib import Path
from typing import Iterator

def read_large_file(path: Path, chunk_size: int = 8192) -> Iterator[str]:
    """Read large file in chunks."""
    with open(path, "r", encoding="utf-8") as f:
        while chunk := f.read(chunk_size):
            yield chunk

def process_lines(path: Path) -> Iterator[str]:
    """Process file line by line (memory efficient)."""
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            yield line.strip()

def count_lines(path: Path) -> int:
    """Count lines without loading entire file."""
    return sum(1 for _ in open(path, "r", encoding="utf-8"))

# Process CSV efficiently
import csv

def process_csv(path: Path) -> Iterator[dict]:
    """Stream CSV rows as dicts."""
    with open(path, "r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            yield row
```

---

## 7. Standard Library Utilities

### functools Examples

```python
from functools import lru_cache, partial, reduce

# Memoization with lru_cache
@lru_cache(maxsize=128)
def expensive_computation(n: int) -> int:
    """Cached expensive computation."""
    return sum(i ** 2 for i in range(n))

# Check cache stats
print(expensive_computation.cache_info())
# CacheInfo(hits=5, misses=10, maxsize=128, currsize=10)

# Partial function application
def power(base: int, exponent: int) -> int:
    return base ** exponent

square = partial(power, exponent=2)
cube = partial(power, exponent=3)

print(square(5))  # 25
print(cube(5))    # 125

# Reduce for cumulative operations
numbers = [1, 2, 3, 4, 5]
product = reduce(lambda a, b: a * b, numbers)
print(product)  # 120
```

### itertools Examples

```python
from itertools import chain, groupby, islice, product, combinations

# Chain multiple iterables
lists = [[1, 2], [3, 4], [5, 6]]
flat = list(chain.from_iterable(lists))
# [1, 2, 3, 4, 5, 6]

# Group consecutive items
data = [
    {"name": "Alice", "dept": "Engineering"},
    {"name": "Bob", "dept": "Engineering"},
    {"name": "Charlie", "dept": "Sales"},
    {"name": "David", "dept": "Sales"},
]

# Must be sorted by grouping key first!
for dept, group in groupby(data, key=lambda x: x["dept"]):
    print(f"{dept}: {[p['name'] for p in group]}")
# Engineering: ['Alice', 'Bob']
# Sales: ['Charlie', 'David']

# Slice iterators
def infinite_counter():
    n = 0
    while True:
        yield n
        n += 1

first_10 = list(islice(infinite_counter(), 10))
# [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

# Cartesian product
colors = ["red", "blue"]
sizes = ["S", "M", "L"]
variants = list(product(colors, sizes))
# [('red', 'S'), ('red', 'M'), ('red', 'L'),
#  ('blue', 'S'), ('blue', 'M'), ('blue', 'L')]

# Combinations
items = ["A", "B", "C", "D"]
pairs = list(combinations(items, 2))
# [('A', 'B'), ('A', 'C'), ('A', 'D'), ('B', 'C'), ('B', 'D'), ('C', 'D')]
```

### collections Examples

```python
from collections import defaultdict, Counter, deque, namedtuple

# Named tuple for simple data structures
Point = namedtuple("Point", ["x", "y"])
p = Point(3, 4)
print(p.x, p.y)  # 3 4

# Deque for efficient queue operations
queue = deque(maxlen=3)
queue.append(1)
queue.append(2)
queue.append(3)
queue.append(4)  # 1 is dropped
print(list(queue))  # [2, 3, 4]

# Rotate
queue.rotate(1)   # [4, 2, 3]
queue.rotate(-1)  # [2, 3, 4]

# Counter operations
words = "the quick brown fox jumps over the lazy dog".split()
word_freq = Counter(words)
print(word_freq.most_common(3))
# [('the', 2), ('quick', 1), ('brown', 1)]

# Combine counters
c1 = Counter(a=3, b=1)
c2 = Counter(a=1, b=2)
print(c1 + c2)  # Counter({'a': 4, 'b': 3})
print(c1 - c2)  # Counter({'a': 2})
```

---

## 8. Virtual Environment and Package Management

### uv Project Setup

```python
# Create new project
# $ uv init my_project --python 3.12

# pyproject.toml generated:
"""
[project]
name = "my-project"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = []

[project.optional-dependencies]
dev = []
"""

# Add dependencies
# $ uv add requests httpx
# $ uv add --dev pytest ruff mypy

# pyproject.toml after adding deps:
"""
[project]
name = "my-project"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = [
    "requests>=2.31.0",
    "httpx>=0.27.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0.0",
    "ruff>=0.8.0",
    "mypy>=1.13.0",
]

[tool.ruff]
line-length = 88
target-version = "py312"

[tool.ruff.lint]
select = ["E", "F", "I", "B", "UP"]

[tool.mypy]
python_version = "3.12"
strict = true
"""
```

### Running with uv

```bash
# Sync environment (install dependencies)
uv sync

# Run Python
uv run python main.py

# Run tests
uv run pytest

# Run type checker
uv run mypy src/

# Run linter
uv run ruff check .
uv run ruff format .

# Install Python versions
uv python install 3.12 3.13

# Pin Python version
uv python pin 3.12
```

---

*Python Basics Examples v2.0*
*Last updated: 2026-01-25*
