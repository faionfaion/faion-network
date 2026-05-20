---
slug: mq-reliability
tier: pro
group: dev
domain: backend-systems
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Reliable message queues require four complementary practices: publisher confirms so "published" means durably stored (not just buffered); DLQ with alerting so poison messages are isolated rather than lost silently; exponential backoff with jitter so retry storms do not DOS the broker; and backpressure via prefetch limits so slow consumers do not starve siblings or OOM the broker.
content_id: "28df9239b1429a98"
tags: [message-queues, reliability, dead-letter-queue, backpressure, schema-versioning]
---
# Message Queue Reliability

## Summary

**One-sentence:** Reliable message queues require four complementary practices: publisher confirms so "published" means durably stored (not just buffered); DLQ with alerting so poison messages are isolated rather than lost silently; exponential backoff with jitter so retry storms do not DOS the broker; and backpressure via prefetch limits so slow consumers do not starve siblings or OOM the broker.

**One-paragraph:** Reliable message queues require four complementary practices: publisher confirms so "published" means durably stored (not just buffered); DLQ with alerting so poison messages are isolated rather than lost silently; exponential backoff with jitter so retry storms do not DOS the broker; and backpressure via prefetch limits so slow consumers do not starve siblings or OOM the broker.

## Applies If (ALL must hold)

- Any queue that carries business-critical messages where loss means a lost order, payment, or user action.
- Any queue with a retry policy — applies backoff and jitter rules.
- Any queue that routes to a DLQ — applies alerting rules.
- Any schema that changes — applies versioning rules.

## Skip If (ANY kills it)

- Fire-and-forget logging pipelines where occasional message loss is acceptable — publisher confirms and DLQs add overhead without value.
- Ephemeral event streams for real-time dashboards where stale data is simply not displayed — at-most-once delivery is correct.

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
