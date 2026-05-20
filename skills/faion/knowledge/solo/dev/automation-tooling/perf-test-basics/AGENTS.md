---
slug: perf-test-basics
tier: solo
group: dev
domain: automation-tooling
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Establish measurable performance baselines for services and detect regressions in CI.
content_id: "00c60a55e984a92c"
tags: [performance-testing, load-testing, profiling, benchmarking, locust, k6]
---
# Performance Testing Basics

## Summary

**One-sentence:** Establish measurable performance baselines for services and detect regressions in CI.

**One-paragraph:** Establish measurable performance baselines for services and detect regressions in CI. Covers load testing with Locust/k6, function-level profiling with cProfile/py-spy/memray, micro-benchmarks with pytest-benchmark, and N+1 query detection via SQLAlchemy event listeners. The core rule: never optimize without a captured baseline from a dedicated environment.

## Applies If (ALL must hold)

- Establishing a first performance baseline for a service that has none — generating Locust/k6 scripts, capturing p50/p95/p99, error rate, throughput.
- Adding profiling (cProfile, py-spy, memory_profiler) to investigate a localized slowdown.
- Wiring pytest-benchmark micro-benchmarks into CI to gate on regressions for hot paths.
- Detecting and asserting against N+1 queries and slow-query thresholds in tests.
- Writing a CI check that fails the build when p95 latency or error rate breaches a threshold.

## Skip If (ANY kills it)

- For full load-testing tool comparison (k6 vs Locust vs Gatling vs Artillery vs JMeter) — use perf-test-tools/ instead.
- For frontend Web Vitals (LCP, INP, CLS) — that's a Lighthouse/RUM domain, not backend perf.
- For chaos engineering / fault injection — separate discipline (Chaos Mesh, Litmus, Gremlin).
- For continuous production load testing without a safety story — agents should not be flooding prod.
- For trading systems / sub-millisecond latency tuning — needs CPU pinning, NUMA, kernel tuning beyond this scope.
- When the bottleneck is clearly architectural (synchronous calls, single-threaded worker) — fix the architecture first; perf-test second.

## Prerequisites

- TBD — list concrete input artifacts and where they come from

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `TBD/path` | TBD — what upstream output this consumes |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules migrated from v1 methodology | ~800 |
| `content/02-output-contract.xml` | essential | Output schema (stub — fill from v1 patterns) | ~800 |
| `content/03-failure-modes.xml` | essential | Antipatterns migrated from v1 methodology | ~800 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| TBD | sonnet | TBD |

## Templates

| File | Purpose |
|------|---------|
| TBD | TBD |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| TBD | TBD | TBD |

## Related

- parent skill: `solo/dev/automation-tooling/`
