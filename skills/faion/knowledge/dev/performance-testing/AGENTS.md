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

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

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

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-performance-testing.py` | Validate the artefact against `content/02-output-contract.xml` schema. | After draft, before merge; pre-commit. |
| `scripts/perf-gate.py` | Compare a current k6 summary vs baseline and fail when a tracked metric regresses beyond tolerance. | In CI after a load run, before merge; supports `--self-test`. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[sql-optimization]]
- [[rate-limiting]]
- [[caching-strategy]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs - SLO present?, staging fidelity, test type, regression vs SLO - onto a rule from `content/01-core-rules.xml`. Use it before drafting the test plan: it decides apply-vs-skip, picks the correct test type, and routes regressions to the CI gate.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/k6-scenario.js`

```javascript
import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  scenarios: {
    steady: {
      executor: 'constant-arrival-rate',
      rate: 500, timeUnit: '1s', duration: '10m',
      preAllocatedVUs: 200, maxVUs: 500,
    },
  },
  thresholds: {
    http_req_duration: ['p(95)<300', 'p(99)<800'],
    http_req_failed: ['rate<0.01'],
  },
  discardResponseBodies: true,
};

export default function () {
  const r = http.get('https://staging.example.com/api/users/123');
  check(r, { 'status 200': (res) => res.status === 200 });
}
```

### `templates/baseline.json`

```json
{
  "git_sha": "REPLACE",
  "env": "staging",
  "dataset_size_rows": 1000000,
  "p50_ms": 110,
  "p95_ms": 240,
  "p99_ms": 470,
  "rps": 500,
  "error_rate": 0.002
}
```

### `templates/_smoke-test.json`

```json
{
  "test_type": "load",
  "slo": {
    "p95_ms": 300,
    "rps": 500,
    "error_rate_ceiling": 0.01
  },
  "baseline_sha": "deadbeef",
  "results": {
    "p50_ms": 100,
    "p95_ms": 200,
    "p99_ms": 400,
    "rps": 500,
    "error_rate": 0.001
  },
  "verdict": "pass"
}
```
