---
slug: caching-in-memory
tier: pro
group: backend-systems
domain: backend
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: "Produces an L1 in-process cache spec: `lru_cache` for pure deterministic functions, `cachetools.TTLCache` with TTL + thread-safety, `WarmableCache` for preload-on-startup; explicit when to fall back to Redis."
content_id: "47ae975b5152eae9"
complexity: medium
produces: config
est_tokens: 3700
tags: [caching, in-memory, lru-cache, ttlcache, cache-warming]
---

# In-Memory Application Cache (L1 with lru_cache + TTLCache + WarmableCache)

## Summary

**One-sentence:** Produces an L1 in-process cache spec: `lru_cache` for pure deterministic functions, `cachetools.TTLCache` with TTL + thread-safety, `WarmableCache` for preload-on-startup; explicit when to fall back to Redis.

**Ефективно для:**

- Hot pure-function results (parser, regex, format mapping).
- Per-process config dictionaries (feature flags after fetch).
- Idempotent computations called >100 times per request.
- Predictable startup keys worth preloading.

**One-paragraph:** Process-local L1 cache: requests that hit L1 never leave the process — sub-millisecond latency, zero network overhead. Python's `lru_cache` is appropriate for pure deterministic functions with stable inputs; `cachetools.TTLCache` adds TTL expiry + thread-safety; a `WarmableCache` wrapper preloads predictable hot keys at startup. L1 is never a replacement for Redis — it cannot be shared across processes and does not survive restarts.

## Applies If (ALL must hold)

- Function inputs are hashable and bounded.
- Stale-tolerance ≥ TTL acceptable for the call site.
- Cache memory budget per worker is documented.
- Multi-worker invalidation is not required.

## Skip If (ANY kills it)

- Result must be consistent across workers — use Redis.
- Values are large (>1 MiB) — risk worker OOM.
- Inputs are unbounded / unhashable — LRU thrashes.
- Strict freshness on writes — TTL alone is insufficient.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Function signature + call pattern | code path | team |
| Memory budget per worker | ops doc | SRE |
| Acceptable staleness (TTL) | product decision | PM |
| Cache hit-rate floor | telemetry SLO | SRE |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `[[python-developer]]` | host language conventions |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 7 testable rules with rationale + source | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid / invalid examples | ~700 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom / root-cause / fix | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure with input / action / output per step | ~900 |
| `content/06-decision-tree.xml` | essential | run / skip router referencing rule ids | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `classify-call-site` | haiku | Pure-vs-IO + stale-tolerance classification. |
| `size-and-ttl` | sonnet | Memory + freshness tradeoff per cache. |
| `warm-plan` | sonnet | Identifies which keys are predictable at startup. |

## Templates

| File | Purpose |
|------|---------|
| `templates/caching-in-memory.json` | JSON Schema for the In-Memory Application Cache (L1 with lru_cache + TTLCache + WarmableCache) output contract |
| `templates/caching-in-memory.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-caching-in-memory.py` | Enforce the In-Memory Application Cache (L1 with lru_cache + TTLCache + WarmableCache) output contract | After subagent returns, before downstream consumer reads |

## Related

- [[caching-write-patterns]]
- [[caching-invalidation]]
- [[caching-stampede-prevention]]

## Decision tree

Lives at `content/06-decision-tree.xml`. Two-question gate: (1) preconditions present? (2) does an existing artefact already cover this gap? Routes to run / skip / update. Every conclusion references a rule id from `content/01-core-rules.xml`.
