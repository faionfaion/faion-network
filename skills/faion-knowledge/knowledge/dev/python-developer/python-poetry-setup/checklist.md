# Poetry Setup Checklist

Step-by-step guide for setting up Poetry in Python projects.

---

## 1. Installation

### Install Poetry

```bash
# Official installer (recommended)
curl -sSL https://install.python-poetry.org | python3 -

# Or via pipx (isolated)
pipx install poetry

# Verify installation
poetry --version
```

### Configure Poetry

```bash
# Create venv in project directory (recommended)
poetry config virtualenvs.in-project true

# Show current config
poetry config --list
```

---

## 2. Project Initialization

### New Project

- [ ] Create project structure
  ```bash
  poetry new my-project
  cd my-project
  ```

### Existing Project

- [ ] Initialize Poetry in existing directory
  ```bash
  cd existing-project
  poetry init
  ```

### Migrate from Poetry 1.x to 2.x

- [ ] Install migration plugin
  ```bash
  poetry self add poetry-plugin-migrate
  ```

- [ ] Run migration (creates backup)
  ```bash
  poetry migrate
  ```

- [ ] Review changes in pyproject.toml

---

## 3. Configure pyproject.toml (Poetry 2.x)

### Project Metadata (PEP 621)

- [ ] Set project name and version
  ```toml
  [project]
  name = "my-project"
  version = "0.1.0"
  ```

- [ ] Set Python version
  ```toml
  requires-python = ">=3.11,<4.0"
  ```

- [ ] Add description and readme
  ```toml
  description = "Project description"
  readme = "README.md"
  ```

- [ ] Configure authors
  ```toml
  authors = [
      {name = "Your Name", email = "you@example.com"}
  ]
  ```

- [ ] Add license
  ```toml
  license = "MIT"
  ```

### Build System

- [ ] Configure build backend
  ```toml
  [build-system]
  requires = ["poetry-core>=2.0.0"]
  build-backend = "poetry.core.masonry.api"
  ```

### Package Mode

- [ ] Set package mode
  ```toml
  [tool.poetry]
  package-mode = true  # or false for non-package projects
  ```

---

## 4. Dependencies Setup

### Main Dependencies

- [ ] Add runtime dependencies
  ```bash
  poetry add fastapi uvicorn pydantic
  ```

- [ ] Add with extras
  ```bash
  poetry add "uvicorn[standard]"
  poetry add "sqlalchemy[asyncio]"
  ```

- [ ] Add with version constraints
  ```bash
  poetry add "fastapi>=0.100.0,<1.0.0"
  poetry add "pydantic@^2.0"
  ```

### Development Dependencies

- [ ] Create dev group
  ```bash
  poetry add -G dev pytest pytest-cov mypy ruff
  ```

### Testing Dependencies

- [ ] Create test group
  ```bash
  poetry add -G test pytest pytest-asyncio pytest-mock
  ```

### Documentation Dependencies (Optional)

- [ ] Create optional docs group
  ```toml
  # In pyproject.toml
  [tool.poetry.group.docs]
  optional = true

  [tool.poetry.group.docs.dependencies]
  mkdocs = "^1.6"
  mkdocs-material = "^9.5"
  ```

- [ ] Or via CLI
  ```bash
  poetry add -G docs mkdocs mkdocs-material
  ```

---

## 5. Virtual Environment

### Setup

- [ ] Install all dependencies
  ```bash
  poetry install
  ```

- [ ] Install with specific groups
  ```bash
  poetry install --with dev,test
  poetry install --without docs
  poetry install --only main
  ```

### Activate

- [ ] Activate shell
  ```bash
  poetry shell
  ```

- [ ] Or run commands directly
  ```bash
  poetry run python script.py
  poetry run pytest
  ```

### Verify

- [ ] Check environment info
  ```bash
  poetry env info
  poetry env info --path
  ```

---

## 6. Lock File Management

### Generate/Update Lock

- [ ] Create/update lock file
  ```bash
  poetry lock
  ```

- [ ] Preview changes without modifying
  ```bash
  poetry update --dry-run
  ```

### Commit Lock File

- [ ] Add poetry.lock to git
  ```bash
  git add poetry.lock
  git commit -m "chore: add poetry.lock"
  ```

### Export (for Docker/legacy)

- [ ] Export requirements.txt
  ```bash
  poetry export -f requirements.txt --output requirements.txt --without-hashes
  poetry export -f requirements.txt --output requirements-dev.txt --with dev --without-hashes
  ```

---

## 7. Tool Configuration

### Ruff (Linter)

- [ ] Add Ruff config
  ```toml
  [tool.ruff]
  line-length = 88
  target-version = "py311"

  [tool.ruff.lint]
  select = ["E", "F", "I", "N", "W", "UP", "B", "C4", "SIM"]
  ignore = ["E501"]
  ```

### MyPy (Type Checker)

