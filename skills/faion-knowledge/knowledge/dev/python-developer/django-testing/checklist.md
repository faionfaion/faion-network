# Django Testing Checklist

Step-by-step checklist for setting up and maintaining Django tests.

## Project Setup Checklist

### 1. Install Dependencies

- [ ] Install pytest and pytest-django
  ```bash
  pip install pytest pytest-django
  ```

- [ ] Install coverage tools
  ```bash
  pip install pytest-cov coverage
  ```

- [ ] Install fixture libraries
  ```bash
  pip install factory-boy model-bakery faker
  ```

- [ ] Install parallel execution (optional)
  ```bash
  pip install pytest-xdist pytest-randomly
  ```

- [ ] Add to requirements
  ```
  # requirements/testing.txt
  pytest>=8.0
  pytest-django>=4.8
  pytest-cov>=4.1
  factory-boy>=3.3
  model-bakery>=1.18
  faker>=22.0
  coverage>=7.4
  pytest-xdist>=3.5  # optional
  pytest-randomly>=3.15  # optional
  ```

### 2. Configure pytest

- [ ] Create pyproject.toml config
  ```toml
  [tool.pytest.ini_options]
  DJANGO_SETTINGS_MODULE = "config.settings.testing"
  python_files = ["test_*.py", "*_test.py"]
  addopts = "-v --tb=short --strict-markers"
  markers = [
      "slow: marks tests as slow (deselect with '-m \"not slow\"')",
      "integration: marks tests as integration tests",
      "unit: marks tests as unit tests",
  ]
  ```

- [ ] Create testing settings file
  ```python
  # config/settings/testing.py
  from .base import *

  DEBUG = False
  DATABASES = {
      'default': {
          'ENGINE': 'django.db.backends.sqlite3',
          'NAME': ':memory:',
      }
  }
  PASSWORD_HASHERS = ['django.contrib.auth.hashers.MD5PasswordHasher']
  EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'
  ```

### 3. Configure Coverage

- [ ] Create .coveragerc or add to pyproject.toml
  ```toml
  # pyproject.toml
  [tool.coverage.run]
  source = ["."]
  omit = [
      "*/migrations/*",
      "*/tests/*",
      "*/__pycache__/*",
      "*/venv/*",
      "manage.py",
      "*/wsgi.py",
      "*/asgi.py",
      "*/settings/*",
  ]
  branch = true

  [tool.coverage.report]
  exclude_lines = [
      "pragma: no cover",
      "def __repr__",
      "raise AssertionError",
      "raise NotImplementedError",
      "if __name__ == .__main__.",
      "if TYPE_CHECKING:",
  ]
  show_missing = true
  skip_covered = true
  fail_under = 80
  ```

### 4. Create Test Directory Structure

- [ ] Create tests directory
  ```
  tests/
  ├── __init__.py
  ├── conftest.py
  ├── factories.py
  ├── test_models.py
  ├── test_services.py
  ├── test_views.py
  └── test_api.py
  ```

- [ ] Or use per-app tests
  ```
  apps/
  └── users/
      ├── models.py
      ├── services.py
      ├── views.py
      └── tests/
          ├── __init__.py
          ├── conftest.py
          ├── factories.py
          ├── test_models.py
          └── test_services.py
  ```

### 5. Setup conftest.py

- [ ] Create root conftest.py with common fixtures
  ```python
  # tests/conftest.py or conftest.py
  import pytest
  from pytest_factoryboy import register
  from tests.factories import UserFactory

  register(UserFactory)

  @pytest.fixture
  def api_client():
      from rest_framework.test import APIClient
      return APIClient()

  @pytest.fixture
  def authenticated_client(api_client, user):
      api_client.force_authenticate(user=user)
      return api_client
  ```

---

## Writing Tests Checklist

### Model Tests

- [ ] Test model creation
- [ ] Test `__str__` method
- [ ] Test custom model methods
- [ ] Test model properties
- [ ] Test model managers and querysets
- [ ] Test model constraints (unique, validators)
- [ ] Test model signals (if any)

### Service/Business Logic Tests

- [ ] Test happy path
- [ ] Test edge cases (None, empty, boundary)
- [ ] Test error handling
- [ ] Test permission checks
- [ ] Test database state changes
- [ ] Test return values

### View Tests

- [ ] Test GET requests (list, detail)
- [ ] Test POST requests (create)
- [ ] Test PUT/PATCH requests (update)
- [ ] Test DELETE requests
- [ ] Test authentication required
- [ ] Test permission denied
- [ ] Test not found (404)
- [ ] Test validation errors (400)
- [ ] Test redirect behavior

