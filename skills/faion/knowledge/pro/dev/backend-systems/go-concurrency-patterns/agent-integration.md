# Agent Integration — Go Concurrency Patterns

## When to use
- Building a worker pool to consume from a queue (Kafka, NATS, SQS, RabbitMQ) with bounded parallelism.
- Fan-out/fan-in over a slice of work items where each item has independent IO (HTTP fetch, DB lookup).
- Pipelines of transforming stages joined by channels (extract → enrich → write).
- Replacing ad-hoc `go func()` calls that have no `context.Context`/`sync.WaitGroup` discipline.
- Rate limiting outbound calls with `golang.org/x/time/rate` or token-bucket channels.

## When NOT to use
- Pure CPU-bound number crunching — `runtime.GOMAXPROCS` and a simple parallel `for` are usually enough; channels add overhead.
- Single-flight de-duplication — use `golang.org/x/sync/singleflight`, not a custom pool.
- Errgroup-style "first error cancels siblings" — use `golang.org/x/sync/errgroup`, not the worker-pool pattern shown.
- Hot path with billions of tiny tasks — channel send/recv is ~50ns; goroutine-per-request HTTP servers already do this.
- When the upstream library exposes its own concurrency primitives (e.g., DB pool); wrapping it in another pool causes contention.

## Where it fails / limitations
- Worker pools shown here have no backpressure: `Submit` blocks when the buffer is full, but the caller can't tell. Callers must select on `ctx.Done()` themselves.
- Fan-out/fan-in with `len(items)`-sized channels allocates O(N) memory; for large N use a streaming channel with a bounded buffer.
- Errors from `_ = job(ctx)` are silently dropped — must wire to a logger or err channel.
- `sync.WaitGroup` does not propagate panics; one panicking goroutine takes the process down. Wrap workers with `defer recover()` for production.
- Goroutine leaks: forgetting to close `jobs` or to drain `results` leaves goroutines blocked forever. `go vet` and `goleak` testing are mandatory.
- `runtime.NumCPU()` is the wrong default for IO-bound work — use a tunable concurrency limit, often 10–100x CPUs.

## Agentic workflow
The agent should (1) classify the task: IO-bound vs CPU-bound vs streaming, (2) pick the primitive: `errgroup` for "wait all, fail fast", worker pool for "long-lived consumer", semaphore for "rate-limit", pipeline for "stages", (3) generate the implementation with mandatory `context.Context`, error reporting, panic recovery, (4) generate a `goleak` test that asserts no goroutines leak after teardown. Always require `go test -race` to pass — race detector catches the most common LLM mistakes (closing over loop variables, shared maps).

### Recommended subagents
- `faion-sdd-executor-agent` — wraps the change as an SDD task; gates: `go test -race ./...`, `go vet`, `golangci-lint run`.
- A general implementer (Sonnet) for boilerplate; an architect (Opus) for picking the right primitive and the bounded-buffer math.

### Prompt pattern
```
You are wiring concurrent processing for <task>. Work items: <type>, count: <expected N>,
per-item latency: <ms>, dependencies: <DB/HTTP>. Pick one of: errgroup / worker pool /
semaphore+stream / pipeline. Justify the choice in 2 sentences, then implement with
context cancellation, panic recovery, structured error return, and a goleak-based test.
```

