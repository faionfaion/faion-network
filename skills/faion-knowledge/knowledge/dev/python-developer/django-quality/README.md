# Django Code Quality

Comprehensive guide to Django code quality covering linting, formatting, security, performance optimization, logging, and system checks for production-grade applications.

## Overview

Django code quality encompasses multiple dimensions:

| Dimension | Focus Areas |
|-----------|-------------|
| **Code Style** | Formatting, linting, import organization |
| **Type Safety** | Type hints, mypy, django-stubs |
| **Security** | CSP, HTTPS, authentication, input validation |
| **Performance** | Query optimization, caching, N+1 prevention |
| **Observability** | Logging, monitoring, debugging |
| **Architecture** | Code organization, service layers, testing |

## Quick Navigation

| File | Purpose |
|------|---------|
| [checklist.md](checklist.md) | Step-by-step quality checklist |
| [examples.md](examples.md) | Real implementation examples |
| [templates.md](templates.md) | Copy-paste configurations |
| [llm-prompts.md](llm-prompts.md) | LLM-assisted quality prompts |

## Core Tools (2025-2026)

### Code Quality Stack

| Tool | Purpose | Replaces |
|------|---------|----------|
| **Ruff** | Linting + formatting | Flake8, Black, isort, pyupgrade |
| **mypy** | Static type checking | - |
| **django-stubs** | Django type hints | - |
| **pre-commit** | Git hook management | Manual checks |

### Security Stack

| Tool | Purpose |
|------|---------|
| **Django 6.0+ CSP** | Native Content Security Policy |
| **django-csp** | Advanced CSP (fine-grained control) |
| **django-axes** | Brute-force protection |
| **django-ratelimit** | Rate limiting |

### Performance Stack

| Tool | Purpose |
|------|---------|
| **Django Debug Toolbar** | Development profiling |
| **django-silk** | Request profiling |
| **Sentry** | Production error tracking |
| **select_related/prefetch_related** | N+1 query prevention |

### Logging Stack

| Tool | Purpose |
|------|---------|
| **structlog** | Structured logging |
| **django-structlog** | Django integration |
| **JSON formatters** | Machine-readable logs |

## Architecture Patterns

### Code Organization

```
myapp/
    models.py      # Data models (thin)
    services.py    # Business logic
    selectors.py   # Query logic (optional)
    views.py       # HTTP handling (thin)
    serializers.py # API serialization
    tasks.py       # Async tasks
    tests/
        test_models.py
        test_services.py
        test_views.py
```

### Service Layer Pattern

The "Simple Service Layer" approach (Hacksoft style):

```python
# services.py
def create_order(*, user: User, items: list[dict]) -> Order:
    """
    Business logic for order creation.
    Called from views, admin, Celery tasks, management commands.
    """
    validate_items(items)
    order = Order.objects.create(user=user)
    create_order_items(order=order, items=items)
    send_order_confirmation.delay(order_id=order.id)
    return order
```

**Key principle:** Keep the same pattern everywhere. Admin actions, Celery tasks, management commands, and views all call services.

## LLM Usage Tips

### When Generating Django Code

1. **Always request type hints** - Ask for fully typed function signatures
2. **Request query optimization** - Specify select_related/prefetch_related usage
3. **Ask for error handling** - Request specific exception types (not bare except)
4. **Include tests** - Ask for pytest fixtures and test cases
5. **Request security checks** - Ask about input validation and permissions

### Context to Provide

When asking LLMs to generate Django code, provide:

- Django version (5.x, 6.x)
- Python version (3.11+, 3.12+)
- Database (PostgreSQL, SQLite)
- API framework (DRF, Django Ninja)
- Whether you use service layer pattern

### Quality Signals to Request

```
Generate Django code with:
- Type hints (using django-stubs)
- Docstrings (Google style)
- Error handling (specific exceptions)
- Query optimization (select_related/prefetch_related where needed)
- Input validation
```

## Security Checklist (Production)

### Required Settings

```python
# Production security settings
DEBUG = False
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
```

### Verify with Django Check

```bash
python manage.py check --deploy
```

## Performance Quick Wins

### N+1 Query Prevention

```python
# Bad: N+1 queries
for order in Order.objects.all():
    print(order.user.email)  # Query per order

# Good: 1 query with JOIN
for order in Order.objects.select_related("user"):
    print(order.user.email)

# Good: 2 queries for M2M
for order in Order.objects.prefetch_related("items"):
    for item in order.items.all():
        print(item.name)
```

### When to Use Each

| Relationship | Method |
|--------------|--------|
| ForeignKey | `select_related()` |
| OneToOneField | `select_related()` |
| ManyToManyField | `prefetch_related()` |
| Reverse ForeignKey | `prefetch_related()` |

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

- [Django Security](https://docs.djangoproject.com/en/5.2/topics/security/)
- [Django Performance](https://docs.djangoproject.com/en/6.0/topics/performance/)
- [Django System Checks](https://docs.djangoproject.com/en/5.0/topics/checks/)
- [Django CSP (6.0+)](https://docs.djangoproject.com/en/dev/ref/csp/)

### Tools Documentation

- [Ruff Documentation](https://docs.astral.sh/ruff/)
- [django-stubs](https://github.com/typeddjango/django-stubs)
- [Django Debug Toolbar](https://django-debug-toolbar.readthedocs.io/)
- [django-structlog](https://django-structlog.readthedocs.io/)
- [django-environ](https://django-environ.readthedocs.io/)

### Security Resources

- [OWASP Django Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Django_Security_Cheat_Sheet.html)
- [django-csp](https://github.com/mozilla/django-csp)
- [django-axes](https://django-axes.readthedocs.io/)

### Architecture Guides

- [Hacksoft Django Styleguide](https://github.com/HackSoftware/Django-Styleguide)
- [Cosmic Python](https://www.cosmicpython.com/book/appendix_django.html)

### Monitoring

- [Sentry for Django](https://docs.sentry.io/platforms/python/integrations/django/)
- [Django Prometheus](https://github.com/korfuri/django-prometheus)

## Related Methodologies

- [django-coding-standards/](../django-coding-standards/) - Django coding conventions
- [django-testing/](../django-testing/) - Testing strategies
- [python-code-quality/](../python-code-quality/) - General Python quality
- [python-type-hints/](../python-type-hints/) - Type safety

## Version Compatibility

| Django | Python | Key Features |
|--------|--------|--------------|
| 6.0+ | 3.11+ | Native CSP, improved async |
| 5.2 LTS | 3.10+ | Long-term support until 2028 |
| 5.1 | 3.10+ | Field groups, LoginRequiredMiddleware |
| 4.2 LTS | 3.8+ | Support until April 2026 |
