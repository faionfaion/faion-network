# Grafana Dashboard Templates

Ready-to-use dashboard JSON templates for common observability scenarios.

## RED Method Dashboard Template

Complete dashboard for monitoring services using the RED method.

```json
{
  "dashboard": {
    "id": null,
    "uid": "red-service-overview",
    "title": "Service Overview (RED)",
    "description": "Rate, Errors, Duration metrics for service monitoring",
    "tags": ["red", "service", "slo"],
    "timezone": "browser",
    "schemaVersion": 39,
    "version": 1,
    "refresh": "30s",
    "time": {
      "from": "now-1h",
      "to": "now"
    },
    "templating": {
      "list": [
        {
          "name": "datasource",
          "type": "datasource",
          "query": "prometheus"
        },
        {
          "name": "namespace",
          "type": "query",
          "datasource": {"type": "prometheus", "uid": "${datasource}"},
          "query": "label_values(http_requests_total, namespace)",
          "refresh": 1,
          "sort": 1
        },
        {
          "name": "service",
          "type": "query",
          "datasource": {"type": "prometheus", "uid": "${datasource}"},
          "query": "label_values(http_requests_total{namespace=\"$namespace\"}, service)",
          "refresh": 2,
          "includeAll": true,
          "multi": true,
          "sort": 1
        },
        {
          "name": "interval",
          "type": "interval",
          "auto": true,
          "auto_min": "1m",
          "options": [
            {"text": "1m", "value": "1m"},
            {"text": "5m", "value": "5m"},
            {"text": "15m", "value": "15m"}
          ]
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
          "titleFormat": "Deploy: {{ deployment }}",
          "iconColor": "blue"
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
        "datasource": {"type": "prometheus", "uid": "${datasource}"},
        "targets": [
          {
            "expr": "sum(rate(http_requests_total{namespace=\"$namespace\", service=~\"$service\"}[$interval]))",
            "legendFormat": "req/s"
          }
        ],
        "fieldConfig": {
          "defaults": {
            "unit": "reqps",
            "thresholds": {
              "mode": "absolute",
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
        "datasource": {"type": "prometheus", "uid": "${datasource}"},
        "targets": [
          {
            "expr": "sum(rate(http_requests_total{namespace=\"$namespace\", service=~\"$service\", status=~\"5..\"}[$interval])) / sum(rate(http_requests_total{namespace=\"$namespace\", service=~\"$service\"}[$interval])) * 100",
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
        },
        "options": {"colorMode": "value", "graphMode": "area"}
      },
      {
        "type": "stat",
        "title": "P99 Latency",
        "gridPos": {"h": 4, "w": 6, "x": 12, "y": 1},
        "datasource": {"type": "prometheus", "uid": "${datasource}"},
        "targets": [
          {
            "expr": "histogram_quantile(0.99, sum(rate(http_request_duration_seconds_bucket{namespace=\"$namespace\", service=~\"$service\"}[$interval])) by (le))",
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
        },
        "options": {"colorMode": "value", "graphMode": "area"}
      },
      {
        "type": "gauge",
        "title": "Availability (30d)",
        "gridPos": {"h": 4, "w": 6, "x": 18, "y": 1},
        "datasource": {"type": "prometheus", "uid": "${datasource}"},
        "targets": [
          {
            "expr": "(1 - sum(rate(http_requests_total{namespace=\"$namespace\", service=~\"$service\", status=~\"5..\"}[30d])) / sum(rate(http_requests_total{namespace=\"$namespace\", service=~\"$service\"}[30d]))) * 100"
          }
        ],
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
      },
      {
        "type": "row",
        "title": "Request Details",
        "gridPos": {"h": 1, "w": 24, "x": 0, "y": 5},
        "collapsed": false
      },
      {
        "type": "timeseries",
        "title": "Request Rate by Status",
        "gridPos": {"h": 8, "w": 12, "x": 0, "y": 6},
        "datasource": {"type": "prometheus", "uid": "${datasource}"},
        "targets": [
          {
            "expr": "sum(rate(http_requests_total{namespace=\"$namespace\", service=~\"$service\"}[$interval])) by (status)",
            "legendFormat": "{{status}}"
          }
        ],
        "fieldConfig": {
          "defaults": {
            "unit": "reqps",
            "custom": {"drawStyle": "line", "fillOpacity": 20}
          },
          "overrides": [
            {
              "matcher": {"id": "byRegexp", "options": "/5../"},
              "properties": [{"id": "color", "value": {"fixedColor": "red", "mode": "fixed"}}]
            },
            {
              "matcher": {"id": "byRegexp", "options": "/2../"},
              "properties": [{"id": "color", "value": {"fixedColor": "green", "mode": "fixed"}}]
            }
          ]
        },
        "options": {
          "legend": {"displayMode": "table", "placement": "right", "calcs": ["mean", "max"]}
        }
      },
      {
        "type": "timeseries",
        "title": "Latency Percentiles",
        "gridPos": {"h": 8, "w": 12, "x": 12, "y": 6},
        "datasource": {"type": "prometheus", "uid": "${datasource}"},
        "targets": [
          {
            "expr": "histogram_quantile(0.50, sum(rate(http_request_duration_seconds_bucket{namespace=\"$namespace\", service=~\"$service\"}[$interval])) by (le))",
            "legendFormat": "P50"
          },
          {
            "expr": "histogram_quantile(0.90, sum(rate(http_request_duration_seconds_bucket{namespace=\"$namespace\", service=~\"$service\"}[$interval])) by (le))",
            "legendFormat": "P90"
          },
          {
            "expr": "histogram_quantile(0.99, sum(rate(http_request_duration_seconds_bucket{namespace=\"$namespace\", service=~\"$service\"}[$interval])) by (le))",
            "legendFormat": "P99"
          }
        ],
        "fieldConfig": {
          "defaults": {"unit": "s", "custom": {"drawStyle": "line", "fillOpacity": 10}}
        },
        "options": {
          "legend": {"displayMode": "table", "placement": "right", "calcs": ["mean", "max"]}
        }
      }
    ]
  },
  "overwrite": true
}
```

