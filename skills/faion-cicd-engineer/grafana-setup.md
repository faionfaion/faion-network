---
id: grafana-setup
name: "Grafana Setup & Provisioning"
domain: OPS
skill: faion-devops-engineer
category: "devops"
---

# Grafana Setup & Provisioning

## Overview

This document covers advanced Grafana setup, including provisioning dashboards and data sources, dashboard as code with Grafonnet, and complex panel configurations.

## Provisioning Dashboards

Grafana supports automatic dashboard provisioning from files, enabling version control and declarative configuration.

### Configuration

```yaml
# provisioning/dashboards/dashboards.yaml
apiVersion: 1

providers:
  - name: 'default'
    orgId: 1
    folder: ''
    folderUid: ''
    type: file
    disableDeletion: false
    updateIntervalSeconds: 10
    allowUiUpdates: true
    options:
      path: /var/lib/grafana/dashboards

  - name: 'infrastructure'
    orgId: 1
    folder: 'Infrastructure'
    type: file
    options:
      path: /var/lib/grafana/dashboards/infrastructure

  - name: 'applications'
    orgId: 1
    folder: 'Applications'
    type: file
    options:
      path: /var/lib/grafana/dashboards/applications
```

### Data Source Provisioning

```yaml
# provisioning/datasources/prometheus.yaml
apiVersion: 1

datasources:
  - name: Prometheus
    type: prometheus
    access: proxy
    url: http://prometheus:9090
    isDefault: true
    editable: false
    jsonData:
      timeInterval: "30s"
      httpMethod: POST

  - name: Loki
    type: loki
    access: proxy
    url: http://loki:3100
    editable: false
```

## Dashboard as Code (Grafonnet)

Grafonnet is a Jsonnet library for generating Grafana dashboards programmatically.

### Installation

```bash
# Install jsonnet
brew install jsonnet  # macOS
apt install jsonnet   # Ubuntu

# Install grafonnet
git clone https://github.com/grafana/grafonnet-lib.git
```

### Basic Dashboard

```jsonnet
// dashboard.jsonnet
local grafana = import 'grafonnet/grafana.libsonnet';
local dashboard = grafana.dashboard;
local row = grafana.row;
local prometheus = grafana.prometheus;
local graphPanel = grafana.graphPanel;
local statPanel = grafana.statPanel;

local promDatasource = 'prometheus';

dashboard.new(
  'MyApp Overview',
  schemaVersion=38,
  tags=['myapp', 'production'],
  time_from='now-1h',
  refresh='30s',
)
.addTemplate(
  grafana.template.datasource(
    'datasource',
    'prometheus',
    'Prometheus',
  )
)
.addTemplate(
  grafana.template.query(
    name='namespace',
    datasource=promDatasource,
    query='label_values(kube_pod_info, namespace)',
    refresh='load',
  )
)
.addRow(
  row.new(title='Overview')
  .addPanel(
    statPanel.new(
      'Request Rate',
      datasource=promDatasource,
      unit='reqps',
    )
    .addTarget(
      prometheus.target(
        'sum(rate(http_requests_total{namespace="$namespace"}[5m]))',
        legendFormat='Requests/s',
      )
    ),
    gridPos={h: 4, w: 6, x: 0, y: 0}
  )
  .addPanel(
    graphPanel.new(
      'Request Rate by Status',
      datasource=promDatasource,
      span=12,
    )
    .addTarget(
      prometheus.target(
        'sum(rate(http_requests_total{namespace="$namespace"}[5m])) by (status)',
        legendFormat='{{status}}',
      )
    ),
    gridPos={h: 8, w: 12, x: 0, y: 4}
  )
)
```

### Generate Dashboard

```bash
# Generate JSON from Jsonnet
jsonnet -J grafonnet-lib dashboard.jsonnet > dashboard.json

# Import to Grafana
curl -X POST http://admin:admin@localhost:3000/api/dashboards/db \
  -H "Content-Type: application/json" \
  -d @dashboard.json
```

## Advanced Panel Examples

### Heatmap Panel

```json
{
  "type": "heatmap",
  "title": "Request Latency Distribution",
  "gridPos": {"h": 8, "w": 12, "x": 12, "y": 5},
  "targets": [
    {
      "expr": "sum(increase(http_request_duration_seconds_bucket{namespace=\"$namespace\"}[$interval])) by (le)",
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
    },
    "tooltip": {
      "show": true,
      "yHistogram": true
    },
    "legend": {
      "show": true
    }
  }
}
```

### Resource Usage Panels

```json
{
  "type": "timeseries",
  "title": "CPU Usage",
  "gridPos": {"h": 6, "w": 12, "x": 0, "y": 13},
  "targets": [
    {
      "expr": "sum(rate(container_cpu_usage_seconds_total{namespace=\"$namespace\",container!=\"\",container!=\"POD\"}[$interval])) by (pod)",
      "legendFormat": "{{pod}}"
    },
    {
      "expr": "sum(kube_pod_container_resource_limits{namespace=\"$namespace\",resource=\"cpu\"}) by (pod)",
      "legendFormat": "{{pod}} limit"
    }
  ],
  "fieldConfig": {
    "defaults": {
      "unit": "short",
      "custom": {
        "drawStyle": "line",
        "fillOpacity": 10
      }
    },
    "overrides": [
      {
        "matcher": {"id": "byRegexp", "options": "/.* limit/"},
        "properties": [
          {"id": "custom.drawStyle", "value": "line"},
          {"id": "custom.lineStyle", "value": {"fill": "dash", "dash": [10, 10]}},
          {"id": "custom.fillOpacity", "value": 0}
        ]
      }
    ]
  }
}
```

