# Agent Integration — Performance Testing Tools

## When to use
- Setting up baseline load tests for a new HTTP API before its first production rollout.
- Adding CI perf gates that block PRs introducing > 10% latency regression.
- Capacity planning: agent runs k6/Locust at increasing user counts to find the knee.
- Reproducing a production incident with realistic scripted scenarios.
- Comparing two implementations (rewrite, ORM swap) under identical synthetic load.

## When NOT to use
- Functional bugs — perf tools don't surface logic errors, just timing/throughput.
- Frontend UX perf (use Lighthouse, WebPageTest, Playwright tracing instead).
- Pre-MVP products with no defined SLOs — you'll measure noise.
- Single-shot benchmarks of pure functions (use `pytest-benchmark` / `vitest bench`).
- Tests against shared staging environments — results are unreproducible due to neighbour load.

## Where it fails / limitations
- Local laptop runs are CPU-bound on the load generator long before the SUT — false ceilings. Use distributed mode (k6 cloud, Locust master/worker) past ~500 RPS.
- k6 scripts are JavaScript but no Node APIs — agents trying to import `fs` or `axios` will fail.
- Locust events block the Python event loop if `@task` does sync I/O without `gevent` — agents miss this.
- Thresholds set too tight in CI cause flakes that erode trust; agents respond by relaxing all thresholds.
- Scenarios that don't include realistic think time produce p95 noise; copy-paste agent scripts often omit `sleep`.

## Agentic workflow
A perf agent reads OpenAPI / route table → generates a weighted scenario file (k6 or Locust) → runs a smoke at 10 VUs to confirm script correctness → escalates to staged ramp → publishes JSON output for a review agent to compare against baseline. Always smoke-test the script first; agents that go straight to 1000 VUs waste time when the scenario is broken. Use `faion-sdd-executor-agent` to gate on JSON threshold checks.

### Recommended subagents
- `faion-sdd-executor-agent` — wraps the perf run as an SDD task with a "thresholds met" quality gate.
- A custom `perf-runner` agent (compose from skills) for scenario generation from OpenAPI specs.

### Prompt pattern
```
Read OpenAPI spec at <path>. Generate a k6 scenario with these weights:
GET-heavy endpoints 70%, POST-write 20%, search 10%.
Add stages: 2m→50, 5m→50, 2m→100, 5m→100, 2m→0.
Thresholds: p95<500ms, http_req_failed<1%.
Run smoke `k6 run --vus 5 --duration 30s` first, paste output, then full run.
Stop and report if smoke fails.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `k6` | Modern JS load testing, single binary | `brew install k6` / docker `grafana/k6` |
| `locust` | Python load testing, web UI | `pip install locust` |
| `wrk` / `wrk2` | Low-overhead HTTP benchmarking | `apt install wrk` |
| `vegeta` | Constant-rate Go HTTP attacker | `go install github.com/tsenart/vegeta/v12@latest` |
| `bombardier` | Fast Go HTTP benchmarking | `go install github.com/codesenberg/bombardier@latest` |
| `pytest-benchmark` | Python micro-benchmarks with regression alerts | `pip install pytest-benchmark` |
| `oha` | Rust `wrk` alternative with TUI | `cargo install oha` |
| `hyperfine` | CLI command benchmark with stats | `cargo install hyperfine` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Grafana k6 Cloud | SaaS | Yes — `k6 cloud` CLI + REST API | Distributed VUs, dashboards. |
| Locust Cloud | SaaS | Yes — CLI | Hosted Locust workers. |
| Artillery | OSS + Cloud | Yes — YAML scenarios + CLI | Good for SaaS multi-tenant tests. |
| Gatling Enterprise | SaaS | Yes — Maven/CLI | Scala DSL — heavier learning curve for agents. |
| BlazeMeter | SaaS | Yes — REST API | JMeter compatible. |
| Datadog Synthetics + APM | SaaS | Yes — API | Tie load runs to APM traces. |
| GitHub Actions `grafana/k6-action` | SaaS | Yes | One-line CI integration. |

## Templates & scripts
See `templates.md` for full Locust + k6 starters. Threshold checker for CI gates (≤50 lines):

```python
#!/usr/bin/env python3
"""check_perf.py — fail CI if thresholds miss. Usage: python check_perf.py results.json"""
import json, sys, pathlib

LIMITS = {"http_req_duration.p(95)": 500, "http_req_failed.rate": 0.01}

data = [json.loads(l) for l in pathlib.Path(sys.argv[1]).read_text().splitlines() if l]
metrics = {}
for entry in data:
    if entry.get("type") == "Point":
        m = entry["metric"]
        metrics.setdefault(m, []).append(entry["data"]["value"])

failed = []
for key, limit in LIMITS.items():
    name, *agg = key.split(".")
    values = metrics.get(name, [])
    if not values:
        failed.append(f"{key}: no samples")
        continue
    if agg and agg[0].startswith("p("):
        pct = float(agg[0][2:-1]) / 100
        v = sorted(values)[int(len(values) * pct)]
    else:
        v = sum(values) / len(values)
    if v > limit:
        failed.append(f"{key}={v:.2f} > {limit}")

if failed:
    print("PERF FAIL:", *failed, sep="\n  ")
    sys.exit(1)
print("PERF OK")
```

## Best practices
- Run a 30-second smoke at 5 VUs before any real test. If smoke fails, fix the script — not the SUT.
- Pin tool versions in CI (`grafana/k6:0.50.0`) — k6 minor versions change metric names.
- Always export raw JSON (`--out json=`) for diffing across runs; HTML reports are throwaway.
- Use realistic think time (`sleep(rand)`) and keep-alive on; without them you're benchmarking the load generator.
- Separate "soak" (8h, low load) from "stress" (3 min, ramp to break) into distinct files; agents conflate them.
- Tag runs with git SHA + scenario name in metric labels — required for trend analysis.

## AI-agent gotchas
- Agents copy the same `BASE_URL` to prod by accident. Force `__ENV.BASE_URL` and fail if unset.
- LLMs hallucinate k6 modules (`k6/http2` doesn't exist). Always run `k6 inspect script.js` before a real run.
- Locust agents that use `requests` instead of `self.client` won't be measured — invisible bug.
- Threshold output reads succeed even when SUT was 5xx-ing if `check()` is missing. Mandate `check + errorRate.add(1)`.
- Human-in-loop checkpoint: review the generated scenario weights and stage shape BEFORE running > 5 minutes (cloud spend).
- Don't let agents auto-tune thresholds based on previous runs — they'll converge on the regressed value.

## References
- k6 docs — https://k6.io/docs/
- Locust docs — https://docs.locust.io/
- Brendan Gregg, "Systems Performance" 2nd ed. — methodology that load tools alone cannot replace.
- "Performance Testing with k6" — Grafana 2024 guide.
- Sibling: `perf-test-basics/` for the methodology layer (USE/RED/GoldenSignals).
