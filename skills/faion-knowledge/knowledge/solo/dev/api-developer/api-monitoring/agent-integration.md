# Agent Integration — API Monitoring

## When to use
- Any HTTP/gRPC/GraphQL service running in production with paying users or SLOs.
- You need quantitative answers to "is the API healthy", "is it getting slower", "who broke it".
- Adding a new endpoint or service — instrument before launch, not after the first incident.
- Setting up readiness probes for k8s / systemd / load balancer drain.
- Diagnosing a regression (p95 spiked, error rate climbing) — metrics + logs + traces correlated by request_id.

## When NOT to use
- Throwaway prototype on localhost — Prometheus scrape config is not a learning goal.
- Internal cron job with one user — exit code + email is enough.
- When you do not yet know what "good" looks like (no SLO defined). Pick SLOs first, then instrument.

## Where it fails / limitations
- Cardinality explosion: labelling a Histogram with `user_id` or `request_id` will OOM Prometheus. Labels must be bounded.
- Liveness probes that hit the database cause cascade restarts when the DB is slow — keep liveness shallow, depth in readiness.
- p99 from a 5-minute window is noisy with low traffic; use longer windows or burn-rate alerts.
- Logs without a `request_id` correlator are unreadable in aggregate. The middleware must run before any other.
- Self-hosted Prometheus has no long-term storage by default — pair with Thanos, Mimir, or a vendor.
- "Synthetic 200 OK" health endpoints lie when downstream is broken — implement dependency checks.

## Agentic workflow
Treat instrumentation as part of the endpoint definition: an agent adding a route must also add metric labels, log fields, and a probe entry. Use a dashboard-as-code repo (Grafana JSON / Terraform) so an agent can land both the code change and the dashboard panel in one PR. For incident triage, give the agent read-only PromQL + Loki access via MCP and let it pull metrics, never let it edit alert rules without human review.

### Recommended subagents
- `faion-sdd-execution` — quality gate that fails CI if a new route lacks metrics middleware or structured logging.
- A `dashboards-as-code` task agent (Sonnet) — reads route list, emits Grafana JSON panels.
- An `slo-writer` agent (Opus) — proposes SLI/SLO from histogram data, drafts burn-rate alerts.
- `nero-tools` if NERO is the runtime — wires Telegram alerts via `tg-send`.

### Prompt pattern
```
You have read access to Prometheus at http://prom:9090 and Loki at
http://loki:3100. The /api/v1/orders endpoint p95 doubled at 14:20 UTC.
Pull request_duration p50/p95/p99 for the last 2h, top 5 error log lines
with request_id from the same window, and the diff of deploys touching
orders/. Output a 6-line incident note. Do NOT silence any alerts.
```

