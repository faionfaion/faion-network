# Prometheus Monitoring

## Summary

**One-sentence:** Prometheus monitoring spec: metric naming + label cardinality limits + recording rules + alert hygiene + scrape-interval discipline for Kubernetes workloads.

**One-paragraph:** Prometheus is the default Kubernetes monitoring stack: pull-based metrics, PromQL queries, Alertmanager routing. The trap teams fall into: unbounded labels (user_id, request_id) blow up cardinality; counter values used directly in dashboards produce sawtooth graphs; alerts fire on causes (pod crashed) instead of symptoms (error rate up) creating alert fatigue. This methodology codifies the rules: histograms over summaries for distributed latency, snake_case namespace_name_unit naming, label-cardinality ≤10, scrape interval ≥15s default, recording rules for expensive dashboard queries, symptom-based alerts with runbook URLs.

**Ефективно для:**

- Kubernetes workload observability — service discovery + scrape + alert.
- Custom-metrics для SLI/SLO measurement (RED/USE method).
- Контроль cardinality blowup до того, як Prometheus OOM-нется.
- Recording rules для expensive dashboard queries (10x швидше).

## Applies If (ALL must hold)

- Kubernetes cluster with workloads needing metric-based observability
- Application SLI/SLO measurement via custom metrics (RED / USE method)
- Alert routing with Alertmanager (Slack, PagerDuty, email)
- Pre-computing expensive dashboard queries with recording rules

## Skip If (ANY kills it)

- Log aggregation — use Loki or ELK; Prometheus is metrics only
- Distributed tracing — use Jaeger or Tempo, not Prometheus
- High-cardinality event data (per-request attributes) — use log/trace systems
- Sub-second resolution required — Prometheus scrape interval minimum ~10s

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Prometheus + Alertmanager + node-exporter | Helm charts or operator install | platform team |
| ServiceMonitor CRD (Prometheus Operator) | Kubernetes manifests | ops |
| Long-term storage backend (Thanos / Mimir / Cortex) | object-storage bucket + remote_write config | platform team |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[alert-deduplication-playbook]] | Alert hygiene context — what 'good alert' means |
| [[slo-definition-template-per-service-class]] | Defines SLI targets the metrics measure |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 7 testable rules with rationale + source | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid/forbidden examples | ~800 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns with symptom/root-cause/fix | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure with input/action/output | ~700 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `metric_audit` | haiku | Mechanical listing of cardinality offenders |
| `rule_rewrite` | sonnet | Bounded judgment on symptom vs cause |
| `recording_rule_design` | sonnet | PromQL synthesis from dashboard queries |

## Templates

| File | Purpose |
|------|---------|
| `templates/alertmanager-config.yaml` | Alertmanager config template |
| `templates/prometheus-rule.yaml` | Prometheus rule template |
| `templates/prompt-monitoring-strategy.txt` | Prompt monitoring strategy template |
| `templates/servicemonitor.yaml` | Servicemonitor template |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-prometheus-monitoring.py` | Validate the artefact against the output-contract schema | Pre-commit; on artefact write |

## Related

- [[alert-deduplication-playbook]]
- [[slo-definition-template-per-service-class]]
- [[alert-noise-budget]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, scope, scale) to a concrete action, each leaf referencing a rule id from `01-core-rules.xml`. Use it before applying any other section of the methodology to confirm scope and pick the right variant.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/alertmanager-config.yaml`

```yaml
apiVersion: monitoring.coreos.com/v1alpha1
kind: AlertmanagerConfig
metadata:
  name: myapp-alerts
  namespace: monitoring
spec:
  route:
    receiver: slack-critical
    groupBy: [alertname, job]
    groupWait:      30s
    groupInterval:  5m
    repeatInterval: 4h
    routes:
      - matchers:
          - name: severity
            value: critical
        receiver: pagerduty
      - matchers:
          - name: severity
            value: warning
        receiver: slack-warnings

  receivers:
    - name: slack-critical
      slackConfigs:
        - apiURL:
            key: url
            name: slack-webhook-secret
          channel: "#alerts-critical"
          title: "[CRITICAL] {{ .GroupLabels.alertname }}"
          text: "{{ range .Alerts }}{{ .Annotations.description }}\nRunbook: {{ .Annotations.runbook_url }}\n{{ end }}"
          color: "danger"

    - name: slack-warnings
      slackConfigs:
        - apiURL:
            key: url
            name: slack-webhook-secret
          channel: "#alerts-warning"
          title: "[WARNING] {{ .GroupLabels.alertname }}"
          color: "warning"

    - name: pagerduty
      pagerdutyConfigs:
        - routingKey:
            key: routing-key
            name: pagerduty-secret
          description: "{{ .GroupLabels.alertname }} — {{ .CommonAnnotations.summary }}"

  inhibitRules:
    - sourceMatchers:
        - name: severity
          value: critical
      targetMatchers:
        - name: severity
          value: warning
      equal: [alertname, job]
```