## USE Method Dashboard Template

Dashboard for infrastructure resources using the USE method.

```json
{
  "dashboard": {
    "id": null,
    "uid": "use-infrastructure",
    "title": "Infrastructure Overview (USE)",
    "description": "Utilization, Saturation, Errors for infrastructure monitoring",
    "tags": ["use", "infrastructure", "node"],
    "timezone": "browser",
    "schemaVersion": 39,
    "version": 1,
    "refresh": "30s",
    "time": {"from": "now-1h", "to": "now"},
    "templating": {
      "list": [
        {
          "name": "datasource",
          "type": "datasource",
          "query": "prometheus"
        },
        {
          "name": "node",
          "type": "query",
          "datasource": {"type": "prometheus", "uid": "${datasource}"},
          "query": "label_values(node_uname_info, nodename)",
          "refresh": 1,
          "includeAll": true,
          "multi": true,
          "sort": 1
        },
        {
          "name": "interval",
          "type": "interval",
          "auto": true,
          "auto_min": "1m"
        }
      ]
    },
    "panels": [
      {
        "type": "row",
        "title": "CPU",
        "gridPos": {"h": 1, "w": 24, "x": 0, "y": 0}
      },
      {
        "type": "gauge",
        "title": "CPU Utilization",
        "gridPos": {"h": 6, "w": 8, "x": 0, "y": 1},
        "datasource": {"type": "prometheus", "uid": "${datasource}"},
        "targets": [
          {
            "expr": "avg(1 - rate(node_cpu_seconds_total{mode=\"idle\", instance=~\"$node.*\"}[$interval])) * 100"
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
      },
      {
        "type": "stat",
        "title": "CPU Saturation (Load)",
        "gridPos": {"h": 6, "w": 8, "x": 8, "y": 1},
        "datasource": {"type": "prometheus", "uid": "${datasource}"},
        "targets": [
          {
            "expr": "avg(node_load1{instance=~\"$node.*\"}) / count(node_cpu_seconds_total{mode=\"idle\", instance=~\"$node.*\"})",
            "legendFormat": "Load per CPU"
          }
        ],
        "fieldConfig": {
          "defaults": {
            "thresholds": {
              "mode": "absolute",
              "steps": [
                {"color": "green", "value": null},
                {"color": "yellow", "value": 0.7},
                {"color": "red", "value": 1}
              ]
            }
          }
        },
        "options": {"colorMode": "value"}
      },
      {
        "type": "timeseries",
        "title": "CPU Usage Over Time",
        "gridPos": {"h": 6, "w": 8, "x": 16, "y": 1},
        "datasource": {"type": "prometheus", "uid": "${datasource}"},
        "targets": [
          {
            "expr": "avg(1 - rate(node_cpu_seconds_total{mode=\"idle\", instance=~\"$node.*\"}[$interval])) by (instance) * 100",
            "legendFormat": "{{instance}}"
          }
        ],
        "fieldConfig": {
          "defaults": {"unit": "percent", "min": 0, "max": 100}
        }
      },
      {
        "type": "row",
        "title": "Memory",
        "gridPos": {"h": 1, "w": 24, "x": 0, "y": 7}
      },
      {
        "type": "gauge",
        "title": "Memory Utilization",
        "gridPos": {"h": 6, "w": 8, "x": 0, "y": 8},
        "datasource": {"type": "prometheus", "uid": "${datasource}"},
        "targets": [
          {
            "expr": "avg((1 - (node_memory_MemAvailable_bytes{instance=~\"$node.*\"} / node_memory_MemTotal_bytes{instance=~\"$node.*\"})) * 100)"
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
                {"color": "yellow", "value": 80},
                {"color": "red", "value": 95}
              ]
            }
          }
        }
      },
      {
        "type": "stat",
        "title": "Memory Saturation (Swap)",
        "gridPos": {"h": 6, "w": 8, "x": 8, "y": 8},
        "datasource": {"type": "prometheus", "uid": "${datasource}"},
        "targets": [
          {
            "expr": "avg(rate(node_vmstat_pswpin{instance=~\"$node.*\"}[$interval]) + rate(node_vmstat_pswpout{instance=~\"$node.*\"}[$interval]))",
            "legendFormat": "Swap I/O"
          }
        ],
        "fieldConfig": {
          "defaults": {
            "unit": "ops",
            "thresholds": {
              "mode": "absolute",
              "steps": [
                {"color": "green", "value": null},
                {"color": "yellow", "value": 10},
                {"color": "red", "value": 100}
              ]
            }
          }
        }
      },
      {
        "type": "timeseries",
        "title": "Memory Usage Over Time",
        "gridPos": {"h": 6, "w": 8, "x": 16, "y": 8},
        "datasource": {"type": "prometheus", "uid": "${datasource}"},
        "targets": [
          {
            "expr": "(1 - (node_memory_MemAvailable_bytes{instance=~\"$node.*\"} / node_memory_MemTotal_bytes{instance=~\"$node.*\"})) * 100",
            "legendFormat": "{{instance}}"
          }
        ],
        "fieldConfig": {
          "defaults": {"unit": "percent", "min": 0, "max": 100}
        }
      },
      {
        "type": "row",
        "title": "Disk",
        "gridPos": {"h": 1, "w": 24, "x": 0, "y": 14}
      },
      {
        "type": "gauge",
        "title": "Disk Utilization",
        "gridPos": {"h": 6, "w": 8, "x": 0, "y": 15},
        "datasource": {"type": "prometheus", "uid": "${datasource}"},
        "targets": [
          {
            "expr": "avg((1 - (node_filesystem_avail_bytes{instance=~\"$node.*\", fstype!~\"tmpfs|overlay\"} / node_filesystem_size_bytes{instance=~\"$node.*\", fstype!~\"tmpfs|overlay\"})) * 100)"
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
      },
      {
        "type": "stat",
        "title": "Disk Saturation (I/O Wait)",
        "gridPos": {"h": 6, "w": 8, "x": 8, "y": 15},
        "datasource": {"type": "prometheus", "uid": "${datasource}"},
        "targets": [
          {
            "expr": "avg(rate(node_cpu_seconds_total{mode=\"iowait\", instance=~\"$node.*\"}[$interval])) * 100",
            "legendFormat": "I/O Wait %"
          }
        ],
        "fieldConfig": {
          "defaults": {
            "unit": "percent",
            "thresholds": {
              "mode": "absolute",
              "steps": [
                {"color": "green", "value": null},
                {"color": "yellow", "value": 10},
                {"color": "red", "value": 30}
              ]
            }
          }
        }
      },
      {
        "type": "timeseries",
        "title": "Disk I/O",
        "gridPos": {"h": 6, "w": 8, "x": 16, "y": 15},
        "datasource": {"type": "prometheus", "uid": "${datasource}"},
        "targets": [
          {
            "expr": "sum(rate(node_disk_read_bytes_total{instance=~\"$node.*\"}[$interval]))",
            "legendFormat": "Read"
          },
          {
            "expr": "sum(rate(node_disk_written_bytes_total{instance=~\"$node.*\"}[$interval]))",
            "legendFormat": "Write"
          }
        ],
        "fieldConfig": {
          "defaults": {"unit": "Bps"}
        }
      }
    ]
  },
  "overwrite": true
}
```

