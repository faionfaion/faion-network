# Agent Integration — Performance Testing Basics

## When to use
- Establishing a first performance baseline for a service that has none — generating Locust/k6 scripts, capturing p50/p95/p99, error rate, throughput.
- Adding profiling (cProfile, py-spy, memory_profiler) to investigate a localized slowdown.
- Wiring `pytest-benchmark` micro-benchmarks into CI to gate on regressions for hot paths.
- Detecting and asserting against N+1 queries and slow-query thresholds in tests.
- Writing a CI check that fails the build when p95 latency or error rate breaches a threshold.

## When NOT to use
- For full load-testing tool comparison (k6 vs Locust vs Gatling vs Artillery vs JMeter) — use `perf-test-tools/`.
- For frontend Web Vitals (LCP, INP, CLS) — that's a Lighthouse/RUM domain, not backend perf.
- For chaos engineering / fault injection — separate discipline (Chaos Mesh, Litmus, Gremlin).
- For continuous production load testing without a safety story — agents should not be the ones flooding prod.
- For trading systems / sub-millisecond latency tuning — needs CPU pinning, NUMA, kernel tuning beyond this scope.
- When the bottleneck is clearly architectural (synchronous calls, single-threaded worker) — fix the architecture first; perf-test second.

## Where it fails / limitations
- README focuses on Python tooling. Node, Go, Java perf workflows differ (clinic.js, pprof, async-profiler) and are not covered here.
- "Test in production-like environment" is one sentence; no concrete guidance on data volume, cache warm-up, or shared infra.
- `pytest-benchmark` micro-benchmarks are excellent for hot pure functions; they tell you nothing about end-to-end latency under concurrency.
- N+1 detector via `caplog` is naive — relies on log capture and a static threshold; better signal is `select_count` from SQLAlchemy event listeners.
- `check_performance.py` script's threshold check has a logic bug for non-rate metrics (`else actual <= threshold` after `if 'rate' in metric`); agents should rewrite, not paste.
- No mention of statistical noise: a single load-test run is a single sample. Trend over runs needed for regression detection.
- Memory profiling needs allocations-vs-resident distinction; the README implies `memory_profiler` is sufficient — for leak hunting use `tracemalloc` + `objgraph`.

## Agentic workflow
A perf agent should always operate in three phases — measure, hypothesize, verify — and refuse to "optimize" without a captured baseline. Phase 1: spin up a load harness in a staging environment, run a fixed scenario (think-time + concurrency + duration), capture metrics into a file. Phase 2: profile the slowest endpoint with cProfile/py-spy on a single-request reproduction. Phase 3: apply one change, re-run identical load, compare. Never run load against shared prod resources; require the agent to verify it has a dedicated env (env name allowlist). For micro-benchmarks, gate CI with `--benchmark-compare-fail=mean:5%` against the previous main commit.

### Recommended subagents
- `general-purpose` — script generation (Locust/k6), profiling sessions, regression analysis.
- `faion-sdd-executor-agent` — when perf work is captured as a feature.
- A narrow `flame-graph-reader` agent — fed `py-spy record -f speedscope` output, returns top-N hot frames + a hypothesis.
- A `regression-bisect` agent — runs benchmark against `git bisect` to localize a perf regression.

### Prompt pattern
```
Read solo/dev/automation-tooling/perf-test-basics/README.md.
Establish a baseline for <endpoint>. Generate a Locust scenario with N=<users>,
spawn-rate=<r>, duration=<d>. Run against $STAGING_URL only (refuse if URL
matches prod). Persist raw stats to perf/baselines/<sha>.json. Print
p50/p95/p99/error_rate/rps.
```
```
Profile <endpoint> handling a single representative request. Use py-spy
record for 30s. Save flame.svg. Identify top-3 hot functions by total time;
propose ONE change (no shotgun edits). Open a PR with the diff, the
benchmark before/after, and the flame graph attached.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `locust` | Python load-test framework, web UI | `pip install locust` · locust.io |
| `k6` | JS-scripted load tester, lightweight | k6.io |
| `wrk` / `wrk2` | HTTP benchmarking, constant-throughput (`wrk2`) | github.com/giltene/wrk2 |
| `vegeta` | HTTP load via constant-rate attacks | github.com/tsenart/vegeta |
| `oha` | Rust-based hey/wrk replacement, pretty TUI | github.com/hatoo/oha |
| `hey` / `bombardier` | Quick HTTP probes | various |
| `pytest-benchmark` | Statistically-aware micro-benchmarks | pypi |
| `cProfile` + `snakeviz` | Function-level profiling + flame view | bundled / pip |
| `py-spy` | Sampling profiler for running Python | github.com/benfred/py-spy |
| `memray` | Allocation tracker (Bloomberg) | github.com/bloomberg/memray |
| `tracemalloc` | Stdlib allocation snapshots | Python stdlib |
| `pyinstrument` | Low-overhead statistical profiler with HTML report | pip |
| `pgbadger` | Postgres slow-log aggregator | pgbadger.darold.net |
| `perf` (Linux) + `flamegraph.pl` | System-level profiling | `apt install linux-tools-common` |
| `node --inspect` + `clinic` (`doctor`/`flame`/`bubbleprof`) | Node profiling suite | clinicjs.org |
| `go tool pprof` | Go profiling | bundled with Go |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Grafana k6 Cloud | SaaS | Yes | Distributed load + dashboards; CLI + API. |
| BlazeMeter | SaaS | Partial | JMeter-centric; agent automation possible. |
| Loader.io | SaaS | Yes | Tiny scenarios, REST API. |
| Locust on Kubernetes (`locust-k8s-operator`) | OSS | Yes | Scale-out workers from CI. |
| Datadog APM | SaaS | Yes | Per-trace flamegraphs; agents can correlate load tests with traces. |
| Honeycomb | SaaS | Yes | Wide-event tracing; great for regression triage. |
| Pyroscope | OSS | Yes | Continuous profiling; pairs with Grafana. |
| Sentry Performance | SaaS | Yes | Web vitals + transaction p95. |
| Speedscope | OSS web | Yes | Open `py-spy record -f speedscope` outputs. |
| Granfana Mimir / Prometheus | OSS | Yes | Long-horizon perf metric storage. |
| New Relic / Dynatrace | SaaS | Partial | Powerful, heavier auth for agents. |
| Artillery Pro | SaaS | Yes | Scenario-based load with Playwright integration. |

## Templates & scripts
See `templates.md` and `examples.md`. Minimum SQLAlchemy query-count assertion fixture (more reliable than log scraping):

```python
# tests/conftest.py
import pytest
from sqlalchemy import event

