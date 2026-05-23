---
slug: embedding-caching
tier: geek
group: ai
domain: ml-engineering
version: 1.1.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: Embedding cache layer — SHA-256 keyed by (model+version+text), TTL aligned with model version, Redis/Valkey backend, cache-hit metric for cost audit.
content_id: "484df2202087698b"
complexity: medium
produces: code
est_tokens: 3200
tags: [embeddings, caching, redis, valkey, cost-reduction]
---
# Embedding Caching Patterns

## Summary

**One-sentence:** Embedding cache layer — SHA-256 keyed by (model+version+text), TTL aligned with model version, Redis/Valkey backend, cache-hit metric for cost audit.

**One-paragraph:** Re-embedding the same text wastes API budget. This methodology produces an `EmbeddingCache` class: SHA-256 cache keys composed of (model_name + model_version + text), TTL bounded by model-deprecation calendar, Redis/Valkey backend, per-call cache-hit metric. MD5 explicitly rejected (collision risk at billion-doc scale).

**Ефективно для:**

- RAG re-ingestion pipelines where same docs flow repeatedly.
- Multi-tenant systems де different tenants embed same source.
- Cost audit — cache_hit_rate як KPI.
- Cache invalidation aligned з model deprecation.
- Browser/edge usage де latency &lt; API round-trip required.

## Applies If (ALL must hold)

- Corpus re-ingestion expected (updates / nightly refresh / multi-tenant).
- Cache backend available (Redis / Valkey / DynamoDB).
- Per-vector model_version stored.
- Named owner.

## Skip If (ANY kills it)

- One-shot embedding (corpus indexed once, never updated).
- &lt;5% repeated-text rate (cache hit savings &lt; cost).
- No cache backend.
- Latency requirement met without cache.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Cache backend client (Redis / Valkey) | client | platform |
| Embedding model client | client | platform |
| Model name + version pin | YAML | service repo |
| Cache hit metric collector | platform | observability |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `[[embedding-generation]]` | Underlying embed call. |
| `[[embedding-cost-optimization]]` | Companion cost methodology. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 4 rules + run/skip terminals | ~700 |
| `content/02-output-contract.xml` | essential | JSON Schema for cache-config | ~600 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns | ~700 |
| `content/04-procedure.xml` | essential | 5-step: pick backend → key gen → TTL → metric → audit | ~700 |
| `content/06-decision-tree.xml` | essential | Routes corpus class to cache vs no-cache | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `compute-cache-key` | haiku | Mechanical hash. |
| `evict-by-model-deprecation` | sonnet | TTL judgment. |
| `audit-hit-rate` | haiku | Numeric. |

## Templates

| File | Purpose |
|------|---------|
| `templates/embedding_cache.py` | EmbeddingCache class with SHA-256 + TTL. |
| `templates/cache-config.json` | Config skeleton. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-embedding-caching.py` | Validate cache-config | Pre-commit + CI |

## Related

- [[embedding-generation]]
- [[embedding-cost-optimization]]
- [[embedding-models]]

## Decision tree

See `content/06-decision-tree.xml`. The tree routes to cache when repeated-text rate &gt;5% AND backend available. Otherwise direct embed.
