---
slug: clean-architecture
tier: pro
group: dev
domain: software-developer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Clean Architecture separates concerns into concentric layers, with dependencies pointing inward.
content_id: "acc09df9033210e2"
tags: [clean-architecture, architecture, ddd, layered-architecture, dependency-inversion]
---
# Clean Architecture

## Summary

**One-sentence:** Clean Architecture separates concerns into concentric layers, with dependencies pointing inward.

**One-paragraph:** Clean Architecture separates concerns into concentric layers, with dependencies pointing inward. The core business logic remains independent of frameworks, databases, and delivery mechanisms. This methodology covers implementation patterns across different languages and frameworks.

## Applies If (ALL must hold)

- Complex business logic applications
- Long-lived enterprise systems
- Projects requiring high testability
- Applications that may change infrastructure
- Teams practicing Domain-Driven Design
- Long-lived enterprise codebases where infrastructure (DB, message bus, auth provider, payment processor) is expected to change at least once over the product lifetime
- Domains with non-trivial business rules — pricing engines, eligibility checks, regulatory calculations — that deserve to be tested without booting the framework
- Polyglot persistence: same domain logic must be servable from REST, GraphQL, gRPC, and a CLI without duplication
- Greenfield builds where the team has DDD literacy and is committed to dependency-inversion as a hard rule
- Existing Big Ball of Mud where you want a strangler-fig migration: extract a use case at a time into a clean core

## Skip If (ANY kills it)

- CRUD apps with thin business logic (form → table). Three layers of indirection over a User table is pure tax.
- Solo MVP / pre-PMF: the cost (entities + interfaces + use cases + DTOs + adapters) buys nothing while the domain is unstable
- Throwaway scripts, batch jobs, glue code. Use the framework directly.
- Teams without DDD/inversion experience — Clean Architecture without aggregate boundaries collapses into "DTOs all the way down" with extra mappers
- Tight latency budgets where every layer's mapping costs measurable µs (HFT, real-time bidding). Direct paths win.
- Frameworks designed against the dependency rule (Rails, Django) where fighting the framework costs more than it saves; modular monolith inside the framework is often the better answer

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
