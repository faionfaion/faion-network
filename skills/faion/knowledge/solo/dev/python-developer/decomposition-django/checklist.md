# Django Decomposition Checklist

Step-by-step checklist for decomposing Django projects.

---

## Phase 1: Assessment

### Codebase Audit

- [ ] Run `python manage.py show_urls` to document all endpoints
- [ ] Run `python manage.py graph_models -a` to visualize model relationships
- [ ] Identify files > 200 lines (priority targets)
- [ ] List all circular imports (blocking issues)
- [ ] Document current test coverage per module

### Metrics to Collect

| Metric | Tool | Target |
|--------|------|--------|
| File line counts | `wc -l */**.py` | <200 lines |
| Cyclomatic complexity | `radon cc` | <10 per function |
| Import depth | Manual review | <3 levels |
| Test coverage | `pytest --cov` | >80% |

### Red Flags

- [ ] `models.py` contains business logic (not just ORM)
- [ ] `views.py` contains database queries
- [ ] Serializers perform mutations
- [ ] Signal handlers contain complex logic
- [ ] Admin methods contain business logic

---

## Phase 2: Planning

### Decomposition Order

1. **Extract shared utilities** first (`core/` or `common/` app)
2. **Split models** before services (services depend on models)
3. **Extract services** before views (views depend on services)
4. **Split views** last (most dependent on other layers)

### Dependency Mapping

- [ ] Map model relationships (ForeignKey, ManyToMany)
- [ ] Map signal connections
- [ ] Map Celery task dependencies
- [ ] Map permission class usage
- [ ] Map serializer inheritance

### Risk Assessment

| Change Type | Risk | Mitigation |
|-------------|------|------------|
| Model split | High | Keep same table, add `db_table` |
| Service extraction | Medium | Add facade for backward compat |
| View split | Low | URL routing stays same |
| Serializer split | Low | Import from new location |

---

## Phase 3: Models Decomposition

### Convert `models.py` to Package

- [ ] Create `models/` directory
- [ ] Create `models/__init__.py`
- [ ] Move each model to separate file
- [ ] Update `__init__.py` with imports
- [ ] Run migrations check (`makemigrations --check`)

### Example Structure

```
Before:
  app/models.py (500 lines, 5 models)

After:
  app/models/
  ├── __init__.py        # Re-exports all models
  ├── user.py            # User model (~80 lines)
  ├── profile.py         # Profile model (~60 lines)
  ├── settings.py        # UserSettings model (~50 lines)
  ├── mixins.py          # Shared model mixins (~40 lines)
  └── managers.py        # Custom managers (~60 lines)
```

### Model File Checklist

- [ ] One model per file (or closely related models)
- [ ] Model-specific managers in same file
- [ ] Model-specific validators in same file
- [ ] Properties that don't cause N+1 stay on model
- [ ] Properties that span relations move to selectors

---

## Phase 4: Services Decomposition

### Create Service Layer

- [ ] Create `services/` directory
- [ ] Create `services/__init__.py`
- [ ] Identify write operations in views
- [ ] Extract to service functions/classes
- [ ] Add transaction decorators

### Service Principles

| Principle | Implementation |
|-----------|----------------|
| Single responsibility | One domain per service file |
| Transaction boundaries | `@transaction.atomic` decorator |
| Input validation | Pydantic models or dataclasses |
| Error handling | Custom exceptions, not HTTP errors |
| No HTTP concepts | Services don't know about requests |

### Example Structure

```
services/
├── __init__.py
├── user_service.py       # User CRUD, registration
├── auth_service.py       # Login, logout, tokens
├── email_service.py      # Email sending
├── payment_service.py    # Payment processing
└── exceptions.py         # Service-specific exceptions
```

### Service Extraction Checklist

For each view with business logic:

- [ ] Identify the core operation (create, update, process)
- [ ] Extract to service function
- [ ] Define input dataclass/Pydantic model
- [ ] Add type hints
- [ ] Add docstring with example
- [ ] Write unit test for service
- [ ] Update view to call service

---

## Phase 5: Selectors Decomposition

### Create Selector Layer

- [ ] Create `selectors/` directory
- [ ] Create `selectors/__init__.py`
- [ ] Identify repeated query patterns
- [ ] Extract to selector functions

### Selector Principles

| Principle | Implementation |
|-----------|----------------|
| Read-only | No mutations, only queries |
| Return QuerySets | Enable further filtering |
| Eager loading | Include `select_related`, `prefetch_related` |
| No side effects | Pure functions |

