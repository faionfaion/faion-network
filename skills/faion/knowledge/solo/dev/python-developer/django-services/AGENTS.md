---
slug: django-services
tier: solo
group: dev
domain: backend
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: The service layer pattern separates business logic from Django models, views, and serializers into dedicated functions with keyword-only arguments, typed signatures, and explicit transaction boundaries.
content_id: "67f1bcbec14acb19"
tags: [django, service-layer, python, architecture, testing]
---
# Django Services Layer

## Summary

**One-sentence:** The service layer pattern separates business logic from Django models, views, and serializers into dedicated functions with keyword-only arguments, typed signatures, and explicit transaction boundaries.

**One-paragraph:** The service layer pattern separates business logic from Django models, views, and serializers into dedicated functions with keyword-only arguments, typed signatures, and explicit transaction boundaries. Services own write operations (CREATE/UPDATE/DELETE and external API calls); selectors handle complex read queries. The canonical naming convention is entity_action (order_create, user_deactivate). Every service that performs two or more writes must use @transaction.atomic.

## Applies If (ALL must hold)

- Any CREATE/UPDATE/DELETE that touches two or more models or invokes an external API.
- Replacing fat-model methods that do email + payment + audit log in one blob.
- Wrapping side-effecting operations behind @transaction.atomic boundaries.
- Building a testable surface for business rules with no Django request/response in tests.
- Layering DRF: serializers validate input, views delegate to services, services own writes.

## Skip If (ANY kills it)

- Simple property calculations — use @property on the model.
- Pure querysets / chained filters — use a custom manager.
- Read-only, permission-aware fetches — use a selector, not a service.
- Trivial single-model CRUD where a direct ORM call is clearer.

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
