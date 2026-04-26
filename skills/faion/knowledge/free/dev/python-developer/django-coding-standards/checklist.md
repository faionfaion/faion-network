# Django Code Review Checklist

> Use this checklist for PR reviews and self-checks before committing.

---

## Quick Reference

| Priority | Category | Critical Items |
|----------|----------|----------------|
| P0 | Security | No secrets, SQL injection, XSS prevention |
| P0 | Data | Transactions for multi-model writes |
| P1 | Architecture | Business logic in services, not views |
| P1 | Performance | N+1 queries addressed |
| P2 | Quality | Type hints, docstrings, tests |

---

## Architecture

### Service Layer

- [ ] Business logic is in services, not views/serializers
- [ ] Services handle all write operations
- [ ] Selectors handle all complex read operations
- [ ] Services use `transaction.atomic()` for multi-model writes
- [ ] Services call `full_clean()` before `save()` for validation
- [ ] Services raise domain exceptions, not HTTP exceptions
- [ ] No ORM calls in views (use services/selectors)

### Views/APIs

- [ ] Views are thin (10-20 lines max)
- [ ] Views only handle: validate, call service, serialize response
- [ ] Proper HTTP status codes used
- [ ] Authentication and permissions checked
- [ ] No business logic in views
- [ ] No direct model queries in views

### Models

- [ ] BaseModel inherited (created_at, updated_at)
- [ ] `clean()` method for multi-field validation
- [ ] `CheckConstraint` for DB-level rules
- [ ] `verbose_name` and `verbose_name_plural` set
- [ ] Proper `Meta.ordering` defined
- [ ] Indexes on frequently queried fields
- [ ] No business logic in `save()` method

---

## Code Quality

### Imports

- [ ] Imports organized (stdlib, third-party, django, local)
- [ ] Cross-app imports use aliases (`from apps.users import models as user_models`)
- [ ] No circular imports
- [ ] No wildcard imports (`from x import *`)
- [ ] `TYPE_CHECKING` used for type-only imports
- [ ] Relative imports for same-app modules

### Type Hints

- [ ] All function parameters typed
- [ ] All return types annotated
- [ ] `| None` used instead of `Optional`
- [ ] Generic types properly annotated (`list[str]`, `dict[str, int]`)
- [ ] `QuerySet[Model]` for queryset returns

### Naming

- [ ] Service functions: `<entity>_<action>` (e.g., `user_create`)
- [ ] Selector functions: `<entity>_<query>` (e.g., `user_list`)
- [ ] Constants: `UPPER_SNAKE_CASE`
- [ ] Model classes: `PascalCase`, singular
- [ ] App names: `snake_case`, plural

### Documentation

- [ ] Public functions have docstrings
- [ ] Docstrings include Args, Returns, Raises
- [ ] Complex logic has inline comments
- [ ] Non-obvious decisions explained

---

## Performance

### Database

- [ ] N+1 queries prevented (`select_related`, `prefetch_related`)
- [ ] Bulk operations used where applicable (`bulk_create`, `bulk_update`)
- [ ] `only()` / `defer()` for partial field loading
- [ ] `exists()` instead of `count() > 0`
- [ ] `update_fields` specified in `save()`
- [ ] Proper indexes on model fields
- [ ] No queries in loops

### Caching

- [ ] Expensive queries cached when appropriate
- [ ] Cache keys include relevant parameters
- [ ] Cache invalidation on data changes
- [ ] `@cached_property` for computed model attributes

---

## Security

### Data Protection

- [ ] No secrets in code (use environment variables)
- [ ] No `.env` files committed
- [ ] Sensitive fields excluded from serializers
- [ ] User input validated and sanitized
- [ ] SQL injection prevented (no raw SQL with user input)

### Authentication & Authorization

- [ ] Views have proper permission classes
- [ ] Object-level permissions checked
- [ ] Ownership verified before modifications
- [ ] Rate limiting on sensitive endpoints
- [ ] CSRF protection enabled

### Django Security

- [ ] `DEBUG = False` in production
- [ ] `SECRET_KEY` from environment
- [ ] `ALLOWED_HOSTS` configured
- [ ] CSP headers configured (Django 6.0)
- [ ] Secure cookies enabled

---

## Testing

### Coverage

- [ ] Services have unit tests
- [ ] Selectors have unit tests (including N+1 checks)
- [ ] APIs have integration tests
- [ ] Edge cases covered
- [ ] Error paths tested

### Test Quality

- [ ] Factory Boy used for test data
- [ ] Tests are isolated (no shared state)
- [ ] Descriptive test names
- [ ] One assertion per test (when reasonable)
- [ ] pytest fixtures for common setup

### API Tests

- [ ] Success cases (200, 201)
- [ ] Validation errors (400)
- [ ] Authentication errors (401)
- [ ] Authorization errors (403)
- [ ] Not found errors (404)

---

## Serializers

### Input Serializers

- [ ] All fields have explicit validators
- [ ] `required`, `allow_blank`, `allow_null` set appropriately
- [ ] Custom validation in `validate_<field>` or `validate()`
- [ ] No business logic (only validation)

### Output Serializers

- [ ] Only necessary fields exposed
- [ ] Sensitive fields excluded
- [ ] Nested serializers for related objects
- [ ] `SerializerMethodField` for computed values
- [ ] Proper `source` attribute usage

---

## Error Handling

- [ ] Specific exceptions caught (not bare `except`)
- [ ] Custom exceptions for business errors
- [ ] Proper error messages returned
- [ ] Errors logged appropriately
- [ ] No sensitive data in error messages

---

## Django 6.0 Specific

- [ ] Native `@task` decorator for background tasks
- [ ] Template partials used for reusable fragments
- [ ] CSP configured in production settings
- [ ] `AsyncPaginator` for async views
- [ ] Python 3.12+ features used appropriately

---

## Constants

- [ ] `TextChoices` for string enums
- [ ] `IntegerChoices` for integer enums
- [ ] Limits in `constants.py` (not magic numbers)
- [ ] Constants documented with comments

---

## Git & PR

- [ ] Commit message follows convention
- [ ] No commented-out code
- [ ] No debug prints or breakpoints
- [ ] No TODO without issue reference
- [ ] Migrations reviewed
- [ ] No conflicting migrations

---

## Quick Checks (Copy-Paste)

```markdown
## PR Review Checklist

### Architecture
- [ ] Services for writes, selectors for reads
- [ ] Thin views (validate -> service -> response)
- [ ] No business logic in views/serializers

### Quality
- [ ] Type hints on all functions
- [ ] Cross-app imports use aliases
- [ ] Tests for new functionality

### Performance
- [ ] N+1 queries addressed (select/prefetch_related)
- [ ] update_fields specified in save()

### Security
- [ ] Permissions checked
- [ ] No secrets in code
```
