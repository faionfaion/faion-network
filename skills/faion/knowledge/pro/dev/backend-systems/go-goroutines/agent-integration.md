# Agent Integration — Go Goroutines & Worker Patterns

## When to use
- Implementing worker pools, semaphores, rate limiters, and bounded parallelism over I/O-bound work.
- Coordinating shutdown of long-lived background tasks via `context.Context`.
- Adding thread-safe in-memory caches (`sync.RWMutex`, `sync.Map`) and lazy initialization (`sync.Once`).
- Wrapping fan-out workloads (HTTP fetches, DB writes) with concurrency caps to avoid downstream overload.

## When NOT to use
- CPU-bound work with no parallelism opportunity — goroutines just add scheduling overhead.
- Code that fits in a single function and runs <1 ms — concurrency gives nothing back.
- Anywhere you'd reach for goroutines + shared state via mutex when channels (or vice-versa) are clearly better — pick one model per concern.
- Replacing a real queue (Redis Streams, Kafka, SQS): in-process worker pools die with the process and lose visibility.

## Where it fails / limitations
- Goroutine leaks are silent — missing `select { ... case <-ctx.Done(): return }` keeps the worker alive forever after the request returns.
- The README's `RateLimiter` uses a refill ticker that never lets the bucket exceed `burst`; under sustained idle it under-fills (only one token per tick) — fine, but agents reuse this code for high-burst traffic and get throttled at startup.
- The semaphore example collects only the *first* error (`for err := range errCh { return err }`) — real workloads need all errors or `errgroup.WithContext` semantics.
- `sync.Once` is per-process; agents reach for it in distributed init and lose race-safety across replicas.
- `sync.RWMutex` write starvation under read-heavy load: many goroutines blocked on writes if reads never drain. Agents rarely benchmark this.
- Closing channels from inside workers (anti-pattern) panics under retry; the README's worker pool dodges this but copy-paste mutations often break it.

## Agentic workflow
Goroutine code is high-risk for LLMs: every change must run with `-race`, `goleak`, and a goroutine-leak benchmark. Have one agent write the worker code with explicit context cancellation contracts, then a second agent enumerate every spawned goroutine and prove it has an exit. Pair worker pool changes with load tests (`vegeta`, `k6`) before merging — goroutine bugs only show under contention.

### Recommended subagents
- `faion-sdd-executor-agent` — quality gates already include `go test -race`; add a custom check that runs `goleak`.
- A custom `goroutine-auditor` (Opus, read-only) — outputs a per-goroutine table: `{file:line, lifetime, owner, cancel_signal, restart_policy}`. Reject "unknown" rows.
- `password-scrubber-agent` — usually unrelated; goroutine code rarely contains credentials.

### Prompt pattern
```
Implement a worker pool with: bounded concurrency=N, ctx-driven shutdown, retry with backoff on transient errors, and a metrics hook (jobs_started, jobs_completed, jobs_failed, queue_depth).
Constraints: no goroutine without ctx exit; results channel closed exactly once by the goroutine that closes the WaitGroup; no panics escape (use defer recover with structured logging).
Deliver: pool.go, pool_test.go (table-driven, includes cancellation + panic-in-job + slow-consumer cases), bench_test.go.
Run go test -race -count=10 and paste output.
```

