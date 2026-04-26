# Go Concurrency Patterns

## Summary

Four battle-tested Go concurrency primitives — worker pool, fan-out/fan-in, errgroup with semaphore, and pipeline — selected by workload type (IO-bound vs CPU-bound vs streaming vs "fail fast"). Every pattern requires context propagation, panic recovery, and a `goleak`-based goroutine-leak test.

## Why

Ad-hoc `go func()` calls without WaitGroup discipline, context cancellation, or error channels are the leading cause of goroutine leaks, silent error drops, and race conditions in Go services. Choosing the wrong primitive (e.g., custom pool when `errgroup` fits) adds complexity with no benefit. The four patterns here cover >90% of real workloads and have known correctness invariants.

## When To Use

- Building a worker pool to consume from a queue (Kafka, NATS, SQS) with bounded parallelism.
- Fan-out/fan-in over a slice where each item has independent IO.
- Pipelines of transforming stages joined by channels.
- Replacing ad-hoc goroutine launches lacking Context/WaitGroup discipline.
- Rate-limiting outbound calls.

## When NOT To Use

- Pure CPU-bound number crunching — simple parallel `for` without channels.
- Single-flight de-duplication — use `golang.org/x/sync/singleflight`.
- "First error cancels siblings" — use `errgroup` directly, not a custom pool.
- Hot path with billions of tiny tasks — goroutine-per-request already in the runtime.
- Libraries exposing their own concurrency (e.g., DB pool) — don't double-wrap.

## Content

| File | What's inside |
|------|---------------|
| `content/01-worker-pool.xml` | Worker pool implementation, Submit/Stop lifecycle, error channel wiring. |
| `content/02-fan-out-fan-in.xml` | Fan-out/fan-in pattern and bounded errgroup+semaphore template. |
| `content/03-rules.xml` | Selection guide (IO vs CPU vs streaming), goroutine-leak rules, antipatterns. |

## Templates

| File | Purpose |
|------|---------|
| `templates/worker_pool.go` | Generic worker pool with context, panic recovery, error reporting. |
| `templates/process_all.go` | errgroup + semaphore bounded-parallel helper (generic, Go 1.21+). |
