---
slug: php-laravel-patterns
tier: pro
group: dev
domain: backend
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Clean-architecture layering for Laravel applications: thin Controller (route → service → Resource) → FormRequest (validation) → Service (business logic + DB::transaction) → Repository (optional, for real abstraction needs) → JsonResource (response shape).
content_id: "5459de4344058100"
tags: [laravel, architecture, patterns, clean-code]
---
# Laravel Patterns

## Summary

**One-sentence:** Clean-architecture layering for Laravel applications: thin Controller (route → service → Resource) → FormRequest (validation) → Service (business logic + DB::transaction) → Repository (optional, for real abstraction needs) → JsonResource (response shape).

**One-paragraph:** Clean-architecture layering for Laravel applications: thin Controller (route → service → Resource) → FormRequest (validation) → Service (business logic + DB::transaction) → Repository (optional, for real abstraction needs) → JsonResource (response shape). Each layer has one responsibility; controllers must not contain Eloquent queries or business logic.

## Applies If (ALL must hold)

- Greenfield Laravel 10/11/12 service that will grow beyond simple CRUD.
- Brownfield refactor where business logic leaks into controllers or models.
- API-first apps where JsonResource + ResourceCollection must stay stable across releases.

## Skip If (ANY kills it)

- Prototypes, admin tooling, or one-off scripts — abstraction tax is wasted; use Eloquent in controller.
- Domains requiring DDD aggregates and explicit bounded contexts — use Symfony + hexagonal layout.
- Essentially-CRUD apps already using Filament/Nova — extra service layer is dead weight.

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

- parent skill: `pro/dev/backend-enterprise/`
