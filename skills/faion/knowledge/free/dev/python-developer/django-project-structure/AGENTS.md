---
slug: django-project-structure
tier: free
group: dev
domain: backend
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Organize a Django project into domain apps under apps/, a shared core/ package, and a config/ package for settings.
content_id: "3aeb40f6f3b9089f"
tags: [django, project-structure, architecture, layout]
---
# Django Project Structure

## Summary

**One-sentence:** Organize a Django project into domain apps under apps/, a shared core/ package, and a config/ package for settings.

**One-paragraph:** Organize a Django project into domain apps under apps/, a shared core/ package, and a config/ package for settings. Each app is self-contained with models, services, selectors, apis, serializers, and tests. This layout scales predictably and aligns with the HackSoft Styleguide and Two Scoops of Django.

## Applies If (ALL must hold)

- Starting a new Django project that will grow beyond a few hundred lines.
- Building APIs with multiple business domains (users, orders, products, payments).
- Team projects where consistent file placement reduces cognitive overhead.
- Refactoring a legacy flat structure into a domain-based layout.

## Skip If (ANY kills it)

- Single-file Django scripts or management commands — full app structure is overkill.
- Django CMS / Wagtail where the framework imposes its own page-tree conventions.
- Tiny utility apps with one model and no business logic — just add to core/.

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
