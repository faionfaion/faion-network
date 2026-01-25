---
name: faion-python-skill
user-invocable: false
description: ""
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(python:*, pip:*, poetry:*, pytest:*, mypy:*, black:*, isort:*, flake8:*)
---

# Python Ecosystem Skill

**Technical skill for Python development: Django, FastAPI, pytest, Poetry, async, typing, and code quality tools.**

---

## Purpose

Provides patterns and best practices for Python ecosystem development. Used by faion-code-agent for:
- Python project setup and dependency management
- Django web application development
- FastAPI REST API development
- Testing with pytest
- Type hints and static analysis
- Code formatting and linting

---

## 3-Layer Architecture

```
Layer 1: Domain Skills (orchestrators)
    |
Layer 2: Agents (executors)
    |   - faion-code-agent (uses this skill)
    |   - faion-test-agent (uses this skill)
    |
Layer 3: Technical Skills (this)
    - faion-python-skill
```

---

## Triggers

Use this skill when:
- Setting up a new Python project
- Writing Django models, views, serializers, admin
- Creating FastAPI routes and dependencies
- Writing pytest tests, fixtures, mocking
- Managing dependencies with Poetry or pip
- Adding type hints and running mypy
- Configuring Black, isort, flake8

---

## Modules

This skill is decomposed into focused modules:

| Module | Content | Lines |
|--------|---------|-------|
| [python-basics.md](python-basics.md) | Poetry setup, venv, pyenv | ~480 |
| [python-typing.md](python-typing.md) | Type hints, mypy, Protocol | ~280 |
| [python-async.md](python-async.md) | asyncio, concurrent execution | ~340 |
| [python-code-quality.md](python-code-quality.md) | Black, isort, flake8, pre-commit | ~280 |
| [python-web-frameworks.md](python-web-frameworks.md) | Django, FastAPI patterns | ~550 |
| [python-testing-pytest.md](python-testing-pytest.md) | pytest, fixtures, mocking | ~400 |

**All Python patterns are now in separate modules.**

---


# Quick Reference (Legacy)

**Django and FastAPI patterns moved to:** [python-web-frameworks.md](python-web-frameworks.md)

**pytest patterns moved to:** [python-testing-pytest.md](python-testing-pytest.md)

---


# Quick Reference

## Tools

| Tool | Purpose | Command |
|------|---------|---------|
| Poetry | Dependency management | `poetry add`, `poetry install` |
| pytest | Testing | `pytest`, `pytest --cov` |
| mypy | Type checking | `mypy src/` |
| Black | Code formatting | `black src/` |
| isort | Import sorting | `isort src/` |
| flake8 | Linting | `flake8 src/` |

## Patterns Summary

| Pattern | Use When |
|---------|----------|
| Services | Business logic, DB writes |
| Thin Views | HTTP handling only |
| Factory Fixtures | Flexible test data |
| TypedDict | Structured dictionaries |
| Protocol | Duck typing with type safety |
| asyncio.gather | Concurrent I/O operations |
| Semaphore | Rate limiting |

## Methodology Index

| Name | File | Purpose |
|------|------|---------|
| Project Setup with Poetry | [python-basics.md](python-basics.md) | Dependency management |
| Virtual Environments | [python-basics.md](python-basics.md) | venv, Poetry, pyenv |
| Type Hints and mypy | [python-typing.md](python-typing.md) | Type safety and static analysis |
| Async Python | [python-async.md](python-async.md) | asyncio, concurrent execution |
| Code Formatting | [python-code-quality.md](python-code-quality.md) | Black, isort, flake8 |
| Django Patterns | [python-web-frameworks.md](python-web-frameworks.md) | Models, views, serializers, admin |
| FastAPI Patterns | [python-web-frameworks.md](python-web-frameworks.md) | Routes, dependencies, Pydantic |
| pytest Patterns | [python-testing-pytest.md](python-testing-pytest.md) | Fixtures, mocking, parametrize |

---

## Sources

- [Python Documentation](https://docs.python.org/3/)
- [Django Documentation](https://docs.djangoproject.com/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [pytest Documentation](https://docs.pytest.org/)
- [mypy Documentation](https://mypy.readthedocs.io/)
- [Poetry Documentation](https://python-poetry.org/docs/)
- [Black Documentation](https://black.readthedocs.io/)
- [isort Documentation](https://pycqa.github.io/isort/)

---

*Python Ecosystem Skill v1.0*
*Layer 3 Technical Skill*
*8 Methodologies | Used by faion-code-agent, faion-test-agent*


---

## Methodologies

| Name | File |
|------|------|
| Project Setup Poetry | [methodologies/project-setup-poetry.md](methodologies/project-setup-poetry.md) |
| Django Patterns | [methodologies/django-patterns.md](methodologies/django-patterns.md) |
| Fastapi Patterns | [methodologies/fastapi-patterns.md](methodologies/fastapi-patterns.md) |
| Pytest Testing | [methodologies/pytest-testing.md](methodologies/pytest-testing.md) |
| Asyncio Patterns | [methodologies/asyncio-patterns.md](methodologies/asyncio-patterns.md) |
| Type Hints | [methodologies/type-hints.md](methodologies/type-hints.md) |
| Packaging | [methodologies/packaging.md](methodologies/packaging.md) |
| Code Quality | [methodologies/code-quality.md](methodologies/code-quality.md) |
