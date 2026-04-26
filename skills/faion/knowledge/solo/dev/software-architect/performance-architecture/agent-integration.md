# Agent Integration — Performance Architecture

## When to use
- Defining SLOs and error budgets at design time, before performance becomes a customer complaint.
- Pre-launch capacity planning for a feature or product expected to receive measurable traffic.
- Performance regression triage where you need a structured layer-by-layer narrowing (client → CDN → LB → app → data).
- Cost optimization driven by tail latency or compute waste, not just instance counts.
- Pre-IPO/audit scenarios that require documented performance commitments.

## When NOT to use
- Pure prototypes — premature optimization makes the product slower to ship without buying anything.
- Pages/APIs with no production traffic yet — measure first.
- Hot fixes of a single slow query — use profiling tools, not full architecture loops.

## Where it fails / limitations
- LLM-suggested SLOs gravitate toward textbook numbers ("p95 < 200ms") regardless of business context. They must be argued from user impact and competitive baseline.
- "Add caching" recommendations skip invalidation cost — see caching-architecture.
- Synthetic load tests miss real traffic shape (Pareto user distributions, bot fluctuations); load profile must come from real telemetry.
- Microbenchmarks are nearly always wrong; agents over-trust them. Demand end-to-end measurements.
- Horizontal scaling recommendations assume statelessness that may not exist; require an explicit state inventory.

## Agentic workflow
Run a measurement-first loop: a profiler-agent (reads APM/traces), an analyzer-agent (identifies bottleneck layer), a designer-agent (proposes change with predicted impact), and a validator-agent (defines and runs the load test that proves/disproves the prediction). Always require the predicted improvement number in the change proposal so the validator has a falsification target. Iterate until SLOs hold under target load.

### Recommended subagents
- `faion-brainstorm` — diverge over scaling and optimization options before committing.
- `faion-sdd-execution` — write performance design with explicit SLOs, load profiles, and acceptance tests.
- `faion-feature-executor` — apply the changes and run the validator load tests.
- `faion-improver` — post-deploy SLO review and budget burn analysis.

### Prompt pattern
```
INPUT: APM traces + flamegraph + slow query log.
TASK: Identify the dominant bottleneck layer (client/CDN/LB/app/data).
OUTPUT: One layer, one root cause, one proposed change with predicted
p95 improvement (ms) and predicted cost delta. No hand-waving.
```

```
ROLE: load-test-validator
INPUT: change proposal with predicted p95 improvement.
TASK: Generate a k6/vegeta script reproducing the production traffic mix
(reads/writes ratio, key skew, RPS profile). Output a pass/fail criterion
based on the prediction. Run it. Report.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| k6 | Modern load testing, JS scripts | https://k6.io/ |
| vegeta | HTTP load generator with histograms | https://github.com/tsenart/vegeta |
| wrk / wrk2 | Constant-throughput load tests | https://github.com/giltene/wrk2 |
| locust | Python-driven load testing | https://locust.io/ |
| hey | Simple HTTP benchmark | `go install github.com/rakyll/hey` |
| pyroscope / parca | Continuous profiling | https://pyroscope.io/ / https://parca.dev/ |
| pprof / async-profiler | Language-specific profiling | per-language |
| pgBadger / pg_stat_statements | PostgreSQL slow query analysis | https://github.com/darold/pgbadger |
| siege | Legacy but still useful HTTP stress | https://github.com/JoeDog/siege |
| Lighthouse CI | Frontend perf budgets in CI | `npm i -g @lhci/cli` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Datadog APM | SaaS | Yes — strong API | Trace-driven analysis, agents can pull spans |
| Grafana Cloud / Tempo / Mimir | SaaS+OSS | Yes — PromQL/LogQL/TraceQL | OTEL-native, queryable from agents |
| New Relic | SaaS | Yes | NRQL queries good for agent loops |
| Honeycomb | SaaS | Yes | High-cardinality tracing; great for agent analysis |
| AWS CloudWatch + X-Ray | SaaS | Yes — AWS SDK | Adequate; cardinality limits hurt agents |
| Sentry Performance | SaaS | Yes | App-side perf, frontend + backend |
| Cloudflare Analytics / Vercel Analytics | SaaS | Partial | Edge view; limited drill-down |
| k6 Cloud / Grafana Cloud k6 | SaaS | Yes | Persisted load tests with diff |

## Templates & scripts
See `templates.md` for Redis, PostgreSQL, k6, and HPA configs. Inline production-shaped k6 script:

```javascript
// load.js — replay a real RPS profile and assert p95 SLO.
import http from 'k6/http';
import { check } from 'k6';

export const options = {
  scenarios: {
    steady: { executor: 'constant-arrival-rate', rate: 200, timeUnit: '1s',
              duration: '5m', preAllocatedVUs: 50, maxVUs: 200 },
    spike:  { executor: 'ramping-arrival-rate', startRate: 200, timeUnit: '1s',
              startTime: '5m', preAllocatedVUs: 100, maxVUs: 500,
              stages: [{ target: 1000, duration: '1m' }, { target: 200, duration: '2m' }] },
  },
  thresholds: { http_req_duration: ['p(95)<300', 'p(99)<800'], http_req_failed: ['rate<0.005'] },
};

export default function () {
  const r = http.get(`${__ENV.BASE_URL}/api/items?id=${Math.floor(Math.random()*10000)}`);
  check(r, { 'status 200': (x) => x.status === 200 });
}
```

## Best practices
- SLOs come from user-impact analysis, not industry table; require an explicit user-journey-to-latency mapping in the prompt.
- Always test at expected peak (3x average is the textbook multiplier; verify with telemetry).
- Measure tails, not means; p99 is where users churn.
- Profile before optimizing — agents will refactor cold paths because they look messier.
- Make every perf change reversible with a feature flag; perf "wins" sometimes regress under real load.
- Track error budget burn as a first-class metric; alert on burn rate, not raw availability.
- Cache hit ratios, DB connection pool saturation, GC pauses, and TLS handshake counts are the four metrics agents miss most often — name them explicitly in the prompt.

## AI-agent gotchas
- Agents conflate throughput and latency; force the prompt to talk about both per change.
- LLM-suggested optimizations frequently change algorithmic complexity without measurement; require Big-O before/after.
- Auto-scaling recommendations skip cold-start cost; demand cold-start latency in the proposal.
- Database "add an index" suggestions ignore write amplification; require a write-cost estimate.
- Human-in-loop gates: SLO sign-off, capacity plan review, post-deploy SLO review at 24h and 7d.

## References
- https://sre.google/workbook/implementing-slos/
- https://sre.google/sre-book/handling-overload/
- https://k6.io/docs/test-types/load-testing/
- https://www.brendangregg.com/methodology.html
- https://www.usenix.org/publications/loginonline/scalability-but-cost
- https://aws.amazon.com/builders-library/