- [ ] Add MyPy config
  ```toml
  [tool.mypy]
  python_version = "3.11"
  strict = true
  warn_return_any = true
  warn_unused_ignores = true
  ```

### Pytest

- [ ] Add pytest config
  ```toml
  [tool.pytest.ini_options]
  asyncio_mode = "auto"
  testpaths = ["tests"]
  addopts = "-v --tb=short --cov=src"
  ```

### Coverage

- [ ] Add coverage config
  ```toml
  [tool.coverage.run]
  source = ["src"]
  omit = ["tests/*"]

  [tool.coverage.report]
  exclude_lines = ["pragma: no cover", "if TYPE_CHECKING:"]
  ```

---

## 8. Scripts and Entry Points

### CLI Scripts

- [ ] Add CLI entry point
  ```toml
  [project.scripts]
  my-cli = "my_project.cli:main"
  ```

### Custom Commands

- [ ] Add in pyproject.toml (Poetry 2.x uses project.scripts)
  ```toml
  [project.scripts]
  serve = "my_project.main:serve"
  migrate = "my_project.db:migrate"
  ```

---

## 9. Publishing Setup

### Configure Package

- [ ] Set package includes
  ```toml
  [tool.poetry]
  packages = [{include = "my_project", from = "src"}]
  ```

- [ ] Add classifiers
  ```toml
  [project]
  classifiers = [
      "Development Status :: 4 - Beta",
      "Intended Audience :: Developers",
      "Programming Language :: Python :: 3.11",
      "Programming Language :: Python :: 3.12",
  ]
  ```

### Configure PyPI

- [ ] Set PyPI token
  ```bash
  poetry config pypi-token.pypi your-token-here
  ```

### Build and Publish

- [ ] Build package
  ```bash
  poetry build
  ```

- [ ] Publish to PyPI
  ```bash
  poetry publish
  ```

- [ ] Or publish to test PyPI first
  ```bash
  poetry config repositories.testpypi https://test.pypi.org/legacy/
  poetry publish -r testpypi
  ```

---

## 10. Version Management

### Bump Version

- [ ] Patch version (0.1.0 -> 0.1.1)
  ```bash
  poetry version patch
  ```

- [ ] Minor version (0.1.1 -> 0.2.0)
  ```bash
  poetry version minor
  ```

- [ ] Major version (0.2.0 -> 1.0.0)
  ```bash
  poetry version major
  ```

- [ ] Specific version
  ```bash
  poetry version 2.0.0
  ```

---

## 11. CI/CD Setup

### GitHub Actions

- [ ] Create workflow file
  ```yaml
  # .github/workflows/ci.yml
  name: CI

  on: [push, pull_request]

  jobs:
    test:
      runs-on: ubuntu-latest
      steps:
        - uses: actions/checkout@v4
        - uses: actions/setup-python@v5
          with:
            python-version: "3.12"
        - uses: snok/install-poetry@v1
          with:
            version: "2.0.1"
            virtualenvs-in-project: true
        - uses: actions/cache@v4
          with:
            path: .venv
            key: venv-${{ hashFiles('**/poetry.lock') }}
        - run: poetry install
        - run: poetry run pytest
  ```

### GitLab CI

- [ ] Create .gitlab-ci.yml
  ```yaml
  test:
    image: python:3.12
    before_script:
      - pip install poetry
      - poetry install
    script:
      - poetry run pytest
  ```

---

## 12. Docker Setup

### Multi-stage Dockerfile

- [ ] Create Dockerfile
  ```dockerfile
  FROM python:3.12-slim AS builder
  WORKDIR /app
  RUN pip install poetry==2.0.1
  COPY pyproject.toml poetry.lock ./
  RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

  FROM python:3.12-slim
  WORKDIR /app
  COPY --from=builder /app/requirements.txt .
  RUN pip install --no-cache-dir -r requirements.txt
  COPY src/ ./src/
  CMD ["python", "-m", "my_project.main"]
  ```

---

## 13. Verification

### Final Checks

- [ ] Verify lock file is committed
  ```bash
  git status | grep poetry.lock
  ```

- [ ] Check for outdated dependencies
  ```bash
  poetry show --outdated
  ```

- [ ] Validate pyproject.toml
  ```bash
  poetry check
  ```

- [ ] Test installation in clean environment
  ```bash
  poetry env remove --all
  poetry install
  poetry run pytest
  ```

---

## Quick Reference

| Task | Command |
|------|---------|
| Install deps | `poetry install` |
| Add dep | `poetry add package` |
| Add dev dep | `poetry add -G dev package` |
| Remove dep | `poetry remove package` |
| Update all | `poetry update` |
| Update one | `poetry update package` |
| Show tree | `poetry show --tree` |
| Export | `poetry export -f requirements.txt -o requirements.txt` |
| Build | `poetry build` |
| Publish | `poetry publish` |
| Version bump | `poetry version patch/minor/major` |

---

*Last updated: 2026-01*
