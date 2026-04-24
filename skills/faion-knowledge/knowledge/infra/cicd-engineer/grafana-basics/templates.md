# Grafana Templates

## Complete Dashboard Template

### Application Overview Dashboard

```json
{
  "dashboard": {
    "id": null,
    "uid": "app-overview",
    "title": "Application Overview",
    "description": "Application performance and health metrics using RED method",
    "tags": ["application", "production", "red-method"],
    "timezone": "browser",
    "schemaVersion": 39,
    "version": 1,
    "refresh": "30s",
    "time": {
      "from": "now-1h",
      "to": "now"
    },
    "fiscalYearStartMonth": 0,
    "liveNow": false,
    "templating": {
      "list": [
        {
          "name": "datasource",
          "type": "datasource",
          "query": "prometheus",
          "current": {},
          "hide": 0
        },
        {
          "name": "namespace",
          "type": "query",
          "datasource": {"type": "prometheus", "uid": "${datasource}"},
          "query": "label_values(kube_pod_info, namespace)",
          "refresh": 1,
          "includeAll": false,
          "current": {"text": "production", "value": "production"}
        },
        {
          "name": "pod",
          "type": "query",
          "datasource": {"type": "prometheus", "uid": "${datasource}"},
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
          "current": {"text": "5m", "value": "5m"}
        }
      ]
    },
    "annotations": {
      "list": [
        {
          "name": "Deployments",
          "datasource": {"type": "prometheus", "uid": "${datasource}"},
          "enable": true,
          "expr": "changes(kube_deployment_status_observed_generation{namespace=\"$namespace\"}[5m]) > 0",
          "titleFormat": "Deployment",
          "textFormat": "{{ deployment }}"
        }
      ]
    },
    "panels": [
      {
        "type": "row",
        "title": "Overview",
        "gridPos": {"h": 1, "w": 24, "x": 0, "y": 0},
        "collapsed": false
      },
      {
        "type": "stat",
        "title": "Request Rate",
        "gridPos": {"h": 4, "w": 6, "x": 0, "y": 1},
        "targets": [
          {
            "expr": "sum(rate(http_requests_total{namespace=\"$namespace\"}[$interval]))",
            "legendFormat": "req/s"
          }
        ],
        "fieldConfig": {
          "defaults": {
            "unit": "reqps",
            "thresholds": {
              "steps": [
                {"color": "green", "value": null}
              ]
            }
          }
        },
        "options": {"colorMode": "value", "graphMode": "area"}
      },
      {
        "type": "stat",
        "title": "Error Rate",
        "gridPos": {"h": 4, "w": 6, "x": 6, "y": 1},
        "targets": [
          {
            "expr": "sum(rate(http_requests_total{namespace=\"$namespace\",status=~\"5..\"}[$interval])) / sum(rate(http_requests_total{namespace=\"$namespace\"}[$interval])) * 100",
            "legendFormat": "errors"
          }
        ],
        "fieldConfig": {
          "defaults": {
            "unit": "percent",
            "decimals": 2,
            "thresholds": {
              "steps": [
                {"color": "green", "value": null},
                {"color": "yellow", "value": 1},
                {"color": "red", "value": 5}
              ]
            }
          }
        },
        "options": {"colorMode": "value", "graphMode": "area"}
      },
      {
        "type": "stat",
        "title": "P99 Latency",
        "gridPos": {"h": 4, "w": 6, "x": 12, "y": 1},
        "targets": [
          {
            "expr": "histogram_quantile(0.99, sum(rate(http_request_duration_seconds_bucket{namespace=\"$namespace\"}[$interval])) by (le))",
            "legendFormat": "p99"
          }
        ],
        "fieldConfig": {
          "defaults": {
            "unit": "s",
            "decimals": 3,
            "thresholds": {
              "steps": [
                {"color": "green", "value": null},
                {"color": "yellow", "value": 0.5},
                {"color": "red", "value": 1}
              ]
            }
          }
        },
        "options": {"colorMode": "value", "graphMode": "area"}
      },
      {
        "type": "stat",
        "title": "Active Pods",
        "gridPos": {"h": 4, "w": 6, "x": 18, "y": 1},
        "targets": [
          {
            "expr": "count(kube_pod_status_phase{namespace=\"$namespace\",phase=\"Running\"})",
            "legendFormat": "pods"
          }
        ],
        "fieldConfig": {
          "defaults": {
            "unit": "none",
            "thresholds": {
              "steps": [
                {"color": "red", "value": null},
                {"color": "green", "value": 1}
              ]
            }
          }
        },
        "options": {"colorMode": "value", "graphMode": "none"}
      },
      {
        "type": "row",
        "title": "Traffic",
        "gridPos": {"h": 1, "w": 24, "x": 0, "y": 5},
        "collapsed": false
      },
      {
        "type": "timeseries",
        "title": "Request Rate by Status",
        "gridPos": {"h": 8, "w": 12, "x": 0, "y": 6},
        "targets": [
          {
            "expr": "sum(rate(http_requests_total{namespace=\"$namespace\"}[$interval])) by (status)",
            "legendFormat": "{{status}}"
          }
        ],
        "fieldConfig": {
          "defaults": {"unit": "reqps"}
        },
        "options": {
          "legend": {"displayMode": "table", "placement": "right", "calcs": ["mean", "max"]}
        }
      },
      {
        "type": "timeseries",
        "title": "Latency Percentiles",
        "gridPos": {"h": 8, "w": 12, "x": 12, "y": 6},
        "targets": [
          {
            "expr": "histogram_quantile(0.50, sum(rate(http_request_duration_seconds_bucket{namespace=\"$namespace\"}[$interval])) by (le))",
            "legendFormat": "p50"
          },
          {
            "expr": "histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket{namespace=\"$namespace\"}[$interval])) by (le))",
            "legendFormat": "p95"
          },
          {
            "expr": "histogram_quantile(0.99, sum(rate(http_request_duration_seconds_bucket{namespace=\"$namespace\"}[$interval])) by (le))",
            "legendFormat": "p99"
          }
        ],
        "fieldConfig": {
          "defaults": {"unit": "s"}
        },
        "options": {
          "legend": {"displayMode": "table", "placement": "right", "calcs": ["mean", "max"]}
        }
      }
    ]
  }
}
```

