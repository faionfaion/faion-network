# Performance Testing Basics

## Summary

Establish measurable performance baselines for services and detect regressions in CI. Covers load testing with Locust/k6, function-level profiling with cProfile/py-spy/memray, micro-benchmarks with pytest-benchmark, and N+1 query detection via SQLAlchemy event listeners. The core rule: never optimize without a captured baseline from a dedicated environment.

## Why

Without baselines, performance work is guesswork. A single load-test run under realistic concurrency (p50/p95/p99/error-rate/RPS) gives a falsifiable target: "change X should improve p95 by Y ms." pytest-benchmark gates CI against regressions on hot paths. Profiling narrows the hypothesis space before any code changes.

## When To Use

- Establishing a first performance baseline for a service that has none.
- Adding `pytest-benchmark` micro-benchmarks to CI for critical hot paths.
- Profiling a localized slowdown with cProfile, py-spy, or memray.
- Detecting N+1 queries via SQLAlchemy event-listener fixture in tests.
- Writing a CI check that fails when p95 latency or error rate breaches a threshold.

## When NOT To Use

- Full load-tool comparison (k6 vs Locust vs Gatling) — use `perf-test-tools/`.
- Frontend Web Vitals (LCP, INP, CLS) — Lighthouse/RUM domain, not backend perf.
- Chaos engineering / fault injection — separate discipline.
- Sub-millisecond latency tuning (trading systems) — needs CPU pinning and kernel tuning.
- When the bottleneck is clearly architectural — fix the architecture first, perf-test second.
- Never load-test shared production resources; require a staging env allowlist.

## Content

| File | What's inside |
|------|---------------|
| `content/01-test-types.xml` | Load, stress, spike, endurance, scalability test types with purpose and duration. |
| `content/02-profiling.xml` | cProfile decorator, py-spy, memray/tracemalloc usage rules and gotchas. |
| `content/03-benchmarks-and-queries.xml` | pytest-benchmark setup, N+1 detection via SQLAlchemy event listener, CI threshold gates. |

## Templates

| File | Purpose |
|------|---------|
| `templates/query-counter-fixture.py` | SQLAlchemy before_cursor_execute fixture for N+1 assertion in pytest. |
| `templates/perf-threshold-check.py` | CI script to parse load-test JSON results and fail on p95/error-rate breaches. |

## Scripts

none
