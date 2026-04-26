# Agent Integration — Prometheus Monitoring

## When to use
- Kubernetes / Nomad / VM-based fleet that needs metrics + alerting (the de-facto choice).
- Microservices observability with `/metrics` endpoints (RED + Golden Signals).
- CI/CD pipeline SLIs (build duration, failure rate) — via Pushgateway for short-lived jobs and exporters for vendor pipelines.
- Recording rules + Alertmanager for SLO-based alerting and error-budget burn.
- Custom application metrics from any language with a Prometheus client library.
- Long-term storage via Mimir/Cortex/Thanos when you outgrow local TSDB.

## When NOT to use
- High-cardinality event streams (per-request, per-user) — use logs/traces (Loki/Tempo) instead.
- Strict-accuracy billing / financial counters — Prometheus samples and gaps in scrape; counts may be off by ε.
- Push-only / firewall-traversed environments where pull is impossible — consider OpenTelemetry collector + remote write or Grafana Cloud receivers.
- One-time batch metrics where Pushgateway is the only fit and you don't have time to operate it correctly.
- As an APM replacement (no transaction context propagation) — pair with OpenTelemetry traces.

## Where it fails / limitations
- **Cardinality explosion** is the #1 outage cause: a label like `user_id`, `request_id`, `path` (without normalization) produces millions of series and OOMs Prometheus. Agents don't know your label cardinality limits.
- Pull model + dynamic targets requires service discovery (k8s SD, Consul, etc.); agents writing static `targets: []` lose half the fleet on autoscale.
- Scrape interval ≠ alert evaluation interval; agents tune one and not the other, producing lag in alerts.
- `rate()` over `_total` counters needs a window ≥ 4× scrape interval; agents use `[1m]` over 15s scrapes and graphs flicker.
- `histogram_quantile` requires `le` buckets — agents replace with `quantile()` (a different function, takes a vector) and silently misreport p95.
- Pushgateway accumulates orphan jobs; without `delete_after` cleanup, dead jobs alert forever.
- Recording rules accumulate stale series after refactors; without `tsdb.delete-series` housekeeping, disk pressure rises.
- Alertmanager group_by misuse: `group_by: ['...']` (literal triple dot) wildcards too aggressively; agents copy-paste and pages stop firing per-instance.
- Grafana Agent retired 2025-11; running it now means missing security fixes. Migrate to Grafana Alloy.
- Federation hides issues: child Prometheus dies, federation appears empty but silently — needs `up{job="federate"}` alerting.

## Agentic workflow
Treat scrape configs, alert rules, and recording rules as code. One agent generates `ServiceMonitor`/`PodMonitor` (kube-prometheus-stack) or static `prometheus.yml` from a service spec; a reviewer agent (Opus) runs `promtool check config/rules` and lints labels for cardinality risk against a documented per-label budget. A separate agent runs `mimirtool/cortextool rules diff` against the cluster before apply. Always validate alert rules against historic data with `promtool test rules` before pushing to prod.

### Recommended subagents
- `faion-sdd-executor-agent` — drives spec → rules → review → apply → verify gates.
- A custom `prometheus-cardinality-auditor` (Opus, read-only) — given a `/metrics` snapshot + label budget table, lists labels that exceed budget with sample series, plus suggested aggregation/normalization.
- A custom `prometheus-rule-validator` (Sonnet) — runs `promtool check rules`, `promtool test rules`, and reports failures + diff vs cluster.
- `password-scrubber-agent` — `remote_write` URLs + basic-auth secrets often inline.

### Prompt pattern
```
Generate Prometheus ServiceMonitor + alert/recording rules for service <X>.
Inputs: service name, port, /metrics path, scrape interval, SLO target (latency/availability), expected RPS, namespace, label budget (max distinct values per label).
Output: (1) ServiceMonitor YAML, (2) recording rules (`job:rate5m`, `job:errors:ratio_rate5m`, `job:latency:p95_rate5m`), (3) alert rules (multi-window multi-burn-rate for SLO), (4) runbook URLs, (5) cardinality estimate per label.
Forbid: `quantile()` on `_bucket`, `irate(...[<scrape*4])`, labels listed in label budget as "do-not-use" (e.g., user_id, request_id), missing `for` clause, duplicate alert names.
```

