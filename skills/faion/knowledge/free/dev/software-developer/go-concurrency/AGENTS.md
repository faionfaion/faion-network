---
slug: go-concurrency
tier: free
group: dev
domain: dev
version: 1.0.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-net]
summary: Produces race-free Go concurrency code (worker pool, rate limiter, semaphore, RWMutex cache, errgroup fan-out) where every goroutine has an explicit exit and `go test -race -count=10` passes.
content_id: "go-concurrency-fb05"
complexity: medium
produces: code
est_tokens: 4200
tags: [go, concurrency, channels, goroutines, race-detector]
---
# Go Concurrency Patterns

## Summary

**One-sentence:** Produces race-free Go concurrency code (worker pool, rate limiter, semaphore, RWMutex cache, errgroup fan-out) where every goroutine has an explicit exit and `go test -race -count=10` passes.

**One-paragraph:** Canonical Go concurrency: the goroutine that writes to a channel is the one that closes it; every goroutine has an explicit exit condition (`ctx.Done()`, channel close, or `WaitGroup.Done`); concurrency is bounded by a semaphore sized to downstream capacity (DB pool / API rate-limit), not to `runtime.NumCPU()`; fan-out uses `errgroup.WithContext` to cancel siblings on first error. Every concurrency-heavy package adds `goleak.VerifyTestMain` and runs `go test -race -count>=10` in CI.

**Ефективно для:** new Go services with parallel workloads, refactoring naked-goroutine code to add ctx + leak detection, fixing race-detector findings, sizing rate limiters and worker pools.

## Applies If (ALL must hold)

- Project ships Go code that launches goroutines or uses channels/select.
- CI can run `go test -race -count>=10`.
- Team accepts `errgroup` + `goleak` as dependencies.

## Skip If (ANY kills it)

- Pure sequential code (CLI, single-process script with no goroutines).
- Generated code paths where concurrency is owned by the framework (gRPC server, http.Handler) and no manual goroutines are spawned.
- Tiny prototype where adding goleak overhead exceeds value.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Concurrency budget | int (max simultaneous outbound calls) | infra ADR |
| Downstream capacity | int (DB pool size, rate limit) | infra config |
| Cancellation scope | parent ctx type (request / server-lifetime) | architecture |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `[[go-backend]]` | Provides the Pool struct location and config wiring. |
| `[[go-error-handling]]` | Errors propagated through channels use the same AppError type. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 9 rules: channel ownership, explicit exit, errgroup, semaphore, RWMutex/sync.Map, wg.Add placement, ctx.Done in select, race detector, goleak | ~800 |
| `content/02-output-contract.xml` | essential | Required code patterns + CI invariants (race -count>=10) | ~700 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns: leaky generator, map race, wg.Add inside, close-from-other-goroutine, ctx-less select | ~700 |
| `content/04-procedure.xml` | medium | 5-step concurrency authoring procedure | ~800 |
| `content/06-decision-tree.xml` | essential | Root: "Does the code spawn goroutines or use channels?" | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| Generate Pool / Semaphore scaffold | sonnet | Pattern from templates. |
| Diagnose race-detector finding | opus | Reasoning across multiple goroutines. |
| Size semaphore from downstream | sonnet | Arithmetic + config lookup. |
| Wire goleak TestMain | haiku | Boilerplate. |

## Templates

| File | Purpose |
|------|---------|
| `templates/ci-race.sh` | CI script: `go vet`, `go test -race -count=3`, `staticcheck`. |
| `templates/goleak-test-main.go` | TestMain with goleak.VerifyTestMain for leak detection per package. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-go-concurrency.py` | Greps for known antipatterns (bare `go func()` without ctx, `wg.Add` inside body, `close()` outside writer). | Pre-commit gate. |

## Related

- parent skill: `free/dev/software-developer/`
- `[[go-backend]]` — Pool struct lives in internal/concurrency/
- `[[go-error-handling]]` — error propagation through channels

## Decision tree

The decision tree at `content/06-decision-tree.xml` filters by whether goroutines exist; for code that does, it asks whether ctx cancellation is wired and whether CI runs the race detector.
