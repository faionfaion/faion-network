---
slug: practices-django-coding
tier: solo
group: dev
domain: automation-tooling
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Consistent Django code across projects requires four conventions: module-level import aliases for cross-app references, services-as-functions (not classes) for DB mutations, thin views that delegate to services, and a BaseModel providing UUID + timestamps on every model.
content_id: "103fc04e12f46d38"
tags: [django, python, coding-standards, services, best-practices]
---
# Django Coding Standards

## Summary

**One-sentence:** Consistent Django code across projects requires four conventions: module-level import aliases for cross-app references, services-as-functions (not classes) for DB mutations, thin views that delegate to services, and a BaseModel providing UUID + timestamps on every model.

**One-paragraph:** Consistent Django code across projects requires four conventions: module-level import aliases for cross-app references, services-as-functions (not classes) for DB mutations, thin views that delegate to services, and a BaseModel providing UUID + timestamps on every model.

## Applies If (ALL must hold)

- Greenfield Django service scaffolding — use as the layout template.
- Refactor passes aligning an existing app to a known-good shape (thin views, services/).
- Cross-language onboarding where the agent must produce a Django service mirroring a Spring or Rails shape.
- Code review gate — any PR touching Django apps/views/services should be checked against these rules.

## Skip If (ANY kills it)

- Architecture decisions (microservices vs modular monolith) — see dev-methodologies-architecture.
- Testing patterns — see dev-methodologies-testing.
- Projects using Django Ninja instead of DRF where the view shape differs — agent will overwrite existing patterns.
- Performance tuning, caching, observability — out of scope.

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

- parent skill: `solo/dev/automation-tooling/`
