# Prometheus Monitoring Templates

## Helm Values (kube-prometheus-stack)

```yaml
# prometheus-values.yaml
# Helm chart: prometheus-community/kube-prometheus-stack
# Version: 60.x+ (2025)

prometheus:
  prometheusSpec:
    replicas: 2
    retention: 30d
    retentionSize: 50GB

    # Resource allocation
    resources:
      requests:
        cpu: 500m
        memory: 2Gi
      limits:
        cpu: 2000m
        memory: 8Gi

    # Persistent storage
    storageSpec:
      volumeClaimTemplate:
        spec:
          storageClassName: standard
          accessModes: ["ReadWriteOnce"]
          resources:
            requests:
              storage: 100Gi

    # External labels for federation
    externalLabels:
      cluster: production
      region: eu-central-1

    # Remote write for long-term storage
    remoteWrite:
      - url: https://thanos-receive.example.com/api/v1/receive
        writeRelabelConfigs:
          - sourceLabels: [__name__]
            regex: 'go_.*'
            action: drop

    # Pod anti-affinity for HA
    podAntiAffinity: hard

    # Scrape configuration
    scrapeInterval: 30s
    scrapeTimeout: 10s
    evaluationInterval: 30s

    # Rule selectors
    ruleSelector:
      matchLabels:
        prometheus: main

    # Additional scrape configs
    additionalScrapeConfigs:
      - job_name: 'kubernetes-pods'
        kubernetes_sd_configs:
          - role: pod
        relabel_configs:
          - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
            action: keep
            regex: true
          - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_path]
            action: replace
            target_label: __metrics_path__
            regex: (.+)
          - source_labels: [__address__, __meta_kubernetes_pod_annotation_prometheus_io_port]
            action: replace
            regex: ([^:]+)(?::\d+)?;(\d+)
            replacement: $1:$2
            target_label: __address__
          - source_labels: [__meta_kubernetes_namespace]
            action: replace
            target_label: namespace
          - source_labels: [__meta_kubernetes_pod_name]
            action: replace
            target_label: pod

alertmanager:
  alertmanagerSpec:
    replicas: 3

    storage:
      volumeClaimTemplate:
        spec:
          storageClassName: standard
          accessModes: ["ReadWriteOnce"]
          resources:
            requests:
              storage: 10Gi

    resources:
      requests:
        cpu: 100m
        memory: 256Mi
      limits:
        cpu: 500m
        memory: 512Mi

  config:
    global:
      resolve_timeout: 5m
      slack_api_url: '${SLACK_WEBHOOK_URL}'

    route:
      group_by: ['alertname', 'namespace', 'severity']
      group_wait: 30s
      group_interval: 5m
      repeat_interval: 4h
      receiver: 'default-receiver'
      routes:
        - match:
            severity: critical
          receiver: 'pagerduty-critical'
          continue: true
        - match:
            severity: warning
          receiver: 'slack-warnings'
        - match_re:
            namespace: 'team-.*'
          receiver: 'team-slack'
          group_by: ['alertname', 'namespace', 'team']

    receivers:
      - name: 'default-receiver'
        slack_configs:
          - channel: '#alerts'
            send_resolved: true
            title: '{{ template "slack.title" . }}'
            text: '{{ template "slack.text" . }}'

      - name: 'slack-warnings'
        slack_configs:
          - channel: '#alerts-warning'
            send_resolved: true

      - name: 'pagerduty-critical'
        pagerduty_configs:
          - service_key: '${PAGERDUTY_SERVICE_KEY}'
            send_resolved: true

      - name: 'team-slack'
        slack_configs:
          - channel: '#team-{{ .GroupLabels.team }}-alerts'
            send_resolved: true

    templates:
      - '/etc/alertmanager/config/*.tmpl'

grafana:
  enabled: true
  adminPassword: '${GRAFANA_ADMIN_PASSWORD}'

  persistence:
    enabled: true
    size: 10Gi

  resources:
    requests:
      cpu: 100m
      memory: 256Mi
    limits:
      cpu: 500m
      memory: 512Mi

  datasources:
    datasources.yaml:
      apiVersion: 1
      datasources:
        - name: Prometheus
          type: prometheus
          url: http://prometheus-prometheus:9090
          isDefault: true
          jsonData:
            timeInterval: "30s"
        - name: Loki
          type: loki
          url: http://loki:3100
        - name: Tempo
          type: tempo
          url: http://tempo:3100

  dashboardProviders:
    dashboardproviders.yaml:
      apiVersion: 1
      providers:
        - name: 'default'
          folder: ''
          type: file
          options:
            path: /var/lib/grafana/dashboards/default

  sidecar:
    dashboards:
      enabled: true
      label: grafana_dashboard
    datasources:
      enabled: true
      label: grafana_datasource

kubeStateMetrics:
  enabled: true

nodeExporter:
  enabled: true

prometheusOperator:
  enabled: true
  resources:
    requests:
      cpu: 100m
      memory: 100Mi
    limits:
      cpu: 200m
      memory: 200Mi

# Default rules
defaultRules:
  create: true
  rules:
    alertmanager: true
    etcd: true
    configReloaders: true
    general: true
    k8s: true
    kubeApiserverAvailability: true
    kubeApiserverBurnrate: true
    kubeApiserverHistogram: true
    kubeApiserverSlos: true
    kubeControllerManager: true
    kubelet: true
    kubeProxy: true
    kubePrometheusGeneral: true
    kubePrometheusNodeRecording: true
    kubernetesApps: true
    kubernetesResources: true
    kubernetesStorage: true
    kubernetesSystem: true
    kubeSchedulerAlerting: true
    kubeSchedulerRecording: true
    kubeStateMetrics: true
    network: true
    node: true
    nodeExporterAlerting: true
    nodeExporterRecording: true
    prometheus: true
    prometheusOperator: true
```

