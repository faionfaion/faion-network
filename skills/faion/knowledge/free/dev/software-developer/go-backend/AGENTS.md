---
slug: go-backend
tier: free
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Production-grade Go backend pattern using the standard cmd/ + internal/ project layout with Gin or Echo routers.
content_id: "f3c43363bde0ba3d"
tags: [go, backend, project-layout, http, error-handling]
---
# Go Backend

## Summary

**One-sentence:** Production-grade Go backend pattern using the standard cmd/ + internal/ project layout with Gin or Echo routers.

**One-paragraph:** Production-grade Go backend pattern using the standard cmd/ + internal/ project layout with Gin or Echo routers. Key conventions: interfaces defined at the consumer side, context.Context as first arg on all I/O functions, typed AppError mapped to HTTP via middleware, worker-pool concurrency via a Pool struct with channel-based job queue.

## Applies If (ALL must hold)

- Greenfield Go service scaffolding with cmd/ + internal/handler/service/repository layers.
- Adding endpoints to an existing Gin/Echo project following this layout.
- Generating typed AppError taxonomies and error-handler middleware.
- Building worker-pool / fan-out-fan-in glue code around a typed Job interface.

## Skip If (ANY kills it)

- Non-standard layouts (Hex / Clean / monorepo multi-module) — import paths will be wrong.
- Performance-critical hot paths needing sync.Pool or escape-analysis awareness.
- Cgo / unsafe / kernel-bypass code — out of scope.
- Generics-heavy domain libraries — examples use pre-generics style.

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

- parent skill: `free/dev/software-developer/`
