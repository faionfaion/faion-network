---
slug: django-quality-security
tier: free
group: dev
domain: backend
version: 1.1.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: Produces a Django production security audit report (HTTPS/HSTS/CSP/cookies + rate limits + input validation + secrets + check --deploy verdict).
content_id: "0494620ea4cbfd07"
complexity: medium
produces: report
est_tokens: 3300
tags: [django, security, csp, rate-limiting, production]
---

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
| `templates/audit-report.md` | output skeleton matching `02-output-contract` |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-django-quality-security.py` | validates the audit report against the schema | after report is generated, before commit |

## Related

- [[django-quality-logging]] — Sentry + before_send PII scrubber
- [[django-serializers]] — input validation via DRF serializers
- [[django-quality-queries]] — `django.db.backends` log level discipline overlaps

## Decision tree

See `content/06-decision-tree.xml`. Routes from "is the service public?" through "are there auth endpoints?" and "is it behind a trusted reverse proxy?" to one of: full baseline rollout, baseline-minus-rate-limit, or skip-this-methodology (internal-only on VPN). The proxy check exists because django-axes / django-ratelimit lock out all users when X-Forwarded-For trust is misconfigured behind a load balancer.
