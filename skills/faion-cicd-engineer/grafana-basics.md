---
id: grafana-basics
name: "Grafana Basics"
domain: OPS
skill: faion-devops-engineer
category: "devops"
---

# Grafana Basics

## Overview

Grafana is an open-source observability platform for visualizing metrics, logs, and traces. It supports multiple data sources (Prometheus, Loki, Elasticsearch), provides rich visualization options, and enables alerting based on dashboard panels.

## When to Use

- Visualizing Prometheus metrics
- Creating operational dashboards
- Building SLO/SLI dashboards
- Log analysis with Loki
- Unified observability across multiple data sources

## Key Concepts

| Concept | Description |
|---------|-------------|
| Dashboard | Collection of panels organized in rows |
| Panel | Individual visualization (graph, table, stat) |
| Data Source | Backend providing data (Prometheus, Loki) |
| Variable | Dynamic values for filtering dashboards |
| Alert | Condition-based notifications from panels |
| Annotation | Event markers on graphs |
| Folder | Organizational container for dashboards |

### Visualization Types

| Type | Use Case |
|------|----------|
| Time series | Metrics over time |
| Stat | Single value display |
| Gauge | Value within range |
| Bar gauge | Comparative values |
| Table | Tabular data |
| Heatmap | Distribution over time |
| Logs | Log aggregation display |

## Dashboard JSON Model

```json
{
  "dashboard": {
    "id": null,
    "uid": "myapp-overview",
    "title": "MyApp Overview",
    "description": "Application performance and health metrics",
    "tags": ["myapp", "production"],
    "timezone": "browser",
    "schemaVersion": 38,
    "version": 1,
    "refresh": "30s",
    "time": {
      "from": "now-1h",
      "to": "now"
    },
    "templating": {
      "list": [
        {
          "name": "namespace",
          "type": "query",
          "datasource": {
            "type": "prometheus",
            "uid": "prometheus"
          },
          "query": "label_values(kube_pod_info, namespace)",
          "refresh": 1,
          "includeAll": false,
          "current": {
            "text": "production",
            "value": "production"
          }
        },
        {
          "name": "pod",
          "type": "query",
          "datasource": {
            "type": "prometheus",
            "uid": "prometheus"
          },
          "query": "label_values(kube_pod_info{namespace=\"$namespace\"}, pod)",
          "refresh": 2,
          "includeAll": true,
          "multi": true
        },
        {
          "name": "interval",
          "type": "interval",
          "options": [
            {"text": "1m", "value": "1m"},
            {"text": "5m", "value": "5m"},
            {"text": "15m", "value": "15m"},
            {"text": "1h", "value": "1h"}
          ],
          "current": {
            "text": "5m",
            "value": "5m"
          }
        }
      ]
    },
    "annotations": {
      "list": [
        {
          "name": "Deployments",
          "datasource": {
            "type": "prometheus",
            "uid": "prometheus"
          },
          "enable": true,
          "expr": "changes(kube_deployment_status_observed_generation{namespace=\"$namespace\"}[5m]) > 0",
          "titleFormat": "Deployment",
          "textFormat": "{{ deployment }}"
        }
      ]
    },
    "panels": []
  }
}
```

## Panel Examples

### Stat Panel (Overview Statistics)

```json
{
  "type": "stat",
  "title": "Request Rate",
  "gridPos": {"h": 4, "w": 4, "x": 0, "y": 1},
  "targets": [
    {
      "expr": "sum(rate(http_requests_total{namespace=\"$namespace\"}[$interval]))",
      "legendFormat": "Requests/s"
    }
  ],
  "options": {
    "reduceOptions": {
      "calcs": ["lastNotNull"],
      "fields": "",
      "values": false
    },
    "colorMode": "value",
    "graphMode": "area",
    "justifyMode": "auto",
    "textMode": "auto"
  },
  "fieldConfig": {
    "defaults": {
      "unit": "reqps",
      "thresholds": {
        "mode": "absolute",
        "steps": [
          {"color": "green", "value": null},
          {"color": "yellow", "value": 1000},
          {"color": "red", "value": 5000}
        ]
      }
    }
  }
}
```

### Time Series Panel

```json
{
  "type": "timeseries",
  "title": "Request Rate by Status",
  "gridPos": {"h": 8, "w": 12, "x": 0, "y": 5},
  "targets": [
    {
      "expr": "sum(rate(http_requests_total{namespace=\"$namespace\"}[$interval])) by (status)",
      "legendFormat": "{{status}}"
    }
  ],
  "options": {
    "legend": {
      "displayMode": "table",
      "placement": "right",
      "showLegend": true,
      "calcs": ["mean", "max", "last"]
    },
    "tooltip": {
      "mode": "multi",
      "sort": "desc"
    }
  },
  "fieldConfig": {
    "defaults": {
      "unit": "reqps",
      "custom": {
        "drawStyle": "line",
        "lineInterpolation": "smooth",
        "lineWidth": 2,
        "fillOpacity": 20,
        "gradientMode": "opacity",
        "spanNulls": false,
        "showPoints": "never",
        "stacking": {
          "mode": "none"
        }
      }
    },
    "overrides": [
      {
        "matcher": {"id": "byRegexp", "options": "/5../"},
        "properties": [
          {"id": "color", "value": {"fixedColor": "red", "mode": "fixed"}}
        ]
      },
      {
        "matcher": {"id": "byRegexp", "options": "/2../"},
        "properties": [
          {"id": "color", "value": {"fixedColor": "green", "mode": "fixed"}}
        ]
      }
    ]
  }
}
```

