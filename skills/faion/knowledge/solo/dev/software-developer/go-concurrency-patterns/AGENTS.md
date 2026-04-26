# Go Concurrency Patterns

## Summary

Safe, leak-free concurrency in Go using bounded worker pools, fan-out/fan-in pipelines, and `context.Context` cancellation. All goroutines have explicit termination paths. Channels have documented ownership (one writer, one closer). `go test -race` is non-negotiable for any concurrent code.

## Why

Go's goroutine model makes concurrent code easy to write but subtle to get right. The most common failures — goroutine leaks, unbounded concurrency, error swallowing, panic propagation, and channel ownership confusion — are invisible until production. Race conditions only manifest under load. Structural patterns (bounded pools, `errgroup`, channel direction types) prevent whole classes of bugs at the type level.

## When To Use

- Fan-out work over goroutines: HTTP request batchers, ETL pipelines, scrapers, queue workers
- CPU-bound parallel processing with `runtime.NumCPU()` workers
- I/O-bound parallel work (HTTP fetches, DB calls) where bounded pools cap concurrency
- Streaming pipelines needing backpressure (bounded channels) and clean shutdown via context

## When NOT To Use

- Single-threaded request handlers — Go's `net/http` already goroutine-per-request; adding pools is overkill
- Trivial sequential loops — concurrency adds complexity (panic recovery, error aggregation) that often outweighs gains
- When `errgroup.Group` already covers the use case — prefer stdlib over hand-rolled pools
- Long-running stateful tasks needing crash recovery — use a real queue (NATS, SQS) instead of in-memory channels

## Content

| File | What's inside |
|------|---------------|
| `content/01-rules.xml` | Goroutine ownership rules, context propagation, error capture, race testing requirements |
| `content/02-examples.xml` | Bounded worker pool and fan-out/fan-in examples with leak-safe Stop() |

## Templates

| File | Purpose |
|------|---------|
| `templates/pool.go` | Leak-safe bounded worker pool with context cancellation and error collection |
