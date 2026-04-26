# Python Basics Checklist

Step-by-step checklist for mastering Python fundamentals.

---

## 1. Environment Setup

- [ ] Install Python 3.12+ (or 3.13+ for latest features)
- [ ] Install uv package manager: `curl -LsSf https://astral.sh/uv/install.sh | sh`
- [ ] Configure IDE (VS Code with Python extension, Pylance)
- [ ] Create first project: `uv init my_project --python 3.12`
- [ ] Understand pyproject.toml structure
- [ ] Install code quality tools: `uv add --dev ruff mypy pytest`

---

## 2. Data Structures

### Lists
- [ ] Create and modify lists: `append()`, `extend()`, `insert()`, `remove()`, `pop()`
- [ ] List slicing: `lst[start:stop:step]`
- [ ] List comprehensions: `[x**2 for x in range(10)]`
- [ ] Conditional comprehensions: `[x for x in items if x > 0]`
- [ ] Nested comprehensions: `[[i*j for j in range(5)] for i in range(5)]`
- [ ] Know when to use `list()` vs `[]`

### Tuples
- [ ] Understand immutability
- [ ] Tuple unpacking: `a, b, c = (1, 2, 3)`
- [ ] Extended unpacking: `first, *rest, last = items`
- [ ] Named tuples: `from collections import namedtuple`
- [ ] Use tuples as dict keys

### Dictionaries
- [ ] Create and access: `d["key"]`, `d.get("key", default)`
- [ ] Dict methods: `keys()`, `values()`, `items()`
- [ ] Dict comprehensions: `{k: v for k, v in pairs}`
- [ ] Merging dicts: `d1 | d2` (3.9+)
- [ ] `defaultdict` for automatic defaults
- [ ] `Counter` for counting

### Sets
- [ ] Set operations: `union`, `intersection`, `difference`
- [ ] Set comprehensions: `{x for x in items}`
- [ ] Use sets for membership testing (O(1) vs O(n) for lists)
- [ ] `frozenset` for immutable sets

### Collections Module
- [ ] `defaultdict` - dict with default factory
- [ ] `Counter` - count hashable objects
- [ ] `OrderedDict` - remember insertion order (less needed in 3.7+)
- [ ] `deque` - fast appends/pops from both ends
- [ ] `ChainMap` - combine multiple dicts

---

## 3. Control Flow

### Conditionals
- [ ] `if/elif/else` statements
- [ ] Ternary operator: `x if condition else y`
- [ ] Truthiness: understand what evaluates to `False`
- [ ] Chained comparisons: `0 < x < 10`
- [ ] `in` operator for membership
- [ ] `is` vs `==` (identity vs equality)

### Loops
- [ ] `for` loops with `range()`, `enumerate()`, `zip()`
- [ ] `while` loops with break conditions
- [ ] `break` and `continue`
- [ ] `for...else` clause (runs if no break)
- [ ] Avoid modifying lists while iterating

### Pattern Matching (3.10+)
- [ ] Basic `match/case` syntax
- [ ] Literal patterns
- [ ] Capture patterns with guards: `case x if x > 0`
- [ ] Sequence patterns: `case [first, *rest]`
- [ ] Mapping patterns: `case {"action": action}`
- [ ] Class patterns: `case Point(x=0, y=y)`
- [ ] OR patterns: `case "yes" | "y"`

### Walrus Operator (3.8+)
- [ ] Assignment expressions: `if (n := len(data)) > 10:`
- [ ] Use in comprehensions: `[y for x in data if (y := f(x))]`
- [ ] Avoid overuse - readability matters

---

## 4. Functions

### Basics
- [ ] Define functions with `def`
- [ ] Return values (single and multiple via tuples)
- [ ] Default arguments (avoid mutable defaults!)
- [ ] `*args` for variable positional arguments
- [ ] `**kwargs` for variable keyword arguments
- [ ] Docstrings with examples

### Advanced Arguments
- [ ] Keyword-only arguments: `def f(*, name):`
- [ ] Positional-only arguments: `def f(x, /)` (3.8+)
- [ ] Combined: `def f(pos_only, /, normal, *, kw_only):`

