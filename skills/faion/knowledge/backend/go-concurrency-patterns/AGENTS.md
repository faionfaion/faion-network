# Go Concurrency Patterns (Worker Pool, Fan-Out/Fan-In, errgroup, Pipeline)

## Summary

**One-sentence:** Produces a per-task concurrency-pattern spec: worker pool (IO-bound), fan-out/fan-in (CPU-bound), errgroup + semaphore (fail-fast), pipeline (streaming). Context propagation + panic recovery + goleak test mandatory.

**Ефективно для:**

- Bulk HTTP calls to external APIs (IO-bound).
- Parallel CPU-heavy transformations.
- Fail-fast batch jobs that must abort on first error.
- Streaming readers → transformers → writers.

**One-paragraph:** Four battle-tested Go concurrency primitives — worker pool, fan-out/fan-in, `errgroup` with semaphore, and pipeline — selected by workload type (IO-bound vs CPU-bound vs streaming vs fail-fast). Every pattern requires context propagation, panic recovery, and a goleak-based goroutine-leak test.

## Applies If (ALL must hold)

- Workload is parallelisable.
- Tasks accept a context for cancellation.
- CI runs goleak + race detector.
- Bound on max parallelism is documented.

## Skip If (ANY kills it)

- Single-task synchronous flow — no concurrency needed.
- Tasks share large mutable state — single goroutine + queue is simpler.
- Latency budget < goroutine spawn cost (~µs) — inline.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Workload classification (IO/CPU/streaming/fail-fast) | design doc | tech lead |
| Max parallelism bound | ops doc | SRE |
| CI gates (race + goleak) | CI config | SRE |
| Per-task timeout policy | ADR | tech lead |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `[[go-channels]]` | channel primitives |
| `[[go-goroutines]]` | goroutine basics |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 10 testable rules with rationale + source | ~1300 |
| `content/02-output-contract.xml` | essential | artefact JSON Schema + code-shape contract + valid / invalid examples + forbidden code shapes | ~1300 |
| `content/03-failure-modes.xml` | essential | 6 antipatterns with symptom / root-cause / fix | ~1100 |
| `content/04-procedure.xml` | essential | 5-step artefact procedure + 5-step implementation sub-procedure | ~1400 |
| `content/05-examples.xml` | recommended | one end-to-end worked example | ~600 |
| `content/06-decision-tree.xml` | essential | run / skip router referencing rule ids | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `classify-task` | haiku | Matrix lookup IO/CPU/streaming/fail-fast. |
| `draft-pattern` | sonnet | Generates pattern code with ctx + recovery. |
| `review-leak-and-bound` | sonnet | Audits semaphore + goleak presence. |

## Templates

| File | Purpose |
|------|---------|
| `templates/go-concurrency-patterns.json` | JSON Schema for the Go Concurrency Patterns (Worker Pool, Fan-Out/Fan-In, errgroup, Pipeline) output contract |
| `templates/go-concurrency-patterns.md` | Markdown skeleton with the required fields |
| `templates/_smoke-test.md.j2` | Filled-in minimum viable example of a go-concurrency-patterns record |
| `templates/_smoke-test.md` | Filled-in minimum viable example of a go-concurrency-patterns record Generated from `templates/_smoke-test.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/pool.go` | Leak-safe bounded worker pool: context cancellation, panic recovery, error collection, sender-owned close |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-go-concurrency-patterns.py` | Enforce the Go Concurrency Patterns (Worker Pool, Fan-Out/Fan-In, errgroup, Pipeline) output contract | After subagent returns, before downstream consumer reads |

## Related

- [[go-channels]]
- [[go-goroutines]]
- [[go-backend]]
- [[go-error-handling-patterns]]

## Decision tree

Lives at `content/06-decision-tree.xml`. Two-question gate: (1) preconditions present? (2) does an existing artefact already cover this gap? Routes to run / skip / update. Every conclusion references a rule id from `content/01-core-rules.xml`.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/go-concurrency-patterns.json`

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://faion.network/schema/go-concurrency-patterns.json",
  "type": "object",
  "required": [
    "artefact_id",
    "owner",
    "decision",
    "rationale",
    "inputs_used",
    "version",
    "last_reviewed"
  ],
  "properties": {
    "artefact_id": {
      "type": "string",
      "pattern": "^gocp\\-[a-z0-9-]+$"
    },
    "owner": {
      "type": "string",
      "minLength": 1,
      "pattern": "^(?!team$|we$|us$|engineering$)"
    },
    "decision": {
      "type": "string",
      "minLength": 4
    },
    "rationale": {
      "type": "string",
      "minLength": 60
    },
    "inputs_used": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "object",
        "required": [
          "name",
          "source"
        ],
        "properties": {
          "name": {
            "type": "string"
          },
          "source": {
            "type": "string"
          }
        }
      }
    },
    "status": {
      "type": "string",
      "enum": [
        "pending",
        "active",
        "deprecated"
      ]
    },
    "version": {
      "type": "string",
      "pattern": "^\\d+\\.\\d+\\.\\d+$"
    },
    "last_reviewed": {
      "type": "string",
      "format": "date"
    },
    "notes": {
      "type": "string"
    }
  }
}
```
