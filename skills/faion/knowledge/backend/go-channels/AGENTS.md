# Go Channels and Pipeline Patterns

## Summary

**One-sentence:** Produces a channel topology spec: directional channels, sender-closes rule, select-with-context, buffered-vs-unbuffered choice, pipeline stages with done-channel, race-detector gate.

**Ефективно для:**

- Multi-stage data pipelines (read → transform → emit).
- Fan-out parallel workers with merged results.
- Event-driven producers / consumers within one process.
- Cancellable streams driven by context.

**One-paragraph:** Channels are Go's primary mechanism for communication between goroutines. Use channels to build data pipelines, coordinate multiple goroutines, distribute work to parallel workers, merge results, and manage event-driven systems. Always use `context` for cancellation, close channels from the sender side, and test under `-race` to prevent deadlocks and data races.

## Applies If (ALL must hold)

- Multiple goroutines need to exchange values.
- Cancellation must propagate via context.
- Race detector + goleak available in CI.
- Pipeline stages each have a defined boundary.

## Skip If (ANY kills it)

- Single-producer single-consumer — a simple function call is enough.
- Shared state mutation — use sync primitives, not channels.
- Heavy CPU-bound work — channels add overhead; pin to GOMAXPROCS workers.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Pipeline stage list | design doc | team |
| Cancellation policy (context, deadline) | ADR | tech lead |
| CI runs `go test -race` | CI config | SRE |
| goleak / race report sink | test infra | SRE |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `[[go-goroutines]]` | goroutine semantics |

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
| `draft-pipeline-topology` | sonnet | Stages + channel types from spec. |
| `annotate-cancellation` | haiku | Wires ctx into selects. |
| `audit-leak-and-race` | sonnet | Runs goleak / race reasoning. |

## Templates

| File | Purpose |
|------|---------|
| `templates/go-channels.json` | JSON Schema for the Go Channels and Pipeline Patterns output contract |
| `templates/go-channels.md` | Markdown skeleton with the required fields |
| `templates/_smoke-test.md` | Filled-in minimum viable example of a go-channels record |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-go-channels.py` | Enforce the Go Channels and Pipeline Patterns output contract | After subagent returns, before downstream consumer reads |

## Related

- [[go-goroutines]]
- [[go-concurrency-patterns]]
- [[go-backend]]

## Decision tree

Lives at `content/06-decision-tree.xml`. Two-question gate: (1) preconditions present? (2) does an existing artefact already cover this gap? Routes to run / skip / update. Every conclusion references a rule id from `content/01-core-rules.xml`.
