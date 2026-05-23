---
slug: performance-testing
tier: solo
group: dev
domain: dev
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Performance test plan + verdict report covering five test types (load, stress, spike, endurance, scalability), SLO-gated CI, coordinated-omission-corrected tooling, and baseline-vs-current comparison.
content_id: "a1999fabdcbbb35d"
complexity: medium
produces: report
est_tokens: 5200
tags: [performance, load-testing, k6, slo, benchmarking]
---
# Performance Testing

## Summary

**One-sentence:** Performance test plan + verdict report covering five test types (load, stress, spike, endurance, scalability), SLO-gated CI, coordinated-omission-corrected tooling, and baseline-vs-current comparison.

**One-paragraph:** Performance testing without an SLO produces data without a verdict; without a baseline it produces no regression signal; without coordinated-omission correction it underreports tail latency. This methodology forces an explicit SLO (p50, p95, p99, RPS, error rate), a committed baseline (git SHA + dataset size + env), and the test-type matrix (load/stress/spike/endurance/scalability) before any run. Output is a performance report comparing current metrics against baseline + SLO with a pass/fail verdict per test type. CI gates on regression.

**Ефективно для:**

- Перед launch - треба підтвердити що API тримає очікуваний RPS.
- Після ORM свопу / query rewrite - regression gate.
- Capacity planning - встановити baseline перед scaling.
- Endurance soak - підозра на memory leak в long-running service.
- Порівняння двох імплементацій (orjson vs json, sync vs async).

## Applies If (ALL must hold)

- API or service has a latency / throughput contract (SLO documented).
- Staging environment exists with production-equivalent data volume.
- CI infrastructure can run load tests (k6 / wrk2 / vegeta).
- A named owner can sign off pass/fail verdicts.

## Skip If (ANY kills it)

- Code is pre-MVP - premature optimisation wastes effort.
- One-off script or batch job without a latency contract.
- Pure UI component without measurable backend interactions.
- No staging env that mirrors production volume - results misleading.
- Bottleneck is already obvious (one EXPLAIN clearly shows N+1).

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| SLO targets | p50/p95/p99 + RPS + error-rate ceiling | product owner |
| Baseline metrics | .perf/baseline.json with git SHA | engineering |
| Staging environment | production-equivalent data + infra | platform |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[rate-limiting]] | limits informing maximum load test target. |
| [[sql-optimization]] | consumer of report findings on slow queries. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 7 rules: SLO before test, baseline committed, CO-corrected tools, prod-like staging, warmup discarded, test type explicit, regression gate | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns (symptom/root-cause/fix) | ~800 |
| `content/04-procedure.xml` | essential | 5-step plan: SLO, baseline, test type, run, gate | ~900 |
| `content/05-examples.xml` | essential | Worked example for a checkout endpoint load test | ~900 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule id | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `author-slo` | sonnet | Numeric targets with business context. |
| `write-k6-scenario` | haiku | Boilerplate scenario file. |
| `interpret-results` | sonnet | Cross-reference SLO + baseline + verdict. |
| `regression-root-cause` | opus | Stakes high when failing PR blocks release. |

## Templates

| File | Purpose |
|------|---------|
| `templates/k6-scenario.js` | k6 load-test scenario with steady + spike stages and SLO thresholds. |
| `templates/baseline.json` | Baseline metrics committed under .perf/baseline.json. |
| `templates/_smoke-test.json` | Minimum viable verdict report for validator smoke-test. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-performance-testing.py` | Validate the artefact against `content/02-output-contract.xml` schema. | After draft, before merge; pre-commit. |

## Related

- [[sql-optimization]]
- [[rate-limiting]]
- [[caching-strategy]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs - SLO present?, staging fidelity, test type, regression vs SLO - onto a rule from `content/01-core-rules.xml`. Use it before drafting the test plan: it decides apply-vs-skip, picks the correct test type, and routes regressions to the CI gate.
