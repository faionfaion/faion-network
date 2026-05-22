---
slug: decomposition-laravel
tier: pro
group: dev
domain: backend
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: LLM-friendly code organization for Laravel using the Action + DTO + Form Request + Resource + Policy pattern.
content_id: "a624613440b8680a"
tags: [laravel, php, decomposition, action-pattern, dto]
---
# Laravel Decomposition Patterns

## Summary

**One-sentence:** LLM-friendly code organization for Laravel using the Action + DTO + Form Request + Resource + Policy pattern.

**One-paragraph:** LLM-friendly code organization for Laravel using the Action + DTO + Form Request + Resource + Policy pattern. One Action = one verb; DTOs derive from Form Requests; controllers stay under 80 lines. Requires PHP 8.1+ for readonly constructor promotion. File size budgets (Controller ≤150, Action ≤100, DTO ≤40 lines) are enforced by the structural lint script.

## Applies If (ALL must hold)

- Greenfield Laravel project where LLM agents must extend the codebase without re-reading 500-line controllers.
- Refactoring legacy "fat controller / fat model" apps before letting agents touch them.
- Multi-developer or multi-agent parallel work where separate feature Actions avoid merge collisions.
- SDD-driven projects: one task = one Action class.

## Skip If (ANY kills it)

- Tiny CRUD admin tools (<20 endpoints) — Action/DTO ceremony costs more than the readability gain.
- Prototype phase where the domain is unstable — locking shapes into DTOs slows discovery.
- Teams without PHP 8.1+ — readonly constructor promotion is load-bearing for the DTO pattern.
- Codebases already using a consistent pattern (e.g., pure Service-class style) — mixing styles is worse than picking one.

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
