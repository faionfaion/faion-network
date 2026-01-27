# Poetry Project Setup

## Overview

Poetry is the modern standard for Python dependency management, providing deterministic builds through lock files, virtual environment management, and streamlined publishing. As of 2025-2026, Poetry 2.x introduces PEP 621 compliance, making pyproject.toml portable across build tools.

**Key capabilities:**
- Dependency resolution with lock files
- Virtual environment management
- Package building and publishing
- Dependency groups (dev, test, docs)
- PEP 621-compliant metadata

## When to Use

| Scenario | Use Poetry |
|----------|------------|
| New Python project | Yes |
| Complex dependency trees | Yes |
| Publishing to PyPI | Yes |
| Reproducible builds | Yes |
| Monorepo (with plugins) | Yes |
| Quick scripts/experiments | Consider uv |
| CI/CD where speed is critical | Consider uv |

## Poetry 2.x Key Changes

Poetry 2.0 (released January 2025) introduced significant changes:

| Feature | Poetry 1.x | Poetry 2.x |
|---------|-----------|------------|
| Metadata location | `[tool.poetry]` | `[project]` (PEP 621) |
| Dependencies | `tool.poetry.dependencies` | `project.dependencies` |
| Python version | `python = "^3.11"` | `requires-python = ">=3.11,<4.0"` |
| Authors | String format | Table format |
| Build backend | `poetry.core.masonry.api` | Same (unchanged) |

### Migration from Poetry 1.x

```bash
# Install migration plugin
poetry self add poetry-plugin-migrate

# Run migration (creates backup)
poetry migrate
```

## Poetry vs uv vs pip

| Feature | Poetry | uv | pip |
|---------|--------|-----|-----|
| Speed | Medium | Very Fast (10-100x) | Slow |
| Lock file | Yes (poetry.lock) | Yes (uv.lock) | No (manual) |
| Virtual env mgmt | Yes | Yes | No |
| Dependency groups | Yes | Yes | No |
| Publishing | Yes | Yes | Requires twine |
| Python version mgmt | No (use pyenv) | Yes (built-in) | No |
| Maturity | High | Medium | High |
| Ecosystem | Large | Growing | Largest |
| Memory usage | High (1-2GB) | Low (10-50MB) | Medium |

### When to Choose Each

**Poetry:**
- Long-term, structured projects
- Publishing libraries to PyPI
- Teams familiar with Poetry
- Need mature ecosystem

**uv:**
- New projects (2025+)
- CI/CD where speed matters
- Quick experiments
- Memory-constrained environments

**pip:**
- Simple scripts
- Legacy projects
- Minimal tooling needed

## Core Concepts

### 1. pyproject.toml

Central configuration file (PEP 518/621):

```toml
[project]
name = "my-project"
version = "1.0.0"
requires-python = ">=3.11,<4.0"

[tool.poetry]
package-mode = true

[build-system]
requires = ["poetry-core>=2.0.0"]
build-backend = "poetry.core.masonry.api"
```

### 2. poetry.lock

Deterministic dependency snapshot:
- Always commit to version control
- Contains exact versions of all dependencies
- Ensures reproducible builds

### 3. Dependency Groups

Organize dependencies by purpose:

```toml
# Main dependencies (runtime)
[project.dependencies]

# Development dependencies
[tool.poetry.group.dev.dependencies]

# Optional groups
[tool.poetry.group.docs]
optional = true
```

### 4. Virtual Environments

Poetry manages isolated environments per project:

```bash
# Create venv in project directory
poetry config virtualenvs.in-project true

# Environment commands
poetry env info
poetry env use python3.12
poetry shell
```

## Directory Structure

```
my-project/
├── pyproject.toml          # Project configuration
├── poetry.lock             # Locked dependencies (COMMIT THIS)
├── README.md
├── .gitignore
│
├── src/                    # Source directory (recommended)
│   └── my_project/
│       ├── __init__.py
│       ├── main.py
│       └── ...
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   └── test_*.py
│
├── docs/
│   └── index.md
│
└── .venv/                  # Virtual environment (gitignored)
```

## Common Commands

| Command | Description |
|---------|-------------|
| `poetry new project` | Create new project |
| `poetry init` | Initialize in existing directory |
| `poetry install` | Install all dependencies |
| `poetry add package` | Add dependency |
| `poetry add -G dev package` | Add dev dependency |
| `poetry remove package` | Remove dependency |
| `poetry update` | Update dependencies |
| `poetry lock` | Update lock file |
| `poetry shell` | Activate virtual environment |
| `poetry run cmd` | Run command in venv |
| `poetry build` | Build package |
| `poetry publish` | Publish to PyPI |
| `poetry show --tree` | Show dependency tree |
| `poetry export` | Export to requirements.txt |

## Monorepo Support

Poetry supports monorepos through plugins:

| Plugin | Description |
|--------|-------------|
| poetry-monoranger-plugin | Shared lockfiles, venvs |
| poetry-workspace-plugin | Yarn-like workspaces |
| poetry-multiproject-plugin | Shared code between services |
| poetry-polylith-plugin | Polylith architecture |

Basic monorepo pattern (without plugins):

```toml
[tool.poetry.group.packages.dependencies]
shared-lib = { path = "../shared-lib", develop = true }
```

## LLM Usage Tips

### For Claude/Cursor/Copilot

1. **Provide context:** Include your pyproject.toml when asking about dependencies
2. **Specify Poetry version:** "Using Poetry 2.x with PEP 621"
3. **Be specific about groups:** "Add to dev group" or "Add as optional"
4. **Request lock file check:** "Verify compatibility with existing dependencies"

### Effective Prompts

```
"Generate pyproject.toml for a FastAPI project with Poetry 2.x:
- Python 3.12
- Dependencies: fastapi, uvicorn, sqlalchemy, asyncpg
- Dev: pytest, pytest-asyncio, mypy, ruff
- Docs: mkdocs (optional group)"
```

### Avoid

- Asking to edit poetry.lock manually
- Mixing pip and poetry commands
- Skipping lock file in version control

## External Resources

### Official Documentation
- [Poetry Documentation](https://python-poetry.org/docs/)
- [Poetry CLI Reference](https://python-poetry.org/docs/cli/)
- [Poetry 2.0 Announcement](https://python-poetry.org/blog/announcing-poetry-2.0.0/)

### Standards
- [PEP 517 - Build System](https://peps.python.org/pep-0517/)
- [PEP 518 - pyproject.toml](https://peps.python.org/pep-0518/)
- [PEP 621 - Project Metadata](https://peps.python.org/pep-0621/)
- [PEP 735 - Dependency Groups](https://peps.python.org/pep-0735/)

### Tutorials & Guides
- [Real Python: Dependency Management](https://realpython.com/dependency-management-python-poetry/)
- [Migrating to Poetry 2.x](https://therenegadecoder.com/code/migrating-to-poetry-2-x-with-some-best-practices/)
- [Poetry vs uv Comparison](https://medium.com/@hitorunajp/poetry-vs-uv-which-python-package-manager-should-you-use-in-2025-4212cb5e0a14)

### Tools
- [Poetry GitHub](https://github.com/python-poetry/poetry)
- [poetry-plugin-migrate](https://github.com/zyf722/poetry-plugin-migrate)
- [uv Documentation](https://docs.astral.sh/uv/)

## Related Methodologies

- [python-fastapi/](../python-fastapi/) - FastAPI project setup
- [django-coding-standards/](../django-coding-standards/) - Django with Poetry
- [python-modern-2026.md](../python-modern-2026.md) - Modern Python patterns

---

*Last updated: 2026-01*
