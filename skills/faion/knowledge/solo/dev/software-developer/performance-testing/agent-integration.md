# Agent Integration — Performance Testing

## When to use
- Pre-launch validation: API/web app must hold expected RPS at acceptable latency.
- Regression gates after major refactors (ORM swap, query rewrite, caching change).
- Baseline establishment for SLOs (p95 < 300 ms, error rate < 1%).
- Capacity planning before scaling infra (faion-net cx53 → cx63 decision).
- Endurance soak tests for memory leaks in long-running services (n8n, neromedia pipeline).
- Comparing two implementations (orjson vs json, sync vs async ORM, Redis vs in-process cache).

## When NOT to use
- Pre-MVP code — premature optimization is wasted effort.
- One-off scripts or batch jobs without latency contract.
- Pure UI components without measurable backend interactions.
- Without a staging environment that mirrors prod data volume — results are misleading.
- When the bottleneck is obvious (a single N+1 query that explain shows clearly).

## Where it fails / limitations
- Local-only load tests are bottlenecked by client; need distributed runners (k6 cloud, Locust workers) for >10k RPS.
- Synthetic traffic doesn't replay real distributions — skews toward equal-weight endpoints.
- Cold cache vs warm cache — first-run results vastly differ; always warm before measuring.
- JIT (PyPy, Node V8 deopt) plus DB query planner stats cause non-stationary results.
- Profilers add overhead (10-30%) — never profile + load test simultaneously.
- Browser-based perf (Lighthouse, Web Vitals) is noisy on a single run; require N=10+ medians.
- Memory leak detection requires hours-long soak; agents impatient and run 5-min tests.
- Network conditions — testing on the same host as the server hides latency the user will see.

## Agentic workflow
Drive perf work as: (1) define SLO/budget upfront (latency p95, RPS, error rate), (2) establish baseline on stable build, (3) run targeted scenarios (load / spike / soak), (4) collect metrics + flame graphs, (5) identify top-N bottlenecks, (6) fix one at a time, re-test, (7) commit budgets to CI as gates. Agents should never "optimize blindly" — every change requires before/after numbers in the commit body. Use `pytest-benchmark --benchmark-compare` for micro, k6/Locust for macro, py-spy/pprof for flame graphs.

### Recommended subagents
- `faion-sdd-executor-agent` — wraps perf work under SDD gates, enforces baseline-fix-retest loop.
- `faion-software-architect-agent` — picks scenarios + interprets bottlenecks (DB, network, CPU, GC).
- `faion-browser-agent` — drives k6/Lighthouse from CLI (despite the name).
- `feature-executor` — orchestrates baseline → optimize → verify as discrete tasks.

### Prompt pattern
```
Define SLO for endpoint <method> <path> based on PRD: latency p50, p95,
p99, RPS sustained, error rate ceiling. Output as YAML:
  slo: {p50_ms:..., p95_ms:..., p99_ms:..., rps:..., error_rate:...}
  scenario: {ramp_up:..., steady_state:..., ramp_down:...}
Stop. Wait for human approval of SLO before running tests.
```

```
Run k6 with the approved scenario at scripts/perf/<endpoint>.js against
staging. Save results to .perf/<date>/. Compare against
.perf/baseline.json. Fail if any threshold regresses by >5%.
On regression, generate py-spy flame graph for top 3 slow paths and
explain delta vs baseline.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `k6` | Modern JS-script load testing | https://k6.io/docs |
| `locust` | Python load testing, web UI | pip install locust |
| `wrk` / `wrk2` | Constant-rate HTTP benchmarking | apt install wrk |
| `hey` | Lightweight Apache Bench replacement | go install github.com/rakyll/hey |
| `vegeta` | Constant-RPS, JSON+plot output | go install github.com/tsenart/vegeta |
| `pytest-benchmark` | Python micro-benchmarks with stats | pip install pytest-benchmark |
| `py-spy` | Sampling profiler for Python (no instrumentation) | pip install py-spy |
| `pprof` (Go) | CPU + memory profiling | bundled in Go |
| `perf` / `flamegraph.pl` | Linux perf events → flamegraph | apt install linux-tools |
| `lighthouse` | Web Vitals + perf audit | npm i -g lighthouse |
| `sitespeed.io` | Web perf + browser metrics | npm i -g sitespeed.io |
| `criterion.rs` | Rust micro-benchmark with stats | cargo add criterion |
| `hyperfine` | Shell command benchmark with warmup | cargo install hyperfine |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Grafana k6 Cloud | SaaS | yes (CLI) | Distributed runners + dashboards. |
| Grafana Cloud / OSS | SaaS+OSS | yes | Pair with Prometheus/Loki for live dashboards during runs. |
| Datadog APM / NR APM | SaaS | yes (agents + API) | Trace + flamegraph during load tests. |
| Sentry Performance | SaaS | yes | Spans + p95 latency tracking from prod. |
| BlazeMeter | SaaS | yes | Hosted JMeter / Gatling / Taurus. |
| Speedscope | OSS | yes | Local flame graph viewer for py-spy/pprof outputs. |
| Pyroscope (Grafana) | OSS+SaaS | yes | Continuous profiling, low overhead. |
| Lighthouse CI Server | OSS | yes | Self-host LHCI; budget enforcement on PRs. |
| WebPageTest | SaaS+OSS | yes (API) | Real-browser, multi-region, network throttling. |

## Templates & scripts
See `templates.md` for full k6 + Locust scripts. Inline minimal CI gate:

```python
# scripts/perf_gate.py — fail if metrics regress vs baseline
import json
import sys
from pathlib import Path