### Gauge Panel (SLO)

```json
{
  "type": "gauge",
  "title": "Availability SLO (99.9%)",
  "gridPos": {"h": 6, "w": 6, "x": 0, "y": 25},
  "targets": [
    {
      "expr": "(1 - sum(rate(http_requests_total{namespace=\"$namespace\",status=~\"5..\"}[30d])) / sum(rate(http_requests_total{namespace=\"$namespace\"}[30d]))) * 100",
      "legendFormat": "Availability"
    }
  ],
  "options": {
    "showThresholdLabels": false,
    "showThresholdMarkers": true
  },
  "fieldConfig": {
    "defaults": {
      "unit": "percent",
      "min": 99,
      "max": 100,
      "thresholds": {
        "mode": "absolute",
        "steps": [
          {"color": "red", "value": null},
          {"color": "yellow", "value": 99.5},
          {"color": "green", "value": 99.9}
        ]
      }
    }
  }
}
```

### Table Panel

```json
{
  "type": "table",
  "title": "Pod Status",
  "gridPos": {"h": 6, "w": 24, "x": 0, "y": 19},
  "targets": [
    {
      "expr": "kube_pod_info{namespace=\"$namespace\"}",
      "format": "table",
      "instant": true
    },
    {
      "expr": "kube_pod_status_phase{namespace=\"$namespace\"}",
      "format": "table",
      "instant": true
    }
  ],
  "transformations": [
    {
      "id": "merge"
    },
    {
      "id": "organize",
      "options": {
        "excludeByName": {
          "Time": true,
          "__name__": true,
          "job": true
        },
        "renameByName": {
          "pod": "Pod",
          "node": "Node",
          "phase": "Status"
        }
      }
    }
  ],
  "fieldConfig": {
    "overrides": [
      {
        "matcher": {"id": "byName", "options": "Status"},
        "properties": [
          {
            "id": "mappings",
            "value": [
              {"type": "value", "options": {"Running": {"color": "green", "text": "Running"}}},
              {"type": "value", "options": {"Pending": {"color": "yellow", "text": "Pending"}}},
              {"type": "value", "options": {"Failed": {"color": "red", "text": "Failed"}}}
            ]
          }
        ]
      }
    ]
  }
}
```

### Logs Panel (Loki)

```json
{
  "type": "logs",
  "title": "Application Logs",
  "gridPos": {"h": 8, "w": 24, "x": 0, "y": 31},
  "datasource": {
    "type": "loki",
    "uid": "loki"
  },
  "targets": [
    {
      "expr": "{namespace=\"$namespace\", pod=~\"$pod\"} |= \"\" | json | line_format \"{{.level}} {{.message}}\"",
      "refId": "A"
    }
  ],
  "options": {
    "showTime": true,
    "showLabels": false,
    "showCommonLabels": false,
    "wrapLogMessage": true,
    "prettifyLogMessage": true,
    "enableLogDetails": true,
    "dedupStrategy": "none",
    "sortOrder": "Descending"
  }
}
```

## Best Practices

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

1. **Too many panels** - Information overload. Focus on key metrics per dashboard.

2. **Missing variables** - Static dashboards don't scale. Add namespace/pod filters.

3. **No thresholds** - Requires mental calculation. Set visual thresholds for quick assessment.

4. **Inconsistent naming** - Hard to find dashboards. Use consistent naming conventions.

5. **Manual dashboard creation** - Changes lost on reinstall. Use provisioning and version control.

6. **Complex queries in panels** - Slow dashboards. Use recording rules for heavy queries.

## References

- [Grafana Documentation](https://grafana.com/docs/grafana/latest/)
- [Dashboard Best Practices](https://grafana.com/docs/grafana/latest/dashboards/build-dashboards/best-practices/)
- [Grafana Dashboards](https://grafana.com/grafana/dashboards/)

## Related

- [grafana-setup.md](grafana-setup.md) - Provisioning and dashboard as code
- [prometheus-monitoring.md](prometheus-monitoring.md) - Metrics collection

## Sources

- [Grafana Documentation](https://grafana.com/docs/grafana/latest/)
- [Grafana Dashboards](https://grafana.com/grafana/dashboards/)
- [Grafana Tutorials](https://grafana.com/tutorials/)
- [Grafana Cloud](https://grafana.com/products/cloud/)
- [Grafana Best Practices](https://grafana.com/docs/grafana/latest/best-practices/)
