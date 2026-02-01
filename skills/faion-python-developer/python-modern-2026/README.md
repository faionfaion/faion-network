# Modern Python 2026

**Comprehensive guide to Python 3.12, 3.13, and 3.14 features, modern tooling, and best practices.**

---

## Overview

Modern Python (2024-2026) represents a significant evolution in the language with:

- **Python 3.12**: Type parameter syntax (PEP 695), f-string improvements (PEP 701), 15% performance boost
- **Python 3.13**: Free-threaded mode (no GIL), experimental JIT, improved REPL, TypeIs/ReadOnly
- **Python 3.14**: Template strings (t-strings), deferred annotations, multiple interpreters, officially supported free-threading

### Version Matrix

| Version | Release | EOL | Key Features |
|---------|---------|-----|--------------|
| Python 3.12 | Oct 2023 | Oct 2028 | PEP 695 generics, PEP 701 f-strings, 15% faster |
| Python 3.13 | Oct 2024 | Oct 2029 | Free-threaded (experimental), JIT, improved REPL |
| Python 3.14 | Oct 2025 | Oct 2030 | t-strings, deferred annotations, free-threading stable |
| Python 3.15 | Oct 2026 (planned) | Oct 2031 | Free-threading likely default |

---

## Key Features by Version

### Python 3.12

**Type Parameter Syntax (PEP 695):**
```python
# Old way (pre-3.12)
from typing import TypeVar, Generic
T = TypeVar('T')
class Box(Generic[T]):
    def __init__(self, value: T) -> None: ...

# New way (3.12+)
class Box[T]:
    def __init__(self, value: T) -> None: ...

# Generic functions
def first[T](items: list[T]) -> T:
    return items[0]

# Type aliases
type Vector[T] = list[tuple[T, T]]
```

**F-String Improvements (PEP 701):**
```python
# Quote reuse (now allowed)
f"Hello {person['name']}"  # Works in 3.12+

# Nested f-strings
f"{f'{value:.2f}'}"  # Arbitrarily nestable

# Multiline expressions
result = f"Sum: {
    a +
    b +
    c
}"

# Backslashes in expressions
f"Path: {path.replace('\\', '/')}"
```

**Performance:**
- 15% faster than Python 3.11
- 10% lower memory usage
- Faster dictionary lookups

### Python 3.13

**Free-Threaded Mode (PEP 703):**
```python
# Run with: python3.13t -X gil=0
# Or set: PYTHON_GIL=0

import threading
from concurrent.futures import ThreadPoolExecutor

def cpu_bound_task(data: list[int]) -> int:
    # Actually runs in parallel without GIL
    return sum(x * x for x in data)

# True parallelism for CPU-bound tasks
with ThreadPoolExecutor(max_workers=4) as executor:
    results = list(executor.map(cpu_bound_task, chunks))
```

**New Typing Features:**
```python
from typing import TypeIs, ReadOnly, TypedDict

# TypeIs for type narrowing (PEP 742)
def is_string_list(val: list[object]) -> TypeIs[list[str]]:
    return all(isinstance(x, str) for x in val)

# ReadOnly for TypedDict fields (PEP 705)
class Config(TypedDict):
    version: ReadOnly[str]  # Cannot be modified
    debug: bool
```

**Improved REPL:**
- Syntax highlighting
- Multi-line editing with proper indentation
- Better auto-completion
- Persistent history

**Experimental JIT Compiler:**
```bash
# Enable with
python3.13 -X jit script.py
```

### Python 3.14

**Template Strings (PEP 750):**
```python
# t-strings for safe string processing
name = "Alice"
greeting = t"Hello, {name}!"  # Returns Template object

# SQL-safe queries
query = t"SELECT * FROM users WHERE name = {user_input}"
# Can be processed to prevent SQL injection

# HTML-safe templates
html = t"<p>{user_content}</p>"
# Can be escaped during processing
```

**Deferred Annotation Evaluation (PEP 649):**
```python
# Annotations evaluated only when accessed
# Reduces import time and circular import issues
class Node:
    def __init__(self, children: list["Node"]) -> None:
        self.children = children
```

