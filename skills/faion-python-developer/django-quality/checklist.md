# Django Quality Checklist

Step-by-step checklist for ensuring Django code quality across all dimensions.

## Pre-Development Setup

### Project Configuration

- [ ] **Ruff configured** in `pyproject.toml`
- [ ] **mypy configured** with django-stubs plugin
- [ ] **pre-commit hooks** installed and configured
- [ ] **Environment variables** managed via django-environ
- [ ] **Settings split** into base/development/production
- [ ] **.env.example** created with all required variables

### Security Baseline

- [ ] **SECRET_KEY** loaded from environment
- [ ] **DEBUG** controlled by environment variable
- [ ] **ALLOWED_HOSTS** properly configured
- [ ] **Database credentials** not hardcoded

## Code Quality Checklist

### Every Function/Method

- [ ] Type hints on all parameters and return values
- [ ] Docstring explaining purpose (Google style)
- [ ] Specific exception handling (no bare `except:`)
- [ ] Input validation for user-provided data
- [ ] Logging for important operations

### Every Model

- [ ] `__str__` method defined
- [ ] `class Meta` with ordering and verbose names
- [ ] Database indexes for frequently queried fields
- [ ] Constraints for data integrity (`CheckConstraint`, `UniqueConstraint`)
- [ ] `clean()` method for model-level validation

### Every View/Endpoint

- [ ] Permission checks (authentication, authorization)
- [ ] Input validation (serializers, forms)
- [ ] Query optimization (select_related, prefetch_related)
- [ ] Error handling with appropriate HTTP status codes
- [ ] Rate limiting for public endpoints

### Every QuerySet

- [ ] `select_related()` for ForeignKey/OneToOne access
- [ ] `prefetch_related()` for ManyToMany/reverse FK access
- [ ] `only()`/`defer()` for large text/binary fields
- [ ] Pagination for list endpoints
- [ ] Indexes for filter/order fields

## Pre-Commit Checklist

### Code Style

- [ ] Ruff lint passes (`ruff check .`)
- [ ] Ruff format passes (`ruff format .`)
- [ ] No unused imports
- [ ] No unused variables
- [ ] Imports sorted correctly

### Type Safety

- [ ] mypy passes (`mypy .`)
- [ ] No `# type: ignore` without explanation
- [ ] django-stubs types used correctly

### Testing

- [ ] Unit tests for new functions/methods
- [ ] Integration tests for endpoints
- [ ] Test coverage maintained (>80%)
- [ ] No failing tests (`pytest`)

### Migrations

- [ ] Migrations created for model changes
- [ ] Migration names are descriptive
- [ ] No data loss in migrations
- [ ] Backwards-compatible migrations (if needed)

## Security Checklist

### Authentication & Authorization

- [ ] Login required for protected views
- [ ] Object-level permissions checked
- [ ] Session timeout configured
- [ ] Password validation rules enforced

### Input Handling

- [ ] All user input validated
- [ ] SQL injection prevented (use ORM, not raw SQL)
- [ ] XSS prevented (templates auto-escape)
- [ ] CSRF protection enabled
- [ ] File uploads validated (type, size, content)

### Sensitive Data

- [ ] No secrets in code or version control
- [ ] Passwords hashed (Django handles this)
- [ ] PII encrypted or masked in logs
- [ ] API keys rotated regularly

### HTTP Security Headers

- [ ] HTTPS enforced (`SECURE_SSL_REDIRECT`)
- [ ] HSTS enabled (`SECURE_HSTS_SECONDS`)
- [ ] Content-Type sniffing prevented
- [ ] XSS filter enabled
- [ ] Frame options set to DENY

## Performance Checklist

### Database

- [ ] N+1 queries eliminated
- [ ] Indexes on frequently filtered fields
- [ ] Bulk operations for multiple creates/updates
- [ ] Connection pooling configured (production)
- [ ] Query count acceptable (check with Debug Toolbar)

### Caching

- [ ] Cache backend configured (Redis/Memcached)
- [ ] Expensive queries cached
- [ ] Template fragments cached
- [ ] Static file caching headers set
- [ ] Cache invalidation strategy defined

### Static Files

- [ ] WhiteNoise or CDN configured
- [ ] Static files compressed
- [ ] Images optimized
- [ ] Cache-busting hashes enabled

## Logging Checklist

### Configuration

- [ ] Logging configured in settings
- [ ] Different levels for dev/production
- [ ] Structured logging (JSON for production)
- [ ] Request ID tracking enabled

### Log Content

- [ ] All errors logged with context
- [ ] No sensitive data in logs (passwords, tokens)
- [ ] Performance metrics logged
- [ ] User actions audited (if required)

### Production Logging

- [ ] Logs shipped to central system
- [ ] Log rotation configured
- [ ] Alerts for critical errors
- [ ] Error tracking (Sentry) configured

## Deployment Checklist

### Pre-Deployment

- [ ] `python manage.py check --deploy` passes
- [ ] All tests pass
- [ ] Static files collected
- [ ] Migrations applied to staging

### Production Settings

```python
# Verify these are set correctly
DEBUG = False
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
```

### Post-Deployment

- [ ] Health check endpoint responds
- [ ] Error tracking receiving events
- [ ] Logs flowing to central system
- [ ] Monitoring alerts configured

## Code Review Checklist

### Functionality

- [ ] Code does what the ticket/issue describes
- [ ] Edge cases handled
- [ ] Error messages are user-friendly
- [ ] No debug code left in

### Code Quality

- [ ] Follows project conventions
- [ ] DRY (no code duplication)
- [ ] SOLID principles applied
- [ ] Clear naming (variables, functions, classes)

### Security

- [ ] No hardcoded secrets
- [ ] User input validated
- [ ] Authorization checked
- [ ] No SQL injection vectors

### Performance

- [ ] No N+1 queries
- [ ] Appropriate caching
- [ ] No blocking operations in request cycle
- [ ] Pagination for list views

### Testing

- [ ] Tests cover happy path
- [ ] Tests cover error cases
- [ ] Tests are deterministic (no flaky tests)
- [ ] Mocks used appropriately

## Periodic Review Checklist

### Monthly

- [ ] Dependencies updated (security patches)
- [ ] Django security advisories reviewed
- [ ] Unused code/features removed
- [ ] Test coverage reviewed

### Quarterly

- [ ] Performance audit (slow queries, bottlenecks)
- [ ] Security audit (check --deploy, dependency scan)
- [ ] Documentation updated
- [ ] Architecture review

### Before Major Releases

- [ ] Load testing completed
- [ ] Security penetration testing
- [ ] Rollback plan documented
- [ ] Monitoring thresholds reviewed

## Quick Reference Commands

```bash
# Code quality
ruff check .                    # Lint
ruff format .                   # Format
mypy .                          # Type check

# Testing
pytest                          # Run tests
pytest --cov                    # With coverage
pytest -x                       # Stop on first failure

# Django checks
python manage.py check          # Basic checks
python manage.py check --deploy # Deployment checks
python manage.py makemigrations --check  # Check for missing migrations

# Security
pip-audit                       # Check for vulnerable packages
safety check                    # Alternative vulnerability check
```
