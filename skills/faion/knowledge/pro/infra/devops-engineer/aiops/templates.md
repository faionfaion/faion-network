# AIOps Templates

## Prometheus Alerting Rules

### SLO-Based Alerts

```yaml
# prometheus-slo-alerts.yaml
groups:
- name: slo-alerts
  rules:
  # Error Budget Burn Rate - Fast Burn (page immediately)
  - alert: SLOErrorBudgetFastBurn
    expr: |
      (
        sum(rate(http_requests_total{status=~"5.."}[5m]))
        /
        sum(rate(http_requests_total[5m]))
      ) > (14.4 * (1 - 0.999))
    for: 2m
    labels:
      severity: critical
      slo: availability
    annotations:
      summary: "SLO error budget burning fast"
      description: "Error rate {{ $value | humanizePercentage }} is burning error budget at >14.4x rate"
      runbook_url: "https://wiki.company.com/runbooks/slo-fast-burn"

  # Error Budget Burn Rate - Slow Burn (ticket)
  - alert: SLOErrorBudgetSlowBurn
    expr: |
      (
        sum(rate(http_requests_total{status=~"5.."}[1h]))
        /
        sum(rate(http_requests_total[1h]))
      ) > (3 * (1 - 0.999))
    for: 30m
    labels:
      severity: warning
      slo: availability
    annotations:
      summary: "SLO error budget slow burn"
      description: "Error rate is burning budget at >3x rate over 1 hour window"

  # Latency SLO
  - alert: SLOLatencyBudgetBurn
    expr: |
      (
        histogram_quantile(0.99, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))
        > 0.5
      )
    for: 5m
    labels:
      severity: warning
      slo: latency
    annotations:
      summary: "P99 latency exceeds SLO target"
      description: "P99 latency is {{ $value | humanizeDuration }}, target is 500ms"
```

### Anomaly Detection Alerts

```yaml
# prometheus-anomaly-alerts.yaml
groups:
- name: anomaly-alerts
  rules:
  # CPU Anomaly - Deviation from historical pattern
  - alert: CPUAnomalyDetected
    expr: |
      abs(
        avg_over_time(node_cpu_seconds_total{mode="idle"}[5m])
        -
        avg_over_time(node_cpu_seconds_total{mode="idle"}[1d] offset 1d)
      ) > 0.2
    for: 10m
    labels:
      severity: warning
      type: anomaly
    annotations:
      summary: "CPU usage anomaly detected"
      description: "CPU usage deviates significantly from historical pattern"

  # Memory Leak Detection
  - alert: MemoryLeakSuspected
    expr: |
      (
        predict_linear(container_memory_working_set_bytes[1h], 3600 * 4)
        >
        container_spec_memory_limit_bytes * 0.9
      )
    for: 15m
    labels:
      severity: warning
      type: anomaly
    annotations:
      summary: "Memory leak suspected"
      description: "Memory usage trending toward limit in 4 hours for {{ $labels.container }}"

  # Request Rate Anomaly
  - alert: RequestRateAnomaly
    expr: |
      abs(
        sum(rate(http_requests_total[5m]))
        -
        sum(rate(http_requests_total[5m] offset 1w))
      ) / sum(rate(http_requests_total[5m] offset 1w)) > 0.5
    for: 10m
    labels:
      severity: info
      type: anomaly
    annotations:
      summary: "Request rate anomaly"
      description: "Request rate differs >50% from same time last week"
```

---

## Grafana Dashboard

### AIOps Overview Dashboard

