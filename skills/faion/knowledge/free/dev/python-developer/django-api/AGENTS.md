---
slug: django-api
tier: free
group: dev
domain: backend
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Patterns for building REST APIs with Django REST Framework (DRF 3.
content_id: "49b08d0160fba49c"
tags: [django, rest-api, drf, django-ninja, jwt]
---
# Django API Development

## Summary

**One-sentence:** Patterns for building REST APIs with Django REST Framework (DRF 3.

**One-paragraph:** Patterns for building REST APIs with Django REST Framework (DRF 3.15+) or Django Ninja 1.x. Covers ViewSet vs APIView selection, serializer/schema design, JWT auth, throttling, pagination, filtering, and OpenAPI documentation. Core rule: keep views thin — validate input with serializers, delegate business logic to a service layer, return typed responses.

## Applies If (ALL must hold)

- Building new REST endpoints on an existing Django 5.x project.
- Choosing between DRF and Ninja at project bootstrap.
- Adding CRUD ViewSets or custom APIView actions to an existing DRF codebase.
- Implementing or hardening JWT/OAuth2/API-key auth, throttling, or cursor pagination.
- Generating OpenAPI specs for client SDKs via `drf-spectacular` or Ninja's built-in spec.

## Skip If (ANY kills it)

- Non-Django Python APIs — use `python-fastapi/` instead.
- Greenfield project with no Django code and no admin requirement — FastAPI is usually a better fit.
- Pure GraphQL APIs — use `graphene-django` / `strawberry-django`; this covers REST only.
- Internal RPC services — gRPC + protobuf; REST overhead is not justified.

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