**Multiple Interpreters (PEP 734):**
```python
import interpreters

# Create isolated interpreter
interp = interpreters.create()

# Run code in isolated namespace
interp.exec("x = 42")
```

**Other Improvements:**
- `uuid6()`, `uuid7()`, `uuid8()` functions
- `compression.zstd` module for Zstandard compression
- `except` without parentheses: `except ValueError, TypeError:`
- Remote debugging with `pdb -p PID`
- Improved startup time

---

## Modern Tooling Stack

### Package Management: uv

**Why uv?**
- 10-100x faster than pip
- Single binary (Rust-based)
- Manages Python versions, packages, and virtual environments
- Global cache saves disk space

```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create project
uv init my_project --python 3.13

# Add dependencies
uv add fastapi uvicorn
uv add --dev pytest ruff mypy

# Sync environment
uv sync

# Run commands
uv run pytest
uv run python main.py

# Manage Python versions
uv python install 3.12 3.13 3.14
uv python pin 3.13
```

### Linting & Formatting: Ruff

**Why Ruff?**
- 10-100x faster than Flake8 + Black + isort
- Single tool replaces multiple linters
- 800+ built-in rules

```bash
# Install
uv add --dev ruff

# Check and fix
ruff check . --fix
ruff format .
```

**Configuration (pyproject.toml):**
```toml
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

[tool.ruff.format]
quote-style = "double"
```

### Type Checking: pyright/mypy

```toml
# pyproject.toml
[tool.pyright]
pythonVersion = "3.13"
typeCheckingMode = "strict"

[tool.mypy]
python_version = "3.13"
strict = true
```

### Testing: pytest

```bash
# Modern pytest setup
uv add --dev pytest pytest-asyncio pytest-cov

# Run tests
uv run pytest -v --cov=src
```

---

## Project Structure