```json
{
  "dashboard": {
    "title": "AIOps Overview",
    "tags": ["aiops", "sre"],
    "timezone": "browser",
    "panels": [
      {
        "title": "Error Budget Status",
        "type": "gauge",
        "gridPos": {"h": 8, "w": 6, "x": 0, "y": 0},
        "targets": [
          {
            "expr": "1 - (sum(increase(http_requests_total{status=~\"5..\"}[30d])) / sum(increase(http_requests_total[30d]))) / 0.001",
            "legendFormat": "Budget Remaining"
          }
        ],
        "fieldConfig": {
          "defaults": {
            "unit": "percentunit",
            "min": 0,
            "max": 1,
            "thresholds": {
              "mode": "percentage",
              "steps": [
                {"color": "red", "value": 0},
                {"color": "yellow", "value": 25},
                {"color": "green", "value": 50}
              ]
            }
          }
        }
      },
      {
        "title": "Anomalies Detected (24h)",
        "type": "stat",
        "gridPos": {"h": 4, "w": 6, "x": 6, "y": 0},
        "targets": [
          {
            "expr": "count(ALERTS{alertstate=\"firing\", type=\"anomaly\"})",
            "legendFormat": "Active Anomalies"
          }
        ]
      },
      {
        "title": "Auto-Remediation Rate",
        "type": "stat",
        "gridPos": {"h": 4, "w": 6, "x": 6, "y": 4},
        "targets": [
          {
            "expr": "sum(increase(aiops_remediation_success_total[24h])) / sum(increase(aiops_incident_total[24h]))",
            "legendFormat": "Auto-Remediation %"
          }
        ],
        "fieldConfig": {
          "defaults": {
            "unit": "percentunit"
          }
        }
      },
      {
        "title": "Burn Rate (1h window)",
        "type": "timeseries",
        "gridPos": {"h": 8, "w": 12, "x": 12, "y": 0},
        "targets": [
          {
            "expr": "(sum(rate(http_requests_total{status=~\"5..\"}[1h])) / sum(rate(http_requests_total[1h]))) / (1 - 0.999)",
            "legendFormat": "Burn Rate"
          }
        ],
        "fieldConfig": {
          "defaults": {
            "custom": {
              "thresholdsStyle": {
                "mode": "line"
              }
            },
            "thresholds": {
              "steps": [
                {"color": "green", "value": 0},
                {"color": "yellow", "value": 1},
                {"color": "red", "value": 3}
              ]
            }
          }
        }
      },
      {
        "title": "Service Health Topology",
        "type": "nodeGraph",
        "gridPos": {"h": 12, "w": 12, "x": 0, "y": 8},
        "targets": [
          {
            "expr": "service_dependency_health",
            "format": "table"
          }
        ]
      },
      {
        "title": "Recent Incidents",
        "type": "table",
        "gridPos": {"h": 12, "w": 12, "x": 12, "y": 8},
        "targets": [
          {
            "expr": "topk(10, ALERTS{alertstate=\"firing\"})",
            "format": "table"
          }
        ]
      }
    ]
  }
}
```

---

## Kubernetes Resources

### Auto-Scaling with Anomaly Awareness

```yaml
# hpa-anomaly-aware.yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: api-service-hpa
  namespace: production
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: api-service
  minReplicas: 3
  maxReplicas: 20
  metrics:
  # Standard CPU metric
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  # Custom metric: Request rate from Prometheus
  - type: External
    external:
      metric:
        name: http_requests_per_second
        selector:
          matchLabels:
            service: api-service
      target:
        type: AverageValue
        averageValue: "100"
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300  # Wait 5 min before scaling down
      policies:
      - type: Percent
        value: 10
        periodSeconds: 60
    scaleUp:
      stabilizationWindowSeconds: 0    # Scale up immediately
      policies:
      - type: Percent
        value: 100
        periodSeconds: 15
      - type: Pods
        value: 4
        periodSeconds: 15
      selectPolicy: Max
```

### PodDisruptionBudget for Controlled Remediation

```yaml
# pdb-api-service.yaml
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: api-service-pdb
  namespace: production
spec:
  minAvailable: 2  # Always keep at least 2 pods running
  selector:
    matchLabels:
      app: api-service
```

---

## Runbook Templates

### Incident Response Runbook

```markdown
# Runbook: High Error Rate

## Metadata
- **Service**: {{ service_name }}
- **Severity**: P{{ severity }}
- **Last Updated**: {{ date }}
- **Owner**: {{ team }}

## Detection
**Alert**: `SLOErrorBudgetFastBurn`
**Threshold**: Error rate > 0.1% (burning at 14.4x rate)

## Impact Assessment

1. Check affected endpoints:
   ```promql
   topk(5, sum by (endpoint) (rate(http_requests_total{status=~"5..", service="{{ service_name }}"}[5m])))
   ```

2. Estimate user impact:
   ```promql
   sum(rate(http_requests_total{status=~"5..", service="{{ service_name }}"}[5m])) / sum(rate(http_requests_total{service="{{ service_name }}"}[5m]))
   ```

## Diagnosis Steps

### Step 1: Check Recent Changes

```bash
# Recent deployments
kubectl rollout history deployment/{{ service_name }} -n production

