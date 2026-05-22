---
slug: mq-idempotent-consumers
tier: pro
group: dev
domain: backend
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: At-least-once delivery means messages arrive more than once.
content_id: "63c67a73e06447d2"
tags: [idempotency, message-queues, deduplication, transactional-outbox, reliability]
---
# Idempotent Message Queue Consumers

## Summary

**One-sentence:** At-least-once delivery means messages arrive more than once.

**One-paragraph:** At-least-once delivery means messages arrive more than once. Idempotent consumers produce the same side-effect on every delivery of the same message. The pattern requires: an idempotency key on every message, a deduplication store (Redis or DB unique index), ack-after-commit ordering, and the transactional outbox pattern to prevent phantom events when a DB transaction rolls back.

## Applies If (ALL must hold)

- Any consumer that performs a side-effect (DB write, external API call, email send) under at-least-once delivery semantics.
- Consumers that receive retried messages from a DLQ replay.
- Saga orchestrators where the same step may be triggered by multiple events.
- Producers that must guarantee a message is published iff a DB transaction commits.

## Skip If (ANY kills it)

- Read-only consumers (analytics aggregation, logging) where duplicate processing produces no harmful side-effect — idempotency adds overhead without benefit.
- Exactly-once streams with full Kafka EOS and read_committed isolation where broker-level deduplication is already enforced — adding Redis dedup is redundant.

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
