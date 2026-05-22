---
slug: caching-write-patterns
tier: pro
group: dev
domain: backend
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Three patterns govern how data enters and exits the cache relative to the database.
content_id: "f9fff2b384e88dd7"
tags: [caching, redis, cache-aside, write-through, write-behind]
---
# Cache Write Patterns: Cache-Aside, Write-Through, Write-Behind

## Summary

**One-sentence:** Three patterns govern how data enters and exits the cache relative to the database.

**One-paragraph:** Three patterns govern how data enters and exits the cache relative to the database. Cache-aside (lazy load) is the default: check cache, miss, load DB, populate. Write-through keeps cache and DB in sync on every write at the cost of write latency. Write-behind accepts eventual DB consistency in exchange for high write throughput. Pick one per entity type based on consistency budget and write frequency.

## Applies If (ALL must hold)

- Cache-aside: read-to-write ratio ≥ 10:1, cache misses are acceptable, data can tolerate bounded staleness.
- Write-through: strong consistency required on reads after writes, write latency below 2× uncached is acceptable, entity update frequency is low-to-medium.
- Write-behind: high write throughput (counters, activity streams, metrics), eventual consistency is acceptable, crash-recovery queue is in place.
- Any entity where the access pattern is well understood and can be documented in a key-schema table before implementation.

## Skip If (ANY kills it)

- Cache-aside on financial balances or inventory counts — stale reads after concurrent writes cause correctness bugs.
- Write-through on high-cardinality entities updated at high frequency — every write adds a cache round-trip that compounds latency.
- Write-behind without a persistent flush queue — a crash between the cache write and the DB flush causes silent data loss.
- Any pattern without TTL + jitter — synchronized expiries cause synchronized stampedes on cold-start or after cache flush.

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
