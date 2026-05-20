---
slug: nosql-redis-patterns
tier: pro
group: dev
domain: backend-systems
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Choose the right Redis data structure for each use case: strings for simple caching, hashes for object fields, lists for queues and stacks, sets for unique membership, sorted sets for leaderboards and rate limiting, pub/sub for real-time fan-out, and streams for durable event sourcing.
content_id: "e07c7f66e766616f"
tags: [redis, nosql, caching, rate-limiting, pub-sub]
---
# Redis Data Structure Patterns

## Summary

**One-sentence:** Choose the right Redis data structure for each use case: strings for simple caching, hashes for object fields, lists for queues and stacks, sets for unique membership, sorted sets for leaderboards and rate limiting, pub/sub for real-time fan-out, and streams for durable event sourcing.

**One-paragraph:** Choose the right Redis data structure for each use case: strings for simple caching, hashes for object fields, lists for queues and stacks, sets for unique membership, sorted sets for leaderboards and rate limiting, pub/sub for real-time fan-out, and streams for durable event sourcing. Always set EXPIRE or use key namespacing to prevent silent key leaks.

## Applies If (ALL must hold)

- High-speed caching layer in front of a slower database (sub-millisecond reads).
- Session storage with automatic TTL-based expiry.
- Real-time leaderboards, ranking, or scoring systems using Sorted Sets.
- Distributed rate limiting using sliding-window Sorted Sets or token-bucket Strings.
- Lightweight task queues (List LPUSH/BRPOP) where message durability is handled by the application.
- Real-time pub/sub notifications or fan-out messaging.
- Durable ordered event streams (Redis Streams with consumer groups).

## Skip If (ANY kills it)

- Durable primary data store — Redis persistence (RDB/AOF) is not a substitute for a proper database; use as a cache or secondary store only.
- Large binary objects (images, videos) — object storage (S3) is more appropriate; Redis memory is expensive.
- Complex relational queries — Redis has no query language; use PostgreSQL or MongoDB.
- Long-lived event streams requiring replay and strong ordering guarantees — Kafka provides durable, partitioned, replayable logs.

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
