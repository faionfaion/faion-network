# Prometheus Monitoring

## Overview

Prometheus is an open-source monitoring and alerting toolkit designed for reliability and scalability. It collects metrics via a pull model, stores them in a time-series database, and provides powerful querying with PromQL. It is the de facto standard for Kubernetes and CI/CD pipeline monitoring.

## When to Use

| Scenario | Applicability |
|----------|---------------|
| Kubernetes cluster monitoring | High |
| Microservices observability | High |
| CI/CD pipeline metrics | High |
| Custom application metrics | High |
| Infrastructure monitoring | High |
| Alert management with Alertmanager | High |
| Short-lived jobs (via Pushgateway) | Medium |

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
| ServiceMonitor | K8s CRD for service discovery |
| PodMonitor | K8s CRD for pod-level scraping |

## Metric Types

| Type | Description | Use Case |
|------|-------------|----------|
| Counter | Monotonically increasing value | Request count, errors, builds |
| Gauge | Value that can go up and down | Temperature, queue size, active connections |
| Histogram | Samples in configurable buckets | Request duration, build times |
| Summary | Quantiles over sliding window | Request duration (client-side calculated) |

## CI/CD Pipeline Metrics

### Key Metrics to Monitor

| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| Build Duration | Time for builds to complete | >2x baseline |
| Deployment Frequency | How often deployments occur | Trending down |
| Failure Rate | Failed builds/tests/deployments | >5% |
| Pipeline Success Rate | Successful pipeline runs | <95% |
| Resource Utilization | CPU/memory of build agents | >85% |
| Queue Wait Time | Time jobs wait before execution | >5min |

### CI/CD Tool Integration

| Tool | Integration Method |
|------|-------------------|
| Jenkins | Prometheus Metrics Plugin (`/prometheus` endpoint) |
| GitLab CI | GitLab CI Pipelines Exporter |
| GitHub Actions | Custom metrics via Pushgateway |
| ArgoCD | Native Prometheus metrics endpoint |
| CircleCI | CircleCI Exporter |
| Tekton | Built-in metrics endpoint |

## Architecture Patterns

### Single Cluster

```
┌─────────────────────────────────────────────────┐
│                  Kubernetes Cluster              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐       │
│  │ App Pods │  │ CI/CD    │  │ Infra    │       │
│  │ /metrics │  │ Tools    │  │ Exporters│       │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘       │
│       │             │             │              │
│       └─────────────┼─────────────┘              │
│                     ▼                            │
│              ┌──────────────┐                    │
│              │  Prometheus  │                    │
│              │   (scrape)   │                    │
│              └──────┬───────┘                    │
│                     ▼                            │
│              ┌──────────────┐                    │
│              │   Grafana    │                    │
│              │ (visualize)  │                    │
│              └──────────────┘                    │
└─────────────────────────────────────────────────┘
```

### Multi-Cluster with Federation

```
┌─────────────┐  ┌─────────────┐  ┌─────────────┐
│  Cluster A  │  │  Cluster B  │  │  Cluster C  │
│ Prometheus  │  │ Prometheus  │  │ Prometheus  │
└──────┬──────┘  └──────┬──────┘  └──────┬──────┘
       │                │                │
       └────────────────┼────────────────┘
                        ▼
              ┌─────────────────┐
              │   Federation    │
              │   Prometheus    │
              └────────┬────────┘
                       ▼
              ┌─────────────────┐
              │  Thanos/Cortex  │
              │ (long-term)     │
              └────────┬────────┘
                       ▼
              ┌─────────────────┐
              │     Grafana     │
              └─────────────────┘
```

## Best Practices (2025-2026)

### Scrape Configuration

| Practice | Recommendation |
|----------|---------------|
| Scrape interval | 15-30s for most apps, 5-10s for critical |
| Scrape timeout | Set to less than scrape interval |
| Label consistency | Use consistent labels across services |
| Service discovery | Use Kubernetes SD for dynamic targets |

### Label Management

| Do | Don't |
|----|-------|
| Use bounded label values | Use high cardinality labels (user_id, UUID) |
| `env="prod"` | `environment_production` |
| Consistent naming across services | Different label schemes per team |
| Document label semantics | Leave labels undocumented |