## Variable Templates

### Namespace Variable

```json
{
  "name": "namespace",
  "label": "Namespace",
  "type": "query",
  "datasource": {"type": "prometheus", "uid": "${datasource}"},
  "query": "label_values(kube_namespace_labels, namespace)",
  "refresh": 1,
  "sort": 1,
  "includeAll": false,
  "multi": false,
  "regex": "",
  "hide": 0
}
```

### Service Variable (Cascading)

```json
{
  "name": "service",
  "label": "Service",
  "type": "query",
  "datasource": {"type": "prometheus", "uid": "${datasource}"},
  "query": "label_values(kube_service_info{namespace=\"$namespace\"}, service)",
  "refresh": 2,
  "sort": 1,
  "includeAll": true,
  "multi": true,
  "allValue": ".*"
}
```

### Environment Variable (Custom)

```json
{
  "name": "environment",
  "label": "Environment",
  "type": "custom",
  "options": [
    {"text": "Production", "value": "production", "selected": true},
    {"text": "Staging", "value": "staging", "selected": false},
    {"text": "Development", "value": "development", "selected": false}
  ],
  "includeAll": false,
  "multi": false
}
```

## Alert Rule Templates

### High Error Rate Alert

```json
{
  "alert": {
    "name": "High Error Rate",
    "condition": "C",
    "data": [
      {
        "refId": "A",
        "datasourceUid": "prometheus",
        "model": {
          "expr": "sum(rate(http_requests_total{namespace=\"$namespace\",status=~\"5..\"}[5m])) / sum(rate(http_requests_total{namespace=\"$namespace\"}[5m])) * 100",
          "intervalMs": 1000,
          "maxDataPoints": 43200
        }
      },
      {
        "refId": "B",
        "datasourceUid": "-100",
        "model": {
          "conditions": [
            {"evaluator": {"params": [5], "type": "gt"}, "reducer": {"type": "last"}}
          ],
          "type": "reduce"
        }
      },
      {
        "refId": "C",
        "datasourceUid": "-100",
        "model": {
          "conditions": [
            {"evaluator": {"params": [0], "type": "gt"}, "reducer": {"type": "last"}}
          ],
          "type": "threshold"
        }
      }
    ],
    "execErrState": "Error",
    "noDataState": "NoData",
    "for": "5m",
    "annotations": {
      "summary": "Error rate is above 5% for {{ $labels.namespace }}",
      "description": "Current error rate: {{ $values.A | printf \"%.2f\" }}%",
      "runbook_url": "https://runbooks.example.com/high-error-rate"
    },
    "labels": {
      "severity": "critical",
      "team": "platform"
    }
  }
}
```

