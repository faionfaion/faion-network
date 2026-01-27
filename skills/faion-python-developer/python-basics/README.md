# Python Basics

**Comprehensive guide to Python fundamentals: data structures, control flow, functions, OOP, error handling, and modern tooling.**

---

## Overview

Python basics form the foundation of all Python development. This methodology covers:

- **Data Structures** - Lists, tuples, dicts, sets, comprehensions
- **Control Flow** - Conditionals, loops, pattern matching (3.10+)
- **Functions** - Arguments, decorators, closures, lambdas
- **Classes and OOP** - Inheritance, composition, dunder methods
- **Error Handling** - Try/except, custom exceptions, EAFP
- **File I/O** - pathlib, context managers, encoding
- **Standard Library** - Essential modules for daily work
- **Virtual Environments** - venv, uv, pyenv
- **Package Management** - pip, uv, pyproject.toml

## Python Version Support (2025-2026)

| Version | Release | EOL | Status |
|---------|---------|-----|--------|
| Python 3.11 | Oct 2022 | Oct 2027 | Stable, widely used |
| Python 3.12 | Oct 2023 | Oct 2028 | Recommended for new projects |
| Python 3.13 | Oct 2024 | Oct 2029 | Free-threading (experimental) |
| Python 3.14 | Oct 2025 | Oct 2030 | T-strings, deferred annotations |

**Recommendation:** Use Python 3.12+ for new projects. Python 3.13+ for free-threading experiments.

---

## Key Concepts

### 1. Data Structures

| Structure | Mutable | Ordered | Duplicates | Use Case |
|-----------|---------|---------|------------|----------|
| `list` | Yes | Yes | Yes | General sequences |
| `tuple` | No | Yes | Yes | Immutable sequences, dict keys |
| `dict` | Yes | Yes (3.7+) | Keys: No | Key-value mapping |
| `set` | Yes | No | No | Unique items, membership tests |
| `frozenset` | No | No | No | Immutable sets, dict keys |

**Modern Python (3.9+):**
- Use `list[int]` instead of `typing.List[int]`
- Use `dict[str, int]` instead of `typing.Dict[str, int]`
- Use `X | Y` instead of `Union[X, Y]` (3.10+)

### 2. Control Flow

**Pattern Matching (3.10+):**
```python
match command:
    case ["quit"]:
        return
    case ["load", filename]:
        load_file(filename)
    case ["save", filename, *options]:
        save_file(filename, options)
    case _:
        print("Unknown command")
```

**Walrus Operator (3.8+):**
```python
if (n := len(data)) > 10:
    print(f"List is too long ({n} elements)")
```

### 3. Functions and Decorators

**Best Practices:**
- Use type hints for all public functions
- Use `functools.wraps` in decorators
- Prefer keyword-only arguments for clarity: `def f(*, name: str)`
- Use positional-only for performance: `def f(x, /, y)` (3.8+)

### 4. Classes and OOP

**Modern Patterns:**
- Prefer composition over inheritance
- Use `@dataclass` for data containers
- Use `Protocol` for duck typing
- Use `__slots__` for memory optimization
- Use `@property` for computed attributes

### 5. Error Handling (EAFP)

**Python Philosophy:** Easier to Ask Forgiveness than Permission
```python
# Pythonic (EAFP)
try:
    value = data["key"]
except KeyError:
    value = default

# vs. non-Pythonic (LBYL)
if "key" in data:
    value = data["key"]
else:
    value = default
```

### 6. Virtual Environments and Package Management

**Modern Stack (2025-2026):**

| Tool | Purpose | Speed |
|------|---------|-------|
| **uv** | Package/env manager | 10-100x faster than pip |
| **pyenv** | Python version manager | Standard |
| **poetry** | Dependency management | Moderate |
| **pip** | Legacy package manager | Baseline |

**Recommended: uv**
- Single tool replaces pip, pip-tools, pipx, poetry, pyenv, virtualenv
- 10-100x faster than pip (warm cache)
- Global cache for disk efficiency
- Written in Rust

---

## LLM Usage Tips

### When Asking for Help

1. **Specify Python version**: "Using Python 3.12..." changes available features
2. **Mention context**: "For a Django project..." or "For data processing..."
3. **Request type hints**: "Include full type annotations"
4. **Ask for tests**: "Include pytest tests"

