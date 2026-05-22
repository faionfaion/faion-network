---
slug: caching-architecture
tier: solo
group: dev
domain: architecture
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Design multi-layer caching strategies (browser → CDN → API gateway → application → database) using the correct pattern per data type: cache-aside, read-through, write-through, write-behind, or write-around.
content_id: "63cca5735ff7977a"
tags: [caching, redis, performance, architecture, scalability]
---
# Caching Architecture and Patterns

## Summary

**One-sentence:** Design multi-layer caching strategies (browser → CDN → API gateway → application → database) using the correct pattern per data type: cache-aside, read-through, write-through, write-behind, or write-around.

**One-paragraph:** Design multi-layer caching strategies (browser → CDN → API gateway → application → database) using the correct pattern per data type: cache-aside, read-through, write-through, write-behind, or write-around. Every cache layer requires explicit TTL with jitter, an invalidation trigger, and stampede control. Always measure hit ratio and p95 latency before and after.

## Applies If (ALL must hold)

- Read-heavy workloads with measured DB or upstream pressure (>30% of latency budget on data fetch).
- Hot, repeatable read paths: profiles, catalogues, configuration, feature flags, auth lookups.
- Cost reduction where compute/IO cost is dominated by repeated queries.
- CDN/edge work for static assets, public APIs, marketing pages, image variants.
- LLM-powered apps needing prompt cache, embedding cache, or tool-result cache layers.

## Skip If (ANY kills it)

- Strong-consistency-critical paths (ledger balances, inventory at checkout) without write-through or distributed-lock pattern.
- Personalized data with hit-rate ceiling below ~30% — the cache adds latency without payback.
- Premature optimization: skip until profiling shows a hot key/query.
- Writes-dominated workloads — caches become invalidation sinks.

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

- parent skill: `solo/dev/software-architect/`
