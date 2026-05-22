---
slug: laravel-patterns
tier: pro
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Laravel 11 architecture patterns: thin controller → FormRequest validation → Action/Service → Eloquent model → API Resource.
content_id: "60f0275ee9b5a7f5"
tags: [laravel, php, eloquent, api, architecture]
---
# Laravel Patterns

## Summary

**One-sentence:** Laravel 11 architecture patterns: thin controller → FormRequest validation → Action/Service → Eloquent model → API Resource.

**One-paragraph:** Laravel 11 architecture patterns: thin controller → FormRequest validation → Action/Service → Eloquent model → API Resource. Enforces $fillable discipline, enum casts, DB transactions, eager loading, typed queues with idempotency, and Policy-based authorization.

## Applies If (ALL must hold)

- Scaffolding a new Laravel 11 app or extending one with models, migrations, FormRequests, Resources
- Generating service/action/DTO classes around Eloquent models
- Authoring API resources with consistent envelopes (JsonResource, ResourceCollection)
- Reviewing PRs for N+1, fat controllers, missing FormRequests, mass-assignment vulnerabilities
- Adding queues (Horizon, Redis, SQS) and event/listener wiring
- Auth flows: Sanctum (SPA), Passport (OAuth2), policies, gates, RBAC

## Skip If (ANY kills it)

- Hot paths needing sub-millisecond latency — PHP-FPM round trip dominates
- Heavy data engineering or streaming workloads — use a JVM/Go pipeline
- Real-time bidirectional protocols beyond Reverb/Echo scope
- Greenfield where the team has no PHP experience

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
