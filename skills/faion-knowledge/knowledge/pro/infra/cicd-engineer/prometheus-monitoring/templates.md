# Prometheus Monitoring Templates

## Helm Values Template

```yaml
# prometheus-stack-values.yaml
# Template for kube-prometheus-stack Helm chart

prometheus:
  prometheusSpec:
    # High Availability
    replicas: {{ REPLICAS | default: 2 }}

    # Retention
    retention: {{ RETENTION_DAYS | default: 15 }}d
    retentionSize: {{ RETENTION_SIZE | default: 50 }}GB

    # Storage
    storageSpec:
      volumeClaimTemplate:
        spec:
          storageClassName: {{ STORAGE_CLASS | default: "standard" }}
          accessModes: ["ReadWriteOnce"]
          resources:
            requests:
              storage: {{ STORAGE_SIZE | default: 100 }}Gi

    # Resources
    resources:
      requests:
        cpu: {{ CPU_REQUEST | default: "500m" }}
        memory: {{ MEMORY_REQUEST | default: "2Gi" }}
      limits:
        cpu: {{ CPU_LIMIT | default: "2000m" }}
        memory: {{ MEMORY_LIMIT | default: "8Gi" }}

    # External labels for federation
    externalLabels:
      cluster: {{ CLUSTER_NAME }}
      region: {{ REGION }}
      environment: {{ ENVIRONMENT }}

    # Remote write (optional)
    # remoteWrite:
    #   - url: {{ REMOTE_WRITE_URL }}
    #     writeRelabelConfigs:
    #       - sourceLabels: [__name__]
    #         regex: 'go_.*'
    #         action: drop

    # Rule selector
    ruleSelector:
      matchLabels:
        prometheus: {{ PROMETHEUS_INSTANCE | default: "main" }}

    # Service monitor selector
    serviceMonitorSelector:
      matchLabels:
        prometheus: {{ PROMETHEUS_INSTANCE | default: "main" }}

    # Pod monitor selector
    podMonitorSelector:
      matchLabels:
        prometheus: {{ PROMETHEUS_INSTANCE | default: "main" }}

alertmanager:
  alertmanagerSpec:
    replicas: 3
    storage:
      volumeClaimTemplate:
        spec:
          storageClassName: {{ STORAGE_CLASS | default: "standard" }}
          accessModes: ["ReadWriteOnce"]
          resources:
            requests:
              storage: 10Gi

  config:
    global:
      resolve_timeout: 5m
      slack_api_url: {{ SLACK_WEBHOOK_URL }}

    route:
      group_by: ['alertname', 'namespace', 'severity']
      group_wait: 30s
      group_interval: 5m
      repeat_interval: 4h
      receiver: 'default-receiver'
      routes:
        - match:
            severity: critical
          receiver: 'critical-receiver'
          continue: true
        - match:
            severity: warning
          receiver: 'warning-receiver'

    receivers:
      - name: 'default-receiver'
        slack_configs:
          - channel: '{{ SLACK_CHANNEL_DEFAULT | default: "#alerts" }}'
            send_resolved: true
            title: '[{{ "{{ .Status | toUpper }}" }}] {{ "{{ .CommonAnnotations.summary }}" }}'
            text: '{{ "{{ .CommonAnnotations.description }}" }}'

      - name: 'critical-receiver'
        slack_configs:
          - channel: '{{ SLACK_CHANNEL_CRITICAL | default: "#alerts-critical" }}'
            send_resolved: true
        # pagerduty_configs:
        #   - service_key: {{ PAGERDUTY_KEY }}
        #     send_resolved: true

      - name: 'warning-receiver'
        slack_configs:
          - channel: '{{ SLACK_CHANNEL_WARNING | default: "#alerts-warning" }}'
            send_resolved: true

grafana:
  enabled: true
  adminPassword: {{ GRAFANA_ADMIN_PASSWORD }}

  persistence:
    enabled: true
    size: 10Gi
    storageClassName: {{ STORAGE_CLASS | default: "standard" }}

  datasources:
    datasources.yaml:
      apiVersion: 1
      datasources:
        - name: Prometheus
          type: prometheus
          url: http://prometheus-prometheus:9090
          isDefault: true
          jsonData:
            timeInterval: "15s"
        - name: Alertmanager
          type: alertmanager
          url: http://alertmanager-operated:9093
          jsonData:
            implementation: prometheus

  dashboardProviders:
    dashboardproviders.yaml:
      apiVersion: 1
      providers:
        - name: 'default'
          folder: ''
          type: file
          disableDeletion: false
          options:
            path: /var/lib/grafana/dashboards/default

  # sidecar for dashboard loading
  sidecar:
    dashboards:
      enabled: true
      label: grafana_dashboard
      searchNamespace: ALL

kubeStateMetrics:
  enabled: true

nodeExporter:
  enabled: true

prometheusOperator:
  enabled: true
```

