---
slug: arch-pattern-hexagonal
tier: solo
group: dev
domain: software-architect
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: The application core is isolated from the outside world through ports (interfaces) and adapters (implementations).
content_id: "9092f73e01f54887"
tags: [hexagonal-architecture, ports-and-adapters, dependency-inversion, adapter-pattern, testability]
---
# Hexagonal Architecture (Ports and Adapters)

## Summary

**One-sentence:** The application core is isolated from the outside world through ports (interfaces) and adapters (implementations).

**One-paragraph:** The application core is isolated from the outside world through ports (interfaces) and adapters (implementations). Primary adapters drive the core (REST, CLI, gRPC); secondary adapters are driven by the core (database, email, payment gateway). All external interactions follow the same symmetric contract.

## Applies If (ALL must hold)

- Multi-interface systems: REST API + CLI + gRPC + scheduled jobs + message-queue consumers all sharing the same core logic.
- Applications with several outbound dependencies (database, cache, email, payment gateway, third-party APIs) where each needs a testable seam.
- Projects requiring symmetric treatment of inputs and outputs via explicit port contracts.
- Systems where new input channels or output adapters are likely to be added frequently.

## Skip If (ANY kills it)

- CRUD-only admin tools — ports add interface overhead with no business logic to protect.
- Single-channel applications (REST only, simple domain) — Clean Architecture is sufficient and less verbose.
- Microservices that are already small enough that the entire domain fits in 200 lines.
- Prototypes — the boilerplate of ports + adapters + mappers is real; start simple and extract later.

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
