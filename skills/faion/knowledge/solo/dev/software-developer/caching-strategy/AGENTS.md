---
slug: caching-strategy
tier: solo
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Multi-level caching (CDN to app in-memory to Redis/Valkey to DB) with explicit pattern selection (cache-aside, write-through, write-behind, SWR) and mandatory per-key TTL, invalidation trigger, and hit-rate monitoring.
content_id: "3f30675742851627"
tags: [caching, redis, performance, database, cdn]
---
# Caching Strategy

## Summary

**One-sentence:** Multi-level caching (CDN to app in-memory to Redis/Valkey to DB) with explicit pattern selection (cache-aside, write-through, write-behind, SWR) and mandatory per-key TTL, invalidation trigger, and hit-rate monitoring.

**One-paragraph:** Multi-level caching (CDN to app in-memory to Redis/Valkey to DB) with explicit pattern selection (cache-aside, write-through, write-behind, SWR) and mandatory per-key TTL, invalidation trigger, and hit-rate monitoring. Every cache layer requires a documented invalidation path and stampede protection for endpoints serving > 100 RPS.

## Applies If (ALL must hold)

- Read-heavy endpoints with bounded staleness tolerance (product catalog, user profile, settings).
- Expensive computations whose inputs repeat (LLM responses, image transforms, search aggregations).
- Static or near-static API responses behind a CDN or edge cache.
- Session storage, OAuth token cache, rate-limit counters — natural Redis fit.
- Aggregation/dashboard responses where 30-60 s freshness is acceptable.
- Reducing DB load when query plans are tuned but still slow under sustained traffic.
- Idempotency: cache request hashes to deduplicate retries.

## Skip If (ANY kills it)

- Highly volatile data (live counts, current bid prices) where any staleness is unacceptable.
- Per-user data with no reuse pattern (expected hit ratio less than 50% — wasted memory).
- Strong-consistency requirements (financial ledger, inventory hold).
- Small datasets that fit in app memory already (use a plain dict).
- Without a measurement plan — caching without hit-rate monitoring is dead weight.
- When cache invalidation logic is more complex than the underlying query.

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

- parent skill: `solo/dev/software-developer/`