### Type Hints
- [ ] Basic hints: `def f(x: int) -> str:`
- [ ] Optional: `def f(x: int | None = None):`
- [ ] Collections: `def f(items: list[str]) -> dict[str, int]:`
- [ ] Callable: `Callable[[int, str], bool]`

### Lambda Functions
- [ ] Single-expression lambdas: `lambda x: x**2`
- [ ] Use in `sorted()`, `filter()`, `map()`
- [ ] Know when to use lambda vs def

### Closures
- [ ] Understand nested functions
- [ ] Capture variables from enclosing scope
- [ ] `nonlocal` keyword for modification

### Decorators
- [ ] Understand decorator pattern
- [ ] Use `@functools.wraps` to preserve metadata
- [ ] Decorators with arguments
- [ ] Class-based decorators with `__call__`
- [ ] Built-in: `@property`, `@staticmethod`, `@classmethod`
- [ ] Common: `@lru_cache`, `@dataclass`

---

## 5. Classes and OOP

### Basics
- [ ] Define classes with `class`
- [ ] `__init__` constructor
- [ ] Instance attributes vs class attributes
- [ ] Instance methods with `self`
- [ ] `@classmethod` with `cls`
- [ ] `@staticmethod` without self/cls

### Dunder Methods
- [ ] `__str__` and `__repr__`
- [ ] `__eq__`, `__lt__`, `__hash__`
- [ ] `__len__`, `__getitem__`, `__iter__`
- [ ] `__enter__` and `__exit__` (context managers)
- [ ] `__call__` (callable objects)

### Inheritance
- [ ] Single inheritance
- [ ] `super()` for parent methods
- [ ] Method Resolution Order (MRO)
- [ ] Avoid deep inheritance hierarchies
- [ ] Prefer composition over inheritance

### Properties
- [ ] `@property` for getters
- [ ] `@name.setter` for setters
- [ ] `@name.deleter` for deleters
- [ ] Use for validation and computed attributes

### Dataclasses (3.7+)
- [ ] Basic `@dataclass` usage
- [ ] Default values and `field()`
- [ ] `frozen=True` for immutability
- [ ] `slots=True` for memory efficiency (3.10+)
- [ ] Post-init processing with `__post_init__`

### Protocols (Structural Subtyping)
- [ ] Define protocols with `Protocol`
- [ ] `@runtime_checkable` for isinstance checks
- [ ] Prefer protocols over ABC for flexibility

---

## 6. Error Handling

### Try/Except Basics
- [ ] Basic `try/except` block
- [ ] Catch specific exceptions (not bare `except:`)
- [ ] Multiple except clauses
- [ ] `except Exception as e` for access to exception
- [ ] `else` clause (runs if no exception)
- [ ] `finally` clause (always runs)

### Best Practices
- [ ] EAFP: Easier to Ask Forgiveness than Permission
- [ ] Keep try blocks narrow
- [ ] Don't catch exceptions silently
- [ ] Re-raise after logging: `raise`
- [ ] Exception chaining: `raise NewError() from original`
- [ ] Use logging instead of print

### Custom Exceptions
- [ ] Inherit from `Exception` (not `BaseException`)
- [ ] Define exception hierarchy for your module
- [ ] Include useful error messages
- [ ] Add custom attributes if needed

### Context Managers
- [ ] Use `with` for resource management
- [ ] File handling: `with open(...) as f:`
- [ ] Create custom with `@contextmanager`
- [ ] Use `ExitStack` for multiple managers

---

## 7. File I/O

### pathlib (Modern Approach)
- [ ] Create paths: `Path("dir/file.txt")`
- [ ] Join paths: `path / "subdir" / "file"`
- [ ] Check existence: `path.exists()`, `path.is_file()`
- [ ] Read/write: `path.read_text()`, `path.write_text()`
- [ ] Iterate: `path.glob("*.txt")`, `path.rglob("**/*.py")`

