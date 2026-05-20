---
slug: monolith-architecture
tier: solo
group: dev
domain: software-architect
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A monolith is a single deployable unit containing all application functionality.
content_id: "3d4134050d8db3c8"
tags: [monolith, architecture, vertical-slice, strangler-fig, scaling]
---
# Monolith Architecture

## Summary

**One-sentence:** A monolith is a single deployable unit containing all application functionality.

**One-paragraph:** A monolith is a single deployable unit containing all application functionality. It is the correct starting architecture for teams of fewer than 10, unvalidated business models, and domains whose boundaries are not yet understood. The "Monolith First" principle (Fowler) holds: start simple, add complexity only when scaling data proves you need it. Modern monoliths use vertical slice organization or modular structure — not the traditional layered anti-pattern that causes anemic domain models.

## Applies If (ALL must hold)

- Team size is fewer than 10 developers
- MVP or startup: speed to market matters more than scalability
- Domain boundaries are unclear or evolving
- Limited DevOps maturity: no Kubernetes/distributed systems expertise
- Budget constraints: single server, simpler infrastructure
- Rapid iteration phase where all code in one place accelerates changes
- Building the foundation for a future modular monolith or selective microservices extraction

## Skip If (ANY kills it)

- Independent per-feature scaling is already needed (measurably different traffic profiles)
- 10+ developers with independent release cadences causing merge conflicts and deploy bottlenecks
- Different modules have fundamentally different tech stack requirements
- Deployment frequency is already high and feature teams are blocking each other — switch to modular-monolith first
- Module build and test time exceeds 30 minutes — a sign the monolith has grown past the modular-monolith extraction threshold

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