```
For each route in app/routes/*.py without a corresponding panel in
grafana/dashboards/api.json, propose a panel JSON with rate + p95 + error.
Output the patch only.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `promtool` | Validate rules, run unit tests on alerts | bundled with Prometheus |
| `amtool` | Inspect/silence Alertmanager from CLI | bundled with Alertmanager |
| `logcli` | Query Loki from terminal | grafana.com/docs/loki/latest/query/logcli/ |
| `vmctl` | VictoriaMetrics import/migration | docs.victoriametrics.com |
| `k6` | Synthetic load + checks → metrics | k6.io |
| `htmx-status` / `httpstat` | Latency breakdown for one URL | `pip install httpstat` |
| `otelcol` | OpenTelemetry collector pipeline | opentelemetry.io |
| `grafonnet` / `grizzly` | Dashboards as code | `grr` CLI |

## Services & apps
| Service | Type | Agent-friendly? | Notes |
|---------|------|-----------------|-------|
| Prometheus + Alertmanager + Grafana | OSS | Yes — file-based config, PromQL via HTTP API | Default for self-hosted |
| Grafana Cloud | SaaS | Yes — Terraform provider, HTTP API | Free tier covers small APIs |
| VictoriaMetrics | OSS | Yes | Drop-in Prometheus, far cheaper at scale |
| Datadog | SaaS | Yes — terraform-provider-datadog, MCP servers exist | Expensive but turnkey APM + logs + traces |
| New Relic | SaaS | Yes — NerdGraph API | Free tier exists |
| Honeycomb | SaaS | Yes — events + tracing API | Best for high-cardinality debugging |
| Sentry | SaaS + OSS | Yes — `sentry-cli`, REST API | Errors + perf, less for SLOs |
| Better Stack (Logtail + Uptime) | SaaS | Yes — REST API | Cheap status page + uptime |
| Loki + Tempo | OSS | Yes | Logs + traces, pairs with Grafana |
| Statuspage / Instatus | SaaS | Yes — REST API | Public status pages |

## Templates & scripts
See `templates.md` for FastAPI metrics middleware, structlog setup, Prometheus rule snippets.

Validate alert rules in CI:

```bash
#!/usr/bin/env bash
set -euo pipefail
promtool check rules ops/prometheus/rules/*.yml
promtool test rules ops/prometheus/tests/*.yml
# Sanity: every recording rule used in dashboards must exist
jq -r '.. | .expr? // empty' ops/grafana/dashboards/*.json \
  | grep -oE '[a-z_]+:[a-z_:]+' | sort -u > /tmp/used.txt
yq -r '.. | select(.record? != null) | .record' ops/prometheus/rules/*.yml \
  | sort -u > /tmp/defined.txt
comm -23 /tmp/used.txt /tmp/defined.txt | tee /tmp/missing.txt
[ ! -s /tmp/missing.txt ] || { echo "Missing recording rules"; exit 1; }
```

## Best practices
- Define SLOs before metrics — the metrics serve the SLO, not the other way around. Start with availability + latency.
- Use the RED method (Rate, Errors, Duration) for request-driven services and USE (Utilization, Saturation, Errors) for resources.
- Histogram buckets must straddle your SLO. If SLO is "p95 < 500ms", you need buckets at 250ms, 500ms, 750ms.
- One `request_id` per request, propagated in headers, logged in every line, included in error responses. Trace IDs from W3C `traceparent` if you have OTel.
- Burn-rate alerts (multi-window, Google SRE workbook) instead of static thresholds — fewer pages, faster detection.
- Liveness = "process alive". Readiness = "can serve traffic now" (DB + cache + critical deps). Don't confuse them.
- Cardinality budget: < 10 labels per metric, < 100 values per label. Audit with `topk(10, count by (__name__)({}))`.
- Synthetic monitoring (k6, Checkly) catches what real users see; complements RUM/server metrics.

## AI-agent gotchas
- Agents will happily add `request_id` as a Prometheus label. Reject in code review — that's the cardinality bomb. Use it as a log field only.
- LLMs hallucinate PromQL functions (`rate_over_time`, `histogram_p95`). Always run `promtool check` before applying.
- An agent diagnosing an incident may "fix" symptoms by widening alert thresholds. Lock alert rules behind a separate review path; agents can propose, humans approve.
- Generated structured-logging code often double-logs (middleware + handler) and inflates costs 10x. Audit log volume in staging before merging.
- Self-healing tempts agents to auto-restart pods on alert. That hides the bug. Restrict agent autonomy to "page humans + collect diagnostics", not "mutate runtime".
- Long-context agents lose track of label conventions across files. Keep a `metrics.md` glossary in the repo and feed it on every metrics task.
- Health endpoints are the agent's first stop. Make them return JSON with structured component states, not just `{status:"ok"}`, so agents can reason about partial failure.

## References
- https://sre.google/sre-book/monitoring-distributed-systems/
- https://sre.google/workbook/alerting-on-slos/
- https://prometheus.io/docs/practices/naming/
- https://prometheus.io/docs/practices/histograms/
- https://www.structlog.org/
- https://opentelemetry.io/docs/specs/semconv/http/
- https://grafana.com/docs/grafana/latest/dashboards/build-dashboards/manage-dashboards/#provisioning
