# Agent Integration — Go Channels & Pipelines

## When to use
- Building staged data pipelines (generate → transform → filter) that must respect cancellation.
- Multiplexing multiple I/O sources / timeouts in a single goroutine via `select`.
- Implementing fan-out (parallel workers) and fan-in (merge results) topologies.
- Broadcasting events to N dynamic subscribers without a message broker.
- Coordinating shutdown across many goroutines via `done` / `ctx.Done()`.

## When NOT to use
- Shared mutable state with random access — use `sync.Mutex` or `sync.Map`; channels are not a database.
- Single-producer/single-consumer with predictable order — a slice + `for` loop is simpler and faster.
- Cross-process communication — use a real queue (Kafka/RabbitMQ/NATS); channels die with the process.
- Replacing function calls with goroutines + channels just to "feel async" — you add scheduling cost, lose stack traces, and gain race-condition risk.

## Where it fails / limitations
- Closing a channel from the wrong side (receiver side) panics; agents conflate "stop reading" with "close".
- `range ch` blocks forever if the producer never closes — the README's anti-pattern is the most common LLM-generated bug.
- Buffered channels mask backpressure; once full, they block silently and the upstream stage stalls.
- The Tee-channel snippet from the README has shadow-name bugs (`out1, out2` rebound inside the loop) — common copy-paste hazard.
- `select` chooses pseudo-randomly; agents that assume priority order (e.g., `done` always wins) write fragile code.
- Goroutine leaks inside fan-in are nearly invisible — workers block on `out <-` forever if the consumer disappeared.

## Agentic workflow
Treat channel topologies as small graphs the agent must diagram (in comments) before coding: sources, stages, sinks, and shutdown signals. Always run `go test -race` and `go vet` after every channel change; the data-race detector catches most concurrency mistakes that escape review. For non-trivial pipelines, ask a reviewer agent to enumerate every goroutine and prove (a) it has an exit condition, (b) something closes its input, (c) the receiver isn't dropped before the sender stops.

### Recommended subagents
- `faion-sdd-executor-agent` — runs the full SDD task; the test gate forces `-race` and `-count=10` reruns.
- A custom `goroutine-auditor` (Opus, read-only) — produces a goroutine inventory: `[goroutine_name, started_at, exit_condition, input_owner, output_owner]` and flags rows missing fields.
- `password-scrubber-agent` — irrelevant here; channel code rarely contains secrets.

### Prompt pattern
```
Build a pipeline with stages: <stage1 → stage2 → stage3>.
Constraints: every stage owns its output channel and closes it on return; every stage takes ctx and exits on ctx.Done(); never close a channel you didn't create; use buffered channels only with a documented capacity rationale.
Deliver: pipeline.go + pipeline_test.go (table-driven, includes a cancellation test).
Run `go test -race -count=10 ./...` and paste the output.
```

```
Audit pipeline.go: list every `go func`. For each row state: who closes the input, who closes the output, what causes exit, max blocked time on send.
Reject if any row has "unknown".
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `go test -race` | Race detector — non-negotiable for channel code | https://go.dev/blog/race-detector |
| `go test -count=N` | Disable test cache, surface flaky concurrency bugs | builtin |
| `go vet` | Catches `unkeyed composite`, `lostcancel` | builtin |
| `staticcheck` | SA1015 (time.After leak), SA4031 (nil channel select) | https://staticcheck.dev/ |
| `pprof` (`/debug/pprof/goroutine`) | Inspect leaked goroutines at runtime | https://pkg.go.dev/net/http/pprof |
| `goleak` (Uber) | Asserts no leaked goroutines at test teardown | https://github.com/uber-go/goleak |
| `gops` | Live goroutine count of a running process | https://github.com/google/gops |
| `delve` | Step-debug goroutines, inspect channel state | https://github.com/go-delve/delve |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| `golang.org/x/sync/errgroup` | OSS | Yes | Replaces ad-hoc `WaitGroup + errCh` in fan-out — agent should default to it. |
| `golang.org/x/sync/semaphore` | OSS | Yes | Use instead of hand-rolled `chan struct{}` semaphores when N is large/dynamic. |
| `eapache/channels` | OSS | Partial | Generic channel utilities (infinite, batching) — useful but extra dep. |
| `nats.io` (in-proc) | OSS | Yes | When the channel pattern outgrows one process, NATS is the smallest jump. |
| Datadog/OTel goroutine metrics | SaaS/OSS | Yes | Track `go_goroutines` to alert on leaks. |
| `goleak` in CI | OSS | Yes | Add `defer goleak.VerifyNone(t)` to every test that spawns goroutines. |

## Templates & scripts
See `templates.md` for pipeline / fan-in / broadcast / orDone snippets. Useful agent regression test (≤30 lines):

```go
// internal/pipeline/leak_test.go
package pipeline_test

import (
    "context"
    "testing"
    "time"

    "go.uber.org/goleak"
)

func TestNoGoroutineLeakOnCancel(t *testing.T) {
    defer goleak.VerifyNone(t)

    ctx, cancel := context.WithCancel(context.Background())
    out := YourPipeline(ctx, []int{1, 2, 3, 4, 5})
    // Read one value, then cancel — make sure all stages unwind.
    <-out
    cancel()

    // Drain any pending values; pipeline must close `out`.
    timeout := time.After(2 * time.Second)
    for {
        select {
        case _, ok := <-out:
            if !ok {
                return
            }
        case <-timeout:
            t.Fatal("pipeline did not close output after cancel")
        }
    }
}
```

## Best practices
- The goroutine that creates a channel owns its close. Document this on every channel-returning function.
- Use `chan<-` and `<-chan` types in signatures so the compiler enforces direction; agents otherwise pass bidirectional channels and accidentally close the input.
- Replace `time.After` inside long-running `select` loops with a reused `time.NewTimer` — `time.After` leaks until the timer fires.
- Prefer `errgroup.WithContext` for fan-out with errors. It cancels siblings on first failure and bounds goroutines.
- Set a buffer capacity only when you can name a backpressure policy ("drop oldest", "block producer for N ms"); otherwise default to unbuffered.
- Add `defer goleak.VerifyNone(t)` (or `goleak.VerifyTestMain`) to test files that spawn goroutines.

## AI-agent gotchas
- LLMs default to `make(chan T)` (unbuffered) but then write `ch <- x` outside any goroutine — instant deadlock. Force `select` or buffered with rationale.
- `select { case <-done: ... default: ... }` is often used to "poll without blocking"; agents put real work in `default` and burn CPU. Reject busy-wait loops in review.
- The Tee snippet's variable shadowing is a known footgun — agents copy it verbatim. Rename inner variables explicitly.
- Agents reach for `sync.Mutex` and `chan` together to "be safe"; the resulting code is both slow and harder to reason about. Pick one model per data structure.
- `nil` channel in `select` blocks forever (intentional pattern, but easy to introduce by accident); flag any `var ch chan T` declaration without a `make`.
- Human-in-loop checkpoint: any new long-lived goroutine (lifetime ≥ request) needs explicit reviewer approval naming the owner, the cancellation source, and the metric/log emitted on exit.

## References
- Pipelines and cancellation — https://go.dev/blog/pipelines
- Context package — https://go.dev/blog/context
- Advanced concurrency patterns talk — https://go.dev/blog/io2013-talk-concurrency
- "Concurrency in Go" (Katherine Cox-Buday) — chapters 4-5.
- goleak — https://github.com/uber-go/goleak
- errgroup — https://pkg.go.dev/golang.org/x/sync/errgroup