### Modern pyproject.toml

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
dependencies = [
    "fastapi>=0.115.0",
    "pydantic>=2.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0",
    "pytest-asyncio>=0.24",
    "pytest-cov>=5.0",
    "ruff>=0.8",
    "mypy>=1.13",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["src/my_project"]

[tool.ruff]
line-length = 88
target-version = "py312"

[tool.ruff.lint]
select = ["E", "F", "I", "B", "UP", "N", "S", "C4", "PT"]

[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["tests"]

[tool.mypy]
python_version = "3.13"
strict = true
```

### Directory Layout

```
my-project/
├── pyproject.toml
├── uv.lock
├── README.md
├── src/
│   └── my_project/
│       ├── __init__.py
│       ├── main.py
│       ├── models.py
│       └── services/
│           ├── __init__.py
│           └── user_service.py
└── tests/
    ├── __init__.py
    ├── conftest.py
    └── test_main.py
```

---

## LLM Usage Tips

### For Code Generation

1. **Specify Python version explicitly**: "Using Python 3.13 with type hints..."
2. **Request modern syntax**: "Use PEP 695 type parameter syntax"
3. **Ask for tooling config**: "Include pyproject.toml with ruff and mypy config"

### For Refactoring

1. **Modernize generics**: "Convert TypeVar to PEP 695 syntax"
2. **Update typing imports**: "Use built-in generics (list, dict) instead of typing module"
3. **Improve f-strings**: "Use PEP 701 f-string features"

### For Code Review

1. **Check modern patterns**: "Review for Python 3.12+ best practices"
2. **Validate typing**: "Ensure strict type hints are used"
3. **Security scan**: "Check for security issues with Ruff S rules"

### Prompt Patterns

```
Generate a [Python 3.13] [FastAPI] service that:
- Uses PEP 695 generics
- Includes strict type hints
- Has pytest tests with pytest-asyncio
- Includes pyproject.toml with uv, ruff, mypy config
```

---

## Performance Comparison

### Free-Threading Benchmarks (Python 3.14)

| Scenario | GIL Enabled | Free-Threaded | Speedup |
|----------|-------------|---------------|---------|
| CPU-bound (6 cores) | 2.0s | 0.6s | 3.3x |
| Mixed I/O + CPU | 1.5s | 0.8s | 1.9x |
| Pure I/O | 0.5s | 0.5s | 1.0x |

### Version Performance (Single-threaded)

| Version | Relative Speed |
|---------|----------------|
| Python 3.10 | 1.0x (baseline) |
| Python 3.11 | 1.25x |
| Python 3.12 | 1.44x |
| Python 3.13 | 1.50x |
| Python 3.14 | 1.55x |

---

## Migration Path

### From Python 3.10/3.11 to 3.12+

1. **Update type hints**: Replace `from typing import List, Dict` with built-in `list`, `dict`
2. **Modernize generics**: Convert `TypeVar` to PEP 695 syntax (optional)
3. **Update f-strings**: Use new capabilities (nested, multiline)
4. **Update tooling**: Switch to Ruff, uv

### From Python 3.12 to 3.13+

1. **Test free-threading**: Check if your code is thread-safe
2. **Update C extensions**: Ensure compatibility with free-threaded build
3. **Use TypeIs/ReadOnly**: For better type narrowing

### From Python 3.13 to 3.14

1. **Adopt t-strings**: For template processing
2. **Use deferred annotations**: Simplify forward references
3. **Test multi-interpreter**: For isolation needs

---

## Agent Selection

| Task | Model | Rationale |
|------|-------|----------|
| Analyze and assess | sonnet | Evaluation and planning |
| Execute implementation | haiku | Apply established patterns |
| Review and validate | sonnet | Quality assurance |
| Strategic decision | opus | Novel scenarios |
| Optimize and refine | haiku | Performance tuning |
| Document approach | haiku | Create documentation |

## External Resources

### Official Documentation

- [Python 3.12 What's New](https://docs.python.org/3/whatsnew/3.12.html)
- [Python 3.13 What's New](https://docs.python.org/3/whatsnew/3.13.html)
- [Python 3.14 What's New](https://docs.python.org/3/whatsnew/3.14.html)
- [Free-Threading HOWTO](https://docs.python.org/3/howto/free-threading-python.html)
- [Typing Documentation](https://docs.python.org/3/library/typing.html)

### PEPs

- [PEP 695 - Type Parameter Syntax](https://peps.python.org/pep-0695/)
- [PEP 701 - Syntactic Formalization of F-Strings](https://peps.python.org/pep-0701/)
- [PEP 703 - Making the GIL Optional](https://peps.python.org/pep-0703/)
- [PEP 742 - TypeIs](https://peps.python.org/pep-0742/)
- [PEP 750 - Template Strings](https://peps.python.org/pep-0750/)
- [PEP 649 - Deferred Evaluation of Annotations](https://peps.python.org/pep-0649/)

### Tooling

- [uv Documentation](https://docs.astral.sh/uv/)
- [Ruff Documentation](https://docs.astral.sh/ruff/)
- [pytest Documentation](https://docs.pytest.org/)
- [pytest-asyncio](https://pytest-asyncio.readthedocs.io/)
- [mypy Documentation](https://mypy.readthedocs.io/)
- [pyright](https://github.com/microsoft/pyright)

### Tutorials and Articles

- [Real Python - Python 3.13 Free Threading and JIT](https://realpython.com/python313-free-threading-jit/)
- [Real Python - Python 3.12 F-Strings](https://realpython.com/python312-f-strings/)
- [Real Python - Python 3.12 Static Typing](https://realpython.com/python312-typing/)
- [DataCamp - Python UV Tutorial](https://www.datacamp.com/tutorial/python-uv)
- [Managing Projects with uv - Real Python](https://realpython.com/python-uv/)

---

## Related Files

| File | Description |
|------|-------------|
| [checklist.md](checklist.md) | Step-by-step adoption checklist |
| [examples.md](examples.md) | Real-world code examples |
| [templates.md](templates.md) | Copy-paste templates |
| [llm-prompts.md](llm-prompts.md) | LLM prompts for Python development |

---

*Modern Python 2026 v2.0*
*Last updated: 2026-01-25*
