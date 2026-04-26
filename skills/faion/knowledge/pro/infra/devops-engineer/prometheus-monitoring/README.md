---
id: prometheus-monitoring
name: "Prometheus Monitoring"
domain: OPS
skill: faion-devops-engineer
category: "devops"
version: "2.0.0"
updated: "2026-01-26"
---

# Prometheus Monitoring

## Overview

Prometheus is an open-source monitoring and alerting toolkit designed for reliability and scalability. It collects metrics via a pull model, stores them in a time-series database, and provides powerful querying with PromQL. It is the de facto standard for Kubernetes and cloud-native monitoring.

## Folder Structure

| File | Purpose |
|------|---------|
| [README.md](README.md) | Overview, concepts, best practices |
| [checklist.md](checklist.md) | Implementation and audit checklists |
| [examples.md](examples.md) | Code examples, PromQL queries |
| [templates.md](templates.md) | Ready-to-use YAML templates |
| [llm-prompts.md](llm-prompts.md) | Prompts for AI-assisted monitoring |

## When to Use

- Kubernetes cluster monitoring
- Microservices observability
- Custom application metrics
- Infrastructure monitoring
- Alert management with Alertmanager
- SLI/SLO measurement and tracking

## Key Concepts

| Concept | Description |
|---------|-------------|
| Metric | Numeric measurement with timestamp |
| Label | Key-value pair for metric dimensions |
| Scrape | Process of collecting metrics from targets |
| Target | Endpoint exposing metrics |
| PromQL | Query language for Prometheus |
| Alert | Condition triggering notifications |
| Recording Rule | Pre-computed query stored as new metric |
| Service Discovery | Automatic target detection |

## Metric Types

| Type | Description | Use Case |
|------|-------------|----------|
| Counter | Monotonically increasing value | Request count, errors, bytes sent |
| Gauge | Value that can go up and down | Temperature, queue size, connections |
| Histogram | Samples in configurable buckets | Request duration, response sizes |
| Summary | Quantiles over sliding window | Request duration (client-side calculation) |

## Architecture Components

```
┌─────────────────────────────────────────────────────────────────┐
│                     Prometheus Ecosystem                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐         │
│  │ Exporters   │    │ Prometheus  │    │ Alertmanager│         │
│  │ - Node      │───>│ Server      │───>│ - Routing   │         │
│  │ - Blackbox  │    │ - Scraping  │    │ - Grouping  │         │
│  │ - Custom    │    │ - Storage   │    │ - Silencing │         │
│  └─────────────┘    │ - Rules     │    └──────┬──────┘         │
│                     └──────┬──────┘           │                │
│                            │                  v                │
│                            v           ┌─────────────┐         │
│                     ┌─────────────┐    │ Receivers   │         │
│                     │ Grafana     │    │ - Slack     │         │
│                     │ - Dashboards│    │ - PagerDuty │         │
│                     │ - Alerts    │    │ - Email     │         │
│                     └─────────────┘    └─────────────┘         │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              Long-term Storage (optional)                │   │
│  │  Thanos | Cortex | Mimir | VictoriaMetrics              │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Best Practices (2025-2026)

### 1. Labels and Cardinality

- **Use bounded labels only** - Never use user IDs, request IDs, or UUIDs as labels
- **Consistent labeling strategy** - Maintain uniformity across microservices
- **Remove unused labels** - Regular housekeeping to reduce cardinality
- **Maximum ~10 labels per metric** - Each additional label multiplies time series

### 2. Naming Conventions

Follow the pattern: `<namespace>_<name>_<unit>_<suffix>`

| Suffix | Usage |
|--------|-------|
| `_total` | Counter metrics |
| `_bucket` | Histogram buckets |
| `_sum` | Histogram/Summary sum |
| `_count` | Histogram/Summary count |
| `_info` | Info metrics |

### 3. Scrape Configuration

| Environment | Interval | Rationale |
|-------------|----------|-----------|
| Critical systems | 10-15s | High-resolution monitoring |
| Standard apps | 15-30s | Balance of detail and overhead |
| Low-priority | 30-60s | Reduced resource usage |

### 4. Recording Rules

- Pre-compute expensive queries for dashboards
- Use for aggregations across many time series
- Name format: `<level>:<metric>:<operation>`
- Example: `job:http_requests_total:rate5m`

### 5. Alerting Philosophy

- **Alert on symptoms, not causes** - Focus on user-facing impact
- **Avoid alert fatigue** - Only critical, actionable alerts
- **Include runbook URLs** - Every alert should have remediation docs
- **Use severity levels** - critical, warning, info
- **Set appropriate `for` duration** - Avoid flapping alerts

### 6. Scaling Strategies

| Strategy | Use Case |
|----------|----------|
| Vertical scaling | Single-node, up to ~10M time series |
| Federation | Multi-cluster, regional aggregation |
| Remote write | Long-term storage (Thanos, Cortex, Mimir) |
| Sharding | High-cardinality workloads |

### 7. High Availability

- Run 2+ Prometheus replicas
- Use Alertmanager cluster (3+ nodes)
- Configure remote write for redundancy
- Use persistent storage for all components

### 8. Security

- Enable TLS for all endpoints
- Use authentication (OAuth2, mTLS)
- Limit scrape permissions with RBAC
- Secure Alertmanager webhook receivers

## Common Pitfalls

| Pitfall | Solution |
|---------|----------|
| High cardinality labels | Use bounded labels only (status codes, methods, not user IDs) |
| Alerting on causes | Alert on error rate, not individual errors |
| No recording rules | Pre-compute expensive dashboard queries |
| Inconsistent naming | Follow `namespace_name_unit_suffix` convention |
| Missing labels | Include relevant dimensions for debugging |
| No retention policy | Set retention time (30d) and size limits (50GB) |
| Single Prometheus | Run replicas for HA, use federation for scale |
| No service discovery | Use Kubernetes SD or Consul for dynamic environments |

## Kubernetes Integration

### Prometheus Operator Resources

| CRD | Purpose |
|-----|---------|
| Prometheus | Prometheus server deployment |
| ServiceMonitor | Scrape services by label selector |
| PodMonitor | Scrape pods directly |
| PrometheusRule | Recording and alerting rules |
| Alertmanager | Alertmanager deployment |

### Essential Exporters

| Exporter | Metrics |
|----------|---------|
| node-exporter | Host-level metrics (CPU, memory, disk) |
| kube-state-metrics | Kubernetes object state |
| blackbox-exporter | Probe endpoints (HTTP, TCP, ICMP) |
| cAdvisor | Container resource usage |

## PromQL Fundamentals

### Selectors

```promql
# Instant vector
http_requests_total{job="api", status="200"}