---

## ServiceMonitor Template

```yaml
# servicemonitor.yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: {{ .Values.app.name }}
  namespace: {{ .Values.namespace }}
  labels:
    prometheus: main
    app.kubernetes.io/name: {{ .Values.app.name }}
spec:
  selector:
    matchLabels:
      app.kubernetes.io/name: {{ .Values.app.name }}

  endpoints:
    - port: metrics
      path: /metrics
      interval: 30s
      scrapeTimeout: 10s
      honorLabels: true

      # Add pod labels
      relabelings:
        - sourceLabels: [__meta_kubernetes_pod_name]
          targetLabel: pod
        - sourceLabels: [__meta_kubernetes_namespace]
          targetLabel: namespace
        - sourceLabels: [__meta_kubernetes_pod_label_app_kubernetes_io_version]
          targetLabel: version

      # Drop high-cardinality metrics
      metricRelabelings:
        - sourceLabels: [__name__]
          regex: 'go_gc_.*'
          action: drop
        - sourceLabels: [__name__]
          regex: 'go_memstats_.*'
          action: drop

  namespaceSelector:
    matchNames:
      - {{ .Values.namespace }}
```

---

## PodMonitor Template

```yaml
# podmonitor.yaml
apiVersion: monitoring.coreos.com/v1
kind: PodMonitor
metadata:
  name: {{ .Values.app.name }}-pods
  namespace: {{ .Values.namespace }}
  labels:
    prometheus: main
spec:
  selector:
    matchLabels:
      app.kubernetes.io/name: {{ .Values.app.name }}

  podMetricsEndpoints:
    - port: metrics
      path: /metrics
      interval: 15s

      relabelings:
        - sourceLabels: [__meta_kubernetes_pod_name]
          targetLabel: pod
        - sourceLabels: [__meta_kubernetes_pod_container_name]
          targetLabel: container

  namespaceSelector:
    matchNames:
      - {{ .Values.namespace }}
```

---

## PrometheusRule Template

