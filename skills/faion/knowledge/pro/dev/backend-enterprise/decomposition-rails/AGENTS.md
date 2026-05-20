---
slug: decomposition-rails
tier: pro
group: dev
domain: backend-enterprise
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: LLM-friendly code organization for Rails 7+ using Service Objects, Query Objects, Serializers, and Policies.
content_id: "8e717464b9b610b4"
tags: [rails, ruby, decomposition, service-object, query-object]
---
# Rails Decomposition Patterns

## Summary

**One-sentence:** LLM-friendly code organization for Rails 7+ using Service Objects, Query Objects, Serializers, and Policies.

**One-paragraph:** LLM-friendly code organization for Rails 7+ using Service Objects, Query Objects, Serializers, and Policies. One Service = one verb; services return domain entities or Result monads — never void. File size budgets enforced by structural lint.

## Applies If (ALL must hold)

- Greenfield Rails 7+ app where LLM agents must work in small files (50–150 LOC) without fat models.
- Refactoring legacy Rails monoliths before safe agent edits are possible.
- Multi-developer or multi-agent teams with parallel work on User, Order, Billing domains.
- SDD-driven projects: one task = one Service Object.

## Skip If (ANY kills it)

- Tiny Rails apps (<20 controllers) — scope + thin controllers cover it; service-object ceremony costs more.
- Codebases on Trailblazer/Hanami/dry-rb — they have their own decomposition idioms; mixing produces incoherence.
- Rails Engines for shared internal libs — engine boundaries apply, not service objects.
- Hot paths (background jobs >1k/s) — service-object indirection adds GC pressure; use PORO or direct AR.
- Prototype phase where domain is unstable — locking shapes into service+form objects slows discovery.

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