# Range vector
http_requests_total[5m]

# Regex matching
http_requests_total{status=~"5.."}

# Negative matching
http_requests_total{status!="200"}
```

### Aggregations

```promql
sum(), avg(), min(), max(), count()
sum by (label)
sum without (label)
topk(10, metric)
bottomk(5, metric)
```

### Rate Functions

```promql
rate(metric[5m])     # Per-second rate
irate(metric[5m])    # Instant rate (volatile)
increase(metric[1h]) # Total increase
```

## Related Technologies

| Technology | Integration |
|------------|-------------|
| Grafana | Visualization and dashboards |
| Thanos | Long-term storage, global view |
| Cortex/Mimir | Multi-tenant long-term storage |
| Loki | Log aggregation (same labels) |
| Jaeger/Tempo | Distributed tracing |
| OpenTelemetry | Unified telemetry collection |

## Agent Selection

| Task | Model | Rationale |
|------|-------|-----------|
| Run terraform plan, docker build, kubectl get commands | haiku | Mechanical CLI operations |
| Review Dockerfile for best practices | sonnet | Code review, security patterns |
| Debug pod crashes, container networking issues | sonnet | Diagnosis and error analysis |
| Design multi-region failover architecture | opus | Complex distributed systems decisions |
| Write Helm values for production rollout | sonnet | Configuration and templating |
| Create monitoring strategy for microservices | opus | System-wide observability design |
| Troubleshoot Kubernetes pod evictions under load | sonnet | Performance debugging and analysis |

---

## Sources

- [Prometheus Documentation](https://prometheus.io/docs/)
- [PromQL Basics](https://prometheus.io/docs/prometheus/latest/querying/basics/)
- [Prometheus Best Practices](https://prometheus.io/docs/practices/)
- [Prometheus Operator](https://prometheus-operator.dev/)
- [CNCF: Prometheus Labels Best Practices](https://www.cncf.io/blog/2025/07/22/prometheus-labels-understanding-and-best-practices/)
- [Better Stack: Prometheus Best Practices](https://betterstack.com/community/guides/monitoring/prometheus-best-practices/)
- [Dash0: Prometheus Monitoring Guide](https://www.dash0.com/guides/prometheus-monitoring)