### File Operations
- [ ] Open files with context managers
- [ ] Specify encoding: `open(file, encoding="utf-8")`
- [ ] Modes: `r`, `w`, `a`, `rb`, `wb`
- [ ] Read methods: `read()`, `readline()`, `readlines()`
- [ ] Write methods: `write()`, `writelines()`

### JSON
- [ ] `json.load()` and `json.dump()` for files
- [ ] `json.loads()` and `json.dumps()` for strings
- [ ] Handle encoding and special types

### CSV
- [ ] `csv.reader()` and `csv.writer()`
- [ ] `csv.DictReader()` and `csv.DictWriter()`

---

## 8. Standard Library Essentials

### functools
- [ ] `@lru_cache` for memoization
- [ ] `@cache` (simpler, unbounded) (3.9+)
- [ ] `partial` for partial function application
- [ ] `reduce` for cumulative operations
- [ ] `wraps` for decorator metadata

### itertools
- [ ] `chain` - flatten iterables
- [ ] `islice` - slice iterators
- [ ] `groupby` - group consecutive items
- [ ] `product`, `permutations`, `combinations`
- [ ] `cycle`, `repeat`, `count`
- [ ] `filterfalse`, `takewhile`, `dropwhile`

### collections
- [ ] `defaultdict` - dict with default values
- [ ] `Counter` - count elements
- [ ] `deque` - double-ended queue
- [ ] `namedtuple` - tuples with named fields
- [ ] `ChainMap` - combine mappings

### Other Essential Modules
- [ ] `logging` - structured logging
- [ ] `datetime` - date/time handling
- [ ] `re` - regular expressions
- [ ] `subprocess` - run external commands
- [ ] `argparse` - CLI argument parsing
- [ ] `os` and `shutil` - OS operations
- [ ] `typing` - type hints

---

## 9. Virtual Environments

### Understanding Virtual Environments
- [ ] Why isolate dependencies
- [ ] How venvs work
- [ ] Global vs local packages

### Built-in venv
- [ ] Create: `python -m venv .venv`
- [ ] Activate: `source .venv/bin/activate` (Unix)
- [ ] Deactivate: `deactivate`

### uv (Recommended)
- [ ] Install: `curl -LsSf https://astral.sh/uv/install.sh | sh`
- [ ] Create project: `uv init my_project`
- [ ] Add deps: `uv add requests`
- [ ] Sync: `uv sync`
- [ ] Run: `uv run python script.py`
- [ ] Manage Python: `uv python install 3.12`

### pyenv (Python Version Management)
- [ ] Install pyenv
- [ ] List versions: `pyenv install --list`
- [ ] Install version: `pyenv install 3.12.0`
- [ ] Set local: `pyenv local 3.12.0`
- [ ] Set global: `pyenv global 3.12.0`

---

## 10. Package Management

### pyproject.toml
- [ ] Understand `[project]` section
- [ ] Dependencies in `dependencies = [...]`
- [ ] Optional dependencies in `[project.optional-dependencies]`
- [ ] Tool configuration (`[tool.ruff]`, `[tool.mypy]`)

### Dependency Management
- [ ] Pin versions for reproducibility
- [ ] Use lock files (uv.lock, poetry.lock)
- [ ] Understand version specifiers: `>=`, `~=`, `^`
- [ ] Separate dev dependencies

### Publishing (Advanced)
- [ ] Build with `uv build` or `python -m build`
- [ ] Publish to PyPI with `uv publish` or `twine`
- [ ] Understand wheel vs sdist

---

## Progress Tracking

| Section | Status |
|---------|--------|
| 1. Environment Setup | [ ] Complete |
| 2. Data Structures | [ ] Complete |
| 3. Control Flow | [ ] Complete |
| 4. Functions | [ ] Complete |
| 5. Classes and OOP | [ ] Complete |
| 6. Error Handling | [ ] Complete |
| 7. File I/O | [ ] Complete |
| 8. Standard Library | [ ] Complete |
| 9. Virtual Environments | [ ] Complete |
| 10. Package Management | [ ] Complete |

---

*Python Basics Checklist v2.0*
*Last updated: 2026-01-25*
