---
slug: django-quality-security
tier: free
group: dev
domain: backend
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Security is not optional in production Django.
content_id: "6c6d5c08d874ddcc"
tags: [django, security, csp, rate-limiting, production]
---
# Django Production Security Baseline

## Summary

**One-sentence:** Security is not optional in production Django.

**One-paragraph:** Security is not optional in production Django. HTTPS, HSTS, CSRF cookies, Content Security Policy, rate limiting on auth endpoints, input validation via forms/serializers, and python manage.py check --deploy are the minimum. Each setting prevents a specific attack class and must be enforced before launch.

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

- TBD — list concrete input artifacts and where they come from

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `TBD/path` | TBD — what upstream output this consumes |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules migrated from v1 methodology | ~800 |
| `content/02-output-contract.xml` | essential | Output schema (stub — fill from v1 patterns) | ~800 |
| `content/03-failure-modes.xml` | essential | Antipatterns migrated from v1 methodology | ~800 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| TBD | sonnet | TBD |

## Templates

| File | Purpose |
|------|---------|
| TBD | TBD |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| TBD | TBD | TBD |

## Related

- parent skill: `free/dev/python-developer/`
