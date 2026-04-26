# Performance Testing

## Summary

A discipline for validating that applications meet latency, throughput, and stability targets under realistic load. Covers five test types (load, stress, spike, endurance, scalability), micro-benchmarking with `pytest-benchmark`, macro load testing with k6/Locust, profiling with py-spy, and CI budget gates that fail PRs on regression.

## Why

Without baselines and automated gates, performance regressions ship silently. Measuring before optimizing prevents wasted effort; coordinated-omission-corrected tools (k6, wrk2, vegeta) surface true tail latency that averages hide. Budget enforcement in CI converts one-off tests into permanent protection.

## When To Use

- Pre-launch validation: API must hold expected RPS at acceptable latency.
- Regression gates after major refactors (ORM swap, query rewrite, caching change).
- Baseline establishment for SLOs (p95 < 300 ms, error rate < 1%).
- Capacity planning before scaling infra.
- Endurance soak tests for memory leaks in long-running services.
- Comparing two implementations (orjson vs json, sync vs async ORM).

## When NOT To Use

- Pre-MVP code — premature optimization wastes effort.
- One-off scripts or batch jobs without a latency contract.
- Pure UI components without measurable backend interactions.
- Without a staging environment that mirrors prod data volume — results are misleading.
- When the bottleneck is obvious (a single N+1 query EXPLAIN shows clearly).

## Content

| File | What's inside |
|------|---------------|
| `content/01-test-types.xml` | Five test types with purpose, duration, and load characteristics. |
| `content/02-benchmarking.xml` | Python micro-benchmarks with pytest-benchmark and DB query profiling. |
| `content/03-antipatterns.xml` | Antipatterns: no baseline, warm-up skipped, profiler + load test combined, local-only runner. |

## Templates

| File | Purpose |
|------|---------|
| `templates/k6-scenario.js` | k6 script with steady + spike scenarios and SLO thresholds. |

## Scripts

| File | Purpose |
|------|---------|
| `scripts/perf-gate.py` | Compare current metrics vs baseline JSON; exit 1 on regression > 5%. |