```
Validate rules. Run promtool. JSON: {syntax_ok:bool, tests_pass:int/total, cardinality_warnings:[{metric,label,distinct_estimate}], rule_diff_vs_cluster:[], approve:bool}.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `promtool check config` / `check rules` / `test rules` / `query` | Validate + test | https://prometheus.io/docs/prometheus/latest/command-line/promtool/ |
| `amtool` | Alertmanager config + silence mgmt | https://github.com/prometheus/alertmanager |
| `mimirtool` / `cortextool` | Rules CRUD against Mimir/Cortex | https://grafana.com/docs/mimir/latest/manage/tools/mimirtool/ |
| `prom-client` libs | Instrument code (Python/Go/Node/Java/Rust) | https://prometheus.io/docs/instrumenting/clientlibs/ |
| `node_exporter` | Host metrics | https://github.com/prometheus/node_exporter |
| `kube-state-metrics` | K8s object state | https://github.com/kubernetes/kube-state-metrics |
| `blackbox_exporter` | Probe endpoints (HTTP/TCP/ICMP/DNS) | https://github.com/prometheus/blackbox_exporter |
| `prometheus-operator` | K8s operator | https://prometheus-operator.dev/ |
| `kube-prometheus-stack` Helm | Bundled stack | https://github.com/prometheus-community/helm-charts |
| Grafana Alloy | Telemetry agent (replaces Grafana Agent) | https://grafana.com/docs/alloy/latest/ |
| OpenTelemetry Collector | Multi-protocol; can write Prometheus remote_write | https://opentelemetry.io/docs/collector/ |
| `pyroscope-cli` | Continuous profiling pair | https://pyroscope.io/ |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Prometheus OSS | OSS | Yes | TSDB + Alertmanager. |
| Mimir | OSS | Yes | Long-term, multi-tenant Prometheus storage. |
| Cortex | OSS | Yes | Multi-tenant Prometheus (older). |
| Thanos | OSS | Yes | HA + long-term + global query. |
| VictoriaMetrics | OSS / SaaS | Yes | Faster, lower-resource alt; remote_write compatible. |
| Grafana Cloud Metrics | SaaS | Yes | Hosted Prometheus + Alertmanager + Mimir. |
| AWS Managed Service for Prometheus (AMP) | SaaS | Yes | IAM-authed remote_write; integrate with Alloy. |
| Azure Monitor managed Prometheus | SaaS | Yes | AAD-authed remote_write. |
| GCP Managed Service for Prometheus | SaaS | Yes | OpenTelemetry + Prom; native to GKE. |
| Pushgateway | OSS | Partial | Short-lived jobs only; stewardship needed (TTLs). |
| Alertmanager | OSS | Yes | Routing, dedup, silences; HA via gossip. |

## Templates & scripts
See `templates.md` and `examples.md` for full ServiceMonitor + rule sets. Inline SLO multi-window multi-burn-rate alert pair (≤40 lines):

```yaml
# slo-alerts.yaml — 99.9% availability over 30d, page on fast burn, ticket on slow burn.
groups:
- name: slo-orders-api
  interval: 30s
  rules:
  - record: job:errors:ratio_rate1h
    expr: |
      sum(rate(http_requests_total{job="orders-api",status=~"5.."}[1h]))
        /
      sum(rate(http_requests_total{job="orders-api"}[1h]))
  - record: job:errors:ratio_rate5m
    expr: |
      sum(rate(http_requests_total{job="orders-api",status=~"5.."}[5m]))
        /
      sum(rate(http_requests_total{job="orders-api"}[5m]))
  - alert: SLOBurnFast
    expr: |
      job:errors:ratio_rate5m > (14.4 * 0.001)
      and
      job:errors:ratio_rate1h > (14.4 * 0.001)
    for: 2m
    labels: { severity: page, slo: orders-api }
    annotations:
      summary: "Fast SLO burn for orders-api"
      runbook_url: "https://runbooks/orders-api-slo"
  - alert: SLOBurnSlow
    expr: |
      job:errors:ratio_rate5m > (1 * 0.001)
      and
      sum(rate(http_requests_total{job="orders-api",status=~"5.."}[6h]))
        /
      sum(rate(http_requests_total{job="orders-api"}[6h])) > (1 * 0.001)
    for: 15m
    labels: { severity: ticket, slo: orders-api }
    annotations:
      summary: "Slow SLO burn for orders-api"
      runbook_url: "https://runbooks/orders-api-slo"
