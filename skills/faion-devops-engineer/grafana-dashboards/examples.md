# Grafana Dashboard Examples

Production-ready panel configurations and PromQL queries for common observability scenarios.

## Variable Definitions

### Namespace Variable

```json
{
  "name": "namespace",
  "type": "query",
  "datasource": {
    "type": "prometheus",
    "uid": "${DS_PROMETHEUS}"
  },
  "query": "label_values(kube_namespace_labels, namespace)",
  "refresh": 1,
  "includeAll": false,
  "sort": 1
}
```

### Pod Variable (Dependent)

```json
{
  "name": "pod",
  "type": "query",
  "datasource": {
    "type": "prometheus",
    "uid": "${DS_PROMETHEUS}"
  },
  "query": "label_values(kube_pod_info{namespace=\"$namespace\"}, pod)",
  "refresh": 2,
  "includeAll": true,
  "multi": true,
  "sort": 1
}
```

### Interval Variable

```json
{
  "name": "interval",
  "type": "interval",
  "auto": true,
  "auto_min": "1m",
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
```

### Data Source Variable

```json
{
  "name": "datasource",
  "type": "datasource",
  "query": "prometheus",
  "includeAll": false,
  "multi": false
}
```

## Stat Panels

### Request Rate

```json
{
  "type": "stat",
  "title": "Request Rate",
  "description": "Total HTTP requests per second across all pods",
  "gridPos": {"h": 4, "w": 4, "x": 0, "y": 0},
  "targets": [
    {
      "expr": "sum(rate(http_requests_total{namespace=\"$namespace\"}[$interval]))",
      "legendFormat": "req/s"
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

### Error Rate Percentage

```json
{
  "type": "stat",
  "title": "Error Rate",
  "description": "Percentage of 5xx responses in the last 5 minutes",
  "gridPos": {"h": 4, "w": 4, "x": 4, "y": 0},
  "targets": [
    {
      "expr": "sum(rate(http_requests_total{namespace=\"$namespace\",status=~\"5..\"}[$interval])) / sum(rate(http_requests_total{namespace=\"$namespace\"}[$interval])) * 100",
      "legendFormat": "Error %"
    }
  ],
  "fieldConfig": {
    "defaults": {
      "unit": "percent",
      "thresholds": {
        "mode": "absolute",
        "steps": [
          {"color": "green", "value": null},
          {"color": "yellow", "value": 1},
          {"color": "red", "value": 5}
        ]
      }
    }
  }
}
```

### P99 Latency

```json
{
  "type": "stat",
  "title": "P99 Latency",
  "description": "99th percentile request latency",
  "gridPos": {"h": 4, "w": 4, "x": 8, "y": 0},
  "targets": [
    {
      "expr": "histogram_quantile(0.99, sum(rate(http_request_duration_seconds_bucket{namespace=\"$namespace\"}[$interval])) by (le))",
      "legendFormat": "P99"
    }
  ],
  "fieldConfig": {
    "defaults": {
      "unit": "s",
      "thresholds": {
        "mode": "absolute",
        "steps": [
          {"color": "green", "value": null},
          {"color": "yellow", "value": 0.5},
          {"color": "red", "value": 1}
        ]
      }
    }
  }
}
```

## Time Series Panels

### Request Rate by Status Code

```json
{
  "type": "timeseries",
  "title": "Request Rate by Status",
  "description": "HTTP request rate grouped by status code class",
  "gridPos": {"h": 8, "w": 12, "x": 0, "y": 4},
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
        "showPoints": "never"
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
        "matcher": {"id": "byRegexp", "options": "/4../"},
        "properties": [
          {"id": "color", "value": {"fixedColor": "orange", "mode": "fixed"}}
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

### Latency Percentiles

```json
{
  "type": "timeseries",
  "title": "Latency Distribution",
  "description": "Request latency percentiles (P50, P90, P99)",
  "gridPos": {"h": 8, "w": 12, "x": 12, "y": 4},
  "targets": [
    {
      "expr": "histogram_quantile(0.50, sum(rate(http_request_duration_seconds_bucket{namespace=\"$namespace\"}[$interval])) by (le))",
      "legendFormat": "P50"
    },
    {
      "expr": "histogram_quantile(0.90, sum(rate(http_request_duration_seconds_bucket{namespace=\"$namespace\"}[$interval])) by (le))",
      "legendFormat": "P90"
    },
    {
      "expr": "histogram_quantile(0.99, sum(rate(http_request_duration_seconds_bucket{namespace=\"$namespace\"}[$interval])) by (le))",
      "legendFormat": "P99"
    }
  ],
  "fieldConfig": {
    "defaults": {
      "unit": "s",
      "custom": {
        "drawStyle": "line",
        "lineInterpolation": "smooth",
        "fillOpacity": 10
      }
    },
    "overrides": [
      {
        "matcher": {"id": "byName", "options": "P50"},
        "properties": [
          {"id": "color", "value": {"fixedColor": "green", "mode": "fixed"}}
        ]
      },
      {
        "matcher": {"id": "byName", "options": "P90"},
        "properties": [
          {"id": "color", "value": {"fixedColor": "yellow", "mode": "fixed"}}
        ]
      },
      {
        "matcher": {"id": "byName", "options": "P99"},
        "properties": [
          {"id": "color", "value": {"fixedColor": "red", "mode": "fixed"}}
        ]
      }
    ]
  }
}
```

### CPU Usage by Pod

```json
{
  "type": "timeseries",
  "title": "CPU Usage by Pod",
  "gridPos": {"h": 8, "w": 12, "x": 0, "y": 12},
  "targets": [
    {
      "expr": "sum(rate(container_cpu_usage_seconds_total{namespace=\"$namespace\", pod=~\"$pod\", container!=\"\"}[$interval])) by (pod)",
      "legendFormat": "{{pod}}"
    }
  ],
  "fieldConfig": {
    "defaults": {
      "unit": "percentunit",
      "custom": {
        "drawStyle": "line",
        "fillOpacity": 20,
        "stacking": {"mode": "none"}
      }
    }
  }
}
```

### Memory Usage by Pod

```json
{
  "type": "timeseries",
  "title": "Memory Usage by Pod",
  "gridPos": {"h": 8, "w": 12, "x": 12, "y": 12},
  "targets": [
    {
      "expr": "sum(container_memory_working_set_bytes{namespace=\"$namespace\", pod=~\"$pod\", container!=\"\"}) by (pod)",
      "legendFormat": "{{pod}}"
    }
  ],
  "fieldConfig": {
    "defaults": {
      "unit": "bytes",
      "custom": {
        "drawStyle": "line",
        "fillOpacity": 20
      }
    }
  }
}
```

## Gauge Panels

### SLO Availability Gauge

```json
{
  "type": "gauge",
  "title": "Availability SLO (99.9%)",
  "description": "30-day rolling availability against 99.9% SLO target",
  "gridPos": {"h": 6, "w": 6, "x": 0, "y": 20},
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

### Error Budget Remaining

```json
{
  "type": "gauge",
  "title": "Error Budget Remaining",
  "description": "Remaining error budget for the month",
  "gridPos": {"h": 6, "w": 6, "x": 6, "y": 20},
  "targets": [
    {
      "expr": "((1 - 0.999) - (sum(rate(http_requests_total{namespace=\"$namespace\",status=~\"5..\"}[30d])) / sum(rate(http_requests_total{namespace=\"$namespace\"}[30d])))) / (1 - 0.999) * 100",
      "legendFormat": "Budget"
    }
  ],
  "fieldConfig": {
    "defaults": {
      "unit": "percent",
      "min": 0,
      "max": 100,
      "thresholds": {
        "mode": "absolute",
        "steps": [
          {"color": "red", "value": null},
          {"color": "yellow", "value": 25},
          {"color": "green", "value": 50}
        ]
      }
    }
  }
}
```

## Table Panels

### Pod Status Table

```json
{
  "type": "table",
  "title": "Pod Status",
  "gridPos": {"h": 6, "w": 24, "x": 0, "y": 26},
  "targets": [
    {
      "expr": "kube_pod_info{namespace=\"$namespace\"}",
      "format": "table",
      "instant": true
    },
    {
      "expr": "kube_pod_status_phase{namespace=\"$namespace\"} == 1",
      "format": "table",
      "instant": true
    }
  ],
  "transformations": [
    {"id": "merge"},
    {
      "id": "organize",
      "options": {
        "excludeByName": {
          "Time": true,
          "__name__": true,
          "job": true,
          "instance": true,
          "uid": true
        },
        "renameByName": {
          "pod": "Pod",
          "node": "Node",
          "phase": "Status",
          "created_by_kind": "Controller"
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
              {"type": "value", "options": {"Failed": {"color": "red", "text": "Failed"}}},
              {"type": "value", "options": {"Succeeded": {"color": "blue", "text": "Succeeded"}}}
            ]
          }
        ]
      }
    ]
  }
}
```

### Top Endpoints by Latency

```json
{
  "type": "table",
  "title": "Top 10 Slowest Endpoints",
  "gridPos": {"h": 6, "w": 12, "x": 0, "y": 32},
  "targets": [
    {
      "expr": "topk(10, histogram_quantile(0.99, sum(rate(http_request_duration_seconds_bucket{namespace=\"$namespace\"}[$interval])) by (le, handler)))",
      "format": "table",
      "instant": true
    }
  ],
  "transformations": [
    {
      "id": "organize",
      "options": {
        "excludeByName": {"Time": true},
        "renameByName": {
          "handler": "Endpoint",
          "Value": "P99 Latency (s)"
        }
      }
    },
    {
      "id": "sortBy",
      "options": {
        "fields": {},
        "sort": [{"field": "P99 Latency (s)", "desc": true}]
      }
    }
  ]
}
```

## Logs Panel (Loki)

### Application Logs

```json
{
  "type": "logs",
  "title": "Application Logs",
  "gridPos": {"h": 8, "w": 24, "x": 0, "y": 38},
  "datasource": {
    "type": "loki",
    "uid": "${DS_LOKI}"
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

### Error Logs Only

```json
{
  "type": "logs",
  "title": "Error Logs",
  "gridPos": {"h": 8, "w": 24, "x": 0, "y": 46},
  "datasource": {
    "type": "loki",
    "uid": "${DS_LOKI}"
  },
  "targets": [
    {
      "expr": "{namespace=\"$namespace\"} | json | level=~\"error|fatal|critical\"",
      "refId": "A"
    }
  ],
  "options": {
    "showTime": true,
    "enableLogDetails": true,
    "sortOrder": "Descending"
  }
}
```

## Annotation Examples

### Deployment Annotations

```json
{
  "name": "Deployments",
  "datasource": {
    "type": "prometheus",
    "uid": "${DS_PROMETHEUS}"
  },
  "enable": true,
  "expr": "changes(kube_deployment_status_observed_generation{namespace=\"$namespace\"}[5m]) > 0",
  "titleFormat": "Deployment: {{ deployment }}",
  "textFormat": "Generation changed",
  "tagKeys": "deployment",
  "iconColor": "blue"
}
```

### Alert Annotations

```json
{
  "name": "Alerts",
  "datasource": {
    "type": "prometheus",
    "uid": "${DS_PROMETHEUS}"
  },
  "enable": true,
  "expr": "ALERTS{namespace=\"$namespace\", alertstate=\"firing\"}",
  "titleFormat": "{{ alertname }}",
  "textFormat": "Severity: {{ severity }}",
  "iconColor": "red"
}
```

## Common PromQL Patterns

### Rate and Increase

```promql
# Rate (per-second average)
rate(http_requests_total[5m])

# Increase (total increase over interval)
increase(http_requests_total[1h])

# irate (instant rate, more volatile)
irate(http_requests_total[5m])
```

### Aggregations

```promql
# Sum across all instances
sum(rate(http_requests_total[5m]))

# Sum by label
sum(rate(http_requests_total[5m])) by (status)

# Average by label
avg(rate(http_requests_total[5m])) by (instance)

# Top K
topk(10, sum(rate(http_requests_total[5m])) by (handler))
```

### Histogram Quantiles

```promql
# P50
histogram_quantile(0.50, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))

# P90
histogram_quantile(0.90, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))

# P99
histogram_quantile(0.99, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))

# Apdex score (threshold 0.5s, tolerating 2s)
(
  sum(rate(http_request_duration_seconds_bucket{le="0.5"}[5m])) +
  sum(rate(http_request_duration_seconds_bucket{le="2"}[5m]))
) / 2 / sum(rate(http_request_duration_seconds_count[5m]))
```

### Resource Calculations

```promql
# CPU utilization percentage
sum(rate(container_cpu_usage_seconds_total{namespace="$namespace"}[5m])) by (pod) /
sum(kube_pod_container_resource_limits{namespace="$namespace", resource="cpu"}) by (pod) * 100

# Memory utilization percentage
sum(container_memory_working_set_bytes{namespace="$namespace"}) by (pod) /
sum(kube_pod_container_resource_limits{namespace="$namespace", resource="memory"}) by (pod) * 100
```
