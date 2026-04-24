# Agent Integration — Observability Architecture

## When to use
- New service / new bounded context — instrument *before* shipping; retrofitting is 5x the cost.
- Recurring "I have no idea why this is slow" / "support says it's broken, dashboards say it's fine" incidents.
- SLO / SRE adoption — observability is the substrate; without correlated metrics + logs + traces, SLOs are guesses.
- Multi-service request flows where bugs span 3+ hops (latency hotspots, intermittent errors, sporadic data loss).
- Cost-spiral on existing observability vendors (Datadog bill grew 4x) — re-architect with cardinality limits, sampling, and tiered retention.
- Compliance / forensics requirement — structured, retained, queryable logs with PII handling.
- AI / LLM features — token cost, prompt latency, tool-call success rate are first-class SLIs that need their own pipeline.

## When NOT to use
- Hobby / pre-PMF — `print` + a single Sentry account covers you. Full OTEL stack is over-engineering.
- Fully serverless event-driven app with managed observability already wired (CloudWatch + X-Ray); don't introduce parallel stack until the gap is real.
- Tiny single-service dashboard with <100 RPS — Grafana + Prometheus + Loki on one VM is enough; no need for Tempo/Mimir.
- The team won't look at the dashboards — telemetry without rituals is paid storage. Build the dashboards customers and on-call actually use.
- Hot path with strict latency budget where instrumentation overhead matters — sample, don't measure everything.

## Where it fails / limitations
- **High-cardinality blowup.** Putting `user_id`, `request_id`, or full URLs into label sets explodes Prometheus / Mimir storage cost. Cardinality discipline is the single biggest reliability factor in the metrics layer.
- **Logs ≠ debugger.** Unstructured logs cannot be correlated; agents and humans alike fish through grep and miss the bug.
- **Trace sampling that hides incidents.** Head-based 1% sampling drops the rare slow request that *is* the bug. Tail-based sampling (kept-if-error-or-slow) is far more useful.
- **Vendor lock-in via instrumentation.** Wiring Datadog SDK into application code makes "switch vendors" a code change. OpenTelemetry decouples instrumentation from backend.
- **Alert fatigue.** Threshold alerts on every metric turn the on-call into a slot machine; SLO burn-rate alerting is the only sustainable pattern.
- **Dashboard sprawl.** 200 dashboards, 5 used. Consolidate around Golden Signals / RED / USE; archive the rest.
- **PII in logs.** Free-text logs leak emails, tokens, prompts; without scrubber + log-retention policy, you have a GDPR incident waiting.
- **Trace-log decoupling.** Traces lack `service.name` / `trace_id` consistency; logs don't include `trace_id`. Without both, jumping from "slow request" to "what did it log?" doesn't work.
- **Cost / value mismatch.** Most teams retain hot logs and metrics far longer than they query them. Tiered retention (hot 7d, warm 30d, cold 1y) saves real money.

## Agentic workflow
Drive observability adoption as a four-pass pipeline: (1) an instrumentation agent walks each service and adds OpenTelemetry spans, structured logging, and Golden Signals / RED metrics — vendor-agnostic; (2) a dashboard-generator agent emits Grafana dashboards bound to per-service SLIs (PromQL / LogQL / TraceQL); (3) an alert-generator agent emits multi-window/multi-burn-rate alerts per SLO and runbook stubs; (4) a cost / cardinality auditor inspects label sets, log volume, trace sample rates, and flags expensive offenders. Critical: agents must always loop a human in for sample-rate / retention changes — those are budget decisions disguised as configs.

### Recommended subagents
- `faion-sdd-executor-agent` (`agents/faion-sdd-executor-agent.md`) — instrument-as-you-build: every PR touching a service must include trace spans + a metric + a structured log line for the new code path.
- A purpose-built **dashboard generator** (worth creating): given `slo.yaml`, emit Grafana JSON with Golden Signals panels and SLO burn-rate panels.
- A purpose-built **cardinality auditor**: read Prometheus `tsdb-status` JSON / Mimir analyzer output; flag labels whose cardinality > N or growth rate > M/day.
- A purpose-built **runbook generator**: per alert rule, emit `runbooks/<alert>.md` with detection, diagnosis, mitigation, escalation, and links to relevant dashboards / traces.
- `password-scrubber-agent` — log lines, traces, dashboards routinely include credentials, customer IDs, raw prompts. Scrub before sharing externally.

### Prompt pattern
Instrumentation:
```
Walk src/. For each public HTTP / gRPC handler, add OpenTelemetry
spans (auto-instrumentation if framework supported, manual otherwise),
a structured log line at INFO entry/exit including trace_id and
business identifiers, and a histogram metric `<service>_http_request_duration_seconds`
with labels {method, route, status_class}. Reject label sets that
include user_id, email, or path with raw IDs.
```

