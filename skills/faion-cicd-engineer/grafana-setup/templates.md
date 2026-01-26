# Grafana Setup Templates

## Directory Structure Template

```
grafana-stack/
├── docker-compose.yaml
├── .env
├── .env.example
├── provisioning/
│   ├── datasources/
│   │   └── datasources.yaml
│   ├── dashboards/
│   │   └── dashboards.yaml
│   ├── alerting/
│   │   ├── alerting.yaml
│   │   └── contact-points.yaml
│   └── plugins/
│       └── plugins.yaml
├── dashboards/
│   ├── default/
│   ├── infrastructure/
│   ├── applications/
│   └── business/
├── alloy/
│   └── config.alloy
├── prometheus/
│   ├── prometheus.yml
│   └── rules/
├── loki/
│   └── loki-config.yaml
└── nginx/
    ├── nginx.conf
    └── certs/
```

---

## Environment Variables Template

```bash
# .env.example

# Grafana Admin
ADMIN_USER=admin
ADMIN_PASSWORD=change_me_in_production

# Database (PostgreSQL for HA)
DB_TYPE=postgres
DB_HOST=postgres
DB_PORT=5432
DB_NAME=grafana
DB_USER=grafana
DB_PASSWORD=secure_database_password

# External Services
PROMETHEUS_URL=http://prometheus:9090
LOKI_URL=http://loki:3100

# Grafana Cloud (optional)
GRAFANA_CLOUD_API_KEY=
GRAFANA_CLOUD_PROMETHEUS_USERNAME=
GRAFANA_CLOUD_LOKI_USERNAME=

# Alerting
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/xxx
PAGERDUTY_KEY=

# OAuth (optional)
OAUTH_CLIENT_ID=
OAUTH_CLIENT_SECRET=
OAUTH_AUTH_URL=
OAUTH_TOKEN_URL=
```

---

## grafana.ini Template

```ini
# grafana.ini - Production configuration template

#################################### Server ####################################
[server]
protocol = http
http_addr = 0.0.0.0
http_port = 3000
domain = grafana.example.com
root_url = %(protocol)s://%(domain)s/
serve_from_sub_path = false
enforce_domain = false

#################################### Database ##################################
[database]
type = postgres
host = ${DB_HOST}:${DB_PORT}
name = ${DB_NAME}
user = ${DB_USER}
password = ${DB_PASSWORD}
ssl_mode = require
max_open_conn = 100
max_idle_conn = 50
conn_max_lifetime = 14400

#################################### Session ###################################
[session]
provider = database
provider_config =
cookie_name = grafana_session
cookie_secure = true
session_life_time = 86400

#################################### Security ##################################
[security]
admin_user = admin
admin_password = ${ADMIN_PASSWORD}
secret_key = ${SECRET_KEY}
disable_gravatar = true
cookie_secure = true
cookie_samesite = strict
strict_transport_security = true
strict_transport_security_max_age_seconds = 63072000
x_content_type_options = true
x_xss_protection = true

#################################### Users #####################################
[users]
allow_sign_up = false
allow_org_create = false
auto_assign_org = true
auto_assign_org_role = Viewer
default_theme = dark

#################################### Anonymous Auth ############################
[auth.anonymous]
enabled = false

#################################### Basic Auth ################################
[auth.basic]
enabled = true

#################################### Auth Proxy ################################
[auth.proxy]
enabled = false

#################################### OAuth #####################################
[auth.generic_oauth]
enabled = ${OAUTH_ENABLED:false}
name = OAuth
allow_sign_up = true
client_id = ${OAUTH_CLIENT_ID}
client_secret = ${OAUTH_CLIENT_SECRET}
scopes = openid profile email
auth_url = ${OAUTH_AUTH_URL}
token_url = ${OAUTH_TOKEN_URL}
api_url = ${OAUTH_API_URL}
role_attribute_path = contains(groups[*], 'admin') && 'Admin' || contains(groups[*], 'editor') && 'Editor' || 'Viewer'

#################################### LDAP ######################################
[auth.ldap]
enabled = false
config_file = /etc/grafana/ldap.toml
allow_sign_up = true

#################################### Unified Alerting ##########################
[unified_alerting]
enabled = true
ha_listen_address = ${POD_IP:0.0.0.0}:9094
ha_peers = ${HA_PEERS}
ha_peer_timeout = 15s

#################################### Alerting ##################################
[alerting]
enabled = false

#################################### Logging ###################################
[log]
mode = console
level = info

[log.console]
format = json

#################################### Metrics ###################################
[metrics]
enabled = true
basic_auth_username = metrics
basic_auth_password = ${METRICS_PASSWORD}

#################################### Plugins ###################################
[plugins]
enable_alpha = false
allow_loading_unsigned_plugins =

#################################### Feature Toggles ###########################
[feature_toggles]
enable = publicDashboards

#################################### SMTP / Email ##############################
[smtp]
enabled = ${SMTP_ENABLED:false}
host = ${SMTP_HOST}:${SMTP_PORT}
user = ${SMTP_USER}
password = ${SMTP_PASSWORD}
from_address = grafana@example.com
from_name = Grafana

#################################### Rendering #################################
[rendering]
server_url = http://renderer:8081/render
callback_url = http://grafana:3000/
```