```
Audit this code for goroutine leaks, race conditions, and missing context propagation.
Run `go vet`, `go test -race ./...` mentally and list every issue with file:line.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `go test -race` | Detects data races at runtime | stdlib |
| `go vet` | Catches obvious concurrency mistakes | stdlib |
| `staticcheck` | Detects misuse of channels, sync primitives | https://staticcheck.dev |
| `golangci-lint` | Aggregator (govet, staticcheck, ineffassign) | https://golangci-lint.run |
| `pprof` | Goroutine, mutex, block profiles | `go tool pprof` |
| `goleak` (uber-go) | Goroutine-leak assertions in tests | https://github.com/uber-go/goleak |
| `errcheck` | Catches dropped errors (`_ = job(ctx)`) | https://github.com/kisielk/errcheck |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Datadog APM (Go tracer) | SaaS | Yes | Wrap `Job` in tracer span; goroutine spans propagate via context. |
| OpenTelemetry Go SDK | OSS | Yes | Same pattern, vendor-neutral. |
| Temporal | SaaS + OSS | Yes (Go SDK) | When the worker-pool pattern is reaching for retry/durability — use Temporal instead. |
| NATS / JetStream | OSS | Yes (CLI + SDK) | Pair with bounded worker pool consuming a stream. |
| Kafka (Sarama / segmentio) | OSS | Yes | Same. |
| pgx pool | OSS | Yes | Don't wrap pgx in another pool; tune `MaxConns` instead. |

## Templates & scripts
See `templates.md`. Inline minimal `errgroup` template (preferred over a custom worker pool when "all or none"):

```go
package processor

import (
	"context"
	"golang.org/x/sync/errgroup"
	"golang.org/x/sync/semaphore"
)

func ProcessAll[T any, R any](
	ctx context.Context, items []T, concurrency int64,
	fn func(context.Context, T) (R, error),
) ([]R, error) {
	results := make([]R, len(items))
	sem := semaphore.NewWeighted(concurrency)
	g, gctx := errgroup.WithContext(ctx)

	for i, it := range items {
		i, it := i, it // capture
		if err := sem.Acquire(gctx, 1); err != nil {
			return nil, err
		}
		g.Go(func() error {
			defer sem.Release(1)
			r, err := fn(gctx, it)
			if err != nil {
				return err
			}
			results[i] = r
			return nil
		})
	}
	if err := g.Wait(); err != nil {
		return nil, err
	}
	return results, nil
}
```

## Best practices
- Always pass `context.Context` as the first arg of the worker function and check `ctx.Done()` in tight loops.
- Cap concurrency with a `semaphore.Weighted` instead of an unbounded goroutine fan-out.
- Recover panics in worker goroutines with `defer func() { if r := recover(); r != nil { log... } }()`; one bad panic shouldn't kill the process.
- Capture loop variables explicitly (`i, it := i, it`) until Go 1.22+ is enforced; mistakes here are silent for years.
- Wire structured logging with the trace ID into every spawned goroutine — error logs without correlation are useless.
- Prefer `errgroup.WithContext` over hand-rolled `WaitGroup`+error-channel for "fail fast" semantics.
- Test with `goleak.VerifyNone(t)` in `TestMain` to catch leaks across the suite.
- Use buffered channels deliberately, with size set to the upstream burst; unbuffered is the safer default for backpressure.

## AI-agent gotchas
- Loop-variable capture: pre-Go-1.22, `for _, x := range xs { go func(){ use(x) }() }` captures the same `x`. LLMs trained on older code emit this constantly. Force them to use `x := x` or to declare `range over func`.
- Forgetting `close(jobs)` produces a deadlocked test that hangs CI — set `go test -timeout 30s` and require a teardown step.
- Agents tend to pick `runtime.NumCPU()` as concurrency for IO work; correct value is much higher and depends on remote service tolerances.
- "Drop errors" pattern (`_ = job(ctx)`) is invisible to a reviewer scanning for `if err != nil`; require an explicit error channel or logger call.
- `select` with only `case <-ch:` and `case <-ctx.Done():` is correct; LLMs sometimes add a `default:` that turns it into a busy-loop.
- Mixing `sync.Mutex` and channels on the same shared state — pick one model. Agents often introduce both.
- Human-in-loop checkpoint: any change to channel buffer sizes or worker counts in production should be reviewed with load-test evidence.

## References
- Effective Go (concurrency): https://go.dev/doc/effective_go#concurrency
- Go Concurrency Patterns (Pike): https://go.dev/blog/pipelines
- `errgroup`: https://pkg.go.dev/golang.org/x/sync/errgroup
- `semaphore`: https://pkg.go.dev/golang.org/x/sync/semaphore
- `goleak`: https://github.com/uber-go/goleak
- Race Detector: https://go.dev/doc/articles/race_detector
- Concurrency in Go (Cox-Buday, O'Reilly)
