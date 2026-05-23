---
slug: rust-tokio-async
tier: solo
group: dev
domain: dev
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Tokio async spec: runtime flavour (multi_thread vs current_thread), no blocking calls in async, structured cancellation (JoinSet / select!), bounded channels, timeouts on every await on the wire.
content_id: "53aec5c28fb4bdc4"
complexity: medium
produces: code
est_tokens: 4800
tags: [rust, tokio, async, concurrency]
---
# Rust Tokio Async

## Summary

**One-sentence:** Tokio async spec: runtime flavour (multi_thread vs current_thread), no blocking calls in async, structured cancellation (JoinSet / select!), bounded channels, timeouts on every await on the wire.

**One-paragraph:** Tokio code breaks when blocking calls (std::fs, sync mutex held across .await) stall worker threads, when unbounded channels accumulate until OOM, when JoinHandle is dropped (silent leak), when select! arms are not cancel-safe, and when timeouts are missing on network awaits. This methodology produces a spec: runtime flavour, blocking offload via `spawn_blocking`, JoinSet or select! for structured concurrency, bounded `tokio::sync::mpsc` channels, and `tokio::time::timeout` on every network await.

**Ефективно для:**

- Перший Tokio service - зафіксувати правила до production.
- Latency spikes - підозра на blocking call всередині async.
- OOM від unbounded mpsc - перейти на bounded.
- Race conditions через select! без cancel-safety.
- Shutdown hangs - JoinHandle dropped silently.

## Applies If (ALL must hold)

- Codebase uses Tokio 1.x runtime.
- Service does network I/O with measurable concurrency.
- Build pipeline can enforce clippy + custom lints.
- Team can refuse PRs that block the runtime.

## Skip If (ANY kills it)

- Code is CPU-bound batch work - use rayon instead.
- Sync Rust app with no async - use blocking std + threads.
- Single-file experiment that will be deleted.
- Async runtime is async-std or smol - this methodology is Tokio-specific.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Runtime requirement | multi_thread vs current_thread + worker count | engineering |
| Blocking inventory | list of blocking calls (fs, ffi, legacy) | engineering |
| Channel cardinality | expected producer/consumer rates | engineering |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[python-async-patterns]] | shared async discipline - bounded fan-out + timeouts. |
| [[websocket-design]] | downstream consumer of WS handlers built on Tokio. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 7 rules: runtime flavour explicit, no blocking in async, timeout on network, bounded channels, structured concurrency, mutex not across await, graceful shutdown | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns (symptom/root-cause/fix) | ~800 |
| `content/04-procedure.xml` | essential | 5-step plan: runtime, blocking offload, channels, timeouts, shutdown | ~900 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule id | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `audit-blocking` | haiku | Mechanical scan of crate dependencies. |
| `size-channels` | sonnet | Per-pipeline judgement on capacity. |
| `rewrite-handler` | sonnet | Translate sync paths to async + spawn_blocking. |
| `review-cancel-safety` | opus | Stakes high; select! arms must be cancel-safe. |

## Templates

| File | Purpose |
|------|---------|
| `templates/main.rs` | Tokio service skeleton: multi_thread runtime, JoinSet, timeout, CancellationToken shutdown. |
| `templates/Cargo.toml` | Cargo manifest snippet declaring Tokio features. |
| `templates/batch-processor.rs` | Tokio batch-processor: bounded channel + join_set + cancellation. |
| `templates/user-service.rs` | Tokio service example: async handlers + tracing + tower middleware. |
| `templates/_smoke-test.json` | Minimum viable tokio-async artefact for validator smoke-test. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-rust-tokio-async.py` | Validate the artefact against `content/02-output-contract.xml` schema. | After draft, before merge; pre-commit. |

## Related

- [[python-async-patterns]]
- [[websocket-design]]
- [[rate-limiting]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs - runtime config, blocking inventory, channel boundedness, timeout coverage - onto a rule from `content/01-core-rules.xml`. Use it before merging Tokio code: it catches blocking-in-async, unbounded mpsc, and missing timeouts upstream.