## Kubernetes Namespace Dashboard Template

```json
{
  "dashboard": {
    "id": null,
    "uid": "k8s-namespace-overview",
    "title": "Kubernetes Namespace Overview",
    "description": "Resource usage and health for a Kubernetes namespace",
    "tags": ["kubernetes", "namespace"],
    "timezone": "browser",
    "schemaVersion": 39,
    "version": 1,
    "refresh": "30s",
    "time": {"from": "now-1h", "to": "now"},
    "templating": {
      "list": [
        {
          "name": "datasource",
          "type": "datasource",
          "query": "prometheus"
        },
        {
          "name": "namespace",
          "type": "query",
          "datasource": {"type": "prometheus", "uid": "${datasource}"},
          "query": "label_values(kube_namespace_labels, namespace)",
          "refresh": 1,
          "sort": 1
        },
        {
          "name": "deployment",
          "type": "query",
          "datasource": {"type": "prometheus", "uid": "${datasource}"},
          "query": "label_values(kube_deployment_status_replicas{namespace=\"$namespace\"}, deployment)",
          "refresh": 2,
          "includeAll": true,
          "multi": true
        }
      ]
    },
    "panels": [
      {
        "type": "row",
        "title": "Deployment Status",
        "gridPos": {"h": 1, "w": 24, "x": 0, "y": 0}
      },
      {
        "type": "stat",
        "title": "Total Pods",
        "gridPos": {"h": 4, "w": 4, "x": 0, "y": 1},
        "datasource": {"type": "prometheus", "uid": "${datasource}"},
        "targets": [
          {
            "expr": "count(kube_pod_info{namespace=\"$namespace\"})"
          }
        ],
        "fieldConfig": {"defaults": {"thresholds": {"steps": [{"color": "blue", "value": null}]}}}
      },
      {
        "type": "stat",
        "title": "Running Pods",
        "gridPos": {"h": 4, "w": 4, "x": 4, "y": 1},
        "datasource": {"type": "prometheus", "uid": "${datasource}"},
        "targets": [
          {
            "expr": "sum(kube_pod_status_phase{namespace=\"$namespace\", phase=\"Running\"})"
          }
        ],
        "fieldConfig": {"defaults": {"thresholds": {"steps": [{"color": "green", "value": null}]}}}
      },
      {
        "type": "stat",
        "title": "Pending Pods",
        "gridPos": {"h": 4, "w": 4, "x": 8, "y": 1},
        "datasource": {"type": "prometheus", "uid": "${datasource}"},
        "targets": [
          {
            "expr": "sum(kube_pod_status_phase{namespace=\"$namespace\", phase=\"Pending\"})"
          }
        ],
        "fieldConfig": {
          "defaults": {
            "thresholds": {
              "steps": [
                {"color": "green", "value": null},
                {"color": "yellow", "value": 1},
                {"color": "red", "value": 5}
              ]
            }
          }
        }
      },
      {
        "type": "stat",
        "title": "Failed Pods",
        "gridPos": {"h": 4, "w": 4, "x": 12, "y": 1},
        "datasource": {"type": "prometheus", "uid": "${datasource}"},
        "targets": [
          {
            "expr": "sum(kube_pod_status_phase{namespace=\"$namespace\", phase=\"Failed\"})"
          }
        ],
        "fieldConfig": {
          "defaults": {
            "thresholds": {
              "steps": [
                {"color": "green", "value": null},
                {"color": "red", "value": 1}
              ]
            }
          }
        }
      },
      {
        "type": "stat",
        "title": "Container Restarts (1h)",
        "gridPos": {"h": 4, "w": 4, "x": 16, "y": 1},
        "datasource": {"type": "prometheus", "uid": "${datasource}"},
        "targets": [
          {
            "expr": "sum(increase(kube_pod_container_status_restarts_total{namespace=\"$namespace\"}[1h]))"
          }
        ],
        "fieldConfig": {
          "defaults": {
            "thresholds": {
              "steps": [
                {"color": "green", "value": null},
                {"color": "yellow", "value": 5},
                {"color": "red", "value": 20}
              ]
            }
          }
        }
      },
      {
        "type": "row",
        "title": "Resource Usage",
        "gridPos": {"h": 1, "w": 24, "x": 0, "y": 5}
      },
      {
        "type": "timeseries",
        "title": "CPU Usage vs Requests",
        "gridPos": {"h": 8, "w": 12, "x": 0, "y": 6},
        "datasource": {"type": "prometheus", "uid": "${datasource}"},
        "targets": [
          {
            "expr": "sum(rate(container_cpu_usage_seconds_total{namespace=\"$namespace\", container!=\"\"}[5m])) by (pod)",
            "legendFormat": "{{pod}} usage"
          },
          {
            "expr": "sum(kube_pod_container_resource_requests{namespace=\"$namespace\", resource=\"cpu\"}) by (pod)",
            "legendFormat": "{{pod}} request"
          }
        ],
        "fieldConfig": {"defaults": {"unit": "short"}}
      },
      {
        "type": "timeseries",
        "title": "Memory Usage vs Requests",
        "gridPos": {"h": 8, "w": 12, "x": 12, "y": 6},
        "datasource": {"type": "prometheus", "uid": "${datasource}"},
        "targets": [
          {
            "expr": "sum(container_memory_working_set_bytes{namespace=\"$namespace\", container!=\"\"}) by (pod)",
            "legendFormat": "{{pod}} usage"
          },
          {
            "expr": "sum(kube_pod_container_resource_requests{namespace=\"$namespace\", resource=\"memory\"}) by (pod)",
            "legendFormat": "{{pod}} request"
          }
        ],
        "fieldConfig": {"defaults": {"unit": "bytes"}}
      },
      {
        "type": "row",
        "title": "Network",
        "gridPos": {"h": 1, "w": 24, "x": 0, "y": 14}
      },
      {
        "type": "timeseries",
        "title": "Network I/O",
        "gridPos": {"h": 8, "w": 24, "x": 0, "y": 15},
        "datasource": {"type": "prometheus", "uid": "${datasource}"},
        "targets": [
          {
            "expr": "sum(rate(container_network_receive_bytes_total{namespace=\"$namespace\"}[5m])) by (pod)",
            "legendFormat": "{{pod}} RX"
          },
          {
            "expr": "-sum(rate(container_network_transmit_bytes_total{namespace=\"$namespace\"}[5m])) by (pod)",
            "legendFormat": "{{pod}} TX"
          }
        ],
        "fieldConfig": {"defaults": {"unit": "Bps"}}
      }
    ]
  },
  "overwrite": true
}
```

