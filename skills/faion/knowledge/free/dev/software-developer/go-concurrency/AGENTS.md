# Go Concurrency Patterns

## Summary

Canonical Go goroutine and concurrency patterns: worker pool, rate limiter, semaphore, `RWMutex` cache, and `sync.Once`. The invariant: every goroutine must have an explicit exit condition (`<-ctx.Done()` or channel close), and the goroutine that writes to a channel is the one that closes it. Tests must pass `go test -race`.

## Why

Agents default to unbounded `for { go work() }` patterns, producing goroutine leaks invisible until production load. Missing context propagation and `WaitGroup.Add`-before-`go` misplacement are the most common silent correctness bugs. The race detector is mandatory but frequently skipped. These patterns encode the channel-ownership rule and leak-prevention idioms explicitly.

## When To Use

- Generating a Go service that processes jobs in parallel (HTTP fan-out, batch ETL, queue consumer).
- Refactoring sequential Go code into a worker pool with bounded concurrency.
- Writing pipelines where stage N feeds stage N+1 via channels.
- Adding context-based cancellation to existing goroutines.
- Building rate limiters or semaphores around external APIs.

## When NOT To Use

- Single-threaded scripts or one-shot CLIs where startup cost dominates.
- Code that needs to share mutable state without a clear ownership boundary — refactor the data model first.
- Pure CPU-bound work with `GOMAXPROCS=1` — goroutines add scheduling overhead with no parallelism.
- When "concurrency" is really async I/O against one source — a single goroutine with `select` suffices.

## Content

| File | What's inside |
|------|---------------|
| `content/01-core-patterns.xml` | Worker pool, rate limiter (token bucket), semaphore channel, `RWMutex` cache, `sync.Once`. |
| `content/02-antipatterns.xml` | Goroutine leak (missing exit), data race on map, channel deadlock — bad/good pairs. |

## Templates

| File | Purpose |
|------|---------|
| `templates/goleak-test-main.go` | `TestMain` with `goleak.VerifyTestMain` for leak detection in every concurrency-heavy package. |
| `templates/ci-race.sh` | CI script: `go vet`, `go test -race -count=3`, `staticcheck`. |