### API Tests (DRF)

- [ ] Test serialization (output format)
- [ ] Test deserialization (input validation)
- [ ] Test authentication (token, session)
- [ ] Test permissions (owner, admin)
- [ ] Test filtering and pagination
- [ ] Test nested serializers
- [ ] Test file uploads
- [ ] Test rate limiting (if applicable)

---

## Test Quality Checklist

### Before Committing

- [ ] All tests pass locally
  ```bash
  pytest
  ```

- [ ] Coverage meets threshold
  ```bash
  pytest --cov=. --cov-report=term-missing
  ```

- [ ] No skipped tests without reason
  ```bash
  pytest --strict-markers
  ```

- [ ] Tests run in any order
  ```bash
  pytest --randomly-seed=random
  ```

### Test Quality Criteria

- [ ] Test names describe behavior
  ```python
  # Good
  def test_user_cannot_delete_others_posts():

  # Bad
  def test_delete():
  ```

- [ ] Single assertion focus (or related assertions)
  ```python
  # Good: Related assertions
  assert response.status_code == 200
  assert response.data['email'] == user.email

  # Bad: Unrelated assertions
  assert response.status_code == 200
  assert User.objects.count() == 5  # Unrelated
  ```

- [ ] Tests are independent
  ```python
  # Each test creates its own data
  @pytest.fixture
  def user(db):
      return baker.make('users.User')
  ```

- [ ] No hardcoded IDs or magic numbers
  ```python
  # Good
  assert response.data['id'] == user.id

  # Bad
  assert response.data['id'] == 1
  ```

- [ ] Edge cases covered
  ```python
  @pytest.mark.parametrize('input_val,expected', [
      ('valid', True),
      ('', False),
      (None, False),
      ('  ', False),
  ])
  def test_validation(input_val, expected):
      assert validate(input_val) == expected
  ```

---

## CI/CD Checklist

### GitHub Actions Setup

- [ ] Create workflow file
  ```yaml
  # .github/workflows/tests.yml
  name: Tests
  on: [push, pull_request]
  jobs:
    test:
      runs-on: ubuntu-latest
      steps:
        - uses: actions/checkout@v4
        - uses: actions/setup-python@v5
          with:
            python-version: '3.12'
        - run: pip install -r requirements/testing.txt
        - run: pytest --cov --cov-report=xml
        - uses: codecov/codecov-action@v4
  ```

- [ ] Add coverage badge to README
- [ ] Configure branch protection rules
- [ ] Set minimum coverage threshold

### Pre-commit Hooks

- [ ] Add pytest to pre-commit (optional)
  ```yaml
  # .pre-commit-config.yaml
  repos:
    - repo: local
      hooks:
        - id: pytest
          name: pytest
          entry: pytest tests/ -x --tb=short
          language: system
          pass_filenames: false
          always_run: true
  ```

---

## Debugging Checklist

### When Tests Fail

- [ ] Read error message carefully
- [ ] Check if database marker is present (`@pytest.mark.django_db`)
- [ ] Check fixture availability
- [ ] Check for test isolation issues
- [ ] Run single test with verbose output
  ```bash
  pytest tests/test_models.py::test_user_creation -vvv
  ```

### Common Issues

| Issue | Solution |
|-------|----------|
| Database not available | Add `@pytest.mark.django_db` |
| Fixture not found | Check conftest.py scope |
| Tests pass alone, fail together | Test isolation issue |
| Slow tests | Use `--keepdb` flag |
| Random failures | Check for state leaks |

---

## Maintenance Checklist

### Weekly

- [ ] Review coverage report for gaps
- [ ] Clean up skipped tests
- [ ] Update deprecated assertions

### Monthly

- [ ] Review slow tests
- [ ] Update testing dependencies
- [ ] Refactor duplicate test code

### Quarterly

- [ ] Audit test quality
- [ ] Review factory patterns
- [ ] Update testing documentation

---

## Quick Commands

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific file
pytest tests/test_models.py

# Run specific test
pytest tests/test_models.py::test_user_creation

# Run with keyword
pytest -k "user"

# Run excluding slow
pytest -m "not slow"

# Run in parallel
pytest -n auto

# Run with fresh database
pytest --create-db

# Keep database between runs
pytest --reuse-db

# Verbose output
pytest -vvv

# Stop on first failure
pytest -x

# Show local variables on failure
pytest --showlocals
```

---

*See also: [examples.md](examples.md) for test examples, [templates.md](templates.md) for configurations*
