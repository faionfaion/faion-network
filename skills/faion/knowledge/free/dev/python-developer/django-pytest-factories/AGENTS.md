---
slug: django-pytest-factories
tier: free
group: dev
domain: backend
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: pytest-factoryboy bridges Factory Boy DjangoModelFactory classes with pytest fixtures, eliminating manual test data creation.
content_id: "1f3ebce629bfeaf1"
tags: [django, pytest, factory-boy, testing, fixtures]
---
# Django pytest Factories

## Summary

**One-sentence:** pytest-factoryboy bridges Factory Boy DjangoModelFactory classes with pytest fixtures, eliminating manual test data creation.

**One-paragraph:** pytest-factoryboy bridges Factory Boy DjangoModelFactory classes with pytest fixtures, eliminating manual test data creation. Define factories in tests/factories/, use SubFactory for FK relationships, Faker for realistic data, and register in conftest.py to auto-create singular and batch fixtures.

## Applies If (ALL must hold)

- Creating test data for Django models in any pytest test.
- Tests that need consistent, realistic data without hard-coding values.
- Setting up related-object graphs (User → Profile → Order → OrderItem).
- Batch-creating multiple instances for list/filter tests.
- Replacing manual User.objects.create() calls in test setUp or fixtures.

## Skip If (ANY kills it)

- Simple, one-off tests where a factory adds more complexity than value.
- Tests that specifically assert on hard-coded values — pass the values explicitly to the factory instead of using Faker defaults.
- Performance benchmarks where factory overhead matters — use bulk_create directly.

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