```json
{
  "type": "timeseries",
  "title": "Memory Usage",
  "gridPos": {"h": 6, "w": 12, "x": 12, "y": 13},
  "targets": [
    {
      "expr": "sum(container_memory_working_set_bytes{namespace=\"$namespace\",container!=\"\",container!=\"POD\"}) by (pod)",
      "legendFormat": "{{pod}}"
    },
    {
      "expr": "sum(kube_pod_container_resource_limits{namespace=\"$namespace\",resource=\"memory\"}) by (pod)",
      "legendFormat": "{{pod}} limit"
    }
  ],
  "fieldConfig": {
    "defaults": {
      "unit": "bytes",
      "custom": {
        "drawStyle": "line",
        "fillOpacity": 10
      }
    }
  }
}
```

### Row with Multiple Stats

```json
{
  "type": "row",
  "title": "Overview",
  "collapsed": false,
  "panels": [
    {
      "type": "stat",
      "title": "Error Rate",
      "gridPos": {"h": 4, "w": 4, "x": 4, "y": 1},
      "targets": [
        {
          "expr": "sum(rate(http_requests_total{namespace=\"$namespace\",status=~\"5..\"}[$interval])) / sum(rate(http_requests_total{namespace=\"$namespace\"}[$interval])) * 100",
          "legendFormat": "Error %"
        }
      ],
      "options": {
        "reduceOptions": {
          "calcs": ["lastNotNull"]
        },
        "colorMode": "value",
        "graphMode": "area"
      },
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
    },
    {
      "type": "stat",
      "title": "P99 Latency",
      "gridPos": {"h": 4, "w": 4, "x": 8, "y": 1},
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
    },
    {
      "type": "stat",
      "title": "Available Pods",
      "gridPos": {"h": 4, "w": 4, "x": 12, "y": 1},
      "targets": [
        {
          "expr": "sum(kube_deployment_status_replicas_available{namespace=\"$namespace\"})",
          "legendFormat": "Available"
        }
      ],
      "fieldConfig": {
        "defaults": {
          "unit": "short",
          "thresholds": {
            "mode": "absolute",
            "steps": [
              {"color": "red", "value": null},
              {"color": "yellow", "value": 2},
              {"color": "green", "value": 3}
            ]
          }
        }
      }
    }
  ]
}
```

### SLO Error Budget Panel

```json
{
  "type": "stat",
  "title": "Error Budget Remaining",
  "gridPos": {"h": 6, "w": 6, "x": 6, "y": 25},
  "targets": [
    {
      "expr": "((1 - 0.999) - (sum(rate(http_requests_total{namespace=\"$namespace\",status=~\"5..\"}[30d])) / sum(rate(http_requests_total{namespace=\"$namespace\"}[30d])))) / (1 - 0.999) * 100",
      "legendFormat": "Budget"
    }
  ],
  "fieldConfig": {
    "defaults": {
      "unit": "percent",
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

## Docker Compose Setup

```yaml
# docker-compose.yaml
version: '3.8'

services:
  grafana:
    image: grafana/grafana:latest
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_USER=admin
      - GF_SECURITY_ADMIN_PASSWORD=admin
      - GF_INSTALL_PLUGINS=grafana-piechart-panel
    volumes:
      - grafana-data:/var/lib/grafana
      - ./provisioning:/etc/grafana/provisioning
      - ./dashboards:/var/lib/grafana/dashboards
    depends_on:
      - prometheus

  prometheus:
    image: prom/prometheus:latest
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus-data:/prometheus

volumes:
  grafana-data:
  prometheus-data:
```

## Best Practices

1. **Use provisioning** - Automate dashboard and data source configuration
2. **Version control** - Store dashboard JSON in Git
3. **Dashboard as code** - Use Grafonnet for complex dashboards
4. **Organize folders** - Group dashboards by team, service, or function
5. **Use variables** - Make dashboards reusable across environments
6. **Test queries** - Verify query performance before adding to dashboards
7. **Document panels** - Add descriptions explaining metrics and thresholds
8. **Set alerts** - Configure notifications for critical metrics

## References

- [Grafana Provisioning](https://grafana.com/docs/grafana/latest/administration/provisioning/)
- [Grafonnet Library](https://github.com/grafana/grafonnet-lib)
- [Dashboard API](https://grafana.com/docs/grafana/latest/developers/http_api/dashboard/)

## Related

- [grafana-basics.md](grafana-basics.md) - Panel types and concepts
- [prometheus-monitoring.md](prometheus-monitoring.md) - Metrics collection

## Sources

- [Grafana Installation Guide](https://grafana.com/docs/grafana/latest/setup-grafana/installation/)
- [Grafana Provisioning](https://grafana.com/docs/grafana/latest/administration/provisioning/)
- [Grafana Helm Chart](https://github.com/grafana/helm-charts)
- [Grafana Alerting](https://grafana.com/docs/grafana/latest/alerting/)
- [Grafana Data Sources](https://grafana.com/docs/grafana/latest/datasources/)
