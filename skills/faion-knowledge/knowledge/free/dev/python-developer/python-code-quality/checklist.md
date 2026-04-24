# Python Code Quality Checklist

Step-by-step checklist for establishing and maintaining code quality in Python projects.

---

## Project Setup Checklist

### Initial Configuration

- [ ] Create `pyproject.toml` with project metadata
- [ ] Configure Ruff (linter + formatter)
- [ ] Configure mypy or pyright (type checker)
- [ ] Create `.pre-commit-config.yaml`
- [ ] Install pre-commit hooks: `pre-commit install`
- [ ] Set up CI/CD pipeline with quality gates
- [ ] Configure test coverage requirements

### Ruff Configuration

- [ ] Set target Python version (`target-version = "py311"`)
- [ ] Set line length (`line-length = 88`)
- [ ] Enable core rule sets: E (errors), F (pyflakes), I (isort), B (bugbear), UP (pyupgrade)
- [ ] Configure import sorting sections
- [ ] Set up per-file ignores for tests (`__init__.py:F401`, `tests/*:S101`)
- [ ] Exclude non-code directories (migrations, .venv, node_modules)

### Type Checking Configuration

- [ ] Enable strict mode for new projects
- [ ] Configure plugins (django-stubs, fastapi-stubs, etc.)
- [ ] Set up mypy.ini or pyproject.toml [tool.mypy]
- [ ] Add type stub packages for dependencies
- [ ] Configure per-module overrides if needed

### Pre-commit Hooks

- [ ] Add Ruff linter hook
- [ ] Add Ruff formatter hook
- [ ] Add mypy hook with dependencies
- [ ] Add trailing-whitespace and end-of-file-fixer
- [ ] Add check-yaml, check-json, check-toml
- [ ] Add no-commit-to-branch (protect main/master)
- [ ] Optional: Add bandit for security scanning
- [ ] Test hooks: `pre-commit run --all-files`

---

## Code Writing Checklist

### Before Writing Code

- [ ] Understand the requirement fully
- [ ] Identify the single responsibility of each function/class
- [ ] Plan the module structure
- [ ] Consider testability from the start

### While Writing Code

#### Naming

- [ ] Use descriptive, intention-revealing names
- [ ] Use verbs for functions (`calculate_total`, `send_email`)
- [ ] Use nouns for classes (`UserService`, `OrderRepository`)
- [ ] Avoid abbreviations except well-known ones (HTTP, URL, etc.)
- [ ] Constants in UPPER_SNAKE_CASE
- [ ] Private members with single underscore prefix

#### Functions

- [ ] Single responsibility (do one thing well)
- [ ] Max 20-30 lines preferred
- [ ] Max 3-4 parameters (use dataclasses for more)
- [ ] Use early returns for guard clauses
- [ ] Avoid deep nesting (max 3 levels)
- [ ] No side effects in functions that return values

#### Type Hints

- [ ] All function parameters typed
- [ ] All function return types specified
- [ ] Use `-> None` for functions without return
- [ ] Use `Optional[T]` or `T | None` for nullable types
- [ ] Use generics for reusable code (`list[T]`, `dict[K, V]`)
- [ ] Use `TypedDict` for structured dictionaries
- [ ] Use `Protocol` for duck typing

#### Documentation

- [ ] Module-level docstring explaining purpose
- [ ] Class docstring with description and attributes
- [ ] Function docstring with params, returns, raises
- [ ] Add usage examples for complex functions
- [ ] Keep docstrings updated when code changes

#### Error Handling

- [ ] Use specific exceptions, not bare `except:`
- [ ] Create custom exceptions for domain errors
- [ ] Don't silence exceptions without logging
- [ ] Use context managers for resource cleanup
- [ ] Validate inputs early (fail fast)

### After Writing Code

- [ ] Run `ruff check --fix` to auto-fix issues
- [ ] Run `ruff format` to format code
- [ ] Run `mypy` to check types
- [ ] Write or update tests
- [ ] Run tests with coverage
- [ ] Review your own code before committing

---

## Code Review Checklist

### Automated Checks (CI/CD)

- [ ] Ruff linting passes (zero errors)
- [ ] Ruff formatting matches
- [ ] mypy/pyright type checking passes
- [ ] All tests pass
- [ ] Coverage threshold met (>80%)
- [ ] No security vulnerabilities (bandit)

### Manual Review

#### Correctness

- [ ] Code does what the ticket/requirement asks
- [ ] Edge cases handled
- [ ] Error conditions handled gracefully
- [ ] No obvious bugs or logic errors

#### Design

- [ ] Follows SOLID principles
- [ ] No code duplication (DRY)
- [ ] Appropriate abstraction level
- [ ] Dependencies injected, not hardcoded
- [ ] No circular dependencies

