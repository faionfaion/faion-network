---
slug: rust-tokio-async
tier: pro
group: dev
domain: backend
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Async primitives for Tokio-based Rust services: tokio::try_join! for parallel independent futures, spawn_blocking for CPU-heavy work, futures::stream::buffer_unordered + Semaphore for bounded-concurrent collection processing, and JoinSet for dynamic task groups.
content_id: "3e53b31414fc5017"
tags: [rust, tokio, async, concurrency, patterns]
---
# Rust Tokio Async Patterns

## Summary

**One-sentence:** Async primitives for Tokio-based Rust services: tokio::try_join! for parallel independent futures, spawn_blocking for CPU-heavy work, futures::stream::buffer_unordered + Semaphore for bounded-concurrent collection processing, and JoinSet for dynamic task groups.

**One-paragraph:** Async primitives for Tokio-based Rust services: tokio::try_join! for parallel independent futures, spawn_blocking for CPU-heavy work, futures::stream::buffer_unordered + Semaphore for bounded-concurrent collection processing, and JoinSet for dynamic task groups. Every pattern requires an explicit concurrency bound, structured error type, and cancellation-safety annotation.

## Applies If (ALL must hold)

- Writing async services on Tokio (Axum, tonic, sqlx, reqwest) with bounded concurrency.
- Replacing sequential .await chains that could run in parallel with try_join!.
- Offloading CPU-intensive work (Argon2, image, compression) via spawn_blocking.
- Streaming bounded-concurrency over large collections with buffer_unordered + Semaphore.
- Migrating from async-std or smol to Tokio.

## Skip If (ANY kills it)

- Single-thread CPU work — async adds no benefit; use sync code.
- Embedded / no_std — use embassy instead.
- Runtime-agnostic library code — depend on futures, not tokio.
- Hard real-time scheduling — Tokio is best-effort, not deadline-driven.

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
