# Django Production Security Baseline

## Summary

**One-sentence:** Harden a production Django service by enforcing the HTTPS / HSTS / CSP / cookie security baseline, rate-limiting auth endpoints, validating every input, and blocking deploys on `manage.py check --deploy` warnings.

**One-paragraph:** Security is not optional for public Django. Set `DEBUG=False`, `SECURE_SSL_REDIRECT`, `SESSION_COOKIE_SECURE`, `CSRF_COOKIE_SECURE`, HSTS (ramped from 300 → 31536000), `X_FRAME_OPTIONS="DENY"`, Django 6.0+ native CSP (or django-csp), DRF throttles or django-ratelimit (never both), django-axes for account lockout behind a trusted proxy, form/serializer validation for every input, specific exception handling, and environment-loaded secrets with a system check guarding the SECRET_KEY default. Gate every deploy with `python manage.py check --deploy --fail-level WARNING`.

**Ефективно для:** pre-launch hardening of a new Django service; quarterly security audit; post-incident remediation; migrating an internal admin tool to public-facing.

## Applies If (ALL must hold)

- Security hardening before public launch of any Django application.
- Any Django project handling user authentication or sensitive data.
- Adding public-facing endpoints to an existing internal Django app.
- Post-incident security remediation (CSP violations, brute-force incidents).
- Quarterly security audit of production settings.

## Skip If (ANY kills it)

- Throwaway prototypes — full security stack costs more than the prototype is worth.
- Internal admin-only tools behind VPN — much of the security stack is external-facing; relax CSP and rate limiting for trusted networks.
- Pure data pipelines without HTTP — CSP and rate limiting do not apply.

## Prerequisites

| Artifact | Format | Source |
|----------|--------|--------|
| `config/settings/production.py` | Python module | repo |
| `MIDDLEWARE` list | Python list | settings |
| `SECRET_KEY`, `DATABASE_URL`, `SENTRY_DSN` | env vars | secret store |
| `urls.py` for the auth endpoints | Python | repo |
| Reverse-proxy config (nginx / cloudflare) | text | infra repo |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `django-quality-logging` | scrubbing PII from Sentry events depends on the logging methodology's `before_send` |
| `python-code-quality` | bare-except / print bans support rule r4 |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: HTTPS+HSTS+CSP, rate limits, input validation, exceptions, secrets | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema for the security audit report + valid/invalid examples | ~700 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns with symptom + root-cause + fix | ~700 |
| `content/04-procedure.xml` | medium | 6-step procedure: settings → middleware → rate → input → secrets → gate | ~500 |
| `content/05-examples.xml` | optional | worked example: HSTS rollout schedule + CSP staged migration | ~400 |
| `content/06-decision-tree.xml` | essential | route through "public?", "auth endpoints?", "behind proxy?" | ~300 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| Settings diff against baseline | sonnet | deterministic checklist application |
| CSP staged-migration plan | opus | judgement on inline script inventory |
| Rate-limit topology design | opus | per-endpoint per-user / per-IP tradeoffs |
| check --deploy parser | sonnet | parse stderr, categorise WARNING/ERROR |

## Templates

| File | Purpose |
|------|---------|
| `templates/production_settings.py` | drop-in security block for `settings/production.py` |
| `templates/system_checks.py` | system checks for SECRET_KEY default + missing Sentry DSN |
| `templates/audit-report.md.j2` | output skeleton matching `02-output-contract` |
| `templates/audit-report.md` | output skeleton matching `02-output-contract` Generated from `templates/audit-report.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-django-quality-security.py` | validates the audit report against the schema | after report is generated, before commit |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[django-quality-logging]] — Sentry + before_send PII scrubber
- [[django-serializers]] — input validation via DRF serializers
- [[django-quality-queries]] — `django.db.backends` log level discipline overlaps

## Decision tree

See `content/06-decision-tree.xml`. Routes from "is the service public?" through "are there auth endpoints?" and "is it behind a trusted reverse proxy?" to one of: full baseline rollout, baseline-minus-rate-limit, or skip-this-methodology (internal-only on VPN). The proxy check exists because django-axes / django-ratelimit lock out all users when X-Forwarded-For trust is misconfigured behind a load balancer.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/production_settings.py`

```python
from .base import *  # noqa: F401, F403

DEBUG = False

# Transport
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# Cookies
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Headers
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"

# HSTS — ramp 300 -> 3600 -> 31536000 across deploys; START AT 300
SECURE_HSTS_SECONDS = 300
SECURE_HSTS_INCLUDE_SUBDOMAINS = False
SECURE_HSTS_PRELOAD = False

# CSP (Django 6.0+ native). Start report-only; switch to enforce after telemetry clean.
MIDDLEWARE.insert(1, "django.middleware.csp.ContentSecurityPolicyMiddleware")  # noqa: F405
CONTENT_SECURITY_POLICY_REPORT_ONLY = {
    "default-src": ["'self'"],
    "script-src": ["'self'", "'nonce-<CSP_NONCE_SENTINEL>'"],
    "style-src": ["'self'", "'nonce-<CSP_NONCE_SENTINEL>'"],
    "img-src": ["'self'", "data:", "https:"],
    "font-src": ["'self'", "https://fonts.gstatic.com"],
    "connect-src": ["'self'"],
    "frame-ancestors": ["'none'"],
    "form-action": ["'self'"],
}

# Before deploy:
#   python manage.py check --deploy --fail-level WARNING --settings=config.settings.production
```

### `templates/system_checks.py`

```python
from django.conf import settings
from django.core.checks import Error, Tags, Warning, register


@register(Tags.security)
def check_secret_key_not_default(app_configs, **kwargs):
    errors = []
    key = settings.SECRET_KEY or ""
    if key.startswith("django-insecure-") or key == "django-insecure-change-me":
        errors.append(
            Error(
                "SECRET_KEY is the django-insecure default.",
                hint=(
                    "Generate via python -c 'from django.core.management.utils "
                    "import get_random_secret_key; print(get_random_secret_key())' "
                    "and load from env."
                ),
                id="security.E001",
            )
        )
    return errors


@register(Tags.security, deploy=True)
def check_sentry_dsn_present(app_configs, **kwargs):
    warnings = []
    if not getattr(settings, "SENTRY_DSN", None) and not settings.DEBUG:
        warnings.append(
            Warning(
                "SENTRY_DSN is not configured for production.",
                hint="Set SENTRY_DSN env var; load it in production.py.",
                id="monitoring.W001",
            )
        )
    return warnings


@register()
def check_cache_not_locmem_in_prod(app_configs, **kwargs):
    warnings = []
    if not settings.DEBUG:
        backend = settings.CACHES.get("default", {}).get("BACKEND", "")
        if "LocMemCache" in backend:
            warnings.append(
                Warning(
                    "Using LocMemCache in production.",
                    hint="Configure Redis/Memcached for production caching.",
                    id="caching.W001",
                )
            )
    return warnings
```