#### Readability

- [ ] Code is self-documenting (clear names)
- [ ] Complex logic has comments explaining "why"
- [ ] Consistent style with codebase
- [ ] No dead code or commented-out code

#### Security

- [ ] No hardcoded secrets or credentials
- [ ] User input validated and sanitized
- [ ] SQL injection prevention (parameterized queries)
- [ ] No unsafe deserialization
- [ ] Sensitive data not logged

#### Performance

- [ ] No N+1 queries
- [ ] Appropriate data structures used
- [ ] Expensive operations not in loops
- [ ] Caching considered where appropriate

#### Testing

- [ ] Unit tests for new functions/methods
- [ ] Integration tests for API endpoints
- [ ] Edge cases tested
- [ ] Error paths tested
- [ ] Tests are readable and maintainable

---

## SOLID Principles Checklist

### Single Responsibility Principle (SRP)

- [ ] Each class has one reason to change
- [ ] Functions do one thing
- [ ] Modules have a clear, focused purpose
- [ ] Large classes split into smaller, focused ones

### Open/Closed Principle (OCP)

- [ ] New features added via extension, not modification
- [ ] Use ABCs or Protocols for extension points
- [ ] Strategy pattern for interchangeable algorithms
- [ ] Plugin architecture where appropriate

### Liskov Substitution Principle (LSP)

- [ ] Subclasses can replace parent classes
- [ ] Subclass doesn't weaken preconditions
- [ ] Subclass doesn't strengthen postconditions
- [ ] Inheritance represents "is-a" relationship

### Interface Segregation Principle (ISP)

- [ ] Interfaces are small and focused
- [ ] Clients don't depend on methods they don't use
- [ ] Use Protocols for defining interfaces
- [ ] Multiple small interfaces > one large interface

### Dependency Inversion Principle (DIP)

- [ ] High-level modules don't depend on low-level modules
- [ ] Both depend on abstractions (Protocols/ABCs)
- [ ] Dependencies injected via constructor
- [ ] Easy to swap implementations (testing, different envs)

---

## Clean Code Checklist

### Naming

- [ ] Names reveal intention
- [ ] Names are pronounceable
- [ ] Names are searchable
- [ ] No encodings (Hungarian notation)
- [ ] Consistent naming across codebase

### Functions

- [ ] Small (do one thing)
- [ ] One level of abstraction per function
- [ ] No boolean flag parameters (split into two functions)
- [ ] Side effects clearly documented
- [ ] Command-query separation

### Comments

- [ ] Explain "why", not "what"
- [ ] No redundant comments
- [ ] TODO comments have ticket references
- [ ] Remove commented-out code
- [ ] Keep comments updated

### Formatting

- [ ] Consistent style (automated with Ruff)
- [ ] Related code grouped together
- [ ] Vertical spacing shows relationships
- [ ] Max line length enforced

### Error Handling

- [ ] Exceptions for exceptional cases
- [ ] Don't return error codes (raise exceptions)
- [ ] Context provided in error messages
- [ ] Stack traces preserved

---

## Pre-Release Checklist

### Code Quality

- [ ] All CI checks pass
- [ ] Code coverage > 80%
- [ ] No TODO comments without tickets
- [ ] No debug code (print statements, debugger)
- [ ] All dependencies pinned

### Documentation

- [ ] README updated
- [ ] API documentation current
- [ ] CHANGELOG updated
- [ ] Migration guide if breaking changes

### Security

- [ ] Security scan passed (bandit)
- [ ] Dependencies scanned for vulnerabilities
- [ ] Secrets management verified
- [ ] Rate limiting configured

### Testing

- [ ] All unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing completed
- [ ] Performance testing if applicable

---

## Quick Reference: Common Ruff Rules

| Rule | Description | Example |
|------|-------------|---------|
| E501 | Line too long | Disable (formatter handles) |
| F401 | Unused import | Remove import |
| F841 | Unused variable | Remove or use |
| B006 | Mutable default argument | Use `None` + `field or []` |
| B007 | Unused loop variable | Use `_` prefix |
| UP035 | Deprecated typing import | `from typing import List` -> `list` |
| I001 | Import not sorted | Run `ruff format` |
| S101 | Assert used | OK in tests |
| C901 | Function too complex | Refactor |

---

## Quick Reference: mypy Flags

| Flag | Description | Recommendation |
|------|-------------|----------------|
| `--strict` | Enable all strict flags | New projects |
| `--disallow-untyped-defs` | Require type hints | Always |
| `--no-implicit-optional` | No implicit `None` | Always |
| `--warn-return-any` | Warn on `Any` returns | Recommended |
| `--ignore-missing-imports` | Skip missing stubs | Development |
