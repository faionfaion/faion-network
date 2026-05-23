---
slug: perf-test-basics
tier: solo
group: dev
domain: sdd
version: 1.0.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Establishes measurable performance baselines (p50/p95/p99 latency + RPS) for service endpoints and detects regressions in CI via load tests, profiling, and benchmarks.
content_id: "00c60a55e984a92c"
complexity: medium
produces: spec
est_tokens: 5000
tags: [performance-testing, load-testing, baselines, profiling, ci-gates]
---
# Performance Testing Basics

## Summary

**One-sentence:** Establishes measurable performance baselines (p50/p95/p99 latency + RPS) for service endpoints and detects regressions in CI via load tests, profiling, and benchmarks.

**One-paragraph:** Establishes measurable performance baselines (p50/p95/p99 latency + RPS) for service endpoints and detects regressions in CI via load tests, profiling, and benchmarks. Decision tree, output contract, failure modes, and a procedure (when complexity ≥ medium) live under `content/`. Templates in `templates/` start with a 5-line `__faion_header__` block; the validator script in `scripts/` is stdlib-only with `--help` and `--self-test`.

**Ефективно для:**

- Service has latency SLOs (e.g. p95 < 300ms) that must be enforced in CI, not just monitored.
- Workload has measurable hot paths (key endpoints, key queries, key functions).
- Team can budget 1-2 days to install baseline + tooling.
- Output produces `spec` matching the schema in `content/02-output-contract.xml`.

## Applies If (ALL must hold)

- Service has latency SLOs (e.g. p95 < 300ms) that must be enforced in CI, not just monitored.
- Workload has measurable hot paths (key endpoints, key queries, key functions).
- Team can budget 1-2 days to install baseline + tooling.

## Skip If (ANY kills it)

- Service is purely batch or asynchronous with no latency SLO.
- Hot paths unknown — instrument first (RUM + tracing).
- Workload too small for load testing to be informative (<10 RPS in prod).

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| SLO definitions | p50/p95/p99 + RPS targets | team |
| Load testing tool | k6 or Locust | infra |
| Profiler | py-spy / clinic.js / pprof | team |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[perf-test-tools]] | tool-specific patterns for k6 + Locust + CI gates |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 7 testable rules (incl. skip-this-methodology) with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid example + invalid example + forbidden traits | 900 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns with symptom + root-cause + fix | 800 |
| `content/04-procedure.xml` | essential | 5-step end-to-end procedure with input/action/output per step | 900 |
| `content/05-examples.xml` | reference | One full worked example end-to-end with the trace and the resulting artefact | 700 |
| `content/06-decision-tree.xml` | essential | Root question + observable branches → conclusion(ref=rule-id); skip leaf always reachable | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `define-baselines` | sonnet | Pick endpoints + targets per SLO. |
| `write-load-test` | sonnet | k6/Locust scripts. |
| `profile-hot-path` | sonnet | Read profiler output, identify hotspots. |

## Templates

| File | Purpose |
|------|---------|
| `templates/baselines.json` | Per-endpoint p95/p99 + RPS baselines |
| `templates/smoke-test.k6.js` | k6 smoke test asserting p95 threshold |
| `templates/_smoke-test.json` | Minimum viable filled-in artefact for sanity-checking the schema. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-perf-test-basics.py` | Validate the produced artefact against the schema in `content/02-output-contract.xml`. | Pre-commit; CI on each artefact change; `--self-test` in dev. |

## Related

- [[perf-test-tools]]
- [[dev-methodologies-architecture]]
- [[best-practices-2026]]

## Decision tree

See `content/06-decision-tree.xml`. Root question: *Does the service have latency SLOs AND known hot paths AND ≥10 RPS?* The tree's purpose is to route an input through observable signals to a conclusion that references a rule from `content/01-core-rules.xml`; the skip-this-methodology branch is always reachable so an inappropriate caller exits cleanly.