```yaml
# prometheusrule.yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: {{ .Values.app.name }}-rules
  namespace: {{ .Values.namespace }}
  labels:
    prometheus: main
    app.kubernetes.io/name: {{ .Values.app.name }}
spec:
  groups:
    # Recording rules
    - name: {{ .Values.app.name }}.recording
      interval: 30s
      rules:
        - record: {{ .Values.app.name }}:request_rate:5m
          expr: |
            sum(rate(http_requests_total{app="{{ .Values.app.name }}"}[5m])) by (method, status)

        - record: {{ .Values.app.name }}:error_rate:5m
          expr: |
            sum(rate(http_requests_total{app="{{ .Values.app.name }}",status=~"5.."}[5m]))
            / sum(rate(http_requests_total{app="{{ .Values.app.name }}"}[5m]))

        - record: {{ .Values.app.name }}:latency_p99:5m
          expr: |
            histogram_quantile(0.99,
              sum(rate(http_request_duration_seconds_bucket{app="{{ .Values.app.name }}"}[5m])) by (le)
            )

    # Alerting rules
    - name: {{ .Values.app.name }}.alerts
      rules:
        - alert: {{ .Values.app.name | title }}HighErrorRate
          expr: {{ .Values.app.name }}:error_rate:5m > 0.05
          for: 5m
          labels:
            severity: critical
            team: {{ .Values.team }}
            service: {{ .Values.app.name }}
          annotations:
            summary: "High error rate for {{ .Values.app.name }}"
            description: "Error rate is {{ "{{ $value | humanizePercentage }}" }} (>5%)"
            runbook_url: "https://runbooks.example.com/{{ .Values.app.name }}/high-error-rate"
            dashboard_url: "https://grafana.example.com/d/{{ .Values.app.name }}"

        - alert: {{ .Values.app.name | title }}HighLatency
          expr: {{ .Values.app.name }}:latency_p99:5m > 1
          for: 10m
          labels:
            severity: warning
            team: {{ .Values.team }}
            service: {{ .Values.app.name }}
          annotations:
            summary: "High P99 latency for {{ .Values.app.name }}"
            description: "P99 latency is {{ "{{ $value | humanizeDuration }}" }}"
            runbook_url: "https://runbooks.example.com/{{ .Values.app.name }}/high-latency"

        - alert: {{ .Values.app.name | title }}PodRestarts
          expr: |
            increase(kube_pod_container_status_restarts_total{
              namespace="{{ .Values.namespace }}",
              container="{{ .Values.app.name }}"
            }[1h]) > 3
          for: 5m
          labels:
            severity: warning
            team: {{ .Values.team }}
            service: {{ .Values.app.name }}
          annotations:
            summary: "{{ .Values.app.name }} pod restarting frequently"
            description: "Pod {{ "{{ $labels.pod }}" }} has restarted {{ "{{ $value }}" }} times in the last hour"

        - alert: {{ .Values.app.name | title }}HighMemory
          expr: |
            container_memory_working_set_bytes{
              namespace="{{ .Values.namespace }}",
              container="{{ .Values.app.name }}"
            }
            / container_spec_memory_limit_bytes{
              namespace="{{ .Values.namespace }}",
              container="{{ .Values.app.name }}"
            }
            > 0.85
          for: 15m
          labels:
            severity: warning
            team: {{ .Values.team }}
            service: {{ .Values.app.name }}
          annotations:
            summary: "{{ .Values.app.name }} memory usage high"
            description: "Memory usage is {{ "{{ $value | humanizePercentage }}" }} of limit"
```

---

## Alertmanager Configuration Template

```yaml
# alertmanager-config.yaml
apiVersion: v1
kind: Secret
metadata:
  name: alertmanager-config
  namespace: monitoring
type: Opaque
stringData:
  alertmanager.yaml: |
    global:
      resolve_timeout: 5m
      slack_api_url: '{{ .Values.slack.webhookUrl }}'
      pagerduty_url: 'https://events.pagerduty.com/v2/enqueue'

    templates:
      - '/etc/alertmanager/config/*.tmpl'

    route:
      group_by: ['alertname', 'namespace', 'severity']
      group_wait: 30s
      group_interval: 5m
      repeat_interval: 4h
      receiver: 'default'

      routes:
        # Critical alerts -> PagerDuty + Slack
        - match:
            severity: critical
          receiver: 'pagerduty-critical'
          continue: true

        # Warning alerts -> Slack
        - match:
            severity: warning
          receiver: 'slack-warning'

        # Info alerts -> Slack (less frequent)
        - match:
            severity: info
          receiver: 'slack-info'
          group_wait: 5m
          repeat_interval: 24h

        # Team-specific routing
        {{- range .Values.teams }}
        - match:
            team: {{ .name }}
          receiver: 'team-{{ .name }}'
          group_by: ['alertname', 'service']
        {{- end }}

    receivers:
      - name: 'default'
        slack_configs:
          - channel: '#alerts'
            send_resolved: true
            title: '{{ "{{ template \"slack.title\" . }}" }}'
            text: '{{ "{{ template \"slack.text\" . }}" }}'

      - name: 'pagerduty-critical'
        pagerduty_configs:
          - service_key: '{{ .Values.pagerduty.serviceKey }}'
            send_resolved: true
            severity: critical
            description: '{{ "{{ template \"pagerduty.description\" . }}" }}'
        slack_configs:
          - channel: '#alerts-critical'
            send_resolved: true
            color: 'danger'

      - name: 'slack-warning'
        slack_configs:
          - channel: '#alerts-warning'
            send_resolved: true
            color: 'warning'

      - name: 'slack-info'
        slack_configs:
          - channel: '#alerts-info'
            send_resolved: true
            color: 'good'

      {{- range .Values.teams }}
      - name: 'team-{{ .name }}'
        slack_configs:
          - channel: '{{ .slackChannel }}'
            send_resolved: true
        {{- if .pagerdutyKey }}
        pagerduty_configs:
          - service_key: '{{ .pagerdutyKey }}'
            send_resolved: true
        {{- end }}
      {{- end }}

    inhibit_rules:
      # Inhibit warnings if critical exists
      - source_match:
          severity: 'critical'
        target_match:
          severity: 'warning'
        equal: ['alertname', 'namespace']

      # Inhibit info if warning exists
      - source_match:
          severity: 'warning'
        target_match:
          severity: 'info'
        equal: ['alertname', 'namespace']
```

