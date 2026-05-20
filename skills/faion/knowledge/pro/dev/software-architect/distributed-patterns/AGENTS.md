---
slug: distributed-patterns
tier: pro
group: dev
domain: software-architect
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Patterns for data consistency, fault tolerance, and coordination in distributed systems.
content_id: "75777129aedec2b9"
tags: [distributed-systems, patterns, fault-tolerance, consistency, microservices]
---
# Distributed Patterns

## Summary

**One-sentence:** Patterns for data consistency, fault tolerance, and coordination in distributed systems.

**One-paragraph:** Patterns for data consistency, fault tolerance, and coordination in distributed systems. Covers Saga (choreography vs orchestration), CQRS, Event Sourcing, Outbox, 2PC vs Saga vs TCC trade-offs, Circuit Breaker, Bulkhead, Retry with jitter, Idempotency, Leader Election, and Rate Limiting algorithms.

## Applies If (ALL must hold)

- Designing a multi-service transaction that spans more than one database
- Implementing event publishing that must survive process crashes (Outbox)
- Adding resilience to service-to-service calls (Circuit Breaker + Retry + Bulkhead)
- Separating read and write models for a high read/write ratio domain (CQRS)
- Needing full audit trail or temporal queries (Event Sourcing)

## Skip If (ANY kills it)

- Monolith or modular monolith — use local transactions instead; distributed patterns add complexity without benefit
- Simple CRUD service without external calls — Circuit Breaker/Bulkhead overhead is not justified
- Event Sourcing when the domain has no meaningful history requirement — storage cost is ~230% higher than snapshot-based
- 2PC for long-running processes — coordinator blocks resources; use Saga instead

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