---

## Data Source Templates

### Prometheus Data Source

```yaml
# provisioning/datasources/prometheus.yaml
apiVersion: 1

datasources:
  - name: Prometheus
    type: prometheus
    access: proxy
    url: ${PROMETHEUS_URL}
    isDefault: true
    editable: false
    version: 1
    jsonData:
      timeInterval: "15s"
      queryTimeout: "60s"
      httpMethod: POST
      manageAlerts: true
      prometheusType: Prometheus
      prometheusVersion: "2.52.0"
      cacheLevel: 'High'
      disableRecordingRules: false
      incrementalQueryOverlapWindow: 10m
      exemplarTraceIdDestinations:
        - name: traceID
          datasourceUid: tempo
```

### Loki Data Source

```yaml
# provisioning/datasources/loki.yaml
apiVersion: 1

datasources:
  - name: Loki
    type: loki
    access: proxy
    url: ${LOKI_URL}
    editable: false
    jsonData:
      maxLines: 1000
      timeout: "60s"
      derivedFields:
        - datasourceUid: tempo
          matcherRegex: "traceID=(\\w+)"
          matcherType: regex
          name: TraceID
          url: "$${__value.raw}"
          urlDisplayLabel: "View Trace"
```

### Tempo Data Source

```yaml
# provisioning/datasources/tempo.yaml
apiVersion: 1

datasources:
  - name: Tempo
    type: tempo
    access: proxy
    url: ${TEMPO_URL}
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
        filterBySpanID: true
      tracesToMetrics:
        datasourceUid: prometheus
        tags: [{ key: 'service.name', value: 'service' }]
        queries:
          - name: 'Request Rate'
            query: 'sum(rate(traces_spanmetrics_calls_total{$$__tags}[5m]))'
          - name: 'Error Rate'
            query: 'sum(rate(traces_spanmetrics_calls_total{$$__tags, status_code="STATUS_CODE_ERROR"}[5m]))'
      serviceMap:
        datasourceUid: prometheus
      nodeGraph:
        enabled: true
      lokiSearch:
        datasourceUid: loki
```

### PostgreSQL Data Source

```yaml
# provisioning/datasources/postgres.yaml
apiVersion: 1

datasources:
  - name: PostgreSQL
    type: postgres
    url: ${PG_HOST}:${PG_PORT}
    database: ${PG_DATABASE}
    user: ${PG_USER}
    editable: false
    secureJsonData:
      password: ${PG_PASSWORD}
    jsonData:
      sslmode: require
      maxOpenConns: 25
      maxIdleConns: 10
      maxIdleConnsAuto: true
      connMaxLifetime: 14400
      postgresVersion: 1500
      timescaledb: false
```

---

## Dashboard Provider Template

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
    updateIntervalSeconds: 30
    allowUiUpdates: false
    options:
      path: /var/lib/grafana/dashboards/default
      foldersFromFilesStructure: true

  - name: 'infrastructure'
    orgId: 1
    folder: 'Infrastructure'
    folderUid: 'infrastructure'
    type: file
    disableDeletion: true
    updateIntervalSeconds: 30
    allowUiUpdates: false
    options:
      path: /var/lib/grafana/dashboards/infrastructure

  - name: 'applications'
    orgId: 1
    folder: 'Applications'
    folderUid: 'applications'
    type: file
    disableDeletion: true
    options:
      path: /var/lib/grafana/dashboards/applications

  - name: 'slo'
    orgId: 1
    folder: 'SLO Dashboards'
    folderUid: 'slo'
    type: file
    disableDeletion: true
    options:
      path: /var/lib/grafana/dashboards/slo

  - name: 'alerts'
    orgId: 1
    folder: 'Alert Dashboards'
    folderUid: 'alerts'
    type: file
    options:
      path: /var/lib/grafana/dashboards/alerts
