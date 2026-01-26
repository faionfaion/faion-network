# Grafana Panel Examples

## Stat Panels

### Request Rate

```json
{
  "type": "stat",
  "title": "Request Rate",
  "gridPos": {"h": 4, "w": 4, "x": 0, "y": 1},
  "targets": [
    {
      "expr": "sum(rate(http_requests_total{namespace=\"$namespace\"}[$__rate_interval]))",
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

### Error Rate Percentage

```json
{
  "type": "stat",
  "title": "Error Rate",
  "gridPos": {"h": 4, "w": 4, "x": 4, "y": 1},
  "targets": [
    {
      "expr": "sum(rate(http_requests_total{namespace=\"$namespace\",status=~\"5..\"}[$__rate_interval])) / sum(rate(http_requests_total{namespace=\"$namespace\"}[$__rate_interval])) * 100",
      "legendFormat": "Error %"
    }
  ],
  "fieldConfig": {
    "defaults": {
      "unit": "percent",
      "decimals": 2,
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

## Time Series Panels

### Request Rate by Status Code

```json
{
  "type": "timeseries",
  "title": "Request Rate by Status",
  "gridPos": {"h": 8, "w": 12, "x": 0, "y": 5},
  "targets": [
    {
      "expr": "sum(rate(http_requests_total{namespace=\"$namespace\"}[$__rate_interval])) by (status)",
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
        "stacking": {"mode": "none"}
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
      },
      {
        "matcher": {"id": "byRegexp", "options": "/4../"},
        "properties": [
          {"id": "color", "value": {"fixedColor": "yellow", "mode": "fixed"}}
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
  "title": "Request Latency (p50, p95, p99)",
  "gridPos": {"h": 8, "w": 12, "x": 12, "y": 5},
  "targets": [
    {
      "expr": "histogram_quantile(0.50, sum(rate(http_request_duration_seconds_bucket{namespace=\"$namespace\"}[$__rate_interval])) by (le))",
      "legendFormat": "p50"
    },
    {
      "expr": "histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket{namespace=\"$namespace\"}[$__rate_interval])) by (le))",
      "legendFormat": "p95"
    },
    {
      "expr": "histogram_quantile(0.99, sum(rate(http_request_duration_seconds_bucket{namespace=\"$namespace\"}[$__rate_interval])) by (le))",
      "legendFormat": "p99"
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
        "matcher": {"id": "byName", "options": "p99"},
        "properties": [
          {"id": "color", "value": {"fixedColor": "red", "mode": "fixed"}}
        ]
      },
      {
        "matcher": {"id": "byName", "options": "p95"},
        "properties": [
          {"id": "color", "value": {"fixedColor": "yellow", "mode": "fixed"}}
        ]
      },
      {
        "matcher": {"id": "byName", "options": "p50"},
        "properties": [
          {"id": "color", "value": {"fixedColor": "green", "mode": "fixed"}}
        ]
      }
    ]
  }
}
```

## Gauge Panels

### SLO Availability Gauge

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
      "decimals": 3,
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

### CPU Utilization Gauge

```json
{
  "type": "gauge",
  "title": "CPU Utilization",
  "gridPos": {"h": 6, "w": 6, "x": 6, "y": 25},
  "targets": [
    {
      "expr": "avg(rate(container_cpu_usage_seconds_total{namespace=\"$namespace\",pod=~\"$pod\"}[$__rate_interval])) / avg(kube_pod_container_resource_limits{namespace=\"$namespace\",pod=~\"$pod\",resource=\"cpu\"}) * 100",
      "legendFormat": "CPU %"
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
          {"color": "green", "value": null},
          {"color": "yellow", "value": 70},
          {"color": "red", "value": 90}
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
    {"id": "merge"},
    {
      "id": "organize",
      "options": {
        "excludeByName": {
          "Time": true,
          "__name__": true,
          "job": true,
          "instance": true
        },
        "renameByName": {
          "pod": "Pod",
          "node": "Node",
          "phase": "Status",
          "container": "Container"
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
  "title": "Top 10 Endpoints by P99 Latency",
  "gridPos": {"h": 8, "w": 12, "x": 0, "y": 31},
  "targets": [
    {
      "expr": "topk(10, histogram_quantile(0.99, sum(rate(http_request_duration_seconds_bucket{namespace=\"$namespace\"}[$__rate_interval])) by (le, handler)))",
      "format": "table",
      "instant": true
    }
  ],
  "transformations": [
    {
      "id": "organize",
      "options": {
        "excludeByName": {"Time": true, "le": true},
        "renameByName": {
          "handler": "Endpoint",
          "Value": "P99 Latency"
        }
      }
    },
    {
      "id": "sortBy",
      "options": {"fields": {}, "sort": [{"field": "P99 Latency", "desc": true}]}
    }
  ],
  "fieldConfig": {
    "defaults": {"unit": "s"},
    "overrides": [
      {
        "matcher": {"id": "byName", "options": "P99 Latency"},
        "properties": [
          {
            "id": "thresholds",
            "value": {
              "mode": "absolute",
              "steps": [
                {"color": "green", "value": null},
                {"color": "yellow", "value": 0.5},
                {"color": "red", "value": 1}
              ]
            }
          },
          {"id": "custom.displayMode", "value": "color-background"}
        ]
      }
    ]
  }
}
```

## Logs Panel (Loki)

### Application Logs

```json
{
  "type": "logs",
  "title": "Application Logs",
  "gridPos": {"h": 8, "w": 24, "x": 0, "y": 39},
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

### Error Logs Only

```json
{
  "type": "logs",
  "title": "Error Logs",
  "gridPos": {"h": 8, "w": 24, "x": 0, "y": 47},
  "datasource": {"type": "loki", "uid": "loki"},
  "targets": [
    {
      "expr": "{namespace=\"$namespace\"} |~ \"error|Error|ERROR|exception|Exception\" | json",
      "refId": "A"
    }
  ],
  "options": {
    "showTime": true,
    "wrapLogMessage": true,
    "enableLogDetails": true,
    "sortOrder": "Descending"
  }
}
```

## Heatmap Panel

### Request Latency Distribution

```json
{
  "type": "heatmap",
  "title": "Request Latency Distribution",
  "gridPos": {"h": 8, "w": 12, "x": 12, "y": 31},
  "targets": [
    {
      "expr": "sum(increase(http_request_duration_seconds_bucket{namespace=\"$namespace\"}[$__rate_interval])) by (le)",
      "format": "heatmap",
      "legendFormat": "{{le}}"
    }
  ],
  "options": {
    "calculate": false,
    "cellGap": 1,
    "color": {
      "mode": "scheme",
      "scheme": "Spectral",
      "steps": 64
    },
    "yAxis": {
      "unit": "s"
    }
  }
}
```

## Annotation Example

### Deployment Annotations

```json
{
  "annotations": {
    "list": [
      {
        "name": "Deployments",
        "datasource": {"type": "prometheus", "uid": "prometheus"},
        "enable": true,
        "expr": "changes(kube_deployment_status_observed_generation{namespace=\"$namespace\"}[5m]) > 0",
        "titleFormat": "Deployment",
        "textFormat": "{{ deployment }} updated",
        "iconColor": "blue"
      },
      {
        "name": "Alerts",
        "datasource": {"type": "prometheus", "uid": "prometheus"},
        "enable": true,
        "expr": "ALERTS{namespace=\"$namespace\",alertstate=\"firing\"}",
        "titleFormat": "Alert: {{ alertname }}",
        "textFormat": "{{ alertname }} - {{ severity }}",
        "iconColor": "red"
      }
    ]
  }
}
```

---

*Grafana Panel Examples | faion-cicd-engineer*
