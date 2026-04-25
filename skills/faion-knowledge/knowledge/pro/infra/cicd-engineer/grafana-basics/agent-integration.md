# Agent Integration — Grafana Basics

## When to use
- Surfacing Prometheus / Loki / Tempo data the team already collects but never looks at — turning silent metrics into a dashboard the on-call actually opens.
- Building per-service RED/USE/Golden-Signals dashboards as part of a service onboarding template, so every new service ships with the same five panels.
- SLO/error-budget visualization once recording rules exist (`job:slo_burn:ratio_rate1h`).
- Incident-response timelines: combining annotations (deploys, releases) with metrics on a single graph.
- Loki log exploration with `LogQL` next to the metric panel that triggered an alert (split-pane view).

## When NOT to use
- As the metrics store itself. Grafana is a rendering layer; a missing datasource or a slow Prometheus is the real failure.
- For long-term query performance audits — use `pprof`/Mimir directly, not the dashboard.
- When you need transactional accuracy (counts must match invoicing). Time-series + downsampling produces approximations.
- As a CMDB or service catalog. Use Backstage / Cortex / Port; Grafana drops "soft" labels.
- Single-pane-of-glass for security events (SIEM). Use Grafana for ops; route auth/audit logs to a SIEM.

## Where it fails / limitations
- Dashboards built ad-hoc in the UI drift away from JSON in Git — agents that "just edit the dashboard" lose changes on next provisioning sync.
- Variable misuse: `$namespace` defined as multi-value but the panel query uses `=~"$namespace"` without `regex_replace_chars`. A namespace named `prod-eu` becomes a regex that matches anywhere.
- Heatmap panels need histogram metrics with `le` buckets — agents replace `histogram_quantile` with `quantile` (a different function) and the latency p95 silently misreports.
- Stat panels with "Last (not null)" reducer cache stale values during scrape gaps; the dashboard looks healthy while the service is dead.
- Time-zone confusion: dashboard default vs user override vs alert evaluation TZ — three different "now"s.
- Alert rules defined inside dashboard panels (legacy "Dashboard alerts") are not the same surface as Grafana Alerting / Prometheus rules; they're fragile and easy to lose.

## Agentic workflow
Treat dashboards as code from day one. One agent generates a dashboard JSON from a service spec (RED + golden signals + variables + thresholds), a reviewer agent (Opus) checks PromQL against actual metric names exposed by the service (`/metrics` curl) and rejects panels that reference non-existent metrics. A third agent diffs the new JSON against the existing provisioned file and produces a Grafana folder PR. Never let an agent click in the UI; always go through `grafana-cli`, the HTTP API, or Grafonnet.

### Recommended subagents
- `faion-sdd-executor-agent` — drives spec → JSON → review → provision PR.
- A custom `dashboard-promql-validator` (Opus, read-only) — given dashboard JSON + a metric name list, lints every panel query, flags missing labels, regex foot-guns, and quantile-vs-histogram_quantile confusion.
- `password-scrubber-agent` — datasource provisioning files often inline basic-auth tokens.

### Prompt pattern
```
Generate Grafana dashboard JSON for service <X>.
Inputs: service name, metric prefix, owner team, SLO target, scrape interval.
Output: (1) variables ($env, $namespace, $instance), (2) RED row (rate, errors%, latency p50/p95/p99), (3) USE row (CPU/mem/saturation), (4) deploy/incident annotations from `events` datasource, (5) thresholds wired to SLO.
Forbid: dashboard-internal alerts, hardcoded namespaces, multi-value vars without `regex_replace_chars`, `quantile()` on `_bucket` metrics.
```

```
Validate dashboard JSON against `curl http://svc/metrics`. For every panel, list (panel_id, query, missing_metrics[], missing_labels[]). Reject if any list non-empty.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `grafana-cli` | Plugin install, admin reset, db migration | https://grafana.com/docs/grafana/latest/cli/ |
| `grizzly` (`grr`) | Apply Grafana resources from YAML/Jsonnet (kubectl-like) | https://grafana.github.io/grizzly/ |
| `grafonnet` | Jsonnet library for dashboard generation | https://grafana.github.io/grafonnet/ |
| `jsonnet` / `jb` (jsonnet-bundler) | Build Grafonnet output | https://github.com/jsonnet-bundler/jsonnet-bundler |
| Grafana HTTP API | CRUD dashboards/folders/datasources via `curl` | https://grafana.com/docs/grafana/latest/developers/http_api/ |
| `promtool check rules` | Validate PromQL in recording/alert rules used by panels | https://prometheus.io/docs/prometheus/latest/command-line/promtool/ |
| `dashboard-linter` (Grafana Labs) | Lints JSON dashboards for best practices | https://github.com/grafana/dashboard-linter |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Grafana OSS | OSS | Yes | Provisioning + HTTP API + service accounts. |
| Grafana Cloud | SaaS | Yes | Free tier sufficient for solo projects; API tokens scoped per stack. |
| Grafana Enterprise | SaaS/self-hosted | Yes | Adds RBAC, reporting, data-source permissions. |
| Mimir / Cortex / Thanos | OSS | Yes | Long-term Prometheus storage; same PromQL surface. |
| Loki | OSS / SaaS | Yes | LogQL queries inside Grafana panels. |
| Tempo | OSS / SaaS | Yes | Trace links from logs/metrics via `derivedFields`. |
| Pyroscope | OSS / SaaS | Partial | Continuous profiling source; agent must understand flame-graph panel. |