```

---

## Alerting Templates

### Alert Rules Template

```yaml
# provisioning/alerting/rules.yaml
apiVersion: 1

groups:
  - orgId: 1
    name: infrastructure
    folder: Infrastructure Alerts
    interval: 1m
    rules:
      - uid: high-cpu
        title: High CPU Usage
        condition: C
        data:
          - refId: A
            relativeTimeRange:
              from: 300
              to: 0
            datasourceUid: prometheus
            model:
              expr: |
                100 - (avg by(instance) (rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)
              refId: A
          - refId: B
            datasourceUid: __expr__
            model:
              type: reduce
              expression: A
              reducer: mean
              refId: B
          - refId: C
            datasourceUid: __expr__
            model:
              type: threshold
              expression: B
              conditions:
                - evaluator:
                    type: gt
                    params: [80]
              refId: C
        noDataState: NoData
        execErrState: Error
        for: 5m
        annotations:
          summary: "High CPU on {{ $labels.instance }}"
          description: "CPU usage is {{ $values.B.Value | printf \"%.1f\" }}%"
          runbook_url: "https://runbooks.example.com/cpu-high"
        labels:
          severity: warning
          team: infrastructure

      - uid: high-memory
        title: High Memory Usage
        condition: C
        data:
          - refId: A
            relativeTimeRange:
              from: 300
              to: 0
            datasourceUid: prometheus
            model:
              expr: |
                (1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes)) * 100
              refId: A
          - refId: B
            datasourceUid: __expr__
            model:
              type: reduce
              expression: A
              reducer: mean
              refId: B
          - refId: C
            datasourceUid: __expr__
            model:
              type: threshold
              expression: B
              conditions:
                - evaluator:
                    type: gt
                    params: [85]
              refId: C
        noDataState: NoData
        execErrState: Error
        for: 5m
        annotations:
          summary: "High memory on {{ $labels.instance }}"
          description: "Memory usage is {{ $values.B.Value | printf \"%.1f\" }}%"
        labels:
          severity: warning
          team: infrastructure

      - uid: disk-space-low
        title: Low Disk Space
        condition: C
        data:
          - refId: A
            datasourceUid: prometheus
            model:
              expr: |
                (1 - (node_filesystem_avail_bytes{fstype!~"tmpfs|overlay"} / node_filesystem_size_bytes{fstype!~"tmpfs|overlay"})) * 100
              refId: A
          - refId: B
            datasourceUid: __expr__
            model:
              type: reduce
              expression: A
              reducer: max
              refId: B
          - refId: C
            datasourceUid: __expr__
            model:
              type: threshold
              expression: B
              conditions:
                - evaluator:
                    type: gt
                    params: [90]
              refId: C
        noDataState: NoData
        execErrState: Error
        for: 10m
        annotations:
          summary: "Low disk space on {{ $labels.instance }}"
          description: "Filesystem {{ $labels.mountpoint }} is {{ $values.B.Value | printf \"%.1f\" }}% full"
        labels:
          severity: critical
          team: infrastructure
```

### Contact Points Template

```yaml
# provisioning/alerting/contact-points.yaml
apiVersion: 1

contactPoints:
  - orgId: 1
    name: slack-general
    receivers:
      - uid: slack-general-1
        type: slack
        settings:
          url: ${SLACK_WEBHOOK_URL}
          recipient: "#alerts-general"
          username: "Grafana Alert"
          icon_emoji: ":grafana:"
          title: |
            {{ template "slack.title" . }}
          text: |
            {{ template "slack.text" . }}
        disableResolveMessage: false

  - orgId: 1
    name: slack-critical
    receivers:
      - uid: slack-critical-1
        type: slack
        settings:
          url: ${SLACK_WEBHOOK_URL}
          recipient: "#alerts-critical"
          username: "Grafana Critical Alert"
          icon_emoji: ":rotating_light:"
          mentionChannel: "here"

  - orgId: 1
    name: pagerduty
    receivers:
      - uid: pagerduty-1
        type: pagerduty
        settings:
          integrationKey: ${PAGERDUTY_INTEGRATION_KEY}
          severity: critical
          class: infrastructure
          component: "{{ .CommonLabels.alertname }}"
          group: "{{ .CommonLabels.team }}"

  - orgId: 1
    name: email-team
    receivers:
      - uid: email-1
        type: email
        settings:
          addresses: "team@example.com"
          singleEmail: true
