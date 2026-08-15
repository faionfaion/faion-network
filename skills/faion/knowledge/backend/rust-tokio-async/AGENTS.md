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
| `content/01-core-rules.xml` | essential | 12 testable rules with rationale + source | ~1600 |
| `content/02-output-contract.xml` | essential | per-pattern JSON Schema + runtime-level companion contract + valid/invalid examples + 9 forbidden patterns | ~1700 |
| `content/03-failure-modes.xml` | essential | 8 antipatterns with symptom + root-cause + fix | ~1400 |
| `content/04-procedure.xml` | essential | 5-step end-to-end procedure + runtime-level spec step | ~1100 |
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
| `templates/main.rs` | Tokio service skeleton: explicit multi_thread runtime, JoinSet, timeout, CancellationToken shutdown. |
| `templates/Cargo.toml` | Cargo manifest snippet declaring the Tokio feature set explicitly. |
| `templates/batch-processor.rs` | Semaphore-bounded concurrent batch processor over a Vec input. |
| `templates/user-service.rs` | Reference service: try_join! for parallel queries, spawn_blocking for Argon2. |
| `templates/runtime-spec-example.json` | Filled-in runtime-level record (flavour, workers, offload, channel policy, timeout, shutdown). |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-rust-tokio-async.py` | Validate the output artefact against the schema in 02-output-contract.xml. | CI on each artefact change; pre-commit. |

## Related

- [[rust-testing-unit]]
- [[rust-testing-integration]]

## Decision tree

See `content/06-decision-tree.xml`. Tree maps (workload size, CPU heaviness, dynamic vs static group) to the correct Tokio primitive; each leaf cites one of the 8 core rules.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/buffer_unordered_with_semaphore.rs`

```rust
use futures::stream::{self, StreamExt};
use std::sync::Arc;
use tokio::sync::Semaphore;
use tokio::time::{timeout, Duration};

pub async fn process_bounded<I, T, F, Fut, E>(
    inputs: I,
    concurrency: usize,
    per_call_timeout: Duration,
    work: F,
) -> Vec<Result<T, E>>
where
    I: IntoIterator<Item = u64>,
    F: Fn(u64) -> Fut + Clone + Send + Sync + 'static,
    Fut: std::future::Future<Output = Result<T, E>> + Send,
    T: Send + 'static,
    E: From<tokio::time::error::Elapsed> + Send + 'static,
{
    let sem = Arc::new(Semaphore::new(concurrency));
    stream::iter(inputs)
        .map(|id| {
            let sem = sem.clone();
            let work = work.clone();
            async move {
                let _permit = sem.acquire_owned().await.expect("semaphore closed");
                match timeout(per_call_timeout, work(id)).await {
                    Ok(res) => res,
                    Err(elapsed) => Err(elapsed.into()),
                }
            }
        })
        .buffer_unordered(concurrency)
        .collect()
        .await
}
```

### `templates/joinset_dynamic.rs`

```rust
use tokio::task::JoinSet;
use tokio::time::{timeout, Duration};

pub async fn fan_out<F, T>(work: Vec<F>, per_task_timeout: Duration) -> Vec<Result<T, String>>
where
    F: std::future::Future<Output = T> + Send + 'static,
    T: Send + 'static,
{
    let mut set: JoinSet<Result<T, String>> = JoinSet::new();
    for fut in work {
        set.spawn(async move {
            match timeout(per_task_timeout, fut).await {
                Ok(t) => Ok(t),
                Err(_) => Err("task timed out".into()),
            }
        });
    }
    let mut out = Vec::new();
    while let Some(res) = set.join_next().await {
        out.push(res.unwrap_or_else(|e| Err(format!("join error: {e}"))));
    }
    out
}
```
