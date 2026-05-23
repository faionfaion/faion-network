# Go Goroutines and Worker Patterns

## Summary

**One-sentence:** Produces a goroutine-lifecycle spec: each goroutine has explicit start + exit; context-driven cancellation; bounded worker pools; goleak-tested; no `go func()` without WaitGroup.

**Ефективно для:**

- Per-request background work (after-response side effects).
- Worker pools serving a task queue.
- Periodic tickers + timers inside a service.
- I/O-bound parallelism (HTTP / DB calls).

**One-paragraph:** Goroutines are lightweight threads managed by the Go runtime. Use them for parallel processing, HTTP servers, background tasks, and I/O-bound work. Key principle: do not share memory; communicate via channels. Keep lock sections small. Avoid leaks by giving every goroutine a defined exit condition. Use `context` for cancellation. Bound parallelism with a worker pool or semaphore.

## Applies If (ALL must hold)

- Caller can give the goroutine a `context.Context` for cancellation.
- Goroutine has a defined exit (channel close, ctx.Done, finite loop).
- Tests run under `-race` and `goleak`.
- Parallelism is bounded by a pool or semaphore.

## Skip If (ANY kills it)

- Synchronous flow is fast enough — no parallelism needed.
- Heavy shared mutable state — single goroutine + queue is safer.
- Tiny tasks (<1µs) — goroutine spawn cost dominates.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Lifecycle owner per goroutine (who waits) | design doc | team |
| Context propagation policy | ADR | tech lead |
| Parallelism cap | ops doc | SRE |
| CI race + goleak gate | CI config | SRE |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `[[go-channels]]` | channel primitives |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 7 testable rules with rationale + source | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid / invalid examples | ~700 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom / root-cause / fix | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure with input / action / output per step | ~900 |
| `content/05-examples.xml` | recommended | one end-to-end worked example | ~600 |
| `content/06-decision-tree.xml` | essential | run / skip router referencing rule ids | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `inventory-goroutines` | sonnet | Finds every `go func()` in code. |
| `annotate-lifecycle` | haiku | Adds WG + ctx to each. |
| `review-leak-risk` | sonnet | Audits exit conditions + bounds. |

## Templates

| File | Purpose |
|------|---------|
| `templates/go-goroutines.json` | JSON Schema for the Go Goroutines and Worker Patterns output contract |
| `templates/go-goroutines.md` | Markdown skeleton with the required fields |
| `templates/_smoke-test.md` | Filled-in minimum viable example of a go-goroutines record |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-go-goroutines.py` | Enforce the Go Goroutines and Worker Patterns output contract | After subagent returns, before downstream consumer reads |

## Related

- [[go-channels]]
- [[go-concurrency-patterns]]
- [[go-backend]]

## Decision tree

Lives at `content/06-decision-tree.xml`. Two-question gate: (1) preconditions present? (2) does an existing artefact already cover this gap? Routes to run / skip / update. Every conclusion references a rule id from `content/01-core-rules.xml`.