```

### Notification Policies Template

```yaml
# provisioning/alerting/policies.yaml
apiVersion: 1

policies:
  - orgId: 1
    receiver: slack-general
    group_by:
      - alertname
      - team
    group_wait: 30s
    group_interval: 5m
    repeat_interval: 4h
    routes:
      # Critical alerts go to PagerDuty
      - receiver: pagerduty
        matchers:
          - severity = critical
        group_wait: 10s
        continue: true

      # Critical also goes to Slack critical channel
      - receiver: slack-critical
        matchers:
          - severity = critical
        continue: false

      # Infrastructure team alerts
      - receiver: slack-general
        matchers:
          - team = infrastructure
        group_by:
          - alertname
          - instance

      # Application team alerts
      - receiver: email-team
        matchers:
          - team = applications
        group_by:
          - alertname
          - service

      # Default: all other alerts
      - receiver: slack-general
        matchers:
          - severity =~ "warning|info"
```

### Mute Timings Template

```yaml
# provisioning/alerting/mute-timings.yaml
apiVersion: 1

muteTimes:
  - orgId: 1
    name: maintenance-window
    time_intervals:
      - times:
          - start_time: "02:00"
            end_time: "04:00"
        weekdays:
          - "sunday"
        location: UTC

  - orgId: 1
    name: business-hours-only
    time_intervals:
      - times:
          - start_time: "18:00"
            end_time: "09:00"
        weekdays:
          - "monday:friday"
      - weekdays:
          - "saturday"
          - "sunday"

  - orgId: 1
    name: holidays
    time_intervals:
      - months:
          - "december"
        days_of_month:
          - "24:26"
          - "31"
      - months:
          - "january"
        days_of_month:
          - "1"
```

---

## Helm Values Templates

### Minimal Production Values

```yaml
# values-minimal.yaml
replicas: 1

persistence:
  enabled: true
  size: 10Gi

ingress:
  enabled: true
  hosts:
    - grafana.example.com

adminPassword: "" # Use secret

datasources:
  datasources.yaml:
    apiVersion: 1
    datasources:
      - name: Prometheus
        type: prometheus
        url: http://prometheus:9090
        isDefault: true
```

### Full Production Values

```yaml
# values-production.yaml
# See examples.md for complete production values
```

---

## Terraform Template

```hcl
# grafana.tf - Terraform configuration for Grafana resources

terraform {
  required_providers {
    grafana = {
      source  = "grafana/grafana"
      version = "~> 3.0"
    }
  }
}

provider "grafana" {
  url  = var.grafana_url
  auth = var.grafana_api_key
}

# Data source
resource "grafana_data_source" "prometheus" {
  type = "prometheus"
  name = "Prometheus"
  url  = var.prometheus_url

  is_default = true

  json_data_encoded = jsonencode({
    timeInterval = "15s"
    httpMethod   = "POST"
  })
}

# Folder
resource "grafana_folder" "infrastructure" {
  title = "Infrastructure"
}

# Dashboard
resource "grafana_dashboard" "node_exporter" {
  folder = grafana_folder.infrastructure.id

  config_json = file("${path.module}/dashboards/node-exporter.json")
}

# Alert rule
resource "grafana_rule_group" "cpu_alerts" {
  name             = "cpu-alerts"
  folder_uid       = grafana_folder.infrastructure.uid
  interval_seconds = 60
  org_id           = 1

  rule {
    name      = "High CPU Usage"
    condition = "C"

    data {
      ref_id = "A"

      relative_time_range {
        from = 300
        to   = 0
      }

      datasource_uid = grafana_data_source.prometheus.uid

      model = jsonencode({
        expr = "100 - (avg by(instance) (rate(node_cpu_seconds_total{mode=\"idle\"}[5m])) * 100)"
      })
    }

    data {
      ref_id         = "C"
      datasource_uid = "__expr__"

      model = jsonencode({
        type       = "threshold"
        expression = "A"
        conditions = [{
          evaluator = {
            type   = "gt"
            params = [80]
          }
        }]
      })
    }

    for = "5m"

    labels = {
      severity = "warning"
    }

    annotations = {
      summary = "High CPU usage detected"
    }
  }
}

