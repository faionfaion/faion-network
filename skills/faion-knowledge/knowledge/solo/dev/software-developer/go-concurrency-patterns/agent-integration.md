# Agent Integration — Go Concurrency Patterns

## When to use
- Building services that fan out work over goroutines: HTTP request batchers, ETL pipelines, scrapers, queue workers.
- CPU-bound parallel processing where `runtime.NumCPU()` workers exhaust available cores.
- I/O-bound parallel work (HTTP fetches, DB calls) where bounded worker pools cap concurrency.
- Streaming pipelines that need backpressure (bounded channels) and clean shutdown via `context.Context`.

## When NOT to use
- Single-threaded request handlers — Go's net/http already gives you one goroutine per request; adding pools is overkill.
- Trivial sequential loops — concurrency adds complexity (panic recovery, error aggregation) that often outweighs gains.
- When `errgroup.Group` or `sync/errgroup` already covers the use case — prefer the stdlib over a hand-rolled pool.
- Long-running stateful tasks needing crash recovery — use a real queue (NATS, SQS, RabbitMQ) instead of in-memory channels.

## Where it fails / limitations
- Goroutine leaks: workers blocking on a channel that never closes silently consume memory; `pprof goroutine` is required maintenance.
- Unbounded `chan` use creates memory growth — agents default to unbuffered or `make(chan T, 1000000)` without thinking about backpressure.
- Error swallowing: `_ = job(ctx)` is a common pattern (and present in this methodology's example) — production code needs structured error capture.
- Panic in a worker takes down the whole process unless every goroutine has `defer recover()` — agents rarely add this.
- Race conditions with shared maps/slices that aren't `sync.Mutex`-guarded — the race detector catches most, but only if tests exercise the path.
- Closing a channel from the consumer side panics; closing twice panics. Ownership rules confuse agents.
- `context.Cancel` propagation is forgotten when a worker spawns a child operation with `context.Background()`.

## Agentic workflow
Drive Go concurrency work in a tight loop with `go vet`, `staticcheck`, and `go test -race`. The race detector is non-negotiable for any code touching channels or shared state. Have the agent (1) sketch the goroutine topology (who creates, who closes, who reads, who writes) before writing code, (2) implement with explicit `context.Context` propagation and bounded channels, (3) write a stress test (`for i := 0; i < 10000; i++`) that runs under `-race`, (4) profile with `go test -bench` + `pprof` if the path is hot.

### Recommended subagents
- `go-concurrency-architect` (Sonnet) — produces the channel/goroutine diagram from a feature description; flags ownership ambiguity.
- `go-implementer` (Sonnet/Haiku) — writes the worker pool / fan-out-fan-in / pipeline.
- `go-race-test-writer` (Sonnet) — produces stress tests that exercise contention; runs under `-race -count=10`.
- `go-pprof-analyst` (Sonnet) — runs `pprof` on benchmarks, identifies contention or leaks.

### Prompt pattern
```
Topology first:
- Describe goroutines: producer P, N workers W, single collector C.
- Channels: jobs (P -> W, buffered N), results (W -> C, buffered N).
- Ownership: P closes jobs; sync.WaitGroup gates close(results).
- Cancellation: ctx propagates; all selects include `<-ctx.Done()`.
Then implement; final step: `go test -race -count=10 -run TestWorkerPool ./...`.
```

```
Audit: review pkg/processor for goroutine leaks.
Steps:
1. Identify every `go func()` call site.
2. For each, prove a termination path (channel close, ctx.Done, timeout).
3. Add a `runtime.NumGoroutine()` guard test that asserts no leak after Stop().
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `go test -race` | Race detector — mandatory | Built-in |
| `go vet` | Stdlib static analysis | Built-in |
| `staticcheck` | Deeper lints, includes concurrency rules | `go install honnef.co/go/tools/cmd/staticcheck@latest` |
| `golangci-lint` | Aggregator (vet + staticcheck + others) | https://golangci-lint.run |
| `go test -bench` + `pprof` | CPU/heap/goroutine profiles | Built-in |
| `dlv` (Delve) | Debugger | `go install github.com/go-delve/delve/cmd/dlv@latest` |
| `golang.org/x/sync/errgroup` | Bounded errgroup | `go get golang.org/x/sync/errgroup` |
| `golang.org/x/sync/semaphore` | Weighted limiter | `go get golang.org/x/sync/semaphore` |
| `goleak` (Uber) | Leak detection in tests | `go get go.uber.org/goleak` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| pkg.go.dev | OSS docs | Yes | Authoritative API reference |
| Honnef.co/go/tools | OSS | Yes via CLI | staticcheck, simple, gosimple |
| Sourcegraph | SaaS / OSS | Yes via API | Cross-repo Go code search for pattern reuse |
| OpenTelemetry Go SDK | OSS | Yes | `runtime/metrics` exporter shows goroutine counts |
| pprof.me | SaaS | Yes | Continuous profiling for prod |
| Grafana Pyroscope | OSS / SaaS | Yes | Go agent ships goroutine + cpu profiles |

## Templates & scripts
See `templates.md`. The README's worker-pool example has a concurrency bug worth fixing — here's a corrected, leak-safe version (≤50 lines):

```go
// pkg/worker/pool.go
package worker

import (
	"context"
	"sync"
)

type Job func(ctx context.Context) error

type Pool struct {
	jobs   chan Job
	wg     sync.WaitGroup
	cancel context.CancelFunc
	errs   chan error
}

func NewPool(ctx context.Context, workers, buffer int) *Pool {
	ctx, cancel := context.WithCancel(ctx)
	p := &Pool{
		jobs:   make(chan Job, buffer),
		errs:   make(chan error, buffer),
		cancel: cancel,
	}
	for i := 0; i < workers; i++ {
		p.wg.Add(1)
		go func() {
			defer p.wg.Done()
			defer func() { _ = recover() } // do not crash on panic
			for {
				select {
				case <-ctx.Done():
					return
				case job, ok := <-p.jobs:
					if !ok {
						return
					}
					if err := job(ctx); err != nil {
						select {
						case p.errs <- err:
						default:
						}
					}
				}
			}
		}()
	}
	return p
}

func (p *Pool) Submit(j Job)        { p.jobs <- j }
func (p *Pool) Errors() <-chan error { return p.errs }
func (p *Pool) Stop() {
	close(p.jobs)
	p.wg.Wait()
	close(p.errs)
	p.cancel()
}
```

## Best practices
- Define channel ownership: one writer, one closer. Document in a comment near the channel declaration.
- Always `select` on `ctx.Done()` in any blocking receive/send inside a worker.
- Use `errgroup.WithContext` instead of hand-rolling for fan-out: it cancels siblings on first error.
- Bound concurrency with `errgroup.SetLimit` or `semaphore.Weighted` — never spawn `len(items)` goroutines blindly.
- Avoid sharing mutable state across goroutines; pass via channels or use `sync.Mutex`/`sync.RWMutex` deliberately.
- For pipelines, use the `<-chan T` (read-only) and `chan<- T` (write-only) types in function signatures to enforce direction.
- Add `goleak.VerifyTestMain(m)` to test packages that touch goroutines.
- Run `go test -race -count=N` (N≥10) for any test exercising concurrent code paths.

## AI-agent gotchas
- Agents reach for unbuffered channels by default; ensure they think about buffer size and backpressure semantics.
- "Forgotten" `defer wg.Done()` is the most common bug from LLM-generated code — review for it explicitly.
- `for range jobs { ... }` looks clean but skips the `<-ctx.Done()` path; agents need a nudge to use `select`.
- Agents close channels in workers (wrong) instead of producers; review channel close site every time.
- LLM-written goroutines often capture loop variables incorrectly (pre-1.22 semantics) — set `go 1.22` in `go.mod` to fix at language level.
- Agents conflate `errgroup` and `sync.WaitGroup` and add both — pick one per construct.
- Worker pools without graceful shutdown: `pool.Stop()` returning while jobs still in flight. Require `wg.Wait()` after channel close.
- Human-in-loop checkpoint: any code path that spawns goroutines from inside a request handler needs review for per-request leaks.

## References
- https://go.dev/blog/pipelines
- https://pkg.go.dev/golang.org/x/sync/errgroup
- https://github.com/golang/go/wiki/CodeReviewComments#concurrency
- https://go.dev/ref/mem (Go memory model)
- https://github.com/uber-go/goleak
- https://www.oreilly.com/library/view/concurrency-in-go/9781491941294/ (Cox-Buday)
- https://github.com/lotusirous/go-concurrency-patterns
- https://go.dev/doc/effective_go#concurrency