```

## Best practices
- Document a per-service label budget (max distinct values per label) and enforce in CI via the cardinality auditor.
- Recording rules for any expression used in 2+ dashboards or alerts; speeds queries 10-100x.
- Multi-window multi-burn-rate SLO alerts (Google SRE workbook) — fewer false alarms, faster real ones.
- Use `kube-prometheus-stack` or Grafana Alloy + managed backend; rolling your own bare Prometheus + node-exporter wastes time.
- Set `external_labels: cluster, region, env` on every Prometheus — federations and remote_write need these.
- Pushgateway only when you must (CI batch, deploy events); set TTLs and use `delete_persistence_file` cleanup.
- Alertmanager: route by `severity`, group by `alertname, cluster, service`, never by ad-hoc label sets.
- `for:` clause >= 5× scrape_interval to dampen flapping.
- Always include `runbook_url` annotation; on-call without runbooks is on-call without sleep.
- Use `histogram_quantile(0.95, sum by (le) (rate(..._bucket[$__rate_interval])))` — never `quantile()` on histograms.
- Migrate Grafana Agent to Alloy; pin chart versions; review changelogs.

## AI-agent gotchas
- Agents instrument with high-cardinality labels (`user_id`, `email`, `path` raw) — costs explode. Force a label-budget review before merging instrumentation.
- LLMs use `irate()` because it appears in tutorials; produces flickery short-window graphs. Default to `rate(...[$__rate_interval])`.
- Alert rules without `for:` flap on every scrape jitter.
- `absent()` on a label-rich metric requires careful matchers; agents write `absent(http_requests_total)` and the alert fires the moment the metric is renamed.
- Pushgateway grouping key — agents push without `instance` label and overwrite each other.
- Federation regex `match[]` filter copy-pasted blindly federates everything → child Prometheus disk fills up. Always scope.
- `remote_write` queue config defaults are too low for chatty fleets; agents see backlog warnings and increase `max_samples_per_send` without raising `max_shards` — backlog persists.
- Agents propose Grafana Agent in 2026 configs; force Alloy.
- Alertmanager silence creation through API: agents forget to set expiry, silence persists forever.
- Human-in-loop checkpoint: new SLO targets, paging routes, and label-budget changes need human approval. Cardinality regressions are expensive and not always reversible without data loss.
- Don't let one agent write rules and ack alerts; split ownership.

## References
- Prometheus docs — https://prometheus.io/docs/
- Prometheus best practices — https://prometheus.io/docs/practices/
- Google SRE workbook (alerting on SLOs) — https://sre.google/workbook/alerting-on-slos/
- kube-prometheus-stack — https://github.com/prometheus-community/helm-charts
- Prometheus Operator — https://prometheus-operator.dev/
- CNCF: Prometheus labels best practices — https://www.cncf.io/blog/2025/07/22/prometheus-labels-understanding-and-best-practices/
- Mimir docs — https://grafana.com/docs/mimir/latest/
- Alertmanager docs — https://prometheus.io/docs/alerting/latest/alertmanager/
- Grafana Alloy — https://grafana.com/docs/alloy/latest/
- VictoriaMetrics — https://docs.victoriametrics.com/