---

## Slack Template

```yaml
# slack-templates.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: alertmanager-templates
  namespace: monitoring
data:
  slack.tmpl: |
    {{ define "slack.title" }}
    [{{ .Status | toUpper }}{{ if eq .Status "firing" }}:{{ .Alerts.Firing | len }}{{ end }}] {{ .CommonLabels.alertname }}
    {{ end }}

    {{ define "slack.text" }}
    {{ range .Alerts }}
    *Alert:* {{ .Annotations.summary }}
    *Severity:* {{ .Labels.severity }}
    *Namespace:* {{ .Labels.namespace }}
    {{ if .Labels.pod }}*Pod:* {{ .Labels.pod }}{{ end }}
    {{ if .Labels.service }}*Service:* {{ .Labels.service }}{{ end }}
    *Description:* {{ .Annotations.description }}
    {{ if .Annotations.runbook_url }}*Runbook:* <{{ .Annotations.runbook_url }}|View Runbook>{{ end }}
    {{ if .Annotations.dashboard_url }}*Dashboard:* <{{ .Annotations.dashboard_url }}|View Dashboard>{{ end }}
    {{ end }}
    {{ end }}

    {{ define "slack.color" }}
    {{ if eq .Status "firing" }}
    {{ if eq (index .Alerts 0).Labels.severity "critical" }}danger{{ else if eq (index .Alerts 0).Labels.severity "warning" }}warning{{ else }}good{{ end }}
    {{ else }}good{{ end }}
    {{ end }}
```

---

## Blackbox Exporter Configuration

```yaml
# blackbox-exporter-config.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: blackbox-exporter-config
  namespace: monitoring
data:
  blackbox.yaml: |
    modules:
      http_2xx:
        prober: http
        timeout: 5s
        http:
          valid_http_versions: ["HTTP/1.1", "HTTP/2.0"]
          valid_status_codes: [200, 201, 202, 204]
          method: GET
          follow_redirects: true
          preferred_ip_protocol: "ip4"
          tls_config:
            insecure_skip_verify: false

      http_post_2xx:
        prober: http
        timeout: 5s
        http:
          method: POST
          valid_status_codes: [200, 201, 202, 204]

      http_basic_auth:
        prober: http
        timeout: 5s
        http:
          method: GET
          valid_status_codes: [200]
          basic_auth:
            username: "${BASIC_AUTH_USERNAME}"
            password: "${BASIC_AUTH_PASSWORD}"

      tcp_connect:
        prober: tcp
        timeout: 5s

      icmp:
        prober: icmp
        timeout: 5s
        icmp:
          preferred_ip_protocol: "ip4"

      dns:
        prober: dns
        timeout: 5s
        dns:
          preferred_ip_protocol: "ip4"
          query_name: "example.com"
          query_type: "A"
```

---

## Grafana Dashboard ConfigMap