## Templates & scripts
See `templates.md` and `examples.md` for full panels. Inline Grafonnet skeleton (≤30 lines) for a RED dashboard:

```jsonnet
local g = import 'grafonnet/main.libsonnet';
local prom = g.query.prometheus;
local var = g.dashboard.variable;

g.dashboard.new('svc/%s' % std.extVar('service'))
+ g.dashboard.withVariables([
    var.query.new('env', prom.new('Prometheus', 'label_values(up{job=~"$service"}, env)')),
    var.query.new('instance', prom.new('Prometheus', 'label_values(up{job=~"$service",env=~"$env"}, instance)')),
])
+ g.dashboard.withPanels([
    g.panel.timeSeries.new('Rate (req/s)')
    + g.panel.timeSeries.queryOptions.withTargets([
        prom.new('Prometheus', 'sum by (route) (rate(http_requests_total{job=~"$service",env=~"$env"}[5m]))'),
      ]),
    g.panel.timeSeries.new('Errors %')
    + g.panel.timeSeries.queryOptions.withTargets([
        prom.new('Prometheus', '100 * sum(rate(http_requests_total{job=~"$service",status=~"5.."}[5m])) / sum(rate(http_requests_total{job=~"$service"}[5m]))'),
      ]),
    g.panel.timeSeries.new('Duration p95')
    + g.panel.timeSeries.queryOptions.withTargets([
        prom.new('Prometheus', 'histogram_quantile(0.95, sum by (le) (rate(http_request_duration_seconds_bucket{job=~"$service",env=~"$env"}[5m])))'),
      ]),
])
```

## Best practices
- Every dashboard goes through provisioning. UI changes are a smell: export, diff, PR.
- Variables use `label_values()` filtered by parent variables, never hand-typed lists.
- Threshold colors: green / amber / red mapped to SLO bands, not arbitrary numbers — and store the SLO target in a constant variable (`$slo_target`).
- Annotations from a `events` table or `deployment_events_total` metric — bind deploys to graphs so spikes are explainable.
- Always link related dashboards (`Dashboard links`): service → host → cluster → company-wide overview. Drill-down in three clicks.
- Use recording rules (`job:rate5m`, `job:errors:ratio_rate5m`) — never compute heavy expressions inside a dashboard query.
- Set the data-source as a variable (`$datasource`), so the same JSON works in dev/staging/prod.

## AI-agent gotchas
- Agents fabricate metric names that "sound right" (`http_request_count` vs the actual `http_requests_total`) — always validate against `/metrics` before merging.
- LLMs reach for `irate(...[1m])` because it appears in tutorials, then dashboards flicker on slow scrape intervals. Force `rate(...[$__rate_interval])`.
- Multi-value variables expand to a regex; agents wire `=` instead of `=~`. The dashboard works for one selection and silently breaks for two.
- LLMs recreate Prometheus metrics inside the dashboard ("calculate p95 from raw events") instead of using the existing `_bucket` series — produces wrong numbers and slow queries.
- Dashboards generated from natural language tend to overfit the demo: hardcoded `namespace="default"`, `instance="localhost:9090"`. Force every panel to reference a variable.
- Human-in-loop checkpoint: any new dashboard goes to a reviewer who sanity-checks SLO mapping and verifies the dashboard renders with empty/no-data series (not just the happy path).
- `dashboard-linter` in CI is non-negotiable — agents pass it once and forget it; pin the linter version so rule changes don't surprise.

## References
- Grafana docs — https://grafana.com/docs/grafana/latest/
- Build dashboards: best practices — https://grafana.com/docs/grafana/latest/dashboards/build-dashboards/best-practices/
- Grafonnet — https://grafana.github.io/grafonnet/
- Dashboard linter — https://github.com/grafana/dashboard-linter
- Grizzly — https://grafana.github.io/grizzly/
- USE method (Brendan Gregg) — https://www.brendangregg.com/usemethod.html
- Google SRE: Four Golden Signals — https://sre.google/sre-book/monitoring-distributed-systems/