## ServiceMonitor Template

```yaml
# servicemonitor-template.yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: {{ SERVICE_NAME }}
  namespace: {{ NAMESPACE }}
  labels:
    prometheus: {{ PROMETHEUS_INSTANCE | default: "main" }}
    app.kubernetes.io/name: {{ SERVICE_NAME }}
spec:
  selector:
    matchLabels:
      app.kubernetes.io/name: {{ SERVICE_NAME }}
  endpoints:
    - port: {{ METRICS_PORT_NAME | default: "metrics" }}
      path: {{ METRICS_PATH | default: "/metrics" }}
      interval: {{ SCRAPE_INTERVAL | default: "30s" }}
      scrapeTimeout: {{ SCRAPE_TIMEOUT | default: "10s" }}
      honorLabels: {{ HONOR_LABELS | default: true }}
      relabelings:
        - sourceLabels: [__meta_kubernetes_pod_name]
          targetLabel: pod
        - sourceLabels: [__meta_kubernetes_namespace]
          targetLabel: namespace
        - sourceLabels: [__meta_kubernetes_pod_label_app_kubernetes_io_version]
          targetLabel: version
      metricRelabelings:
        # Drop high cardinality or unneeded metrics
        - sourceLabels: [__name__]
          regex: 'go_gc_.*'
          action: drop
  namespaceSelector:
    matchNames:
      - {{ NAMESPACE }}
```

## PodMonitor Template

```yaml
# podmonitor-template.yaml
apiVersion: monitoring.coreos.com/v1
kind: PodMonitor
metadata:
  name: {{ POD_NAME }}
  namespace: {{ NAMESPACE }}
  labels:
    prometheus: {{ PROMETHEUS_INSTANCE | default: "main" }}
spec:
  selector:
    matchLabels:
      app.kubernetes.io/name: {{ APP_NAME }}
  podMetricsEndpoints:
    - port: {{ METRICS_PORT_NAME | default: "metrics" }}
      path: {{ METRICS_PATH | default: "/metrics" }}
      interval: {{ SCRAPE_INTERVAL | default: "30s" }}
      scrapeTimeout: {{ SCRAPE_TIMEOUT | default: "10s" }}
  namespaceSelector:
    matchNames:
      - {{ NAMESPACE }}
```

## PrometheusRule Template

