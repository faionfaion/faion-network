---
slug: decomposition-django
tier: solo
group: dev
domain: backend
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: The HackSoft services+selectors decomposition pattern for Django: business logic lives in `services/` (write operations, `@transaction.
content_id: "e8a1609ac5ce4098"
tags: [django, python, architecture, refactoring, services-pattern]
---
# Decomposition (Django)

## Summary

**One-sentence:** The HackSoft services+selectors decomposition pattern for Django: business logic lives in `services/` (write operations, `@transaction.

**One-paragraph:** The HackSoft services+selectors decomposition pattern for Django: business logic lives in `services/` (write operations, `@transaction.atomic`, keyword-only args), read queries in `selectors/` (return QuerySets, no mutations), models stay thin (ORM fields + validators, no business logic), views stay thin (parse → call service → serialize). Trigger decomposition when `models.py` exceeds 300 lines or `views.py` exceeds 200 lines. Execute one bounded context at a time with `pytest` green at every step.

## Applies If (ALL must hold)

- Django app where `models.py` exceeds ~300 lines or `views.py` exceeds ~200 lines
- Migrating a fat-model codebase to services + selectors layout
- Splitting a monolithic Django project by bounded context (DDD per-domain apps)
- Preparing a codebase for AI-assisted refactoring — small focused files improve reliability
- Onboarding a new team where views mix auth, queries, business logic, and serialization

## Skip If (ANY kills it)

- One-shot scripts, admin command tools, or proof-of-concept apps
- Apps with a single model and 5 or fewer endpoints — premature decomposition adds friction
- Codebases in maintenance-only mode where churn risk outweighs clarity gain
- Teams without test coverage to validate the refactor — break-and-freeze is the result

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

- parent skill: `solo/dev/python-developer/`
