---
slug: go-channels
tier: pro
group: dev
domain: backend-systems
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Channels are Go's primary mechanism for communication between goroutines.
content_id: "f799e5de6fa2d005"
tags: [go, concurrency, channels, pipelines, goroutines]
---
# Go Channels and Pipeline Patterns

## Summary

**One-sentence:** Channels are Go's primary mechanism for communication between goroutines.

**One-paragraph:** Channels are Go's primary mechanism for communication between goroutines. Use channels to build data pipelines, coordinate multiple goroutines, distribute work to parallel workers, merge results, and manage event-driven systems. Always use context for cancellation, close channels from the sender side, and test with race detector to prevent deadlocks and data races.

## Applies If (ALL must hold)

- Data pipeline processing where output of one stage feeds input of the next.
- Event-driven systems where goroutines react to events from multiple sources.
- Coordinating multiple goroutines without shared memory mutation.
- Building producer-consumer patterns and pub-sub systems.
- Multiplexing I/O sources (network, timers, done signals) in a single goroutine.

## Skip If (ANY kills it)

- Shared mutable state with random access. Use sync.Mutex or sync.Map instead; channels are not a database.
- Single-producer/single-consumer with predictable order. A slice plus for loop is simpler and faster.
- Cross-process communication. Use a real queue (Kafka/RabbitMQ/NATS); channels die with the process.
- Replacing function calls with goroutines plus channels just to feel async. You add scheduling cost, lose stack traces, and gain race-condition risk.

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

- parent skill: `pro/dev/backend-systems/`