```yaml
# prometheusrule-template.yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: {{ SERVICE_NAME }}-rules
  namespace: {{ NAMESPACE }}
  labels:
    prometheus: {{ PROMETHEUS_INSTANCE | default: "main" }}
spec:
  groups:
    # Recording Rules
    - name: {{ SERVICE_NAME }}.recording
      interval: {{ RECORDING_INTERVAL | default: "30s" }}
      rules:
        - record: {{ SERVICE_NAME }}:request_rate:5m
          expr: sum(rate(http_requests_total{app="{{ SERVICE_NAME }}"}[5m])) by (method, status)

        - record: {{ SERVICE_NAME }}:error_rate:5m
          expr: |
            sum(rate(http_requests_total{app="{{ SERVICE_NAME }}",status=~"5.."}[5m]))
            / sum(rate(http_requests_total{app="{{ SERVICE_NAME }}"}[5m]))

        - record: {{ SERVICE_NAME }}:latency_p50:5m
          expr: histogram_quantile(0.50, sum(rate(http_request_duration_seconds_bucket{app="{{ SERVICE_NAME }}"}[5m])) by (le))

        - record: {{ SERVICE_NAME }}:latency_p90:5m
          expr: histogram_quantile(0.90, sum(rate(http_request_duration_seconds_bucket{app="{{ SERVICE_NAME }}"}[5m])) by (le))

        - record: {{ SERVICE_NAME }}:latency_p99:5m
          expr: histogram_quantile(0.99, sum(rate(http_request_duration_seconds_bucket{app="{{ SERVICE_NAME }}"}[5m])) by (le))

    # Alert Rules
    - name: {{ SERVICE_NAME }}.alerts
      rules:
        # High Error Rate
        - alert: {{ SERVICE_NAME | capitalize }}HighErrorRate
          expr: {{ SERVICE_NAME }}:error_rate:5m > {{ ERROR_RATE_THRESHOLD | default: 0.05 }}
          for: {{ ERROR_RATE_FOR | default: "5m" }}
          labels:
            severity: critical
            team: {{ TEAM }}
            service: {{ SERVICE_NAME }}
          annotations:
            summary: "High error rate for {{ SERVICE_NAME }}"
            description: "Error rate is {{ '{{ $value | humanizePercentage }}' }} (>{{ ERROR_RATE_THRESHOLD | default: 0.05 | multiply: 100 }}%)"
            runbook_url: {{ RUNBOOK_BASE_URL }}/{{ SERVICE_NAME }}-high-error-rate

        # High Latency
        - alert: {{ SERVICE_NAME | capitalize }}HighLatency
          expr: {{ SERVICE_NAME }}:latency_p99:5m > {{ LATENCY_THRESHOLD | default: 1 }}
          for: {{ LATENCY_FOR | default: "10m" }}
          labels:
            severity: warning
            team: {{ TEAM }}
            service: {{ SERVICE_NAME }}
          annotations:
            summary: "High P99 latency for {{ SERVICE_NAME }}"
            description: "P99 latency is {{ '{{ $value | humanizeDuration }}' }}"
            runbook_url: {{ RUNBOOK_BASE_URL }}/{{ SERVICE_NAME }}-high-latency

        # Pod Restarts
        - alert: {{ SERVICE_NAME | capitalize }}PodRestarts
          expr: increase(kube_pod_container_status_restarts_total{namespace="{{ NAMESPACE }}",container="{{ SERVICE_NAME }}"}[1h]) > {{ RESTART_THRESHOLD | default: 3 }}
          for: 5m
          labels:
            severity: warning
            team: {{ TEAM }}
            service: {{ SERVICE_NAME }}
          annotations:
            summary: "{{ SERVICE_NAME }} pod restarting frequently"
            description: "Pod {{ '{{ $labels.pod }}' }} has restarted {{ '{{ $value }}' }} times in the last hour"
            runbook_url: {{ RUNBOOK_BASE_URL }}/{{ SERVICE_NAME }}-pod-restarts

        # High Memory Usage
        - alert: {{ SERVICE_NAME | capitalize }}HighMemory
          expr: |
            container_memory_working_set_bytes{namespace="{{ NAMESPACE }}",container="{{ SERVICE_NAME }}"}
            / container_spec_memory_limit_bytes{namespace="{{ NAMESPACE }}",container="{{ SERVICE_NAME }}"}
            > {{ MEMORY_THRESHOLD | default: 0.85 }}
          for: 15m
          labels:
            severity: warning
            team: {{ TEAM }}
            service: {{ SERVICE_NAME }}
          annotations:
            summary: "{{ SERVICE_NAME }} memory usage high"
            description: "Memory usage is {{ '{{ $value | humanizePercentage }}' }} of limit"
            runbook_url: {{ RUNBOOK_BASE_URL }}/{{ SERVICE_NAME }}-high-memory

        # CPU Throttling
        - alert: {{ SERVICE_NAME | capitalize }}CPUThrottling
          expr: |
            sum(increase(container_cpu_cfs_throttled_periods_total{namespace="{{ NAMESPACE }}",container="{{ SERVICE_NAME }}"}[5m]))
            / sum(increase(container_cpu_cfs_periods_total{namespace="{{ NAMESPACE }}",container="{{ SERVICE_NAME }}"}[5m]))
            > {{ CPU_THROTTLE_THRESHOLD | default: 0.25 }}
          for: 15m
          labels:
            severity: warning
            team: {{ TEAM }}
            service: {{ SERVICE_NAME }}
          annotations:
            summary: "{{ SERVICE_NAME }} CPU throttling detected"
            description: "CPU throttling at {{ '{{ $value | humanizePercentage }}' }}"
            runbook_url: {{ RUNBOOK_BASE_URL }}/{{ SERVICE_NAME }}-cpu-throttling
```

## CI/CD Pipeline Alerts Template

