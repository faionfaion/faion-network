---
slug: arch-pattern-onion
tier: solo
group: dev
domain: software-architect
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Jeffrey Palermo (2008) formalised Onion Architecture: all coupling points toward the center.
content_id: "e78d0cea8f3a3248"
tags: [onion-architecture, domain-driven, layered-architecture, enterprise-patterns, dotnet]
---
# Onion Architecture

## Summary

**One-sentence:** Jeffrey Palermo (2008) formalised Onion Architecture: all coupling points toward the center.

**One-paragraph:** Jeffrey Palermo (2008) formalised Onion Architecture: all coupling points toward the center. The Domain Model (entities, value objects, repository interfaces) occupies the innermost ring with zero outward dependencies. Domain Services wrap cross-entity logic. Application Services orchestrate use cases. Infrastructure sits at the outermost ring.

## Applies If (ALL must hold)

- Enterprise .NET applications (C#, F#) where the Onion vocabulary is well established and tooling (Project References, .NET solution structure) maps naturally to layers.
- Applications where domain services as a separate layer is conceptually meaningful — e.g., a pricing engine that spans Product, Customer, and Promotion aggregates.
- Teams familiar with the Onion naming convention (Domain, Domain.Services, Application, Infrastructure) who want consistency across projects.
- Complex enterprise apps where the domain must be completely independent of UI, database, and framework choices.

## Skip If (ANY kills it)

- Simple domains without meaningful cross-entity business logic — the Domain.Services layer will be empty and adds confusion.
- Non-.NET stacks where teams are more familiar with Clean or Hexagonal vocabulary — use whichever fits the team's shared mental model.
- Prototypes or scripts — overhead of multiple projects/layers exceeds value.
- Microservices where the domain fits in 200 lines — the four-layer split is overhead.

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

- parent skill: `solo/dev/software-architect/`
