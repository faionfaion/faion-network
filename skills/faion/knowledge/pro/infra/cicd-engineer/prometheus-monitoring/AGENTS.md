# Prometheus Monitoring

## Summary

Prometheus is the de facto standard for metrics collection in Kubernetes and CI/CD environments. It uses a pull model with PromQL for querying, ServiceMonitor/PodMonitor CRDs for service discovery, and PrometheusRule for recording rules and alerts. Never use high-cardinality labels (user_id, UUIDs) — they blow up memory. Use `for` clause on all alerts (5–15m minimum) to prevent flapping. Use recording rules for frequently-queried dashboard expressions to reduce load.

## Why

Prometheus integrates natively with Kubernetes service discovery, Alertmanager, and Grafana. It is the only monitoring system that covers CI/CD pipeline metrics (Jenkins, GitLab CI, ArgoCD, GitHub Actions via Pushgateway) alongside application and infrastructure metrics in a single unified query language.

## When To Use

- Setting up observability for Kubernetes workloads (any scale)
- Monitoring CI/CD pipeline health (build duration, failure rate, queue depth)
- Instrumenting custom applications in Python, Node.js, or Go
- Defining SLI/SLO alerting with error budget burn rates
- Replacing a pull-based metrics system or adding long-term storage (Thanos/VictoriaMetrics)

## When NOT To Use

- Non-Kubernetes environments where push-based metrics (StatsD, InfluxDB) are already in use and migration cost is high
- Long-lived metrics storage over 30 days without Thanos/Cortex/VictoriaMetrics — Prometheus is not designed for multi-year retention
- High-cardinality event streams (per-request traces) — use Jaeger or Tempo instead

## Content

| File | What's inside |
|------|---------------|
| `content/01-concepts.xml` | Metric types, scrape model, label best practices, CI/CD tool integration matrix |
| `content/02-rules.xml` | Recording rule naming convention, alert quality rules (for clause, severity, runbook_url), Alertmanager routing rules |
| `content/03-instrumentation.xml` | Python/FastAPI, Node.js/Express, Go instrumentation patterns with RED method |
| `content/04-examples.xml` | PromQL queries for RED metrics, Kubernetes resource metrics, CI/CD-specific queries |

## Templates

| File | Purpose |
|------|---------|
| `templates/servicemonitor.yaml` | ServiceMonitor CRD template with relabeling and metric drop rules |
| `templates/prometheusrule.yaml` | PrometheusRule with recording rules + alerts for a service (parameterized) |
| `templates/alertmanager-config.yaml` | Alertmanager routing: critical to PagerDuty, warning to Slack, team routing |
| `templates/pushgateway-job.sh` | Shell script for pushing CI/CD job metrics to Pushgateway |
