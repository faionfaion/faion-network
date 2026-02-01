# Django Testing Reference

Comprehensive guide to testing Django applications with pytest-django, Factory Boy, model_bakery, and Django REST Framework.

## Overview

| Aspect | Recommendation |
|--------|----------------|
| Test Runner | pytest + pytest-django |
| Fixtures | Factory Boy (complex) or model_bakery (simple) |
| API Testing | DRF APIClient + APITestCase |
| Coverage | pytest-cov + coverage.py |
| CI/CD | GitHub Actions with coverage reports |

## When to Use This Reference

- Setting up pytest-django from scratch
- Writing model, service, and view tests
- Testing Django REST Framework APIs
- Configuring test factories (Factory Boy / model_bakery)
- Setting up coverage and CI/CD pipelines
- Handling database transactions in tests

## File Structure

| File | Purpose |
|------|---------|
| README.md | Overview and LLM usage tips |
| checklist.md | Step-by-step Django testing checklist |
| examples.md | Real-world test examples |
| templates.md | Copy-paste configurations |
| llm-prompts.md | Effective prompts for LLM-assisted testing |

## Core Concepts

### pytest-django vs Django TestCase

| Feature | pytest-django | Django TestCase |
|---------|---------------|-----------------|
| Syntax | Functions | Classes |
| Fixtures | pytest fixtures | setUp/tearDown |
| Assertions | Plain assert | self.assertEqual |
| Parametrization | Built-in | Requires subtest |
| Parallel | pytest-xdist | Limited |

**Recommendation:** Use pytest-django for new projects. Existing unittest-style tests work without modification.

### Factory Boy vs model_bakery

| Feature | Factory Boy | model_bakery |
|---------|-------------|--------------|
| Complexity | High control | Simple |
| Learning Curve | Steeper | Minimal |
| Declarations | Explicit | Auto-generate |
| ORMs | Django, SQLAlchemy, Mongo | Django only |
| Best For | Complex relationships | Quick prototyping |

**Rule of thumb:**
- model_bakery: Rapid prototyping, simple models
- Factory Boy: Production codebases, complex relationships, reusable factories

### Database Access Markers

```python
# Basic database access (transaction rollback)
@pytest.mark.django_db
def test_create_user():
    ...

# Transaction support (for testing transactions)
@pytest.mark.django_db(transaction=True)
def test_atomic_operation():
    ...

# Reset sequences (for testing auto-increment)
@pytest.mark.django_db(reset_sequences=True)
def test_with_fresh_ids():
    ...
```

### Test Organization

```
tests/
├── conftest.py           # Shared fixtures, factory registration
├── test_models.py        # Model unit tests
├── test_services.py      # Service layer tests
├── test_views.py         # View tests (function/class-based)
├── test_api.py           # DRF API tests
├── test_serializers.py   # Serializer tests
└── factories.py          # Factory Boy factories
```

## Quick Start

### 1. Install Dependencies

```bash
pip install pytest pytest-django pytest-cov factory-boy model-bakery faker
```

### 2. Configure pytest

```toml
# pyproject.toml
[tool.pytest.ini_options]
DJANGO_SETTINGS_MODULE = "config.settings.testing"
python_files = ["test_*.py", "*_test.py"]
addopts = "-v --tb=short --strict-markers"
markers = [
    "slow: marks tests as slow",
    "integration: marks integration tests",
]
```

### 3. Write Your First Test

```python
import pytest
from model_bakery import baker

@pytest.mark.django_db
def test_user_str():
    user = baker.make('users.User', email='test@example.com')
    assert str(user) == 'test@example.com'
```

## LLM Usage Tips

### Effective Context for LLMs

When asking an LLM to write Django tests, provide:

1. **Model definitions** - Full model code with fields and relationships
2. **Service/view code** - The actual code being tested
3. **Existing factories** - Factory patterns already in use
4. **Test configuration** - pytest.ini or pyproject.toml settings

### Prompt Patterns

```
"Write pytest tests for this Django service function: [paste code]
Use Factory Boy for fixtures. Include happy path and edge cases."

"Generate a Factory Boy factory for this model: [paste model]
Handle the ForeignKey relationships with SubFactory."

"Write DRF API tests for this ViewSet: [paste viewset]
Test authentication, permissions, and serialization."
```

### Common LLM Mistakes to Avoid

| Mistake | Correct Approach |
|---------|------------------|
| Missing `@pytest.mark.django_db` | Always add for DB tests |
| Using `Model.objects.create()` in fixtures | Use factories instead |
| Hardcoding IDs | Use factory-generated objects |
| Testing implementation details | Test behavior and outcomes |
| Mocking database operations | Use real DB with transaction rollback |

## Key Principles

### 1. Test Real Code

```python
# Bad: Over-mocking
@patch('apps.users.services.User.objects.filter')
def test_get_active_users(mock_filter):
    mock_filter.return_value = [Mock(is_active=True)]
    ...

# Good: Test real behavior
@pytest.mark.django_db
def test_get_active_users(user_factory):
    active = user_factory(is_active=True)
    inactive = user_factory(is_active=False)
    result = get_active_users()
    assert active in result
    assert inactive not in result
```

### 2. Explicit Assertions

```python
# Bad: Vague assertion
assert response.status_code == 200

# Good: Specific assertions
assert response.status_code == 200
assert response.data['email'] == user.email
assert 'password' not in response.data
```

### 3. Edge Cases

Always test:
- Empty inputs (`None`, `[]`, `''`)
- Invalid inputs (wrong types, negative numbers)
- Boundary conditions (max length, zero, one)
- Permission denied scenarios
- Not found scenarios

### 4. Test Isolation

```python
# Bad: Test depends on another test's data
def test_first():
    User.objects.create(email='test@example.com')

def test_second():
    user = User.objects.get(email='test@example.com')  # May fail

# Good: Each test creates its own data
@pytest.fixture
def user(db):
    return baker.make('users.User')

def test_with_user(user):
    assert user.is_active
```

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

- [pytest Documentation](https://docs.pytest.org/) - Core pytest guide
- [pytest-django](https://pytest-django.readthedocs.io/) - Django plugin for pytest
- [Factory Boy](https://factoryboy.readthedocs.io/) - Test fixtures replacement
- [model_bakery](https://model-bakery.readthedocs.io/) - Smart Django fixtures
- [Django Testing](https://docs.djangoproject.com/en/stable/topics/testing/) - Official Django testing guide
- [DRF Testing](https://www.django-rest-framework.org/api-guide/testing/) - REST framework testing

### Tutorials and Guides

- [Real Python - Django pytest Fixtures](https://realpython.com/django-pytest-fixtures/)
- [pytest-with-eric - Django REST API Testing](https://pytest-with-eric.com/pytest-advanced/pytest-django-restapi-testing/)
- [DjangoCon US - factory_boy: testing like a pro](https://2022.djangocon.us/talks/factory-boy-testing-like-a-pro/)

### Tools

- [pytest-cov](https://pytest-cov.readthedocs.io/) - Coverage plugin
- [pytest-xdist](https://pytest-xdist.readthedocs.io/) - Parallel test execution
- [pytest-randomly](https://github.com/pytest-dev/pytest-randomly) - Randomize test order
- [Faker](https://faker.readthedocs.io/) - Fake data generation

## Related Methodologies

- [django-pytest.md](../django-pytest.md) - pytest-django specific patterns
- [python-code-quality/](../python-code-quality/) - Code quality and linting
- [faion-testing-developer](../../faion-testing-developer/CLAUDE.md) - Testing strategies

---

*Last updated: 2026-01*
