---
slug: mq-patterns
tier: pro
group: dev
domain: backend
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Message queues enable asynchronous communication between services, providing decoupling, load leveling, and reliability.
content_id: "616ec34e0618654f"
tags: [message-queues, async, distributed-systems, event-driven, patterns]
---
# Message Queue Patterns

## Summary

**One-sentence:** Message queues enable asynchronous communication between services, providing decoupling, load leveling, and reliability.

**One-paragraph:** Message queues enable asynchronous communication between services, providing decoupling, load leveling, and reliability. Four foundational topologies cover the vast majority of use cases: point-to-point work queue, publish/subscribe fan-out, request/reply, and dead letter queue for failed messages.

## Applies If (ALL must hold)

- Decoupling services in distributed systems so failures isolate — the order service should not block when the email service is down.
- Async background jobs (image resize, ETL, ML inference) where users should not wait on the response path.
- Load leveling — absorb traffic spikes that the downstream cannot handle synchronously.
- Event-driven architectures with multiple consumers (audit, analytics, search index) per published event.
- Reliable hand-off across process or network boundaries with at-least-once or exactly-once delivery semantics.

## Skip If (ANY kills it)

- Request/response with low latency requirement under 50 ms end-to-end — synchronous gRPC or HTTP wins.
- Strong-consistency transactional flows that span multiple services — use SAGA or 2PC instead, but understand the trade-offs first.
- Adding queues just to scale without measuring backpressure or queue depth — adds operational burden with no benefit.
- Cache invalidation chains — use pub/sub on Redis directly.
- Pure fan-out logging — use a log shipper instead.
- Tiny apps that fit on one box — a goroutine with a channel or a Python queue.Queue is simpler and faster.

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