### Example Structure

```
selectors/
├── __init__.py
├── user_selectors.py     # User queries
└── order_selectors.py    # Order queries
```

### Query Migration Checklist

- [ ] Find duplicate queries in views/services
- [ ] Create selector function with clear name
- [ ] Add proper `select_related` / `prefetch_related`
- [ ] Add type hints for return type
- [ ] Update all usages to call selector

---

## Phase 6: Views Decomposition

### Convert `views.py` to Package

- [ ] Create `views/` directory
- [ ] Create `views/__init__.py`
- [ ] Group by resource or action type
- [ ] Update URL patterns

### View Organization Patterns

**By Resource:**
```
views/
├── user_views.py         # /users/*
├── order_views.py        # /orders/*
└── product_views.py      # /products/*
```

**By Action Type:**
```
views/
├── crud_views.py         # Standard CRUD
├── action_views.py       # Custom actions
└── nested_views.py       # Nested resources
```

### View Thinning Checklist

For each view:

- [ ] Move business logic to service
- [ ] Move queries to selector
- [ ] Keep only: parse request, call service, format response
- [ ] Target: 10-20 lines per view method

---

## Phase 7: Serializers Decomposition

### Split Serializer Patterns

**By Direction:**
```
serializers/
├── user_input.py         # Create, Update serializers
├── user_output.py        # List, Detail serializers
└── user_nested.py        # Embedded serializers
```

**By Use Case:**
```
serializers/
├── user_public.py        # Public API responses
├── user_admin.py         # Admin API responses
└── user_internal.py      # Internal API responses
```

### Serializer Checklist

- [ ] No business logic in `create()` / `update()` - delegate to service
- [ ] No complex validation - delegate to service
- [ ] One serializer per use case (not one per model)
- [ ] Clear naming: `{Model}{Action}Serializer`

---

## Phase 8: Testing

### Test Organization

```
tests/
├── __init__.py
├── conftest.py           # Shared fixtures
├── factories.py          # Factory Boy factories
├── test_models.py        # Model tests
├── test_services.py      # Service tests (most important)
├── test_selectors.py     # Selector tests
├── test_views.py         # API tests
└── test_integration.py   # End-to-end tests
```

### Test Priority After Decomposition

1. **Services** - Core business logic (highest priority)
2. **Selectors** - Query correctness
3. **Views** - API contract
4. **Models** - Validation, properties

### Post-Decomposition Verification

- [ ] All tests pass
- [ ] Coverage maintained or improved
- [ ] No N+1 queries introduced (use `django-debug-toolbar`)
- [ ] No circular imports
- [ ] All imports resolve

---

## Phase 9: Documentation

### Update Project Documentation

- [ ] Update `CLAUDE.md` with new structure
- [ ] Add app-level `CLAUDE.md` files
- [ ] Update API documentation
- [ ] Document service contracts

### CLAUDE.md Template for Apps

```markdown
# {App Name}

## Structure

| Directory | Purpose |
|-----------|---------|
| models/ | Data models |
| services/ | Write operations |
| selectors/ | Read operations |
| views/ | API endpoints |
| serializers/ | Input/output |

## Key Services

- `user_service.create()` - Create new user
- `user_service.update()` - Update user
- `user_service.deactivate()` - Soft delete

## Key Selectors

- `get_active_users()` - All active users
- `get_user_by_email()` - Find by email
```

---

## Quick Reference

### Commands

```bash
# Audit
python manage.py show_urls
python manage.py graph_models -a -o models.png
radon cc . -a -s

# Testing
pytest --cov=apps --cov-report=html
pytest -x --ff  # Fast feedback

# Migrations
python manage.py makemigrations --check
python manage.py migrate --plan
```

### File Size Targets

| File Type | Target | Max | Action if exceeded |
|-----------|--------|-----|-------------------|
| Model | 80 | 150 | Split to models/ package |
| Service | 120 | 200 | Split by subdomain |
| Selector | 60 | 100 | Split by entity |
| View | 80 | 150 | Split by resource |
| Serializer | 80 | 120 | Split by use case |

---

## Related

- [README.md](README.md) - Overview and patterns
- [examples.md](examples.md) - Real-world examples
- [templates.md](templates.md) - Code templates
- [llm-prompts.md](llm-prompts.md) - LLM prompts for decomposition