```yaml
# cicd-alerts-template.yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: cicd-pipeline-alerts
  namespace: monitoring
  labels:
    prometheus: main
spec:
  groups:
    - name: cicd.alerts
      rules:
        # Jenkins Build Failure Rate
        - alert: JenkinsBuildFailureRateHigh
          expr: |
            sum(rate(jenkins_builds_failed_total[1h])) by (job_name)
            / sum(rate(jenkins_builds_total[1h])) by (job_name)
            > {{ JENKINS_FAILURE_THRESHOLD | default: 0.2 }}
          for: 15m
          labels:
            severity: warning
            team: {{ TEAM | default: "platform" }}
          annotations:
            summary: "Jenkins job {{ '{{ $labels.job_name }}' }} has high failure rate"
            description: "Failure rate is {{ '{{ $value | humanizePercentage }}' }}"
            runbook_url: {{ RUNBOOK_BASE_URL }}/jenkins-high-failure-rate

        # Jenkins Queue Too Long
        - alert: JenkinsQueueTooLong
          expr: jenkins_queue_size_value > {{ JENKINS_QUEUE_THRESHOLD | default: 10 }}
          for: 30m
          labels:
            severity: warning
            team: {{ TEAM | default: "platform" }}
          annotations:
            summary: "Jenkins queue is too long"
            description: "Queue size is {{ '{{ $value }}' }} jobs"
            runbook_url: {{ RUNBOOK_BASE_URL }}/jenkins-queue-long

        # GitLab CI Pipeline Duration
        - alert: GitLabCIPipelineSlow
          expr: |
            avg(gitlab_ci_pipeline_duration_seconds) by (project)
            > {{ GITLAB_DURATION_THRESHOLD | default: 1800 }}
          for: 1h
          labels:
            severity: warning
            team: {{ TEAM | default: "platform" }}
          annotations:
            summary: "GitLab CI pipelines are slow for {{ '{{ $labels.project }}' }}"
            description: "Average duration is {{ '{{ $value | humanizeDuration }}' }}"
            runbook_url: {{ RUNBOOK_BASE_URL }}/gitlab-pipeline-slow

        # ArgoCD Application Out of Sync
        - alert: ArgoCDAppOutOfSync
          expr: argocd_app_info{sync_status!="Synced"} == 1
          for: 30m
          labels:
            severity: warning
            team: {{ TEAM | default: "platform" }}
          annotations:
            summary: "ArgoCD application {{ '{{ $labels.name }}' }} is out of sync"
            description: "Sync status: {{ '{{ $labels.sync_status }}' }}"
            runbook_url: {{ RUNBOOK_BASE_URL }}/argocd-out-of-sync

        # ArgoCD Application Unhealthy
        - alert: ArgoCDAppUnhealthy
          expr: argocd_app_info{health_status!="Healthy"} == 1
          for: 15m
          labels:
            severity: critical
            team: {{ TEAM | default: "platform" }}
          annotations:
            summary: "ArgoCD application {{ '{{ $labels.name }}' }} is unhealthy"
            description: "Health status: {{ '{{ $labels.health_status }}' }}"
            runbook_url: {{ RUNBOOK_BASE_URL }}/argocd-unhealthy

        # ArgoCD Sync Failed
        - alert: ArgoCDSyncFailed
          expr: increase(argocd_app_sync_total{phase="Failed"}[1h]) > 0
          for: 5m
          labels:
            severity: critical
            team: {{ TEAM | default: "platform" }}
          annotations:
            summary: "ArgoCD sync failed for {{ '{{ $labels.name }}' }}"
            description: "Application sync has failed"
            runbook_url: {{ RUNBOOK_BASE_URL }}/argocd-sync-failed
```

## Alertmanager Config Template

