# Prometheus Monitoring

## Summary

Prometheus is the de facto standard for Kubernetes and cloud-native monitoring: pull-based metrics collection, PromQL queries, and Alertmanager routing. Never use unbounded labels (user IDs, request IDs) — each unique label combination creates a new time series and can cause out-of-memory crashes. Alert on symptoms (error rate), not causes (specific errors).

## Why

Pull-based collection and a simple data model make Prometheus reliable by default — a scrape failure is immediately visible as a gap rather than silent data loss. PromQL's rate/histogram_quantile functions enable SLI measurement directly from application metrics without a separate observability stack.

## When To Use

- Kubernetes cluster and workload monitoring (kube-state-metrics, node-exporter, cAdvisor)
- Application SLI/SLO measurement via custom metrics
- Alert routing with Alertmanager (Slack, PagerDuty, email)
- Pre-computing expensive dashboard queries with recording rules
- Long-term storage via remote write to Thanos, Mimir, or Cortex

## When NOT To Use

- Log aggregation — use Loki or ELK; Prometheus is metrics only
- Distributed tracing — use Jaeger or Tempo
- High-cardinality event data (per-request attributes) — use a log/trace system
- When you need sub-second resolution — Prometheus scrape interval minimum is ~10s

## Content

| File | What's inside |
|------|---------------|
| `content/01-concepts.xml` | Metric types (counter/gauge/histogram/summary), naming conventions, label cardinality rules |
| `content/02-configuration.xml` | Scrape intervals, ServiceMonitor/PodMonitor CRDs, recording rules, alerting philosophy |
| `content/03-promql.xml` | PromQL selectors, aggregations, rate functions, SLI query patterns |

## Templates

| File | Purpose |
|------|---------|
| `templates/prometheus-rule.yaml` | PrometheusRule CRD with recording rules and alert examples |
| `templates/servicemonitor.yaml` | ServiceMonitor CRD for scraping a Kubernetes service |
| `templates/alertmanager-config.yaml` | Alertmanager routing config with Slack and PagerDuty receivers |
| `templates/prompt-monitoring-strategy.txt` | LLM prompt for designing a monitoring strategy for microservices |
