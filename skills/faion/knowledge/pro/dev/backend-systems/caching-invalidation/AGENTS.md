---
slug: caching-invalidation
tier: pro
group: dev
domain: backend-systems
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Cache invalidation is the hardest part of caching.
content_id: "45f154c64dcf54cf"
tags: [caching, redis, invalidation, ttl, cache-tags]
---
# Cache Invalidation: TTL, Event-Based, Tag-Based, and Version-Based

## Summary

**One-sentence:** Cache invalidation is the hardest part of caching.

**One-paragraph:** Cache invalidation is the hardest part of caching. Four strategies exist: TTL (time-to-live, simplest), event-based (invalidate on write events), tag-based (invalidate groups via Redis SETs), and version-based (namespace keys with a bumped version number). Every entity needs at least TTL; event-based is required for strong freshness; tags and versions handle cascading invalidation.

## Applies If (ALL must hold)

- TTL-based: all entities as a safety net; standalone for data where bounded staleness is explicitly acceptable (analytics, public catalog).
- Event-based: entities with a write path you control (user profiles, orders) and a freshness budget under 5 minutes.
- Tag-based: entities with group membership (products in a category, articles by author) where you need to invalidate an entire group on a single event.
- Version-based: schema changes across deployments, or any time you need atomic invalidation of all cached instances of an entity type.

## Skip If (ANY kills it)

- Event-based invalidation without a write-path audit — incomplete invalidation leaves stale keys that TTL alone eventually expires.
- Tag-based invalidation without TTL on the tag sets themselves — orphaned tag keys accumulate and consume memory indefinitely.
- Version-based invalidation as the sole strategy — old versioned keys are orphaned until their TTL expires, so memory grows linearly with deploys.
- KEYS * for bulk invalidation in production — O(N), blocks Redis single-thread loop, causes latency spikes under load.

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
