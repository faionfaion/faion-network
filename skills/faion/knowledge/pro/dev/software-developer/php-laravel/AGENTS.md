---
slug: php-laravel
tier: pro
group: dev
domain: software-developer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Production Laravel backend patterns: Controller → FormRequest → Service → Eloquent model → API Resource slice.
content_id: "2bb6a9d655536100"
tags: [laravel, php, backend, architecture, mvc]
---
# PHP Laravel Backend

## Summary

**One-sentence:** Production Laravel backend patterns: Controller → FormRequest → Service → Eloquent model → API Resource slice.

**One-paragraph:** Production Laravel backend patterns: Controller → FormRequest → Service → Eloquent model → API Resource slice. Controllers are thin HTTP adapters (10-30 lines). Business logic and DB::transaction live in service classes. Form Requests own validation and policy authorization. API Resources produce explicit field lists. No Request::all(), no Eloquent in controllers, no request() in services.

## Applies If (ALL must hold)

- Greenfield CRUD-heavy backends (SaaS, e-commerce, internal tools) with 1-5 person teams.
- API-first products pairing Sanctum/Passport for auth and Resource classes for serialization.
- Brownfield migration from raw PHP, WordPress, or CodeIgniter when shipping speed matters.
- Any project where convention-over-configuration can replace bespoke framework glue.

## Skip If (ANY kills it)

- Sub-millisecond hot paths (HFT, ad serving) — PHP request bootstrap (~30-80ms cold) is a floor.
- Heavy CPU/ML workloads — use Laravel as the front door, offload via queues.
- WebSocket-first apps with persistent connections — use Reverb only as a complement.
- Stateful long-lived processes (game servers, media transcoders) — wrong runtime model.
- Teams with zero PHP experience facing a hard deadline.

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
