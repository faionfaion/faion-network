---
slug: perf-test-tools
tier: solo
group: dev
domain: sdd
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Load and stress testing using k6 (JavaScript, single binary) and Locust (Python, web UI), with CI/CD performance gates that block PRs introducing latency regressions.
content_id: "4632371c5cd50312"
tags: [performance-testing, load-testing, k6, locust, ci-gates, threshold-monitoring]
---
# Performance Testing Tools: k6 and Locust

## Summary

**One-sentence:** Load and stress testing using k6 (JavaScript, single binary) and Locust (Python, web UI), with CI/CD performance gates that block PRs introducing latency regressions.

**One-paragraph:** Load and stress testing using k6 (JavaScript, single binary) and Locust (Python, web UI), with CI/CD performance gates that block PRs introducing latency regressions. The concrete rule: run a 30-second smoke at 5 VUs before any real test — if smoke fails, fix the script, not the system under test.

## Applies If (ALL must hold)

- Establishing a baseline load test for a new HTTP API before first production rollout.
- Adding CI perf gates that block PRs introducing more than 10% latency regression.
- Capacity planning: finding the knee by ramping VUs at increasing targets.
- Reproducing a production incident with a scripted realistic scenario.
- Comparing two implementations (rewrite, ORM swap) under identical synthetic load.

## Skip If (ANY kills it)

- Functional bugs — perf tools don't surface logic errors, just timing/throughput.
- Frontend UX perf — use Lighthouse, WebPageTest, Playwright tracing instead.
- Pre-MVP products with no defined SLOs — you'll measure noise.
- Single-shot benchmarks of pure functions — use pytest-benchmark / vitest bench.
- Tests against shared staging environments — results are unreproducible due to neighbour load.

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
