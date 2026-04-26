# Performance Testing Tools

## Summary

Load and stress testing using k6 (JavaScript, single binary) and Locust (Python, web UI), with CI/CD performance gates that block PRs introducing latency regressions. The concrete rule: run a 30-second smoke at 5 VUs before any real test — if smoke fails, fix the script, not the system under test.

## Why

Without baseline perf tests, latency regressions slip into production undetected. k6 and Locust model realistic user behavior (weighted scenarios, think time, staged ramps) and emit structured JSON output that CI can diff against baselines. The `p(95)<500ms, error_rate<1%` threshold pattern is the minimum gate; tighter thresholds must be validated over multiple runs before being added to CI.

## When To Use

- Establishing a baseline load test for a new HTTP API before first production rollout
- Adding CI perf gates that block PRs introducing more than 10% latency regression
- Capacity planning: find the knee by ramping VUs at increasing targets
- Reproducing a production incident with a scripted realistic scenario
- Comparing two implementations (rewrite, ORM swap) under identical synthetic load

## When NOT To Use

- Functional bugs: perf tools don't surface logic errors, only timing/throughput
- Frontend UX performance (use Lighthouse, WebPageTest, Playwright tracing instead)
- Pre-MVP products with no defined SLOs: measuring noise
- Single-shot benchmarks of pure functions (use pytest-benchmark / vitest bench)
- Tests against shared staging environments: results are unreproducible due to neighbour load

## Content

| File | What's inside |
|------|---------------|
| `content/01-k6-locust.xml` | k6 and Locust scripting patterns; staged ramp config; threshold setup; CI integration |
| `content/02-agent-workflow.xml` | Perf agent workflow; gotchas; CLI tools table; services table |

## Templates

| File | Purpose |
|------|---------|
| `templates/locustfile.py` | Locust scenario with weighted tasks, auth setup, custom metrics |
| `templates/k6-test.js` | k6 scenario with staged ramp, thresholds, scenario functions |
| `templates/check-perf.py` | CI threshold checker: fail if p95 or error rate exceeds limits |
| `templates/performance.yml` | GitHub Actions workflow running k6 gate + pytest benchmarks |
