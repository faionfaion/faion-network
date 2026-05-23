---
slug: caching-invalidation
tier: pro
group: backend-systems
domain: backend
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: "Produces a per-entity invalidation strategy: TTL floor, event-based purges on write, Redis SET-backed tag groups, and version-prefixed namespaces; selection by freshness SLO."
content_id: "314a0a535f35b7e2"
complexity: deep
produces: spec
est_tokens: 4300
tags: [caching, redis, invalidation, ttl, cache-tags]
---

# Cache Invalidation (TTL, Event-Based, Tag-Based, Version-Based)

## Summary

**One-sentence:** Produces a per-entity invalidation strategy: TTL floor, event-based purges on write, Redis SET-backed tag groups, and version-prefixed namespaces; selection by freshness SLO.

**Ефективно для:**

- Read-heavy entities with write events on a known channel.
- Cascading invalidations (one parent → many cached children).
- Computed views that depend on multiple entities.
- Migrations / schema changes that must drop old caches instantly.

**One-paragraph:** Cache invalidation is the hardest part of caching. Four strategies exist: TTL (time-to-live, simplest, always include as a floor), event-based (invalidate on write events, required for strong freshness), tag-based (invalidate groups via Redis SETs of keys), and version-based (namespace keys with a bumped version number, useful for schema or computation changes). Every entity needs at least TTL; event-based is required when staleness SLO is below the TTL; tags / versions handle cascading invalidation.

## Applies If (ALL must hold)

- A shared cache (Redis / Memcached / CDN) is in front of origin.
- Write events are observable (DB log, app event, message bus).
- Staleness SLO is documented per entity type.
- Tag / version overhead (~10% extra ops) fits the budget.

## Skip If (ANY kills it)

- Single-process L1 cache only — use L1 invalidation hook instead.
- Read-once data — invalidation is unnecessary.
- No write-event channel — TTL is the only option.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Entity → cache-key map | spec | team |
| Write-event channel (DB log / bus) | infra doc | SRE |
| Per-entity staleness SLO | product decision | PM |
| Redis ACL for tag / version ops | ops doc | SRE |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `[[backend-systems]]` | host stack |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 7 testable rules with rationale + source | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid / invalid examples | ~700 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom / root-cause / fix | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure with input / action / output per step | ~900 |
| `content/05-examples.xml` | recommended | one end-to-end worked example | ~600 |
| `content/06-decision-tree.xml` | essential | run / skip router referencing rule ids | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `pick-strategy-per-entity` | sonnet | Maps SLO + write-channel to TTL / event / tag / version. |
| `design-key-namespace` | haiku | Generates key + tag templates. |
| `draft-purge-handlers` | sonnet | Wires events to purge functions with idempotency check. |

## Templates

| File | Purpose |
|------|---------|
| `templates/caching-invalidation.json` | JSON Schema for the Cache Invalidation (TTL, Event-Based, Tag-Based, Version-Based) output contract |
| `templates/caching-invalidation.md` | Markdown skeleton with the required fields |
| `templates/_smoke-test.md` | Filled-in minimum viable example of a caching-invalidation record |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-caching-invalidation.py` | Enforce the Cache Invalidation (TTL, Event-Based, Tag-Based, Version-Based) output contract | After subagent returns, before downstream consumer reads |

## Related

- [[caching-write-patterns]]
- [[caching-stampede-prevention]]
- [[caching-http-headers]]

## Decision tree

Lives at `content/06-decision-tree.xml`. Two-question gate: (1) preconditions present? (2) does an existing artefact already cover this gap? Routes to run / skip / update. Every conclusion references a rule id from `content/01-core-rules.xml`.
