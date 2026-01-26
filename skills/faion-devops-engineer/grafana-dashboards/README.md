# Grafana Dashboards

Comprehensive methodology for designing, building, and managing Grafana dashboards with best practices from Grafana Labs and the DevOps community.

## Overview

Grafana is the leading open-source observability platform for visualizing metrics, logs, and traces. This methodology covers dashboard design principles, variable usage, alerting strategies, and provisioning automation.

## When to Use

- Visualizing Prometheus/Loki/Elasticsearch metrics
- Building operational dashboards for infrastructure
- Creating SLO/SLI dashboards for service reliability
- Implementing RED/USE method dashboards
- Establishing unified observability across data sources

## Contents

| File | Purpose |
|------|---------|
| [checklist.md](checklist.md) | Pre-flight checklist for dashboard creation |
| [examples.md](examples.md) | Panel configurations and PromQL queries |
| [templates.md](templates.md) | Dashboard JSON templates for common use cases |
| [llm-prompts.md](llm-prompts.md) | AI prompts for dashboard generation |

## Key Concepts

| Concept | Description |
|---------|-------------|
| Dashboard | Collection of panels organized in rows/tabs |
| Panel | Individual visualization (graph, table, stat, gauge) |
| Data Source | Backend providing data (Prometheus, Loki, InfluxDB) |
| Variable | Dynamic values for filtering dashboards |
| Alert | Condition-based notifications from panels |
| Annotation | Event markers on graphs (deployments, incidents) |
| Tab | Grafana 12+ feature for segmenting dashboards |

## Observability Frameworks

### USE Method (Infrastructure)

Best for hardware resources: CPU, memory, network, disk.

| Signal | Description | Example Query |
|--------|-------------|---------------|
| Utilization | Resource busy percentage | `avg(rate(node_cpu_seconds_total{mode!="idle"}[5m]))` |
| Saturation | Workload queue length | `node_load1 / count(node_cpu_seconds_total{mode="idle"})` |
| Errors | Error event counts | `rate(node_disk_io_time_seconds_total[5m])` |

### RED Method (Services)

Best for microservices and user-facing applications.

| Signal | Description | Example Query |
|--------|-------------|---------------|
| Rate | Requests per second | `sum(rate(http_requests_total[5m]))` |
| Errors | Failed request count | `sum(rate(http_requests_total{status=~"5.."}[5m]))` |
| Duration | Request latency | `histogram_quantile(0.99, rate(http_request_duration_seconds_bucket[5m]))` |

### Four Golden Signals (Google SRE)

| Signal | Description |
|--------|-------------|
| Latency | Time to service a request |
| Traffic | Demand on the system |
| Errors | Rate of failed requests |
| Saturation | System resource utilization |

## Dashboard Maturity Model

| Level | Characteristics |
|-------|-----------------|
| **Low** | Ad-hoc creation, dashboard sprawl, no version control |
| **Medium** | Strategy-based design, variables, hierarchical structure |
| **High** | GitOps provisioning, scripted generation, usage tracking |

## Grafana 12+ Features

| Feature | Description |
|---------|-------------|
| **Tabs** | Segment dashboards by context without splitting metrics |
| **Dashboard Outline** | Tree-view navigation for large dashboards |
| **Conditional Rendering** | Show/hide panels based on variables or data |
| **Auto-Grid Layout** | Responsive panel layout adapting to screen size |
| **Context-Aware Pane** | Quick edits without full edit mode |

## Quick Reference

### Variable Types

| Type | Use Case |
|------|----------|
| Query | Dynamic values from data source |
| Custom | Predefined static options |
| Interval | Time aggregation selection |
| Datasource | Multi-datasource dashboards |
| Text box | User input for filtering |
| Constant | Hidden configuration values |

### Visualization Selection

| Data Type | Recommended Panel |
|-----------|-------------------|
| Time series metrics | Time series, Line chart |
| Current value | Stat, Gauge |
| Comparison | Bar chart, Bar gauge |
| Tabular data | Table |
| Distribution | Heatmap, Histogram |
| Logs | Logs panel |
| Geographic | Geomap |

## Related Files

| Skill | File |
|-------|------|
| Prometheus | `../faion-cicd-engineer/methodologies/prometheus-monitoring.md` |
| Loki | `../faion-cicd-engineer/methodologies/loki-logging.md` |
| Alerting | `../faion-cicd-engineer/methodologies/alerting-strategies.md` |

## Sources

- [Grafana Dashboard Best Practices](https://grafana.com/docs/grafana/latest/visualizations/dashboards/build-dashboards/best-practices/)
- [Grafana 12 Dynamic Dashboards](https://grafana.com/blog/2025/05/07/dynamic-dashboards-grafana-12/)
- [GrafanaCON 2025 Best Practices Lab](https://grafana.com/events/grafanacon/2025/hands-on-labs/best-practices-to-level-up-your-grafana-dashboarding-skills/)
- [Grafana Cloud Documentation](https://grafana.com/docs/grafana-cloud/visualizations/dashboards/build-dashboards/best-practices/)
- [AWS Managed Grafana Best Practices](https://docs.aws.amazon.com/grafana/latest/userguide/v10-dash-bestpractices.html)
