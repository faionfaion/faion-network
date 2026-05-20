---
slug: caching-in-memory
tier: pro
group: dev
domain: backend-systems
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: In-memory (process-local) caching is the L1 layer in a multi-level cache stack: requests that hit L1 never leave the process, achieving sub-millisecond latency with zero network overhead.
content_id: "74a95ed6e0c6ca08"
tags: [caching, in-memory, lru-cache, ttlcache, cache-warming]
---
# In-Memory Application Cache: lru_cache, TTLCache, and Cache Warming

## Summary

**One-sentence:** In-memory (process-local) caching is the L1 layer in a multi-level cache stack: requests that hit L1 never leave the process, achieving sub-millisecond latency with zero network overhead.

**One-paragraph:** In-memory (process-local) caching is the L1 layer in a multi-level cache stack: requests that hit L1 never leave the process, achieving sub-millisecond latency with zero network overhead. Python's lru_cache is appropriate for deterministic pure functions with stable inputs; cachetools TTLCache adds TTL expiry and thread-safety; WarmableCache adds preload-on-startup for predictable hot keys. L1 is not a replacement for Redis — it cannot be shared across processes and does not survive restarts.

## Applies If (ALL must hold)

- Static or semi-static config loaded from DB at startup — warmable, never stale.
- Permission and role tables accessed on every authenticated request — high hit rate, infrequent updates, short TTL acceptable.
- Feature flags polled per request — low-cardinality keys, bounded staleness acceptable (30–300s).
- Expensive pure computations with stable inputs (hash functions, Markdown rendering, regex compilation) — lru_cache without TTL is correct when the input space is bounded.
- Hot product or article data in a read-heavy API serving one process per machine — L1 reduces Redis load by the L1 hit rate.

## Skip If (ANY kills it)

- User session data — must be shared across all processes; use Redis.
- Data requiring cross-process invalidation after writes — L1 has no shared invalidation signal without a Redis pub/sub or version-check mechanism.
- High-cardinality data (one key per user per request) — L1 cache fills with cold entries, evicting hot ones; hit rate collapses.
- Large values (>1MB per entry) — in-process caches constrained to <20% of total RAM; a few large values exhaust the maxsize budget.
- Multi-worker deployments where each worker serves different traffic — L1 caches are independent per worker and cannot be coordinated.

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
