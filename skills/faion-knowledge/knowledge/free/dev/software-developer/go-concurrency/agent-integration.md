# Agent Integration — Go Goroutines & Worker Patterns

## When to use
- Agent generates a Go service that processes jobs in parallel (HTTP fan-out, batch ETL, queue consumer).
- Refactoring sequential Go code into a worker pool with bounded concurrency.
- Writing pipelines where stage N feeds stage N+1 via channels.
- Adding context-based cancellation to existing goroutines.
- Building rate limiters / semaphores around external APIs.

## When NOT to use
- Single-threaded scripts or one-shot CLIs where startup cost dominates.
- Code that needs to share mutable state across goroutines without a clear ownership boundary — refactor data model first.
- Pure CPU-bound number crunching with `GOMAXPROCS=1`; goroutines add scheduling overhead with no parallelism.
- When the "concurrency" is really just async I/O against one source — a single goroutine with `select` is enough.

## Where it fails / limitations
- Agents tend to write goroutines without exit conditions, causing leaks invisible until production.
- LLMs frequently miss `context.Context` propagation through nested calls.
- `sync.WaitGroup` misuse: `wg.Add` after `go func` (race), or missing `Done()` on panic path.
- Channels are easy to deadlock — closed-channel sends, unbuffered without ready receiver, nil channels in `select`.
- `go test -race` is mandatory but agents skip it; correctness "looks right" until under load.

## Agentic workflow
Drive Go concurrency with a focused subagent that owns a single package: it writes the goroutine pattern, runs `go test -race -count=10`, runs `go vet`, then captures the diff. A second subagent reviews for leak vectors (every `go func()` must answer "what cancels it?"). Use a senior model (Opus/Sonnet-4) for design (channel topology, ownership rules) and a cheap model for boilerplate (struct definitions, signature stubs). Always include the `-race` flag in the test command — without it concurrency bugs ship green.

### Recommended subagents
- `faion-sdd-executor-agent` — implements the pattern from a spec, runs the race detector, blocks on lint failures.
- A custom `go-reviewer` subagent (not yet shipped) — instructed to scan only for: missing `ctx.Done()`, unbuffered-channel deadlock risk, `WaitGroup.Add` placement, leaked tickers/timers, missing `defer close(ch)`.

### Prompt pattern
```
Implement <pattern> in package <pkg>. Constraints:
1. Every goroutine must have an explicit exit on `<-ctx.Done()`.
2. The function returning a channel must own its close.
3. Tests must pass with `go test -race -count=10 ./...`.
Reject any solution that uses bare `go func()` without ctx or WaitGroup tracking.
```

```
Review the diff. For each `go` keyword answer: who cancels it? who closes the channels it writes? Block PR if any answer is "unclear".
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `go test -race` | Built-in data race detector | https://go.dev/blog/race-detector |
| `go vet` | Static analysis incl. lock copying, struct tags | bundled with Go |
| `staticcheck` | Deep linter (SA codes for concurrency bugs) | https://staticcheck.dev |
| `golangci-lint` | Aggregator (govet + staticcheck + gocritic + errcheck) | https://golangci-lint.run |
| `goleak` (uber-go) | Asserts no goroutine leaks at test end | https://github.com/uber-go/goleak |
| `pprof` (go tool pprof) | Goroutine/heap/CPU profiling | bundled |
| `delve` (`dlv`) | Debugger with goroutine inspection | https://github.com/go-delve/delve |
| `errgroup` (x/sync) | `sync.WaitGroup` + first-error propagation | https://pkg.go.dev/golang.org/x/sync/errgroup |
| `semaphore` (x/sync) | Weighted semaphore | https://pkg.go.dev/golang.org/x/sync/semaphore |
| `singleflight` (x/sync) | Deduplicate concurrent identical calls | https://pkg.go.dev/golang.org/x/sync/singleflight |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| GitHub Actions | SaaS | yes | Run `go test -race` matrix on every PR; agents read logs via `gh run view`. |
| Datadog APM Go tracer | SaaS | partial | Goroutine and contention metrics; agents can query via `dd-cli` for incident investigation. |
| Grafana Pyroscope | OSS | yes | Continuous profiling; agents can compare goroutine count between revisions. |
| temporal.io | SaaS+OSS | yes | When channel-based concurrency outgrows itself, move to durable workflows; Go SDK pairs well with agent-generated activities. |
| Asynq | OSS | yes | Redis-backed task queue (Go) for jobs that exceed in-process worker pool. |

## Templates & scripts
See `templates.md` for full pattern stubs. Inline minimal goroutine-leak guard for test files:

```go
package mypkg_test

import (
    "testing"
    "go.uber.org/goleak"
)

func TestMain(m *testing.M) {
    goleak.VerifyTestMain(m)
}
```

Add to every concurrency-heavy package; agent must include this when generating `_test.go` files.

CI snippet enforcing race detector + leak detection:

```bash
#!/usr/bin/env bash
set -euo pipefail
go vet ./...
go test -race -count=3 -timeout=120s ./...
go run honnef.co/go/tools/cmd/staticcheck@latest ./...
```

## Best practices
- Channel-ownership rule: the goroutine that writes to a channel is the one that closes it. No exceptions.
- `errgroup.WithContext` over hand-rolled `WaitGroup + errCh` for fan-out — kills siblings on first error automatically.
- Bound concurrency with a buffered semaphore channel sized to downstream capacity (DB pool, API rate limit), not to `runtime.NumCPU()`.
- Pass `context.Context` as the first parameter, never store it in a struct (except `http.Server` style request-scoped helpers).
- Use `sync.Pool` only after `pprof` shows allocation pressure; misused it slows code down.
- Prefer `time.After` only inside `select` with cancellation; otherwise it leaks until the timer fires.
- For shutdown, `context.WithCancel` at top of main + `signal.NotifyContext` for SIGINT/SIGTERM. Agents tend to forget signal hookup.

## AI-agent gotchas
- LLMs default to `for { go work() }` patterns — unbounded goroutines. Always require explicit pool size in the prompt.
- Agents copy stale 2017 patterns: `WaitGroup` without `errgroup`, manual error channels with leaks. Anchor prompts to Go ≥1.21 idioms (`errgroup`, `slog`, `context.WithCancelCause`).
- LLMs misuse `select` with `default:` branches, turning blocking sends into silent drops. Require explicit comment on every `default:`.
- Code generated for `sync.Map` is often wrong fit — only useful when keys are write-once and reads dominate; otherwise `sync.RWMutex` + `map`.
- Human-in-loop checkpoint: review the channel topology diagram (or ASCII description) before code is written. Agents will happily generate fan-out where you wanted pipeline.
- When agent edits an existing file with goroutines, force a re-run of `-race` even if no concurrency-looking code changed — closures capture surrounding scope.

## References
- https://go.dev/blog/pipelines — Go concurrency patterns: pipelines and cancellation
- https://go.dev/blog/context — Go concurrency patterns: context
- https://go.dev/ref/mem — The Go memory model
- https://github.com/uber-go/goleak — Goroutine leak detector
- https://github.com/golang/go/wiki/CommonMistakes — Common goroutine mistakes
- Bryan Mills, "Rethinking Classical Concurrency Patterns" (GopherCon 2018) — https://www.youtube.com/watch?v=5zXAHh5tJqQ