## Provisioning Configuration Template

### Grafana Provisioning YAML

```yaml
# /etc/grafana/provisioning/dashboards/default.yaml
apiVersion: 1

providers:
  - name: 'default'
    orgId: 1
    folder: ''
    folderUid: ''
    type: file
    disableDeletion: false
    updateIntervalSeconds: 30
    allowUiUpdates: true
    options:
      path: /var/lib/grafana/dashboards
      foldersFromFilesStructure: true
```

### Kubernetes ConfigMap for Dashboards

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: grafana-dashboards
  namespace: monitoring
  labels:
    grafana_dashboard: "1"
data:
  red-dashboard.json: |
    {
      "dashboard": {
        "uid": "red-service-overview",
        "title": "Service Overview (RED)"
        # ... rest of dashboard JSON
      }
    }
```

### Helm Values for Grafana

```yaml
# values.yaml for grafana helm chart
grafana:
  dashboardProviders:
    dashboardproviders.yaml:
      apiVersion: 1
      providers:
        - name: 'default'
          orgId: 1
          folder: ''
          type: file
          disableDeletion: false
          editable: true
          options:
            path: /var/lib/grafana/dashboards/default

  dashboards:
    default:
      red-dashboard:
        gnetId: 1860  # From grafana.com
        revision: 27
        datasource: Prometheus

      custom-dashboard:
        json: |
          {
            "uid": "custom-dashboard",
            "title": "Custom Dashboard"
          }