# Recent config changes
kubectl get configmap -n production -o yaml | head -50
```

### Step 2: Check Dependencies

```promql
# Downstream service health
sum by (target_service) (rate(http_requests_total{source_service="{{ service_name }}", status=~"5.."}[5m]))
```

### Step 3: Check Resources

```promql
# Memory usage
container_memory_working_set_bytes{container="{{ service_name }}"} / container_spec_memory_limit_bytes{container="{{ service_name }}"}

# CPU throttling
rate(container_cpu_cfs_throttled_seconds_total{container="{{ service_name }}"}[5m])
```

## Remediation Actions

### Option A: Rollback (if recent deployment)

```bash
kubectl rollout undo deployment/{{ service_name }} -n production
```

### Option B: Scale Up (if resource constrained)

```bash
kubectl scale deployment/{{ service_name }} -n production --replicas=10
```

### Option C: Restart Pods (if memory leak suspected)

```bash
kubectl rollout restart deployment/{{ service_name }} -n production
```

## Verification

1. Error rate returning to normal:
   ```promql
   sum(rate(http_requests_total{status=~"5..", service="{{ service_name }}"}[5m])) / sum(rate(http_requests_total{service="{{ service_name }}"}[5m])) < 0.001
   ```

2. No new alerts firing

## Escalation

If not resolved within 15 minutes:
- Page on-call SRE: {{ pager_email }}
- Slack: #{{ incident_channel }}

## Post-Incident

- [ ] Create postmortem document
- [ ] Update this runbook if needed
- [ ] Add test coverage if missing
- [ ] Schedule follow-up for systemic fixes
```

---

## Terraform Module

### AIOps Infrastructure

```hcl
# modules/aiops/main.tf

variable "environment" {
  type = string
}

variable "slack_webhook_url" {
  type      = string
  sensitive = true
}

variable "pagerduty_integration_key" {
  type      = string
  sensitive = true
}

# Prometheus for metrics
resource "helm_release" "prometheus" {
  name       = "prometheus"
  repository = "https://prometheus-community.github.io/helm-charts"
  chart      = "kube-prometheus-stack"
  namespace  = "monitoring"
  version    = "55.0.0"

  values = [
    yamlencode({
      prometheus = {
        prometheusSpec = {
          retention = "30d"
          resources = {
            requests = {
              memory = "2Gi"
              cpu    = "500m"
            }
            limits = {
              memory = "4Gi"
              cpu    = "2"
            }
          }
          storageSpec = {
            volumeClaimTemplate = {
              spec = {
                storageClassName = "standard"
                accessModes      = ["ReadWriteOnce"]
                resources = {
                  requests = {
                    storage = "100Gi"
                  }
                }
              }
            }
          }
        }
      }
      alertmanager = {
        config = {
          receivers = [
            {
              name = "slack-critical"
              slack_configs = [
                {
                  api_url  = var.slack_webhook_url
                  channel  = "#alerts-critical"
                  title    = "{{ .Status | toUpper }}: {{ .CommonAnnotations.summary }}"
                  text     = "{{ .CommonAnnotations.description }}"
                }
              ]
            },
            {
              name = "pagerduty-critical"
              pagerduty_configs = [
                {
                  service_key = var.pagerduty_integration_key
                  severity    = "critical"
                }
              ]
            }
          ]
          route = {
            receiver = "slack-critical"
            routes = [
              {
                match = {
                  severity = "critical"
                }
                receiver = "pagerduty-critical"
              }
            ]
          }
        }
      }
    })
  ]
}

# Fluent Bit for log collection
resource "helm_release" "fluent_bit" {
  name       = "fluent-bit"
  repository = "https://fluent.github.io/helm-charts"
  chart      = "fluent-bit"
  namespace  = "logging"
  version    = "0.40.0"

  values = [
    yamlencode({
      config = {
        outputs = <<-EOT
          [OUTPUT]
              Name            es
              Match           *
              Host            elasticsearch.logging.svc.cluster.local
              Port            9200
              Index           logs-${var.environment}
        EOT
      }
    })
  ]
}

# Jaeger for distributed tracing
resource "helm_release" "jaeger" {
  name       = "jaeger"
  repository = "https://jaegertracing.github.io/helm-charts"
  chart      = "jaeger"
  namespace  = "tracing"
  version    = "0.72.0"

  values = [
    yamlencode({
      provisionDataStore = {
        cassandra = false
        elasticsearch = true
      }
      storage = {
        type = "elasticsearch"
        elasticsearch = {
          host = "elasticsearch.logging.svc.cluster.local"
          port = 9200
        }
      }
    })
  ]
}

output "prometheus_endpoint" {
  value = "http://prometheus-kube-prometheus-prometheus.monitoring.svc.cluster.local:9090"
}

output "jaeger_endpoint" {
  value = "http://jaeger-query.tracing.svc.cluster.local:16686"
}
```