```yaml
# grafana-dashboard.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: grafana-dashboard-{{ .Values.app.name }}
  namespace: monitoring
  labels:
    grafana_dashboard: "1"
data:
  {{ .Values.app.name }}-dashboard.json: |
    {
      "dashboard": {
        "title": "{{ .Values.app.name | title }} Overview",
        "uid": "{{ .Values.app.name }}-overview",
        "tags": ["{{ .Values.app.name }}", "{{ .Values.team }}"],
        "timezone": "browser",
        "panels": [
          {
            "title": "Request Rate",
            "type": "timeseries",
            "gridPos": { "x": 0, "y": 0, "w": 12, "h": 8 },
            "targets": [
              {
                "expr": "sum(rate(http_requests_total{app=\"{{ .Values.app.name }}\"}[$__rate_interval])) by (status)",
                "legendFormat": "{{ "{{status}}" }}"
              }
            ]
          },
          {
            "title": "Error Rate",
            "type": "stat",
            "gridPos": { "x": 12, "y": 0, "w": 6, "h": 4 },
            "targets": [
              {
                "expr": "{{ .Values.app.name }}:error_rate:5m * 100"
              }
            ],
            "fieldConfig": {
              "defaults": {
                "unit": "percent",
                "thresholds": {
                  "mode": "absolute",
                  "steps": [
                    { "color": "green", "value": null },
                    { "color": "yellow", "value": 1 },
                    { "color": "red", "value": 5 }
                  ]
                }
              }
            }
          },
          {
            "title": "P99 Latency",
            "type": "stat",
            "gridPos": { "x": 18, "y": 0, "w": 6, "h": 4 },
            "targets": [
              {
                "expr": "{{ .Values.app.name }}:latency_p99:5m"
              }
            ],
            "fieldConfig": {
              "defaults": {
                "unit": "s",
                "thresholds": {
                  "mode": "absolute",
                  "steps": [
                    { "color": "green", "value": null },
                    { "color": "yellow", "value": 0.5 },
                    { "color": "red", "value": 1 }
                  ]
                }
              }
            }
          },
          {
            "title": "Latency Percentiles",
            "type": "timeseries",
            "gridPos": { "x": 0, "y": 8, "w": 12, "h": 8 },
            "targets": [
              {
                "expr": "histogram_quantile(0.50, sum(rate(http_request_duration_seconds_bucket{app=\"{{ .Values.app.name }}\"}[$__rate_interval])) by (le))",
                "legendFormat": "P50"
              },
              {
                "expr": "histogram_quantile(0.90, sum(rate(http_request_duration_seconds_bucket{app=\"{{ .Values.app.name }}\"}[$__rate_interval])) by (le))",
                "legendFormat": "P90"
              },
              {
                "expr": "histogram_quantile(0.99, sum(rate(http_request_duration_seconds_bucket{app=\"{{ .Values.app.name }}\"}[$__rate_interval])) by (le))",
                "legendFormat": "P99"
              }
            ]
          },
          {
            "title": "Memory Usage",
            "type": "timeseries",
            "gridPos": { "x": 12, "y": 8, "w": 12, "h": 8 },
            "targets": [
              {
                "expr": "container_memory_working_set_bytes{namespace=\"{{ .Values.namespace }}\", container=\"{{ .Values.app.name }}\"}",
                "legendFormat": "{{ "{{pod}}" }}"
              }
            ],
            "fieldConfig": {
              "defaults": { "unit": "bytes" }
            }
          }
        ]
      }
    }
```

---

## Network Policy for Prometheus

```yaml
# prometheus-network-policy.yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: prometheus-network-policy
  namespace: monitoring
spec:
  podSelector:
    matchLabels:
      app.kubernetes.io/name: prometheus
  policyTypes:
    - Ingress
    - Egress
  ingress:
    # Allow Grafana to query
    - from:
        - podSelector:
            matchLabels:
              app.kubernetes.io/name: grafana
      ports:
        - port: 9090
          protocol: TCP
    # Allow other Prometheus for federation
    - from:
        - podSelector:
            matchLabels:
              app.kubernetes.io/name: prometheus
      ports:
        - port: 9090
          protocol: TCP
  egress:
    # Allow scraping all namespaces
    - to:
        - namespaceSelector: {}
      ports:
        - port: 9090
          protocol: TCP
        - port: 8080
          protocol: TCP
        - port: 9100
          protocol: TCP
    # Allow Alertmanager
    - to:
        - podSelector:
            matchLabels:
              app.kubernetes.io/name: alertmanager
      ports:
        - port: 9093
          protocol: TCP
    # Allow DNS
    - to:
        - namespaceSelector: {}
          podSelector:
            matchLabels:
              k8s-app: kube-dns
      ports:
        - port: 53
          protocol: UDP
```