```yaml
# alertmanager-config-template.yaml
global:
  resolve_timeout: 5m
  slack_api_url: '{{ SLACK_WEBHOOK_URL }}'
  # pagerduty_url: 'https://events.pagerduty.com/v2/enqueue'

templates:
  - '/etc/alertmanager/templates/*.tmpl'

route:
  group_by: ['alertname', 'namespace', 'severity']
  group_wait: 30s
  group_interval: 5m
  repeat_interval: 4h
  receiver: 'default-receiver'

  routes:
    # Critical alerts to PagerDuty and Slack
    - match:
        severity: critical
      receiver: 'critical-pagerduty'
      continue: true

    - match:
        severity: critical
      receiver: 'critical-slack'

    # Warning alerts to Slack
    - match:
        severity: warning
      receiver: 'warning-slack'

    # Team-specific routing
    - match_re:
        team: 'backend|frontend|platform'
      receiver: 'team-slack'
      group_by: ['alertname', 'namespace', 'team']

    # CI/CD specific
    - match:
        alertname: '^(Jenkins|GitLab|ArgoCD).*'
      receiver: 'cicd-slack'

inhibit_rules:
  # Inhibit warnings if critical is firing
  - source_match:
      severity: 'critical'
    target_match:
      severity: 'warning'
    equal: ['alertname', 'namespace']

receivers:
  - name: 'default-receiver'
    slack_configs:
      - channel: '{{ SLACK_CHANNEL_DEFAULT | default: "#alerts" }}'
        send_resolved: true
        icon_url: 'https://avatars.githubusercontent.com/u/3380462'
        title: '{{ "{{ template \"slack.title\" . }}" }}'
        text: '{{ "{{ template \"slack.text\" . }}" }}'
        actions:
          - type: button
            text: 'Runbook'
            url: '{{ "{{ (index .Alerts 0).Annotations.runbook_url }}" }}'
          - type: button
            text: 'Dashboard'
            url: '{{ GRAFANA_URL }}/d/{{ "{{ (index .Alerts 0).Labels.service }}" }}'

  - name: 'critical-slack'
    slack_configs:
      - channel: '{{ SLACK_CHANNEL_CRITICAL | default: "#alerts-critical" }}'
        send_resolved: true
        color: '{{ "{{ if eq .Status \"firing\" }}danger{{ else }}good{{ end }}" }}'
        title: '[CRITICAL] {{ "{{ .CommonAnnotations.summary }}" }}'
        text: '{{ "{{ .CommonAnnotations.description }}" }}'

  - name: 'critical-pagerduty'
    pagerduty_configs:
      - service_key: '{{ PAGERDUTY_SERVICE_KEY }}'
        send_resolved: true
        description: '{{ "{{ .CommonAnnotations.summary }}" }}'
        severity: critical
        details:
          firing: '{{ "{{ .Alerts.Firing | len }}" }}'
          num_alerts: '{{ "{{ .Alerts | len }}" }}'

  - name: 'warning-slack'
    slack_configs:
      - channel: '{{ SLACK_CHANNEL_WARNING | default: "#alerts-warning" }}'
        send_resolved: true
        color: '{{ "{{ if eq .Status \"firing\" }}warning{{ else }}good{{ end }}" }}'
        title: '[WARNING] {{ "{{ .CommonAnnotations.summary }}" }}'
        text: '{{ "{{ .CommonAnnotations.description }}" }}'

  - name: 'team-slack'
    slack_configs:
      - channel: '#team-{{ "{{ .CommonLabels.team }}" }}-alerts'
        send_resolved: true
        title: '{{ "{{ .CommonAnnotations.summary }}" }}'
        text: '{{ "{{ .CommonAnnotations.description }}" }}'

  - name: 'cicd-slack'
    slack_configs:
      - channel: '{{ SLACK_CHANNEL_CICD | default: "#cicd-alerts" }}'
        send_resolved: true
        title: '[CI/CD] {{ "{{ .CommonAnnotations.summary }}" }}'
        text: '{{ "{{ .CommonAnnotations.description }}" }}'
```

## Pushgateway Job Template (Shell)