# Contact point
resource "grafana_contact_point" "slack" {
  name = "Slack Notifications"

  slack {
    url       = var.slack_webhook_url
    recipient = "#alerts"
    username  = "Grafana"
  }
}

# Notification policy
resource "grafana_notification_policy" "default" {
  contact_point = grafana_contact_point.slack.name
  group_by      = ["alertname"]
}

# Variables
variable "grafana_url" {
  description = "Grafana URL"
  type        = string
}

variable "grafana_api_key" {
  description = "Grafana API key"
  type        = string
  sensitive   = true
}

variable "prometheus_url" {
  description = "Prometheus URL"
  type        = string
}

variable "slack_webhook_url" {
  description = "Slack webhook URL"
  type        = string
  sensitive   = true
}
```

---

## Grafana Alloy Config Template

```alloy
// config.alloy - Production template

// ============================================================================
// DISCOVERY
// ============================================================================

// Kubernetes pod discovery
discovery.kubernetes "pods" {
  role = "pod"

  namespaces {
    names = ["default", "production", "staging"]
  }
}

// Kubernetes node discovery
discovery.kubernetes "nodes" {
  role = "node"
}

// ============================================================================
// METRICS COLLECTION
// ============================================================================

// Scrape Kubernetes pods with prometheus.io annotations
prometheus.scrape "pods" {
  targets    = discovery.kubernetes.pods.targets
  forward_to = [prometheus.relabel.pods.receiver]

  scrape_interval = "30s"
  scrape_timeout  = "10s"
}

prometheus.relabel "pods" {
  forward_to = [prometheus.remote_write.default.receiver]

  rule {
    source_labels = ["__meta_kubernetes_pod_annotation_prometheus_io_scrape"]
    action        = "keep"
    regex         = "true"
  }

  rule {
    source_labels = ["__meta_kubernetes_pod_annotation_prometheus_io_path"]
    action        = "replace"
    target_label  = "__metrics_path__"
    regex         = "(.+)"
  }

  rule {
    source_labels = ["__meta_kubernetes_namespace"]
    target_label  = "namespace"
  }

  rule {
    source_labels = ["__meta_kubernetes_pod_name"]
    target_label  = "pod"
  }
}

// Node exporter scrape
prometheus.scrape "node_exporter" {
  targets = discovery.kubernetes.nodes.targets
  forward_to = [prometheus.remote_write.default.receiver]

  job_name = "node-exporter"
  metrics_path = "/metrics"

  scrape_interval = "30s"
}

// ============================================================================
// REMOTE WRITE
// ============================================================================

prometheus.remote_write "default" {
  endpoint {
    url = env("PROMETHEUS_REMOTE_WRITE_URL")

    basic_auth {
      username = env("REMOTE_WRITE_USERNAME")
      password = env("REMOTE_WRITE_PASSWORD")
    }

    queue_config {
      capacity          = 10000
      max_samples_per_send = 5000
      batch_send_deadline  = "5s"
    }

    metadata_config {
      send = true
      send_interval = "1m"
    }
  }

  external_labels = {
    cluster = env("CLUSTER_NAME"),
    env     = env("ENVIRONMENT"),
  }
}

// ============================================================================
// LOG COLLECTION
// ============================================================================

// Discover pod logs
discovery.kubernetes "pod_logs" {
  role = "pod"
}

loki.source.kubernetes "pods" {
  targets    = discovery.kubernetes.pod_logs.targets
  forward_to = [loki.process.default.receiver]
}

loki.process "default" {
  forward_to = [loki.write.default.receiver]

  stage.json {
    expressions = {
      level   = "level",
      message = "msg",
    }
  }

  stage.labels {
    values = {
      level = "",
    }
  }

  stage.drop {
    expression = ".*healthz.*"
    drop_counter_reason = "health_check"
  }
}

loki.write "default" {
  endpoint {
    url = env("LOKI_URL")

    basic_auth {
      username = env("LOKI_USERNAME")
      password = env("LOKI_PASSWORD")
    }
  }

  external_labels = {
    cluster = env("CLUSTER_NAME"),
  }
}

// ============================================================================
// SELF-MONITORING
// ============================================================================

prometheus.scrape "alloy" {
  targets = [{
    __address__ = "127.0.0.1:12345",
  }]

  forward_to = [prometheus.remote_write.default.receiver]
  job_name = "alloy"
}
```