### Recording Rules

| When to Use | Benefit |
|-------------|---------|
| Frequently queried expressions | Faster dashboard loading |
| Complex aggregations | Reduced query complexity |
| SLI/SLO calculations | Consistent measurements |
| Cross-service calculations | Pre-computed results |

### Alerting Strategy

| Principle | Description |
|-----------|-------------|
| Alert on symptoms | Focus on user-facing impact |
| Use `for` clause | Prevent flapping alerts (5-15m typical) |
| Include runbook_url | Link to remediation docs |
| Test in staging | Validate alerts before production |
| Review regularly | Update thresholds based on experience |

## Grafana Integration

### Data Sources

| Type | Use Case |
|------|----------|
| Prometheus | Primary metrics source |
| Loki | Correlated logs |
| Tempo | Distributed traces |
| Alertmanager | Alert management |

### Dashboard Best Practices

| Practice | Description |
|----------|-------------|
| Use variables | Environment, namespace, service selectors |
| Recording rules | Pre-compute for dashboard queries |
| Consistent layout | RED/USE method across services |
| Alert annotations | Show alert states on graphs |

### Recommended Dashboards

| Dashboard | ID | Purpose |
|-----------|-----|---------|
| Kubernetes Cluster | 6417 | Cluster overview |
| Node Exporter Full | 1860 | Node-level metrics |
| GitLab CI Pipelines | 10620 | Pipeline monitoring |
| Jenkins Performance | 9964 | Jenkins metrics |

## Pushgateway for CI/CD

Use Pushgateway for short-lived jobs (batch, CI/CD pipelines):

| Use Case | Appropriate |
|----------|-------------|
| CI/CD pipeline metrics | Yes |
| Batch job completion | Yes |
| Deployment events | Yes |
| Long-running services | No (use scrape) |

## Modern Tooling (2025-2026)

| Tool | Purpose | Status |
|------|---------|--------|
| Grafana Alloy | Telemetry collector (replaced Grafana Agent) | Active |
| Thanos | Long-term storage, HA | Active |
| Cortex | Multi-tenant long-term storage | Active |
| VictoriaMetrics | High-performance alternative | Active |
| GraCIe | CI/CD observability plugin for Grafana | Emerging |

## Related Methodologies

| Methodology | Path |
|-------------|------|
| Grafana Basics | `grafana-basics.md` |
| Grafana Setup | `grafana-setup.md` |
| ELK Stack Logging | `elk-stack-logging.md` |
| DORA Metrics | `dora-metrics.md` |
| AIOps | `aiops.md` |

## Agent Selection

| Task | Model | Rationale |
|------|-------|----------|
| Set up GitHub Actions workflow from template | haiku | Pattern application, simple configuration |
| Design CI/CD pipeline architecture | opus | Complex system design with many variables |
| Write terraform code for infrastructure | sonnet | Implementation with moderate complexity |
| Debug failing pipeline step | sonnet | Debugging and problem-solving |
| Implement AIOps anomaly detection | opus | Novel ML approach, complex decision |
| Configure webhook and secret management | haiku | Mechanical setup using checklists |


## Sources

- [Prometheus Documentation](https://prometheus.io/docs/)
- [Prometheus Operator](https://prometheus-operator.dev/)
- [Grafana Prometheus Integration](https://grafana.com/docs/grafana/latest/datasources/prometheus/)
- [CNCF Prometheus Labels Best Practices](https://www.cncf.io/blog/2025/07/22/prometheus-labels-understanding-and-best-practices/)
- [Better Stack Prometheus Best Practices](https://betterstack.com/community/guides/monitoring/prometheus-best-practices/)
- [Grafana GitLab CI/CD Integration](https://www.infoq.com/news/2025/11/grafana-gitlab-serverless-cicd/)
- [Dash0 Prometheus Monitoring Guide](https://www.dash0.com/guides/prometheus-monitoring)

## Folder Contents

| File | Description |
|------|-------------|
| README.md | This overview document |
| checklist.md | Implementation checklists |
| examples.md | Code examples and configurations |
| templates.md | Reusable YAML/config templates |
| llm-prompts.md | Prompts for LLM-assisted work |