```bash
#!/bin/bash
# pushgateway-metrics.sh
# Template for pushing CI/CD job metrics

set -euo pipefail

# Configuration
PUSHGATEWAY_URL="${PUSHGATEWAY_URL:-http://pushgateway:9091}"
JOB_NAME="${JOB_NAME:-ci_pipeline}"
INSTANCE="${INSTANCE:-$(hostname)}"

# Metrics
JOB_DURATION="${JOB_DURATION:-0}"
JOB_STATUS="${JOB_STATUS:-unknown}"  # success, failure, cancelled
JOB_TIMESTAMP="$(date +%s)"

# Labels (customize as needed)
PIPELINE="${PIPELINE:-unknown}"
BRANCH="${BRANCH:-unknown}"
COMMIT="${COMMIT:-unknown}"

# Push metrics
push_metrics() {
  cat <<EOF | curl --fail --silent --data-binary @- \
    "${PUSHGATEWAY_URL}/metrics/job/${JOB_NAME}/instance/${INSTANCE}"
# HELP ci_job_duration_seconds Duration of CI job in seconds
# TYPE ci_job_duration_seconds gauge
ci_job_duration_seconds{pipeline="${PIPELINE}",branch="${BRANCH}",status="${JOB_STATUS}"} ${JOB_DURATION}

# HELP ci_job_last_timestamp Unix timestamp of last job run
# TYPE ci_job_last_timestamp gauge
ci_job_last_timestamp{pipeline="${PIPELINE}",branch="${BRANCH}"} ${JOB_TIMESTAMP}

# HELP ci_job_success Success status of job (1=success, 0=failure)
# TYPE ci_job_success gauge
ci_job_success{pipeline="${PIPELINE}",branch="${BRANCH}"} $([ "${JOB_STATUS}" = "success" ] && echo 1 || echo 0)

# HELP ci_job_info Job information
# TYPE ci_job_info gauge
ci_job_info{pipeline="${PIPELINE}",branch="${BRANCH}",commit="${COMMIT}"} 1
EOF
}

# Delete metrics (call when job group is deleted)
delete_metrics() {
  curl --fail --silent -X DELETE \
    "${PUSHGATEWAY_URL}/metrics/job/${JOB_NAME}/instance/${INSTANCE}"
}

# Main
case "${1:-push}" in
  push)
    push_metrics
    echo "Metrics pushed successfully"
    ;;
  delete)
    delete_metrics
    echo "Metrics deleted successfully"
    ;;
  *)
    echo "Usage: $0 [push|delete]"
    exit 1
    ;;
esac
```

## Grafana Dashboard ConfigMap Template

```yaml
# grafana-dashboard-configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: {{ DASHBOARD_NAME }}-dashboard
  namespace: monitoring
  labels:
    grafana_dashboard: "1"
data:
  {{ DASHBOARD_NAME }}.json: |
    {
      "annotations": {
        "list": []
      },
      "editable": true,
      "fiscalYearStartMonth": 0,
      "graphTooltip": 0,
      "id": null,
      "links": [],
      "liveNow": false,
      "panels": [
        {
          "datasource": {
            "type": "prometheus",
            "uid": "${datasource}"
          },
          "fieldConfig": {
            "defaults": {
              "color": {
                "mode": "palette-classic"
              },
              "thresholds": {
                "mode": "absolute",
                "steps": [
                  {"color": "green", "value": null},
                  {"color": "yellow", "value": 80},
                  {"color": "red", "value": 95}
                ]
              },
              "unit": "percent"
            }
          },
          "gridPos": {"h": 8, "w": 12, "x": 0, "y": 0},
          "id": 1,
          "options": {
            "colorMode": "value",
            "graphMode": "area",
            "justifyMode": "auto",
            "orientation": "auto",
            "reduceOptions": {
              "calcs": ["lastNotNull"],
              "fields": "",
              "values": false
            },
            "textMode": "auto"
          },
          "targets": [
            {
              "expr": "{{ SERVICE_NAME }}:error_rate:5m * 100",
              "legendFormat": "Error Rate"
            }
          ],
          "title": "Error Rate",
          "type": "stat"
        }
      ],
      "refresh": "30s",
      "schemaVersion": 38,
      "style": "dark",
      "tags": ["{{ SERVICE_NAME }}", "generated"],
      "templating": {
        "list": [
          {
            "current": {
              "selected": false,
              "text": "Prometheus",
              "value": "Prometheus"
            },
            "hide": 0,
            "includeAll": false,
            "multi": false,
            "name": "datasource",
            "options": [],
            "query": "prometheus",
            "refresh": 1,
            "regex": "",
            "skipUrlSync": false,
            "type": "datasource"
          },
          {
            "current": {},
            "datasource": {
              "type": "prometheus",
              "uid": "${datasource}"
            },
            "definition": "label_values(up{job=\"{{ SERVICE_NAME }}\"}, namespace)",
            "hide": 0,
            "includeAll": true,
            "multi": true,
            "name": "namespace",
            "options": [],
            "query": {
              "query": "label_values(up{job=\"{{ SERVICE_NAME }}\"}, namespace)",
              "refId": "StandardVariableQuery"
            },
            "refresh": 2,
            "regex": "",
            "skipUrlSync": false,
            "sort": 1,
            "type": "query"
          }
        ]
      },
      "time": {
        "from": "now-1h",
        "to": "now"
      },
      "title": "{{ SERVICE_NAME }} Dashboard",
      "uid": "{{ SERVICE_NAME }}-dashboard",
      "version": 1
    }
```