### `templates/prometheus-rule.yaml`

```yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: myapp-rules
  namespace: monitoring
  labels:
    prometheus: main
spec:
  groups:
    - name: http.recording
      interval: 30s
      rules:
        - record: job:http_requests:rate5m
          expr: sum(rate(http_requests_total[5m])) by (job)

        - record: job:http_request_duration_seconds:p99
          expr: |
            histogram_quantile(0.99,
              sum(rate(http_request_duration_seconds_bucket[5m])) by (job, le)
            )

        - record: job:sli_availability:rate5m
          expr: |
            sum(rate(http_requests_total{status!~"5.."}[5m])) by (job)
            / sum(rate(http_requests_total[5m])) by (job)

    - name: http.alerts
      rules:
        - alert: HighErrorRate
          expr: |
            1 - job:sli_availability:rate5m < 0.95
          for: 5m
          labels:
            severity: critical
          annotations:
            summary: "High error rate for {{ $labels.job }}"
            description: "Availability {{ $value | humanizePercentage }} below 95%"
            runbook_url: "https://runbooks.example.com/high-error-rate"

        - alert: HighLatencyP99
          expr: job:http_request_duration_seconds:p99 > 1
          for: 10m
          labels:
            severity: warning
          annotations:
            summary: "High P99 latency for {{ $labels.job }}"
            description: "P99 latency is {{ $value | humanizeDuration }}"
            runbook_url: "https://runbooks.example.com/high-latency"

        - alert: ErrorBudgetBurn
          expr: |
            (1 - job:sli_availability:rate5m) / (1 - 0.999) > 14.4
          for: 5m
          labels:
            severity: critical
          annotations:
            summary: "Error budget burning at {{ $value }}x rate for {{ $labels.job }}"
            runbook_url: "https://runbooks.example.com/error-budget-burn"
```

### `templates/prompt-monitoring-strategy.txt`

```text
Design a Prometheus monitoring strategy for the following system:

System description:
[DESCRIBE THE ARCHITECTURE: microservices / monolith, language, deployment platform (K8s/bare-metal), existing metrics, current gaps]

Specific concerns:
[List the top 3-5 things you need to monitor: latency SLOs, database connection pools, queue depths, etc.]

Deliverables requested:

1. Metric inventory
   - List custom metrics to instrument per service (name, type, labels, rationale)
   - Label set design (bounded labels only — no user IDs or request IDs)
   - Naming convention validation against: namespace_name_unit_suffix pattern

2. Scrape configuration
   - Scrape intervals per service tier (critical / standard / low-priority)
   - ServiceMonitor selector strategy (label-based vs namespace-based)
   - Retention settings (local TSDB duration, remote write targets if needed)

3. Recording rules
   - Pre-compute expensive queries for dashboard load
   - SLI recording rules (availability, latency, error rate) in job:metric:operation format
   - Kubernetes aggregations (namespace/pod CPU, memory, restart rates)

4. Alerting strategy
   - Symptom-based alerts only (error rate, latency, availability — not individual pod failures)
   - Alert thresholds per SLO tier
   - for: duration guidelines to prevent flapping
   - Routing: Slack for warnings, PagerDuty for critical

5. PromQL query library
   - RED method queries (Rate, Errors, Duration) for each service type
   - SLO compliance and error budget queries
   - Kubernetes resource utilization queries

Output as YAML (PrometheusRule CRDs) and PromQL snippets, with rationale for each alert threshold.
```

### `templates/servicemonitor.yaml`

```yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: myapp
  namespace: monitoring
  labels:
    prometheus: main     # Must match the Prometheus CR's serviceMonitorSelector
spec:
  selector:
    matchLabels:
      app: myapp         # Must match the Service labels
  namespaceSelector:
    matchNames:
      - production
      - staging
  endpoints:
    - port: metrics      # Must match the Service port name
      path: /metrics
      interval: 15s
      scrapeTimeout: 10s
      honorLabels: false
```