```

## Alert Rule Template

### Prometheus Alerting Rules

```yaml
# alerting-rules.yaml
groups:
  - name: service-alerts
    rules:
      - alert: HighErrorRate
        expr: |
          sum(rate(http_requests_total{status=~"5.."}[5m])) by (namespace, service)
          / sum(rate(http_requests_total[5m])) by (namespace, service)
          > 0.05
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "High error rate in {{ $labels.namespace }}/{{ $labels.service }}"
          description: "Error rate is {{ $value | humanizePercentage }} (> 5%)"
          dashboard: "https://grafana.example.com/d/red-service-overview?var-namespace={{ $labels.namespace }}"
          runbook: "https://wiki.example.com/runbooks/high-error-rate"

      - alert: HighLatency
        expr: |
          histogram_quantile(0.99,
            sum(rate(http_request_duration_seconds_bucket[5m])) by (le, namespace, service)
          ) > 1
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High P99 latency in {{ $labels.namespace }}/{{ $labels.service }}"
          description: "P99 latency is {{ $value | humanizeDuration }}"
```

### Grafana Alert Rule (JSON)

```json
{
  "apiVersion": 1,
  "groups": [
    {
      "orgId": 1,
      "name": "service-alerts",
      "folder": "alerts",
      "interval": "1m",
      "rules": [
        {
          "uid": "high-error-rate",
          "title": "High Error Rate",
          "condition": "C",
          "data": [
            {
              "refId": "A",
              "datasourceUid": "prometheus",
              "model": {
                "expr": "sum(rate(http_requests_total{status=~\"5..\"}[5m])) by (namespace, service)",
                "instant": false
              }
            },
            {
              "refId": "B",
              "datasourceUid": "prometheus",
              "model": {
                "expr": "sum(rate(http_requests_total[5m])) by (namespace, service)"
              }
            },
            {
              "refId": "C",
              "datasourceUid": "__expr__",
              "model": {
                "type": "math",
                "expression": "$A / $B > 0.05"
              }
            }
          ],
          "for": "5m",
          "labels": {
            "severity": "critical"
          },
          "annotations": {
            "summary": "High error rate detected",
            "runbook_url": "https://wiki.example.com/runbooks/high-error-rate"
          }
        }
      ]
    }
  ]
}
```
