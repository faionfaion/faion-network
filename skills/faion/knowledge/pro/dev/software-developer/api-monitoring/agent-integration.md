# Agent Integration — API Monitoring

## When to use
- Bringing observability to a Python/Node/Go API that has shipped without metrics, structured logs, traces, or proper liveness/readiness probes.
- Adding RED (Rate, Errors, Duration) and USE (Utilization, Saturation, Errors) dashboards before a planned launch / scale event.
- Migrating from legacy APM SDKs to OpenTelemetry as the standard instrumentation layer.
- Establishing SLOs/SLIs and error budgets, with alert rules wired to PagerDuty / Opsgenie.
- Diagnosing recurring p99 latency spikes that aggregate metrics hide — add traces + exemplars.
- Onboarding a new microservice into the existing observability stack (Prometheus + Grafana + Loki + Tempo / Datadog / New Relic / Honeycomb).

## When NOT to use
- Pre-product-fit prototypes — `/health` + log-to-stdout is enough; full RED/USE + alerts is overhead.
- Internal tools used by <10 people daily — alert fatigue exceeds incident value.
- Static sites / CDN-only deployments — CDN provider's metrics already cover availability.
- One-shot batch jobs / cron tasks — use job-completion alerts (Healthchecks.io, Dead Man's Snitch) not full APM.
- Strict-latency embedded / industrial systems where instrumentation cost (Prometheus client allocs, OTel SDK CPU) breaks the SLO. Use sampled, async exporters or skip in-process collection.
- Compliance contexts (HIPAA, PCI) where any unredacted span/log export may leak PHI/PAN — stricter pipelines required.

## Where it fails / limitations
- **Client-side cardinality explosion.** `request_id` or `user_id` as a metric label kills Prometheus (millions of series). Belongs in logs / traces, never in metric labels.
- **`p99` from histograms is approximate.** Histograms with default buckets (`0.005s` to `10s` in 7 buckets) have terrible resolution at the tail. Tune buckets to your latency profile or use native histograms (Prometheus 2.40+).
- **Sampling hides rare failures.** Tail-sampling traces drop "boring" successes but agents over-sample errors and miss capacity issues. Decide head vs. tail vs. probabilistic per service.
- **Health checks lie.** README's `/health` returns 200 if process is up; `/health/ready` checks dependencies. Liveness probes that hit downstream cause cascade failures (k8s restart loop). Liveness must check ONLY the process; readiness checks dependencies.
- **External dep timeouts in readiness.** README has `httpx.AsyncClient` with `timeout=5` to `https://api.stripe.com/health` — Stripe's health page is not a contract; that URL also doesn't exist. Always use a vendor's documented status endpoint or your own canary.
- **Log volume cost.** `logger.info` per request at 1000 RPS = 86M lines/day = $$. Without structured sampling, log bills exceed compute bills.
- **Trace context propagation gaps.** Async tasks (Celery, Sidekiq, queue consumers) drop `traceparent` if the agent doesn't wire it. Distributed traces look like detached fragments.
- **Alert noise.** Out-of-the-box "p99 > 1s" alerts fire constantly on cold-start, deploy, downstream blip. Without burn-rate alerting (multi-window multi-burn-rate), on-call is hated.

## Agentic workflow
Drive observability instrumentation as a five-stage pipeline: (1) a discovery agent inventories endpoints, downstream deps, and existing log statements; (2) an instrumentation agent wires OpenTelemetry SDK + auto-instrumentations (FastAPI/Express/Spring) + manual spans for business operations; (3) a metrics agent adds RED counters/histograms with bounded label cardinality and a `/metrics` endpoint; (4) an SLO agent emits an SLO doc per service (latency/availability/saturation targets) plus PromQL alert rules with multi-window burn-rate; (5) a dashboard agent generates Grafana JSON for the RED + USE dashboard. Persist SLO config in `.aidocs/product_docs/slo-<service>.md`. Use `faion-sdd-executor-agent` to drive each service onboarding as one SDD task.

### Recommended subagents
- `faion-sdd-executor-agent` (`agents/faion-sdd-executor-agent.md`) — opus model fits because SLO trade-offs (target, error budget, burn rate) are decision-heavy and political (negotiate with PM).
- A purpose-built **cardinality-lint agent** (worth adding under `agents/`): scan code for `Counter(...).labels(user_id=..., request_id=..., session_id=...)` patterns and block. Should also catch `userId` / `traceId` / random UUIDs as metric labels.
- `password-scrubber-agent` (`agents/password-scrubber-agent.md`) — run before logs, traces, and metric exemplars are exported; tokens / emails / card data leak constantly through structured-log middleware.
- An **alert-rule-review agent** that consumes the proposed PromQL and rejects rules without (a) a runbook URL annotation, (b) burn-rate windows, (c) a `severity` label, (d) a "for: 5m" minimum.
- For tracing-specific changes, pair with sibling `pro/infra/devops-engineer/observability-*` methodologies and gate trace-sampling-config changes behind human review.

### Prompt pattern
Instrumentation generation:
```
You are wiring OpenTelemetry to a FastAPI service. Output:
1. A `telemetry.py` that initializes TracerProvider, MeterProvider,
   OTLP HTTP exporter (env: OTEL_EXPORTER_OTLP_ENDPOINT). Resource
   attributes: service.name, service.version, deployment.environment.
2. FastAPI auto-instrumentation + httpx auto-instrumentation.
3. Three Prometheus metrics:
   - http_requests_total (Counter, labels: method, route, status_class)
   - http_request_duration_seconds (Histogram, native histogram or
     buckets tuned for your p99 target)
   - http_in_flight (Gauge)
   Labels MUST be bounded; never use user_id, request_id, ip.
4. A /metrics endpoint exporting Prometheus format.
5. Two health endpoints:
   - /healthz: returns 200 if process is up. NO downstream calls.
   - /readyz: checks DB + Redis + critical external; returns 503 if any
     fail.
6. JSON-formatted logs via structlog/python-json-logger including
   trace_id, span_id from OTel context.
```

Alert-rule generation:
```
For service <name> with SLOs:
  availability >= 99.9% over 30d
  p95 latency <= 500ms
  p99 latency <= 1s
emit Prometheus alert rules using multi-window multi-burn-rate
(2% budget over 1h, 5% over 6h). Each rule MUST have:
  for: >= 2m
  labels: severity (page|ticket), service
  annotations: summary, description, runbook_url
NEVER emit "p99 > 1s for: 5m" — that's noise. Always burn-rate.
Reference: SRE Workbook ch.5 — Alerting on SLOs.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `prometheus` / `promtool` | Scraping, alert-rule lint, query | `brew install prometheus` ; https://prometheus.io |
| `grafana` / `grafanactl` | Dashboards as code; provision JSON | https://grafana.com/docs |
| `otel-cli` | Send spans / metrics from shell scripts and CI | https://github.com/equinix-labs/otel-cli |
| `otel-collector` | Receive, batch, route telemetry | https://opentelemetry.io/docs/collector |
| `tempo-cli` / `loki-cli` (`logcli`) | Query traces / logs | https://grafana.com/docs/tempo , https://grafana.com/docs/loki |
| `k6` / `vegeta` | Load + canary tests; emit OTel metrics | https://k6.io , https://github.com/tsenart/vegeta |
| `httpstat` / `curl-format` | Per-request timing breakdown | https://github.com/davecheney/httpstat |
| `slo-generator` (Google) | SLO config → SLI burn-rate alerts | https://github.com/google/slo-generator |
| `pyrra` | Define SLOs in YAML, generate Prom rules | https://github.com/pyrra-dev/pyrra |
| `sloth` | CLI to generate SLI/SLO Prom rules | https://github.com/slok/sloth |
| `mimirtool` / `cortextool` | Linting / unit tests for Prom rules | https://grafana.com/docs/mimir |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Prometheus + Grafana + Loki + Tempo | OSS | yes | The default OSS stack; Helm charts + k8s operator. |
| Grafana Cloud | SaaS | yes | Managed PLG stack with free tier. |
| Datadog | SaaS | yes | Full APM/log/RUM/synthetics; agent installable; cost grows fast. |
| New Relic | SaaS | yes | Free 100GB/month tier; OTel-native. |
| Honeycomb | SaaS | yes | Trace-first; best for high-cardinality debug; OTel-native. |
| Lightstep / ServiceNow Cloud Observability | SaaS | yes | Trace-first like Honeycomb. |
| AWS CloudWatch + X-Ray | SaaS | yes | Default if you live on AWS; OTel exporter available. |
| GCP Cloud Operations | SaaS | yes | Default on GCP; OTel-native. |
| Sentry | SaaS / OSS | yes | Errors + perf; complement to APM, not replacement. |
| BetterStack / Uptime Kuma | SaaS / OSS | yes | External synthetic uptime checks. |
| Healthchecks.io / Dead Man's Snitch | SaaS / OSS | yes | Cron / job heartbeat. |
| PagerDuty / Opsgenie / Squadcast | SaaS | yes | Alert routing + on-call rotation; APIs scriptable. |

## Templates & scripts

The methodology already ships health-check + middleware + alert-rule examples in `README.md` and templates in `templates.md`. The gap is automated lint of bad metric usage (high-cardinality labels, missing runbook links). Inline drop-in (≤50 lines) — `scripts/api-monitoring-lint.sh`:

```bash
#!/usr/bin/env bash
# api-monitoring-lint.sh — block bad observability patterns.
# Usage: api-monitoring-lint.sh <project-root>
set -euo pipefail
root="${1:?usage: api-monitoring-lint.sh PROJECT_ROOT}"
fail=0
echo "# api-monitoring lint ($root)"

echo "## High-cardinality metric labels"
grep -rEn '\.labels?\([^)]*\b(user_id|request_id|session_id|trace_id|email|ip|userId)\b' \
  "$root" --include='*.py' --include='*.go' --include='*.js' --include='*.ts' \
  --include='*.java' --include='*.rb' \
  | tee /tmp/mon.card || true
[[ -s /tmp/mon.card ]] && fail=1

echo "## Liveness probe calling downstream (must check process only)"
grep -rEn -A 5 'def health_check\b|@.*"/healthz"|@.*"/health"' "$root" --include='*.py' \
  | grep -E 'await|requests\.|httpx\.|asyncpg\.|aioredis\.' \
  | tee /tmp/mon.live || true
[[ -s /tmp/mon.live ]] && fail=1

echo "## Alert rules without runbook_url annotation"
for f in $(find "$root" -name '*.rules.yml' -o -name 'alert*.yaml' 2>/dev/null); do
  grep -L 'runbook_url' "$f" && echo "  └ $f missing runbook_url"
done | tee /tmp/mon.runbook || true
[[ -s /tmp/mon.runbook ]] && fail=1

echo "## Alerts firing instantly (for: 0s / missing)"
grep -rE '^\s*(- alert:|alert:)' "$root" --include='*.yml' --include='*.yaml' -A 3 \
  | grep -B 1 'for: 0s\|for: $' \
  | tee /tmp/mon.for || true

echo "## Plain-text logging of secrets"
grep -rEn 'logger\.\w+\([^)]*(password|secret|token|api_key)' "$root" \
  --include='*.py' --include='*.js' --include='*.ts' \
  | tee /tmp/mon.secret-log || true
[[ -s /tmp/mon.secret-log ]] && fail=1

exit "$fail"
```

Wire into pre-commit + CI. Combine with `promtool check rules *.rules.yml` for syntactic correctness.

## Best practices
- **Liveness ≠ readiness.** Liveness: process alive (no downstream call). Readiness: dependencies reachable. README's `/health` would cause cascade restarts under k8s if used as liveness — fix the example before copy-paste.
- **RED + USE.** Per-endpoint Rate, Errors, Duration; per-resource Utilization, Saturation, Errors. Two dashboards, one consistent.
- **Bounded label cardinality.** Method (GET/POST), route template (`/users/:id`, NEVER `/users/123`), status class (`2xx/3xx/4xx/5xx`). Anything else is a log/trace concern.
- **Native histograms (Prom 2.40+) over fixed buckets** when stack supports it; precise p99 without bucket guessing.
- **OpenTelemetry first.** Don't use vendor SDK (`datadog`/`newrelic` import) directly; wire OTel and configure exporter — vendor swap then takes config change, not code change.
- **Burn-rate alerts.** Multi-window (e.g., 2% budget in 1h AND 5% in 6h triggers page; 10% in 24h triggers ticket). SRE Workbook ch.5.
- **Every alert has a runbook URL.** Alert without "what to do" is noise. Block in CI.
- **Sampling strategy declared.** Head sampling (1%) for trace volume; tail sampling for "always send if error or slow". Decide explicitly.
- **Trace context propagation in async work.** Wrap Celery / Sidekiq / Bull queue producers + consumers with OTel context; otherwise traces split.
- **Structured logs with trace_id.** `logger.info(..., trace_id=ctx.trace_id)` so logs join traces; cheap, high-leverage.
- **Synthetic external probes.** External uptime check (BetterStack / k6 cloud) — internal monitoring sees its own outages last.
- **Metric exemplars.** Attach a sample trace_id to histogram buckets — clicking a latency outlier in Grafana jumps to the exact trace.
- **SLO before alerts.** Don't alert before defining the objective. Most teams reverse this and end up with 200 noisy alerts.

## AI-agent gotchas
- **High-cardinality reflex.** Agents `metric.labels(user_id=ctx.user_id, route=request.path)` because it's "useful". Lint and reject. Route TEMPLATES only, never raw paths.
- **Liveness probe cascade.** Agents make `/health` check DB + Redis + Stripe because "more thorough is better". Cascade-failure under k8s. Force separation.
- **Hallucinated vendor health URLs.** README's `https://api.stripe.com/health` is fictional. Agents copy that pattern. Use vendor's documented status (Stripe: `https://status.stripe.com/api/v2/status.json`) or in-house canary.
- **Wrong percentile from histogram.** Agents query `histogram_quantile(0.99, sum(rate(...)))` without aggregation by label and get global p99 instead of per-route. Pin the PromQL pattern in templates.
- **Alert without `for:`.** Agents emit alerts that fire on a single bad scrape. Force `for: >= 2m` minimum.
- **Sampling forgotten.** Agents wire OTel without sampler config; production drowns in spans. Force `OTEL_TRACES_SAMPLER=parentbased_traceidratio` + a ratio in the prompt.
- **Logs of full request body.** Agents `logger.info(request.json())`. PII / secrets leak. Force a redaction middleware.
- **Datadog / New Relic SDK direct import.** Agents trained on vendor docs import vendor SDK. Force OTel + OTLP exporter.
- **No exemplars on histograms.** Agents wire histograms without exemplars; debugging tail latency is then blind. Pin exemplar API.
- **Missing trace context in queue handlers.** Agents miss async context propagation. Provide a wrapper helper (`with_trace_context(producer)`) the agent must use.
- **Alert thresholds plucked from air.** Agents emit "5xx > 1%". Without an SLO it's arbitrary. Tie all thresholds to a stated SLO.
- **Human-in-the-loop on SLO targets.** SLO numbers are business decisions. Never auto-merge; require PM/ops sign-off in PR.
- **Dashboard JSON drift.** Agents hand-edit Grafana JSON. Manage as code (jsonnet / `grafanactl pull`); commit machine-formatted JSON only.

## References
- Google SRE Workbook — Alerting on SLOs. https://sre.google/workbook/alerting-on-slos/
- Google SRE Book — Monitoring Distributed Systems. https://sre.google/sre-book/monitoring-distributed-systems/
- OpenTelemetry — Specification. https://opentelemetry.io/docs/specs/otel
- Prometheus — Best practices. https://prometheus.io/docs/practices/naming/
- Brendan Gregg — USE method. https://www.brendangregg.com/usemethod.html
- Tom Wilkie — RED method. https://www.weave.works/blog/the-red-method-key-metrics-for-microservices-architecture
- Honeycomb — Observability Engineering (book). https://www.honeycomb.io/oreilly-observability-engineering
- Pyrra (SLOs as code) — https://github.com/pyrra-dev/pyrra
- Sloth (SLO Prom rules) — https://github.com/slok/sloth
- k6 — https://k6.io/docs/
- Sibling methodologies in this repo: `pro/dev/software-developer/api-gateway-patterns/`, `continuous-delivery/`, `pro/infra/devops-engineer/`, `pro/infra/cicd-engineer/`.