### High Latency Alert

```json
{
  "alert": {
    "name": "High P99 Latency",
    "condition": "C",
    "data": [
      {
        "refId": "A",
        "datasourceUid": "prometheus",
        "model": {
          "expr": "histogram_quantile(0.99, sum(rate(http_request_duration_seconds_bucket{namespace=\"$namespace\"}[5m])) by (le))"
        }
      },
      {
        "refId": "B",
        "model": {"type": "reduce", "conditions": [{"reducer": {"type": "last"}}]}
      },
      {
        "refId": "C",
        "model": {
          "type": "threshold",
          "conditions": [{"evaluator": {"params": [1], "type": "gt"}}]
        }
      }
    ],
    "for": "5m",
    "annotations": {
      "summary": "P99 latency is above 1s for {{ $labels.namespace }}",
      "description": "Current P99: {{ $values.A | printf \"%.3f\" }}s"
    },
    "labels": {
      "severity": "warning",
      "team": "platform"
    }
  }
}
```

### Pod Not Ready Alert

```json
{
  "alert": {
    "name": "Pod Not Ready",
    "condition": "C",
    "data": [
      {
        "refId": "A",
        "datasourceUid": "prometheus",
        "model": {
          "expr": "kube_pod_status_ready{namespace=\"$namespace\",condition=\"true\"} == 0"
        }
      }
    ],
    "for": "5m",
    "annotations": {
      "summary": "Pod {{ $labels.pod }} is not ready",
      "description": "Pod {{ $labels.pod }} in namespace {{ $labels.namespace }} has been not ready for more than 5 minutes"
    },
    "labels": {
      "severity": "warning"
    }
  }
}
```

## Data Source Provisioning Templates

### Prometheus Data Source

```yaml
apiVersion: 1
datasources:
  - name: Prometheus
    type: prometheus
    access: proxy
    url: http://prometheus-server:9090
    isDefault: true
    editable: false
    jsonData:
      timeInterval: "15s"
      httpMethod: POST
      manageAlerts: true
      prometheusType: Prometheus
      prometheusVersion: "2.45.0"
```

### Loki Data Source

```yaml
apiVersion: 1
datasources:
  - name: Loki
    type: loki
    access: proxy
    url: http://loki:3100
    editable: false
    jsonData:
      maxLines: 1000
      derivedFields:
        - name: TraceID
          matcherRegex: "traceID=(\\w+)"
          url: "$${__value.raw}"
          datasourceUid: tempo
```

### Tempo Data Source (Tracing)

```yaml
apiVersion: 1
datasources:
  - name: Tempo
    type: tempo
    access: proxy
    url: http://tempo:3200
    editable: false
    jsonData:
      httpMethod: GET
      tracesToLogs:
        datasourceUid: loki
        tags: ['job', 'instance', 'pod', 'namespace']
        mappedTags: [{ key: 'service.name', value: 'service' }]
        mapTagNamesEnabled: true
        spanStartTimeShift: '-1h'
        spanEndTimeShift: '1h'
        filterByTraceID: true
        filterBySpanID: false
```

## Dashboard Provisioning

### Dashboard Provider Configuration

```yaml
apiVersion: 1
providers:
  - name: 'default'
    orgId: 1
    folder: 'Infrastructure'
    folderUid: 'infrastructure'
    type: file
    disableDeletion: false
    updateIntervalSeconds: 30
    allowUiUpdates: true
    options:
      path: /var/lib/grafana/dashboards
      foldersFromFilesStructure: true
```

## Notification Channel Templates

### Slack Contact Point

```yaml
apiVersion: 1
contactPoints:
  - orgId: 1
    name: slack-alerts
    receivers:
      - uid: slack-critical
        type: slack
        settings:
          url: ${SLACK_WEBHOOK_URL}
          recipient: "#alerts-critical"
          username: Grafana
          icon_emoji: ":alert:"
          mentionChannel: "here"
        disableResolveMessage: false
```

### PagerDuty Contact Point

```yaml
apiVersion: 1
contactPoints:
  - orgId: 1
    name: pagerduty-critical
    receivers:
      - uid: pagerduty-1
        type: pagerduty
        settings:
          integrationKey: ${PAGERDUTY_INTEGRATION_KEY}
          severity: critical
          class: "infrastructure"
          component: "{{ .Labels.service }}"
```

---

*Grafana Templates | faion-cicd-engineer*