def cmp(current: Path, baseline: Path, tol: float = 0.05) -> int:
    cur = json.loads(current.read_text())["metrics"]
    base = json.loads(baseline.read_text())["metrics"]
    fail = 0
    keys = ["http_req_duration_p95", "http_req_failed_rate"]
    for k in keys:
        c = cur.get(k, {}).get("value", 0)
        b = base.get(k, {}).get("value", 0)
        if b == 0:
            continue
        delta = (c - b) / b
        flag = "REGRESS" if delta > tol else "OK"
        if flag == "REGRESS":
            fail += 1
        sys.stdout.write(f"{k}: cur={c:.2f} base={b:.2f} delta={delta:+.1%} {flag}\n")
    return 1 if fail else 0

if __name__ == "__main__":
    sys.exit(cmp(Path(sys.argv[1]), Path(sys.argv[2])))
```

Sample k6 stub (target SLO):

```js
// scripts/perf/search.js
import http from 'k6/http';
import { check } from 'k6';

export const options = {
  thresholds: {
    http_req_failed: ['rate<0.01'],
    http_req_duration: ['p(95)<500', 'p(99)<1000'],
  },
  scenarios: {
    steady: { executor: 'constant-arrival-rate', rate: 50, timeUnit: '1s', duration: '5m', preAllocatedVUs: 50 },
    spike:  { executor: 'ramping-arrival-rate', startRate: 0, timeUnit: '1s',
              stages: [{ duration: '30s', target: 200 }, { duration: '1m', target: 200 }, { duration: '30s', target: 0 }],
              preAllocatedVUs: 200, startTime: '5m30s' },
  },
};

export default function () {
  const r = http.get(`${__ENV.BASE}/api/search?q=hello`);
  check(r, { 'status 200': (x) => x.status === 200 });
}
```

## Best practices
- Baseline before optimizing — commit a `.perf/baseline.json` per environment.
- Test prod-like data volume; empty DBs lie about query plans.
- Warm caches before measuring; first 30-60s of a run is throwaway.
- Separate latency from throughput — fix latency first, then push RPS.
- Always use coordinated-omission-corrected tools (`wrk2`, `vegeta`, `k6`) for true tail latency.
- Pin all client-side perf tooling versions in CI; output formats change.
- Annotate runs with git SHA + env + dataset size — comparison is meaningless without context.
- Profile with `py-spy record` (sampling) over `cProfile` (deterministic, slow) for live services.
- Flame graphs > flat profiles: flat profiles miss call-graph context.
- Run soak tests overnight (8h+) to surface memory leaks; track RSS over time.
- Track p99/p999 — averages hide tail; tails are what users feel during outage.
- Budget enforcement in CI: fail PR if p95 regresses >5%.

## AI-agent gotchas
- LLMs report "fast" based on a single 5-second run; require N=3+ runs and stats (mean ± stdev).
- Agents conflate `time.time()` with monotonic — use `time.perf_counter()` / `process_time_ns()`.
- Generated benchmarks often forget warm-up; first iteration includes import/JIT cost.
- Async benchmarks: agents await sequentially when concurrency is the point — verify with `asyncio.gather`.
- Profilers + load tests at once skew results; agents enable both. Force serial: profile small load, then load test without profiler.
- LLMs add `print()` inside hot loops "for debugging" — kills perf and pollutes logs. Run with T20 ruff rule.
- Async ORM regressions: agent "optimizes" with cache, but cache layer adds round-trip on cold path; require A/B with cache disabled.
- Human-in-loop checkpoint: SLO numbers — they're product/business decisions, not technical. Agent suggests, human ratifies.
- Agents draw conclusions from local-machine runs; remind them prod has different CPU governor, network, IO. Always verify on staging.
- "Performance bug" vs "performance feature": agents will optimize a rarely-used endpoint and ignore the hot one. Prioritize by RPS × latency.

## References
- k6 docs — https://k6.io/docs
- Locust docs — https://docs.locust.io
- pytest-benchmark — https://pytest-benchmark.readthedocs.io
- py-spy — https://github.com/benfred/py-spy
- Brendan Gregg flame graphs — https://www.brendangregg.com/flamegraphs.html
- Web Vitals — https://web.dev/vitals/
- "Coordinated omission" — http://www.azulsystems.com/presentation/javaone-2013-bof-jvm-performance/4-systems-performance-mistakes
- Pyroscope — https://pyroscope.io/docs/
- Grafana k6 + tracing — https://grafana.com/blog/2024/02/27/k6-tracing/
