---
slug: microservices-saga-pattern
tier: pro
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: The saga pattern manages distributed transactions across microservices as a sequence of local transactions, each publishing an event or message triggering the next step.
content_id: "7006ff7a8d1a6a60"
tags: [microservices, saga, distributed-transactions, compensation, eventual-consistency]
---
# Saga Pattern for Distributed Transactions

## Summary

**One-sentence:** The saga pattern manages distributed transactions across microservices as a sequence of local transactions, each publishing an event or message triggering the next step.

**One-paragraph:** The saga pattern manages distributed transactions across microservices as a sequence of local transactions, each publishing an event or message triggering the next step. On failure, compensation transactions undo previously completed steps in reverse order. Every step requires a paired compensation path — partial compensation is a data-integrity incident.

## Applies If (ALL must hold)

- Multi-step workflows that span more than one service and require all-or-nothing semantics (create order, reserve inventory, process payment).
- Long-running business processes where locking resources for the duration is impractical.
- When using Temporal, Cadence, or Camunda as an orchestration engine for complex workflows.
- Any distributed operation where partial completion must be observable, retryable, and compensatable.

## Skip If (ANY kills it)

- Single-service operations — use a local DB transaction instead.
- Operations where the business domain cannot define a meaningful compensation (e.g., sending an email — you cannot unsend it; use a separate notification step instead).
- Sub-millisecond latency requirements — saga orchestration adds at least one network round-trip per step.
- Simple two-service workflows with no compensation risk — a direct event and consumer is sufficient.

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