---

## GitHub Actions Workflow

### AIOps CI/CD Integration

```yaml
# .github/workflows/aiops-integration.yaml
name: AIOps Integration

on:
  deployment_status:
    types: [created]
  workflow_dispatch:
    inputs:
      action:
        description: 'Action to perform'
        required: true
        type: choice
        options:
          - rollback
          - scale-up
          - restart

jobs:
  notify-deployment:
    if: github.event_name == 'deployment_status'
    runs-on: ubuntu-latest
    steps:
      - name: Send deployment event to AIOps
        run: |
          curl -X POST "${{ secrets.AIOPS_WEBHOOK_URL }}" \
            -H "Content-Type: application/json" \
            -d '{
              "event_type": "deployment",
              "service": "${{ github.repository }}",
              "environment": "${{ github.event.deployment.environment }}",
              "status": "${{ github.event.deployment_status.state }}",
              "sha": "${{ github.sha }}",
              "timestamp": "${{ github.event.deployment_status.created_at }}"
            }'

  manual-remediation:
    if: github.event_name == 'workflow_dispatch'
    runs-on: ubuntu-latest
    steps:
      - name: Configure kubectl
        uses: azure/setup-kubectl@v3

      - name: Set up kubeconfig
        run: |
          echo "${{ secrets.KUBE_CONFIG }}" | base64 -d > kubeconfig.yaml
          export KUBECONFIG=kubeconfig.yaml

      - name: Execute remediation
        run: |
          case "${{ github.event.inputs.action }}" in
            rollback)
              kubectl rollout undo deployment/api-service -n production
              ;;
            scale-up)
              kubectl scale deployment/api-service -n production --replicas=10
              ;;
            restart)
              kubectl rollout restart deployment/api-service -n production
              ;;
          esac

      - name: Notify completion
        run: |
          curl -X POST "${{ secrets.SLACK_WEBHOOK }}" \
            -H "Content-Type: application/json" \
            -d '{
              "text": "Manual remediation completed: ${{ github.event.inputs.action }} by ${{ github.actor }}"
            }'
```

---

## ServiceNow Integration Template

### Incident Creation Payload

```json
{
  "short_description": "{{ alert_name }}: {{ service }} - {{ environment }}",
  "description": "## Alert Details\n\n**Alert**: {{ alert_name }}\n**Service**: {{ service }}\n**Environment**: {{ environment }}\n**Severity**: {{ severity }}\n**Timestamp**: {{ timestamp }}\n\n## Summary\n{{ description }}\n\n## Metrics\n- Error Rate: {{ error_rate }}%\n- Latency P99: {{ latency_p99 }}ms\n\n## Suggested Actions\n{{ runbook_url }}",
  "caller_id": "aiops-system",
  "category": "software",
  "subcategory": "application",
  "impact": "{{ impact_level }}",
  "urgency": "{{ urgency_level }}",
  "assignment_group": "{{ assignment_group }}",
  "cmdb_ci": "{{ cmdb_ci }}",
  "u_aiops_correlation_id": "{{ correlation_id }}",
  "u_aiops_confidence": "{{ rca_confidence }}"
}
```

### Event Correlation Mapping

```yaml
# servicenow-event-mapping.yaml
event_mappings:
  - source_pattern: "SLOErrorBudgetFastBurn"
    servicenow:
      category: "availability"
      subcategory: "error_rate"
      impact: 1
      urgency: 1
      assignment_group: "SRE-Team"

  - source_pattern: "MemoryLeakSuspected"
    servicenow:
      category: "performance"
      subcategory: "memory"
      impact: 2
      urgency: 2
      assignment_group: "Platform-Team"

  - source_pattern: "CPUAnomalyDetected"
    servicenow:
      category: "performance"
      subcategory: "cpu"
      impact: 3
      urgency: 3
      assignment_group: "App-Team"
```
