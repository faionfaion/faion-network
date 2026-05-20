---
slug: clean-architecture
tier: pro
group: dev
domain: code-quality
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Clean Architecture: four concentric layers with inward-only dependencies.
content_id: "acc09df9033210e2"
tags: [architecture, layering, clean-code, ddd, testing]
---
# Clean Architecture

## Summary

**One-sentence:** Clean Architecture: four concentric layers with inward-only dependencies.

**One-paragraph:** Clean Architecture: four concentric layers with inward-only dependencies. Domain layer has no framework imports. Dependencies point inward; frameworks point outward.

## Applies If (ALL must hold)

- Complex business logic that must survive infrastructure changes (DB migration, framework upgrade)
- Long-lived enterprise system where testability and onboarding speed justify the layer overhead
- Domain-Driven Design projects — Clean Architecture layers map directly to DDD layers
- Applications that may need to run in multiple delivery mechanisms (REST API + CLI + event handler)
- Teams that need to enforce layer boundaries via architecture tests (import-linter, ArchUnit)

## Skip If (ANY kills it)

- CRUD apps with trivial logic — four layers for a GET /users endpoint is over-engineering
- Rapid prototypes where the goal is feature exploration, not stability
- Teams not willing to enforce the dependency rule via tests — without enforcement it degrades into a layered monolith with import cycles
- Small scripts or ETL jobs where a single file is appropriate

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

- parent skill: `pro/dev/code-quality/`