```
Inventory all goroutines spawned in <pkg>. For each: lifetime, exit condition, who owns the input, who owns the output, max wait on send, panic policy.
Reject any row missing exit condition or panic policy.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `go test -race` | Race detector — required for any goroutine PR | https://go.dev/blog/race-detector |
| `goleak` | Test-time leak assertion | https://github.com/uber-go/goleak |
| `pprof` (`/debug/pprof/goroutine`, `/heap`) | Live goroutine + heap dump | https://pkg.go.dev/net/http/pprof |
| `gops` | Live goroutine count of running process | https://github.com/google/gops |
| `delve` | Debug paused goroutines | https://github.com/go-delve/delve |
| `vegeta` / `k6` | Load test the worker pool under contention | https://github.com/tsenart/vegeta · https://k6.io |
| `staticcheck` SA1015 / SA1029 | Catches `time.After` in loops, ctx misuse | https://staticcheck.dev/ |
| `errcheck` | Forbids ignored returns inside goroutines | https://github.com/kisielk/errcheck |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| `golang.org/x/sync/errgroup` | OSS | Yes | Default for fan-out with errors. |
| `golang.org/x/sync/semaphore` | OSS | Yes | Replaces hand-rolled `chan struct{}` semaphores. |
| `golang.org/x/time/rate` | OSS | Yes | Token-bucket limiter — preferred over the hand-rolled snippet. |
| `github.com/sourcegraph/conc` | OSS | Yes | Higher-level pool/iter helpers; agent-friendly API. |
| `github.com/uber-go/goleak` | OSS | Yes | Test gate that fails CI on leaks. |
| Datadog / OTel `runtime.Goroutines` | SaaS / OSS | Yes | Production canary on goroutine count. |
| Sentry / Rollbar | SaaS | Yes | Capture panics from `defer recover()` — required for fire-and-forget pools. |
| Prometheus | OSS | Yes | Expose `pool_jobs_inflight`, `pool_queue_depth`, `pool_failed_total`. |

## Templates & scripts
See `templates.md` for worker pool, semaphore, rate limiter, and cache snippets. Useful reusable primitive (≤30 lines):

```go
// internal/concurrency/run.go
package concurrency

import (
    "context"
    "log/slog"

    "golang.org/x/sync/errgroup"
    "golang.org/x/sync/semaphore"
)

// Run executes fn over items with at most n concurrent invocations.
// Cancels on first error; returns the joined error.
func Run[T any](ctx context.Context, n int64, items []T, fn func(context.Context, T) error) error {
    g, ctx := errgroup.WithContext(ctx)
    sem := semaphore.NewWeighted(n)
    for _, it := range items {
        it := it
        if err := sem.Acquire(ctx, 1); err != nil {
            return err
        }
        g.Go(func() error {
            defer sem.Release(1)
            defer func() {
                if r := recover(); r != nil {
                    slog.Error("panic in worker", "panic", r)
                }
            }()
            return fn(ctx, it)
        })
    }
    return g.Wait()
}
```

## Best practices
- Default to `errgroup.WithContext` + `semaphore.Weighted` instead of hand-rolling channels + WaitGroups; the README examples are educational, not production defaults.
- Every goroutine must have (1) an owner, (2) an exit signal, (3) a panic policy. Make this a checklist item in code review.
- Use `runtime.NumCPU()` only for CPU-bound work; for I/O-bound, parameterize concurrency from config and validate via load tests.
- Replace `time.After(d)` inside a loop with `t := time.NewTimer(d); defer t.Stop()`; otherwise timers leak until they fire.
- Wrap pools in metrics: `inflight`, `queue_depth`, `latency_seconds`, `failed_total`. Without metrics, capacity tuning is guessing.
- Use `goleak.VerifyTestMain` so any test that leaks fails fast.

## AI-agent gotchas
- LLMs add `defer wg.Done()` but forget `wg.Add(1)` (or vice-versa) — always pair Adds and Dones; better, return early to errgroup.
- `for _, x := range xs { go func() { use(x) } }` captures the loop var (pre-Go 1.22). Agents trained on older code still produce this. Force the `x := x` shadow even though Go 1.22 fixed it — code may run on older toolchains.
- Agents pick `runtime.NumCPU()` for I/O-bound pools and saturate downstreams; require an explicit concurrency-rationale comment.
- `sync.Map` is misused as a generic concurrent map — it's only faster than `map+RWMutex` for stable-key, high-read patterns. Force a benchmark before adoption.
- Recovery is often missing inside goroutines — a panic on a worker crashes the process. Require `defer func() { if r := recover(); ... }`.
- Human-in-loop checkpoint: any new background goroutine with unbounded lifetime (cron, supervisor, long-poll) must be approved by a reviewer with the cancellation source and metric named.

## References
- Pipelines and cancellation — https://go.dev/blog/pipelines
- Context — https://go.dev/blog/context
- Advanced concurrency patterns — https://go.dev/blog/io2013-talk-concurrency
- Share memory by communicating — https://go.dev/blog/codelab-share
- "Concurrency in Go" (Katherine Cox-Buday) — chapters 4-5.
- errgroup — https://pkg.go.dev/golang.org/x/sync/errgroup
- goleak — https://github.com/uber-go/goleak
