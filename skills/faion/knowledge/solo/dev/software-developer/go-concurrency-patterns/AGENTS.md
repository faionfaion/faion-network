---
slug: go-concurrency-patterns
tier: solo
group: dev
domain: dev
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Implement safe, leak-free Go concurrency via bounded worker pools, fan-out/fan-in pipelines, and context-cancellation throughout.
content_id: "07220ddb2d1d598e"
complexity: medium
produces: code
est_tokens: 4000
tags: [go, concurrency, goroutines, channels, patterns]
---
# Go Concurrency Patterns

## Summary

**One-sentence:** Implement safe, leak-free Go concurrency via bounded worker pools, fan-out/fan-in pipelines, and context-cancellation throughout.

**One-paragraph:** Every concurrent Go path uses bounded worker pools (no unbounded goroutine spawns), passes context.Context for cancellation, closes channels on the sender side, and pairs each goroutine with a deterministic exit signal. Fan-out/fan-in is the canonical pipeline shape; errgroup.WithContext coordinates worker shutdown on first error. Output is concurrent code + lifecycle invariants documented at the package level.

**Ефективно для:**

- Backend services with parallelisable I/O or CPU work.
- Replacing ad-hoc `go func()` calls with bounded pools.
- Refactoring leaking pipelines that build up goroutines under load.
- Adding cancellation to existing long-running operations.

## Applies If (ALL must hold)

- Go 1.21+ project with measurable concurrent work.
- Service handles concurrent requests or processes bounded queues.
- Code touches I/O (HTTP, DB, message queue) where parallelism reduces latency.
- Goroutine leaks have been observed or are a real risk (pprof shows growth).

## Skip If (ANY kills it)

- Service is sequential with no I/O parallelism opportunity.
- Concurrency is delegated to a framework (gqlgen DataLoader, etc.) that owns the pool.
- Project uses an alternative runtime model (work stealing, async runtime).
- Single-shot CLI where complexity exceeds payoff.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Workload description: producer rate, consumer cost, latency budget | doc | tech-lead |
| pprof goroutine profile of current state (if refactoring) | profile | ops |
| Cancellation source: HTTP context, signal handler, parent context | code | tech-lead |
| errgroup or sync/x packages available (golang.org/x/sync) | dep | platform |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[go-error-handling-patterns]] | Worker errors propagate through errgroup. |
| [[logging-patterns]] | Pool lifecycle events log structured fields. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules (bounded pool, context everywhere, channel closed by sender, no goroutine without exit signal, fan-out-fan-in pipeline, errgroup for first-error) | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema for concurrent code module spec + valid/invalid examples | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom/root-cause/fix | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure: workload sketch → pool sizing → pipeline shape → cancellation → leak audit | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree → rule from 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `pool_design` | opus | Pool sizing + backpressure decisions need deep synthesis. |
| `pipeline_assembly` | sonnet | Mechanical fan-out/fan-in wiring. |
| `cancellation_plumbing` | sonnet | Thread context through call sites. |
| `leak_audit` | sonnet | Run pprof and identify goroutine accumulators. |

## Templates

| File | Purpose |
|------|---------|
| `templates/pool.go` | Bounded worker pool with context cancellation + errgroup coordination |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-go-concurrency-patterns.py` | Validate concurrent code module spec against 02-output-contract schema | Pre-publish gate / pre-commit |

## Related

- [[go-error-handling-patterns]]
- [[logging-patterns]]
- [[performance-testing]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps workload type, framework ownership, and observed leaks to a rule from `01-core-rules.xml`, telling the agent whether to apply Go concurrency patterns or skip when the runtime already owns the model. Walk it on every fresh invocation; do not memo-ise outcomes across distinct engagements.