Cardinality audit:
```
Read tsdb_status.json. For each metric, list the top 10 labels by
cardinality and the labels with growth rate > 5% / week. Flag any
label that looks like an unbounded identifier (regex: 'id', 'uuid',
'token', 'session'). Output a remediation plan: which labels to drop,
which to bucket (e.g., status_class instead of raw status code).
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `otel-cli` | Send OTEL spans/metrics from shell scripts | https://github.com/equinix-labs/otel-cli |
| `prometheus` / `promtool` | Validate alerting + recording rules | https://prometheus.io |
| `pyrra` / `sloth` / `slo-generator` | Generate SLO Prometheus rules from declarative spec | https://github.com/pyrra-dev/pyrra ; https://sloth.dev |
| `logcli` (Loki) | Query logs from terminal with LogQL | https://grafana.com/docs/loki/latest/query/logcli/ |
| `tempo-cli` | Inspect trace backends, repair tenant indexes | https://grafana.com/docs/tempo/latest/operations/cli/ |
| `mimirtool` | Manage Mimir tenants, validate rules, analyze cardinality | https://grafana.com/docs/mimir/latest/manage/tools/mimirtool/ |
| `jaeger-query` | Query traces from Jaeger | https://www.jaegertracing.io |
| `grafanactl` / `grizzly` | Manage Grafana dashboards as code | https://github.com/grafana/grizzly |
| `vector` | Pipe / transform / route logs and metrics; cheap log preprocessing | https://vector.dev |
| `tcpdump` / `mitmproxy` | Validate that what you think is being sent actually is | bundled |
| `claude` (Anthropic CLI) | Run instrumentation / dashboard / alert / audit passes headless | https://docs.anthropic.com |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| OpenTelemetry Collector | OSS | yes | Vendor-agnostic instrumentation; the load-bearing piece. Avoid wiring SDKs directly to vendors. |
| Grafana LGTM (self-host or Cloud) | OSS / SaaS | yes | Loki + Grafana + Tempo + Mimir; cheapest credible stack. |
| Datadog | SaaS | yes | Full APM + logs + metrics + RUM; fastest to adopt, most expensive at scale. |
| New Relic | SaaS | yes | Strong APM; pricing model worth modeling before commitment. |
| Honeycomb | SaaS | yes | Best-in-class wide events / high-cardinality querying for distributed debugging. |
| Splunk / Sumo Logic / Elastic Cloud | SaaS | yes | Heavyweight log analytics; common in enterprises. |
| AWS CloudWatch / GCP Cloud Logging / Azure Monitor | SaaS | yes | Cloud-native; cheap entry point, expensive at scale. |
| Sentry | SaaS / OSS | yes | Error tracking with releases / breadcrumbs / source maps; pair with the above. |
| BetterStack / OpsGenie / PagerDuty | SaaS | yes | Alert routing; SLO burn-rate hooks. |
| Lightstep / SigNoz / Uptrace | SaaS / OSS | yes | OTEL-native APM alternatives. |
| Coralogix / Logz.io | SaaS | yes | Mid-market log analytics with OTEL support. |
| Cloudflare Logpush + R2 | SaaS | yes | Cheap edge-log ingestion + cold storage. |

## Templates & scripts
The README ships RED/USE/Golden Signals + LGTM stack + structured-log shape. The high-leverage missing piece is a **PromQL recording-rules pack** for the canonical service shape so dashboards and alerts wire up identically across services. Inline drop-in (≤50 lines):

```yaml
# observability/recording_rules.yaml — canonical RED rules per service.
# Validate: promtool check rules observability/recording_rules.yaml
groups:
  - name: service_red
    interval: 30s
    rules:
      - record: service:http_requests:rate5m
        expr: sum by (service, status_class) (
          rate(http_server_requests_total[5m])
        )
      - record: service:http_errors:rate5m
        expr: sum by (service) (
          rate(http_server_requests_total{status_class="5xx"}[5m])
        )
      - record: service:http_latency_seconds:p99_5m
        expr: histogram_quantile(
          0.99,
          sum by (service, le) (
            rate(http_server_request_duration_seconds_bucket[5m])
          )
        )
      - record: service:http_availability:ratio_30d
        expr: 1 - (
          sum by (service) (
            increase(http_server_requests_total{status_class="5xx"}[30d])
          )
          /
          sum by (service) (
            increase(http_server_requests_total[30d])
          )
        )
  - name: service_burn_rate
    rules:
      - alert: ServiceBurnRateFast
        expr: service:http_errors:rate5m / service:http_requests:rate5m
              > (1 - 0.999) * 14.4
        for: 2m
        labels: { severity: page }
        annotations:
          summary: "{{ $labels.service }} burning fast 2%/1h"
          runbook: "runbooks/burn-rate.md"