@pytest.fixture
def query_counter(db_session):
    counter = {"n": 0}
    bind = db_session.get_bind()

    @event.listens_for(bind, "before_cursor_execute")
    def _count(conn, cursor, statement, params, ctx, em):
        counter["n"] += 1

    yield counter
    event.remove(bind, "before_cursor_execute", _count)


def test_orders_endpoint_no_n_plus_one(client, query_counter):
    r = client.get("/orders?limit=10")
    assert r.status_code == 200
    assert query_counter["n"] <= 3, f"N+1 suspected: {counter['n']} queries"
```

## Best practices
- Always capture: p50, p95, p99, error rate, RPS, concurrent users, duration. A single "average latency" number lies.
- Compare runs on identical hardware/data — perf numbers are not transferable across environments.
- Warm caches before measuring (one full pass with `wrk -t1 -c1 -d30s`) so JIT/connection-pool/buffer-pool effects don't dominate.
- Store raw results (not summaries) so you can re-aggregate later.
- For micro-benchmarks, run `pytest-benchmark` with `--benchmark-min-rounds=20`; default rounds give noisy results.
- Set explicit thresholds in CI per critical endpoint; fail the pipeline on regression rather than reviewing graphs.
- Use sampling profilers (py-spy, pyinstrument) over deterministic (cProfile) on running services — overhead is bounded.
- For memory leaks, run an endurance test for hours and watch RSS slope, not single-snapshot peak.
- Never load-test from the same machine as the system under test — observer effect dominates.

## AI-agent gotchas
- Premature optimization: agents will rewrite a function for "perf" without a benchmark. Refuse to merge without before/after numbers from the same machine.
- "Add caching" reflex: agents wrap everything in `@lru_cache` — works for pure functions, breaks for stateful ones (DB calls, time-dependent results).
- Locust spawn-rate: agents set `spawn_rate = users` and overwhelm the target before the test even starts. Force a ramp profile (e.g. 10/s).
- Agents read pytest-benchmark mean and ignore stddev; force fail criteria on `mean ± 2σ` of baseline.
- N+1 detection: agents use the `caplog` snippet from the README and miss the actual queries because logging is set to INFO. Use the SQLAlchemy event listener fixture instead.
- Profiling: agents profile `localhost` with no network latency and conclude the service is fast. Add a realistic latency simulation (`tc qdisc add dev lo root netem delay 20ms`).
- Memory: `memory_profiler` `@profile` works only on the decorated function; agents miss leaks elsewhere. Use `memray run` for the whole process.
- Agents will load-test prod by accident. Hard-code an env-name allowlist (`assert "prod" not in TARGET_URL`).
- Threshold drift: agents push the threshold up after every regression to keep CI green. Require a human approver for threshold changes.

## References
- Brendan Gregg, Systems Performance (Pearson).
- pytest-benchmark: https://pytest-benchmark.readthedocs.io/
- py-spy: https://github.com/benfred/py-spy
- memray: https://bloomberg.github.io/memray/
- Locust: https://docs.locust.io/
- k6: https://k6.io/docs/
- Pyroscope: https://pyroscope.io/
- Web Vitals (separate domain): https://web.dev/vitals/
- Sibling: `solo/dev/automation-tooling/perf-test-tools/`.
