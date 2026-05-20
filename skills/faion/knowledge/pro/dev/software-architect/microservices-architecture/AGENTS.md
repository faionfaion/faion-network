---
slug: microservices-architecture
tier: pro
group: dev
domain: software-architect
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Decomposing applications into independently deployable services around business capabilities.
content_id: "4be8a99080e4b107"
tags: [microservices, architecture, service-decomposition, distributed-systems, ddd]
---
# Microservices Architecture

## Summary

**One-sentence:** Decomposing applications into independently deployable services around business capabilities.

**One-paragraph:** Decomposing applications into independently deployable services around business capabilities. Decision framework, decomposition strategies (DDD subdomains, volatility, Strangler Fig), communication patterns, database-per-service, and anti-patterns.

## Applies If (ALL must hold)

- Team size exceeds 30 developers with clear sub-team ownership per domain
- Domain boundaries are well-understood via DDD or business capability mapping
- Mature CI/CD, container orchestration, and observability are already in place
- Different services have genuinely different scaling profiles (catalogue vs checkout)
- Strangler Fig migration: extracting bounded contexts from an existing monolith

## Skip If (ANY kills it)

- Team smaller than 10 developers — operational overhead outweighs autonomy benefits
- MVP or early-stage product where domain boundaries are not yet understood
- Limited DevOps maturity — microservices require automation to be operational
- Simple CRUD application — a monolith or modular monolith is cheaper and faster
- Tight budget — microservices multiply infrastructure and observability costs

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

- parent skill: `pro/dev/software-architect/`