```

Pair with: a `recording_rules` job in CI that runs `promtool check rules` and `mimirtool rules diff` against staging.

## Best practices
- **OpenTelemetry, not vendor SDKs.** Instrument once with OTEL; backends are configured in the collector. Vendor-portability matters because vendor pricing changes.
- **Structured logs from line one.** JSON, with `service.name`, `trace_id`, `span_id`, `level`, `timestamp`. Free-text logs die in production.
- **Trace ID propagation across every hop.** W3C Trace Context in HTTP, message broker headers, scheduled-job context. Without it, distributed debug is impossible.
- **RED for services, USE for resources, Golden Signals as the dashboard skeleton.** Don't invent your own taxonomy.
- **SLO burn-rate alerts only.** Threshold alerts on raw metrics ("CPU > 80%") are noise. Burn rate is the only signal worth waking someone up for.
- **Cardinality budgets per service.** Document max cardinality per metric; reject merge if a new label adds >Nk series.
- **Sampling: head 100% in dev, tail-based in prod.** Always keep error and high-latency traces; sample healthy ones aggressively.
- **PII scrubber in the collector pipeline.** Don't trust application code to scrub; do it at the collector.
- **Tiered retention.** Logs: 7d hot, 30d warm S3, 1y cold. Metrics: 15d high-res, 1y downsampled. Traces: 7d. Tune to actual query patterns.
- **Dashboards as code.** Store JSON in git, deploy via grizzly / Terraform; click-ops dashboards rot.
- **Runbook per alert.** Linked from the annotation; reviewed when the alert changes.
- **Observability for the agent itself.** When agents ship code, instrument with `agent.name`, `agent.run_id`, `model`, `prompt_tokens` — a new pillar in 2026 stacks.

## AI-agent gotchas
- **Cardinality bombs.** Agents merrily add `user_id`, `tenant_id`, raw URL paths as Prometheus labels. Lint label names against an allow-list; reject unbounded identifiers.
- **`print` instead of structured log.** Generated code uses `print(f"…")`; ruff `T201` catches it. Force structured loggers (`structlog`, Python `logging.JSONFormatter`).
- **Vendor SDK coupling.** Agents `import datadog` / `import newrelic_agent` directly into business logic. Force OTEL SDK + collector exporter pattern.
- **Trace ID lost across async hops.** Agents spawn `asyncio.create_task` without context propagation; trace breaks. Use `opentelemetry.context.attach`.
- **Hallucinated metric names.** Agents reference `http_request_count` in dashboards, but instrumentation emits `http_server_requests_total`. Validate metric names against a registry / catalogue.
- **Logs without trace_id.** Generated logs missing the correlation field. Add a logging filter that injects `trace_id`/`span_id` from the active context.
- **Alert without runbook.** Agents emit alert rules with empty `annotations.runbook`. Reject in CI.
- **Sample-rate change in a perf-critical path.** Agents change `OTEL_TRACES_SAMPLER_ARG` from `0.01` to `1.0` and bury it in a refactor PR. Diff sample rates in CI; gate behind human review.
- **Threshold-alert spam.** Agents create per-metric threshold alerts ("p99 > X"); override with SLO burn-rate templates only.
- **PII in dashboard panels.** Agents put raw email addresses in table panels for "easier debugging." Hard rule: dashboards consume scrubbed/aggregated data only.
- **Wrong base unit for histograms.** Agents emit latency in milliseconds while Prometheus convention is seconds; downstream PromQL silently divides by 1000 nowhere. Force `_seconds` suffix discipline.
- **Dashboard JSON drift.** Agents edit Grafana via UI in dev and forget to sync to git. Lock dashboards to read-only in environments without grizzly sync.
- **No human checkpoint on retention deletion.** Reducing log/trace retention is destructive and silent — never autonomous-merge.

## References
- Beyer, Murphy, et al. — "The Site Reliability Workbook," Ch. 5 ("Alerting on SLOs") + Ch. 4 ("SLOs"). https://sre.google/workbook/
- Majors, C., et al. — "Observability Engineering." O'Reilly, 2022.
- Sridharan, C. — "Distributed Systems Observability." O'Reilly, 2018. (Free)
- OpenTelemetry docs — concepts, instrumentation, collector. https://opentelemetry.io/docs/
- W3C Trace Context. https://www.w3.org/TR/trace-context/
- Grafana — "LGTM stack docs." https://grafana.com/docs/
- Prometheus — Naming and labels best practices. https://prometheus.io/docs/practices/naming/
- Honeycomb — "Cardinality matters." https://www.honeycomb.io/blog/cardinality-matters
- Sibling: `pro/dev/software-architect/reliability-architecture/` (this batch).
- Sibling: `pro/dev/software-architect/quality-attributes-analysis/` (this batch).
- Sibling: `pro/infra/devops-engineer/`.
