---
slug: caching-stampede-prevention
tier: pro
group: dev
domain: backend
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A cache stampede (thundering herd) occurs when a popular cache key expires and multiple concurrent requests simultaneously attempt to reload it from the origin.
content_id: "351f6daf65faa799"
tags: [caching, redis, stampede, distributed-lock, thundering-herd]
---
# Cache Stampede Prevention: Distributed Lock, Probabilistic Refresh, Coalescing

## Summary

**One-sentence:** A cache stampede (thundering herd) occurs when a popular cache key expires and multiple concurrent requests simultaneously attempt to reload it from the origin.

**One-paragraph:** A cache stampede (thundering herd) occurs when a popular cache key expires and multiple concurrent requests simultaneously attempt to reload it from the origin. Without a guard, all requests hit the database simultaneously, causing a load spike that can cascade into a full outage. Three patterns prevent this: distributed lock (one process rebuilds, others wait), probabilistic early refresh (rebuild before expiry with increasing probability), and request coalescing (in-flight deduplication).

## Applies If (ALL must hold)

- Any cache key that is accessed by more than ~10 concurrent requests per second and has an expensive origin load (slow query, external API call, ML inference).
- Keys with a TTL shorter than the origin load time multiplied by peak concurrency — the danger zone where multiple requests can land in the window between expiry and repopulation.
- After a cache flush or cold start, when the entire keyspace is empty and all requests are simultaneous cache misses.
- Materialized views or aggregation results that take seconds to compute.

## Skip If (ANY kills it)

- Low-concurrency endpoints (single-digit concurrent requests) — lock overhead exceeds stampede risk.
- Very fast origin loads (<5ms) — the stampede window is too small to cause measurable damage.
- High-cardinality keys where each key is accessed infrequently — no stampede risk by definition.
- Probabilistic early refresh on keys where stale serving is never acceptable — early refresh serves slightly stale data during the refresh window.

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
