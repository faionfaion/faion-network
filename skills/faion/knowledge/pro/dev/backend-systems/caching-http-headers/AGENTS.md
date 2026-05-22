---
slug: caching-http-headers
tier: pro
group: dev
domain: backend
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: HTTP caching is the highest-leverage caching layer: a correctly set Cache-Control header eliminates origin requests entirely for eligible responses, reducing latency to near-zero and offloading up to 90% of traffic to CDN edge nodes.
content_id: "8f39d0d23438d63b"
tags: [caching, http, cdn, cache-control, etag]
---
# HTTP Caching Headers: Cache-Control, ETag, Vary, and CDN Edge Caching

## Summary

**One-sentence:** HTTP caching is the highest-leverage caching layer: a correctly set Cache-Control header eliminates origin requests entirely for eligible responses, reducing latency to near-zero and offloading up to 90% of traffic to CDN edge nodes.

**One-paragraph:** HTTP caching is the highest-leverage caching layer: a correctly set Cache-Control header eliminates origin requests entirely for eligible responses, reducing latency to near-zero and offloading up to 90% of traffic to CDN edge nodes. The four critical headers are Cache-Control (freshness policy), ETag (conditional revalidation), Vary (cache key dimensions), and Surrogate-Key/Cache-Tag (CDN group invalidation).

## Applies If (ALL must hold)

- Public API endpoints serving read-heavy data that changes on a predictable schedule (product catalog, article content, pricing).
- Static assets (JS, CSS, images, fonts) — set immutable + long max-age after content-hashing the filename.
- Personalized API responses — set private to allow browser caching but prevent CDN from serving one user's data to another.
- Any endpoint where reducing origin request volume or improving time-to-first-byte is a requirement.

## Skip If (ANY kills it)

- Endpoints returning real-time data (live scores, auction prices, stock quotes) — set no-store or max-age=0 must-revalidate to prevent any caching.
- POST/PUT/DELETE responses — HTTP caching applies only to GET and HEAD by default; non-idempotent responses should not be cached.
- Responses containing authentication tokens or session cookies in the body — use private at minimum; prefer no-store.
- Endpoints where cache invalidation is impossible or impractical without a CDN purge API — prefer short max-age over surrogate keys when CDN purge is not available.

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
