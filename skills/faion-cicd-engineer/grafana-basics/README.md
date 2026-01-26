---
id: grafana-basics
name: "Grafana Basics"
domain: OPS
skill: faion-devops-engineer
category: "devops"
---

# Grafana Basics

## Overview

Grafana is an open-source observability platform for visualizing metrics, logs, and traces. It supports multiple data sources (Prometheus, Loki, Elasticsearch, InfluxDB), provides rich visualization options, and enables alerting based on dashboard panels.

## When to Use

- Visualizing Prometheus metrics
- Creating operational dashboards
- Building SLO/SLI dashboards
- Log analysis with Loki
- Unified observability across multiple data sources
- Real-time monitoring and incident response

## Key Concepts

| Concept | Description |
|---------|-------------|
| Dashboard | Collection of panels organized in rows |
| Panel | Individual visualization (graph, table, stat, gauge) |
| Data Source | Backend providing data (Prometheus, Loki, InfluxDB) |
| Variable | Dynamic values for filtering dashboards |
| Alert | Condition-based notifications from panels |
| Annotation | Event markers on graphs |
| Folder | Organizational container for dashboards |
| Playlist | Auto-rotating dashboard slideshow |

## Visualization Types

| Type | Use Case | Best For |
|------|----------|----------|
| Time series | Metrics over time | Trend analysis, rate monitoring |
| Stat | Single value display | KPIs, current values |
| Gauge | Value within range | SLO compliance, utilization |
| Bar gauge | Comparative values | Side-by-side comparisons |
| Table | Tabular data | Pod status, detailed metrics |
| Heatmap | Distribution over time | Request latency distribution |
| Logs | Log aggregation display | Loki integration |
| Pie chart | Proportional data | Resource distribution |
| Geomap | Location-based data | Geographic metrics |

## Observability Frameworks

### RED Method (Request-driven)

| Signal | Metric | Panel Type |
|--------|--------|------------|
| Rate | Requests per second | Time series |
| Errors | Error rate percentage | Stat + threshold |
| Duration | Request latency (p50, p95, p99) | Time series, heatmap |

### USE Method (Resource-driven)

| Signal | Metric | Panel Type |
|--------|--------|------------|
| Utilization | % time resource busy | Gauge |
| Saturation | Queue depth, wait time | Time series |
| Errors | Error counts | Stat |

### Four Golden Signals

| Signal | Focus |
|--------|-------|
| Latency | Time to serve request |
| Traffic | Demand on system |
| Errors | Rate of failed requests |
| Saturation | How "full" the service is |

## Data Source Configuration

### Prometheus

```yaml
apiVersion: 1
datasources:
  - name: Prometheus
    type: prometheus
    access: proxy
    url: http://prometheus:9090
    isDefault: true
    jsonData:
      timeInterval: "15s"
      httpMethod: POST
```

### Loki

```yaml
apiVersion: 1
datasources:
  - name: Loki
    type: loki
    access: proxy
    url: http://loki:3100
    jsonData:
      maxLines: 1000
```

## Best Practices Summary

1. **Use variables** - Enable filtering by namespace, pod, environment
2. **Set appropriate time ranges** - Match dashboard purpose (real-time vs historical)
3. **Use consistent colors** - Red for errors, green for success across dashboards
4. **Add descriptions** - Panel descriptions explain what metrics mean
5. **Group related panels** - Use rows for logical organization
6. **Set thresholds** - Visual indicators for healthy/warning/critical states
7. **Include annotations** - Mark deployments, incidents on graphs
8. **Version control dashboards** - Export JSON and store in Git
9. **Use dashboard links** - Connect related dashboards for drill-down
10. **Optimize queries** - Use recording rules for complex queries

## Common Pitfalls

| Pitfall | Impact | Solution |
|---------|--------|----------|
| Too many panels | Information overload | Focus on key metrics per dashboard |
| Missing variables | Static dashboards don't scale | Add namespace/pod filters |
| No thresholds | Requires mental calculation | Set visual thresholds |
| Inconsistent naming | Hard to find dashboards | Use naming conventions |
| Manual creation | Changes lost on reinstall | Use provisioning |
| Complex panel queries | Slow dashboards | Use recording rules |
| No documentation | Context lost | Add Text panels, descriptions |
| Alert fatigue | Ignored notifications | Symptom-based alerting |

## Folder Contents

| File | Purpose |
|------|---------|
| [checklist.md](checklist.md) | Implementation checklist |
| [examples.md](examples.md) | Panel and dashboard examples |
| [templates.md](templates.md) | Ready-to-use JSON templates |
| [llm-prompts.md](llm-prompts.md) | AI-assisted dashboard creation |

## References

- [Grafana Documentation](https://grafana.com/docs/grafana/latest/)
- [Dashboard Best Practices](https://grafana.com/docs/grafana/latest/visualizations/dashboards/build-dashboards/best-practices/)
- [Grafana Alerting Best Practices](https://grafana.com/docs/grafana/latest/alerting/guides/best-practices/)
- [Grafana Dashboards Library](https://grafana.com/grafana/dashboards/)

## Related

- [grafana-setup.md](../grafana-setup.md) - Provisioning and dashboard as code
- [prometheus-monitoring.md](../prometheus-monitoring.md) - Metrics collection
- [elk-stack-logging.md](../elk-stack-logging.md) - Log aggregation

---

*Grafana Basics | faion-cicd-engineer*
