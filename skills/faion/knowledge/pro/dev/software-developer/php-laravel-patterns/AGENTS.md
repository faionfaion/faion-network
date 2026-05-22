---
slug: php-laravel-patterns
tier: pro
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Layered Laravel architecture: thin HTTP controllers, service classes that own business logic and transactions, Eloquent models accessed through service methods, and API Resources for response shaping.
content_id: "5459de4344058100"
tags: [laravel, architecture, patterns, controller, service]
---
# Laravel Patterns (Controller → Service → Resource)

## Summary

**One-sentence:** Layered Laravel architecture: thin HTTP controllers, service classes that own business logic and transactions, Eloquent models accessed through service methods, and API Resources for response shaping.

**One-paragraph:** Layered Laravel architecture: thin HTTP controllers, service classes that own business logic and transactions, Eloquent models accessed through service methods, and API Resources for response shaping. Form Requests handle validation and authorization. No Eloquent calls in controllers; no request() helper in services; inject contracts, not facades.

## Applies If (ALL must hold)

- Greenfield Laravel 10/11/12 APIs that need Controller → Service → Resource layering.
- Brownfield refactors extracting business logic out of fat controllers.
- Generating CRUD slices (Controller + FormRequest + Resource + Service + Policy) for new resources.
- Cross-cutting hardening: FormRequests for validation, Resources for serialization, Services for transactions.
- Standardizing API versioning (Api\V1\) and Sanctum/Passport authentication at the controller boundary.

## Skip If (ANY kills it)

- Tiny apps (<10 routes) where Service + Resource is over-engineering — Eloquent inside controllers is acceptable.
- Projects standardized on lorisleiva/laravel-actions or Spatie LaravelData + DDD — check team standard first.
- Inertia / Livewire / Filament apps where the framework idiom (controller → component) is the boundary.
- Console-only artisan apps — the controller/FormRequest/Resource trio doesn't apply.

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

- parent skill: `pro/dev/software-developer/`
