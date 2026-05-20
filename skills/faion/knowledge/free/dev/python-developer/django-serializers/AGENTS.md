---
slug: django-serializers
tier: free
group: dev
domain: python-developer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Use separate Input serializers (for request data validation) and Output serializers (for response formatting).
content_id: "4e7347bcf3c20124"
tags: [django, serializers, drf, api]
---
# Django DRF Serializer Conventions

## Summary

**One-sentence:** Use separate Input serializers (for request data validation) and Output serializers (for response formatting).

**One-paragraph:** Use separate Input serializers (for request data validation) and Output serializers (for response formatting). Never put business logic in serializers. Declare all fields explicitly — avoid ModelSerializer's automatic field discovery. Nested serializers rely on selectors to provide pre-fetched data, never trigger their own queries.

## Applies If (ALL must hold)

- Any Django REST Framework API endpoint that accepts input data.
- Any API endpoint that returns model data as JSON.
- Views that need to validate request payload before passing to a service.
- Endpoints with nested related data that must be serialized efficiently.

## Skip If (ANY kills it)

- Internal utility functions that manipulate data in Python — no HTTP boundary, no serializer needed.
- Admin-only views using Django admin's built-in forms — ModelAdmin handles that.
- Django Ninja projects — use Pydantic schemas instead of DRF serializers.

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