### Effective Prompts

```
Generate a Python 3.12+ function that [task] with:
- Full type hints
- Docstring with examples
- Error handling for [specific cases]
- pytest test cases
```

### Common Pitfalls LLMs Can Help With

| Problem | Ask LLM |
|---------|---------|
| Mutable default args | "Review this function for mutable default argument issues" |
| Memory efficiency | "Optimize this loop using generators/itertools" |
| Exception handling | "Add proper exception handling to this code" |
| Type safety | "Add mypy-compatible type hints" |

---

## Quick Reference

### Essential Imports

```python
# Standard library essentials
from pathlib import Path
from typing import Any
from collections import defaultdict, Counter
from functools import lru_cache, partial
from itertools import chain, groupby, islice
from contextlib import contextmanager
from dataclasses import dataclass, field
import json
import logging
```

### pyproject.toml (Modern Setup)

```toml
[project]
name = "my-project"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = []

[project.optional-dependencies]
dev = ["pytest", "ruff", "mypy"]

[tool.ruff]
line-length = 88
target-version = "py312"

[tool.ruff.lint]
select = ["E", "F", "I", "B", "UP"]

[tool.mypy]
python_version = "3.12"
strict = true
```

### uv Commands

```bash
# Project setup
uv init my_project --python 3.12
uv add requests fastapi
uv add --dev pytest ruff mypy

# Environment management
uv sync                    # Install dependencies
uv run python main.py      # Run in venv
uv run pytest              # Run tests

# Python management
uv python install 3.12 3.13
uv python pin 3.12
```

---

## External Resources

### Official Documentation

- [Python Tutorial](https://docs.python.org/3/tutorial/index.html)
- [Python Standard Library](https://docs.python.org/3/library/index.html)
- [Python Language Reference](https://docs.python.org/3/reference/index.html)
- [PEP 8 Style Guide](https://peps.python.org/pep-0008/)

### Package Management

- [uv Documentation](https://docs.astral.sh/uv/)
- [Poetry Documentation](https://python-poetry.org/docs/)
- [pyenv GitHub](https://github.com/pyenv/pyenv)
- [pip Documentation](https://pip.pypa.io/)

### Best Practices

- [Real Python Tutorials](https://realpython.com/tutorials/best-practices/)
- [Python Best Practices 2025](https://johal.in/python-programming-best-practices-in-2025/)
- [Modern Good Practices for Python](https://www.stuartellis.name/articles/python-modern-practices/)

### Tooling

- [Ruff Documentation](https://docs.astral.sh/ruff/)
- [mypy Documentation](https://mypy.readthedocs.io/)
- [pytest Documentation](https://docs.pytest.org/)

### PEPs (Python Enhancement Proposals)

- [PEP 8 - Style Guide](https://peps.python.org/pep-0008/)
- [PEP 20 - The Zen of Python](https://peps.python.org/pep-0020/)
- [PEP 484 - Type Hints](https://peps.python.org/pep-0484/)
- [PEP 636 - Structural Pattern Matching](https://peps.python.org/pep-0636/)
- [PEP 695 - Type Parameter Syntax](https://peps.python.org/pep-0695/)

---

## Related Methodologies

| Methodology | Focus |
|-------------|-------|
| [python-typing/](../python-typing/) | Type hints and static typing |
| [python-async/](../python-async/) | Async/await patterns |
| [python-code-quality/](../python-code-quality/) | Linting, formatting, quality |
| [python-modern-2026/](../python-modern-2026/) | Python 3.12-3.14 features |
| [python-poetry-setup/](../python-poetry-setup/) | Poetry configuration |
| [python-testing-pytest/](../python-testing-pytest/) | pytest testing |

---

## Related Files

| File | Description |
|------|-------------|
| [checklist.md](checklist.md) | Step-by-step learning checklist |
| [examples.md](examples.md) | Real Python code examples |
| [templates.md](templates.md) | Copy-paste code templates |
| [llm-prompts.md](llm-prompts.md) | Effective prompts for LLM-assisted learning |

---

*Python Basics v2.0*
*Last updated: 2026-01-25*
