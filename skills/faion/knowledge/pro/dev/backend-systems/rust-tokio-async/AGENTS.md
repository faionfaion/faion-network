---
slug: rust-tokio-async
tier: pro
group: dev
domain: backend
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Produces Tokio async code that picks the lightest correct primitive per workload class (try_join, spawn_blocking, buffer_unordered+Semaphore, JoinSet), wraps all I/O in timeouts, and holds no MutexGuard across .await.
content_id: "53aec5c28fb4bdc4"
complexity: deep
produces: code
est_tokens: 4300
tags: [rust, tokio, async, concurrency, patterns]
---
# Rust Tokio Async Patterns

## Summary

**One-sentence:** Produces Tokio async code that picks the lightest correct primitive per workload class (try_join, spawn_blocking, buffer_unordered+Semaphore, JoinSet), wraps all I/O in timeouts, and holds no MutexGuard across .await.

**One-paragraph:** Each concurrent pattern is classified by workload size + semantics and mapped to the lightest correct primitive: try_join! for small fixed N, spawn_blocking for CPU-heavy work, futures::stream::buffer_unordered + Semaphore for large bounded-N streams, JoinSet for dynamic groups. Every external I/O call carries an explicit timeout; non-cancel-safe futures in select! are annotated; std::sync::MutexGuard never crosses .await.

**Ефективно для:**

- Fixed-N parallel futures — `try_join!`; колекції — `buffer_unordered + Semaphore`.
- Argon2/bcrypt/zip — `spawn_blocking`, інакше блокується runtime.
- Динамічні групи tasks — `JoinSet` замість `Vec<JoinHandle>`.
- Кожен external call загорнутий у `tokio::time::timeout`.
- `select!` — anotate cancel-safety кожної гілки.

## Applies If (ALL must hold)

- Writing async services on Tokio (Axum, tonic, sqlx, reqwest) with bounded concurrency.
- Replacing sequential .await chains with try_join! or buffer_unordered.
- Offloading CPU-intensive work via spawn_blocking.
- Migrating from async-std or smol to Tokio.

## Skip If (ANY kills it)

- Single-thread CPU work — async adds no benefit; use sync code.
- Embedded / no_std — use embassy.
- Runtime-agnostic library — depend on futures, not tokio.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Tokio-enabled application | Rust crate | service repo |
| futures crate (for streams) | Cargo dep | Cargo.toml |
| Concurrency budget N | policy | ops decision |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[rust-testing-unit]] | Tokio tests use the flavors authored by rust-testing-unit |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 9 testable rules with rationale + source | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns with symptom + root-cause + fix | ~900 |
| `content/04-procedure.xml` | essential | 5-step end-to-end procedure | ~800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `classify-workload` | sonnet | Pick primitive per workload class. |
| `write-pattern` | sonnet | Implement chosen pattern with timeout + concurrency bound. |
| `audit-cancel-safety` | opus | Cross-future review of cancel-safety in select! branches. |
| `validate-output` | haiku | Schema check via the validator script. |

## Templates

| File | Purpose |
|------|---------|
| `templates/buffer_unordered_with_semaphore.rs` | buffer_unordered + Semaphore bounded-concurrency stream. |
| `templates/joinset_dynamic.rs` | JoinSet for dynamic task groups with cancellation on drop. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-rust-tokio-async.py` | Validate the output artefact against the schema in 02-output-contract.xml. | CI on each artefact change; pre-commit. |

## Related

- [[rust-testing-unit]]
- [[rust-testing-integration]]

## Decision tree

See `content/06-decision-tree.xml`. Tree maps (workload size, CPU heaviness, dynamic vs static group) to the correct Tokio primitive; each leaf cites one of the 8 core rules.
