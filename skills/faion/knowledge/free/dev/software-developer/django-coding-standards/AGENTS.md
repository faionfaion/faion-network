---
slug: django-coding-standards
tier: free
group: dev
domain: software-developer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Structural and code conventions for Django projects establishing consistent directory layout (apps/ + core/ + config/settings/), aliased cross-app imports to prevent circular dependencies, service-layer architecture isolating business logic from HTTP concerns, keyword-only service arguments for clarity, TextChoices for model constants, and mandatory update_fields on.
content_id: "a477bf1edebbe194"
tags: [django, coding-standards, architecture, service-layer]
---
# Django Coding Standards

## Summary

**One-sentence:** Structural and code conventions for Django projects establishing consistent directory layout (apps/ + core/ + config/settings/), aliased cross-app imports to prevent circular dependencies, service-layer architecture isolating business logic from HTTP concerns, keyword-only service arguments for clarity, TextChoices for model constants, and mandatory update_fields on.

**One-paragraph:** Structural and code conventions for Django projects establishing consistent directory layout (apps/ + core/ + config/settings/), aliased cross-app imports to prevent circular dependencies, service-layer architecture isolating business logic from HTTP concerns, keyword-only service arguments for clarity, TextChoices for model constants, and mandatory update_fields on .save() calls to prevent full-row writes. These rules apply equally to new code and refactoring targets, ensuring the codebase is testable by default and reviewable without domain-specific knowledge.

## Applies If (ALL must hold)

- Bootstrapping a new Django app: wiring apps/, core/, config/settings/{base,development,production}.py
- Refactoring a Django repo where business logic is in views or model save()
- Code-review pass enforcing "fat services, thin views" on every PR
- Onboarding a multi-app project where circular imports are a risk
- Generating service scaffolds and unit tests from a feature spec

## Skip If (ANY kills it)

- Single-file Django scripts or management commands under ~10 lines
- Async-first stacks (FastAPI, Litestar) — service pattern needs async adaptation
- Greenfield prototypes where speed over structure is acceptable for day one
- Heavy DDD / hexagonal architecture — a richer pattern set is needed beyond this baseline

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

- parent skill: `free/dev/software-developer/`
