# Grafana Setup Examples

## Docker Compose Examples

### Basic Stack (Development)

```yaml
# docker-compose.yaml
version: '3.8'

services:
  grafana:
    image: grafana/grafana:11.6.0
    container_name: grafana
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_USER=${ADMIN_USER:-admin}
      - GF_SECURITY_ADMIN_PASSWORD=${ADMIN_PASSWORD:-admin}
      - GF_INSTALL_PLUGINS=grafana-clock-panel,grafana-piechart-panel
    volumes:
      - grafana-data:/var/lib/grafana
      - ./provisioning:/etc/grafana/provisioning
      - ./dashboards:/var/lib/grafana/dashboards
    restart: unless-stopped

  prometheus:
    image: prom/prometheus:v2.52.0
    container_name: prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus-data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
      - '--storage.tsdb.retention.time=15d'
    restart: unless-stopped

  loki:
    image: grafana/loki:3.1.0
    container_name: loki
    ports:
      - "3100:3100"
    volumes:
      - ./loki-config.yaml:/etc/loki/local-config.yaml
      - loki-data:/loki
    command: -config.file=/etc/loki/local-config.yaml
    restart: unless-stopped

  alloy:
    image: grafana/alloy:v1.4.0
    container_name: alloy
    volumes:
      - ./alloy-config.alloy:/etc/alloy/config.alloy
      - /var/log:/var/log:ro
    command:
      - run
      - /etc/alloy/config.alloy
      - --server.http.listen-addr=0.0.0.0:12345
    ports:
      - "12345:12345"
    restart: unless-stopped

volumes:
  grafana-data:
  prometheus-data:
  loki-data:
```

### Full Stack with High Availability

```yaml
# docker-compose-ha.yaml
version: '3.8'

services:
  postgres:
    image: postgres:16-alpine
    container_name: grafana-db
    environment:
      POSTGRES_DB: grafana
      POSTGRES_USER: grafana
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres-data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U grafana"]
      interval: 10s
      timeout: 5s
      retries: 5
    restart: unless-stopped

  grafana-1:
    image: grafana/grafana:11.6.0
    container_name: grafana-1
    environment:
      - GF_DATABASE_TYPE=postgres
      - GF_DATABASE_HOST=postgres:5432
      - GF_DATABASE_NAME=grafana
      - GF_DATABASE_USER=grafana
      - GF_DATABASE_PASSWORD=${DB_PASSWORD}
      - GF_SERVER_ROOT_URL=https://grafana.example.com
      - GF_UNIFIED_ALERTING_HA_LISTEN_ADDRESS=0.0.0.0:9094
      - GF_UNIFIED_ALERTING_HA_PEERS=grafana-2:9094
    volumes:
      - ./provisioning:/etc/grafana/provisioning
      - ./dashboards:/var/lib/grafana/dashboards
    depends_on:
      postgres:
        condition: service_healthy
    restart: unless-stopped

  grafana-2:
    image: grafana/grafana:11.6.0
    container_name: grafana-2
    environment:
      - GF_DATABASE_TYPE=postgres
      - GF_DATABASE_HOST=postgres:5432
      - GF_DATABASE_NAME=grafana
      - GF_DATABASE_USER=grafana
      - GF_DATABASE_PASSWORD=${DB_PASSWORD}
      - GF_SERVER_ROOT_URL=https://grafana.example.com
      - GF_UNIFIED_ALERTING_HA_LISTEN_ADDRESS=0.0.0.0:9094
      - GF_UNIFIED_ALERTING_HA_PEERS=grafana-1:9094
    volumes:
      - ./provisioning:/etc/grafana/provisioning
      - ./dashboards:/var/lib/grafana/dashboards
    depends_on:
      postgres:
        condition: service_healthy
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    container_name: grafana-lb
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./certs:/etc/nginx/certs
    depends_on:
      - grafana-1
      - grafana-2
    restart: unless-stopped

volumes:
  postgres-data:
```

---

## Provisioning Examples

### Data Sources

```yaml
# provisioning/datasources/datasources.yaml
apiVersion: 1

deleteDatasources:
  - name: Old-Prometheus
    orgId: 1

datasources:
  # Prometheus - Primary metrics
  - name: Prometheus
    type: prometheus
    access: proxy
    url: http://prometheus:9090
    isDefault: true
    editable: false
    jsonData:
      timeInterval: "15s"
      httpMethod: POST
      manageAlerts: true
      prometheusType: Prometheus
      prometheusVersion: "2.52.0"

  # Loki - Logs
  - name: Loki
    type: loki
    access: proxy
    url: http://loki:3100
    editable: false
    jsonData:
      maxLines: 1000
      derivedFields:
        - datasourceUid: tempo
          matcherRegex: "traceID=(\\w+)"
          name: TraceID
          url: "$${__value.raw}"

  # PostgreSQL - Application data
  - name: PostgreSQL
    type: postgres
    url: postgres:5432
    database: appdb
    user: grafana_reader
    secureJsonData:
      password: ${PG_PASSWORD}
    jsonData:
      sslmode: require
      maxOpenConns: 10
      maxIdleConns: 5
      connMaxLifetime: 14400

  # InfluxDB - Time series
  - name: InfluxDB
    type: influxdb
    access: proxy
    url: http://influxdb:8086
    jsonData:
      version: Flux
      organization: myorg
      defaultBucket: metrics
    secureJsonData:
      token: ${INFLUX_TOKEN}

  # Elasticsearch - Logs (legacy)
  - name: Elasticsearch
    type: elasticsearch
    url: http://elasticsearch:9200
    database: "logs-*"
    jsonData:
      esVersion: "8.0.0"
      timeField: "@timestamp"
      logMessageField: message
      logLevelField: level
```

### Dashboard Provider

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

  - name: 'infrastructure'
    orgId: 1
    folder: 'Infrastructure'
    folderUid: 'infra'
    type: file
    disableDeletion: true
    updateIntervalSeconds: 30
    allowUiUpdates: false
    options:
      path: /var/lib/grafana/dashboards/infrastructure

  - name: 'applications'
    orgId: 1
    folder: 'Applications'
    folderUid: 'apps'
    type: file
    options:
      path: /var/lib/grafana/dashboards/applications

  - name: 'business'
    orgId: 1
    folder: 'Business Metrics'
    folderUid: 'business'
    type: file
    options:
      path: /var/lib/grafana/dashboards/business
```

### Alert Rules

```yaml
# provisioning/alerting/alerting.yaml
apiVersion: 1

groups:
  - orgId: 1
    name: infrastructure-alerts
    folder: Infrastructure
    interval: 1m
    rules:
      - uid: high-cpu-alert
        title: High CPU Usage
        condition: C
        data:
          - refId: A
            relativeTimeRange:
              from: 300
              to: 0
            datasourceUid: prometheus
            model:
              expr: 100 - (avg by(instance) (rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)
              instant: false
              intervalMs: 1000
              maxDataPoints: 43200
              refId: A
          - refId: B
            relativeTimeRange:
              from: 300
              to: 0
            datasourceUid: __expr__
            model:
              conditions:
                - evaluator:
                    params: [80]
                    type: gt
                  operator:
                    type: and
                  query:
                    params: [A]
                  reducer:
                    type: avg
              refId: B
              type: classic_conditions
          - refId: C
            relativeTimeRange:
              from: 300
              to: 0
            datasourceUid: __expr__
            model:
              expression: B
              refId: C
              type: threshold
        noDataState: NoData
        execErrState: Error
        for: 5m
        annotations:
          summary: "High CPU usage detected on {{ $labels.instance }}"
          description: "CPU usage is above 80% for more than 5 minutes"
        labels:
          severity: warning
          team: infrastructure

contactPoints:
  - orgId: 1
    name: slack-notifications
    receivers:
      - uid: slack-1
        type: slack
        settings:
          url: ${SLACK_WEBHOOK_URL}
          recipient: "#alerts"
          username: Grafana Alerts
          icon_emoji: ":grafana:"
          mentionChannel: here
        disableResolveMessage: false

  - orgId: 1
    name: pagerduty-critical
    receivers:
      - uid: pd-1
        type: pagerduty
        settings:
          integrationKey: ${PAGERDUTY_KEY}
          severity: critical

policies:
  - orgId: 1
    receiver: slack-notifications
    group_by: ['alertname', 'team']
    group_wait: 30s
    group_interval: 5m
    repeat_interval: 4h
    routes:
      - receiver: pagerduty-critical
        matchers:
          - severity = critical
        continue: true
      - receiver: slack-notifications
        matchers:
          - severity =~ "warning|info"

muteTimings:
  - orgId: 1
    name: maintenance-window
    time_intervals:
      - times:
          - start_time: "02:00"
            end_time: "04:00"
        weekdays: ["sunday"]
```

---

## Kubernetes Helm Examples

### Basic Values.yaml

```yaml
# values.yaml
replicas: 1

image:
  repository: grafana/grafana
  tag: "11.6.0"
  pullPolicy: IfNotPresent

service:
  type: ClusterIP
  port: 80
  targetPort: 3000
  annotations: {}

ingress:
  enabled: true
  ingressClassName: nginx
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
  hosts:
    - grafana.example.com
  tls:
    - secretName: grafana-tls
      hosts:
        - grafana.example.com

persistence:
  enabled: true
  storageClassName: standard
  size: 10Gi

resources:
  requests:
    cpu: 100m
    memory: 256Mi
  limits:
    cpu: 500m
    memory: 512Mi

adminUser: admin
adminPassword: "" # Use existing secret instead

envFromSecret: grafana-secrets

grafana.ini:
  server:
    root_url: https://grafana.example.com
  auth:
    disable_login_form: false
  auth.anonymous:
    enabled: false

datasources:
  datasources.yaml:
    apiVersion: 1
    datasources:
      - name: Prometheus
        type: prometheus
        url: http://prometheus-server.monitoring.svc.cluster.local
        isDefault: true
        editable: false

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
    kubernetes-cluster:
      gnetId: 315
      revision: 3
      datasource: Prometheus
    node-exporter:
      gnetId: 1860
      revision: 37
      datasource: Prometheus
```

### Production HA Values.yaml

```yaml
# values-ha.yaml
replicas: 3

image:
  repository: grafana/grafana
  tag: "11.6.0"

deploymentStrategy:
  type: RollingUpdate
  rollingUpdate:
    maxUnavailable: 1
    maxSurge: 1

service:
  type: ClusterIP
  port: 80

ingress:
  enabled: true
  ingressClassName: nginx
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod
    nginx.ingress.kubernetes.io/affinity: "cookie"
    nginx.ingress.kubernetes.io/session-cookie-name: "grafana-session"
    nginx.ingress.kubernetes.io/session-cookie-max-age: "172800"
  hosts:
    - grafana.example.com
  tls:
    - secretName: grafana-tls
      hosts:
        - grafana.example.com

persistence:
  enabled: false  # Using external database

resources:
  requests:
    cpu: 250m
    memory: 512Mi
  limits:
    cpu: 1000m
    memory: 1Gi

# Anti-affinity for HA
affinity:
  podAntiAffinity:
    preferredDuringSchedulingIgnoredDuringExecution:
      - weight: 100
        podAffinityTerm:
          labelSelector:
            matchLabels:
              app.kubernetes.io/name: grafana
          topologyKey: kubernetes.io/hostname

# External PostgreSQL
envFromSecrets:
  - name: grafana-database-secret
  - name: grafana-admin-secret

grafana.ini:
  server:
    root_url: https://grafana.example.com
  database:
    type: postgres
    host: postgres-cluster.database.svc.cluster.local:5432
    name: grafana
    user: grafana
    # password from secret
  unified_alerting:
    enabled: true
    ha_listen_address: "${POD_IP}:9094"
    ha_peers: "grafana-0.grafana-headless:9094,grafana-1.grafana-headless:9094,grafana-2.grafana-headless:9094"
  auth.generic_oauth:
    enabled: true
    name: Keycloak
    allow_sign_up: true
    client_id: grafana
    # client_secret from secret
    scopes: openid email profile
    auth_url: https://keycloak.example.com/realms/main/protocol/openid-connect/auth
    token_url: https://keycloak.example.com/realms/main/protocol/openid-connect/token
    api_url: https://keycloak.example.com/realms/main/protocol/openid-connect/userinfo

# Headless service for alerting HA
headlessService: true

# Pod disruption budget
podDisruptionBudget:
  minAvailable: 2

# Service account
serviceAccount:
  create: true
  name: grafana
  annotations:
    eks.amazonaws.com/role-arn: arn:aws:iam::123456789:role/grafana-role

# Sidecar for dashboard loading from ConfigMaps
sidecar:
  dashboards:
    enabled: true
    label: grafana_dashboard
    labelValue: "1"
    folder: /tmp/dashboards
    searchNamespace: ALL
  datasources:
    enabled: true
    label: grafana_datasource
    labelValue: "1"
```

### Kubernetes Monitoring Helm Chart 2.0

```yaml
# k8s-monitoring-values.yaml
cluster:
  name: production-cluster

externalServices:
  prometheus:
    host: https://prometheus-prod-13-prod-us-east-0.grafana.net
    basicAuth:
      username: "123456"
      password: ${GRAFANA_CLOUD_API_KEY}
  loki:
    host: https://logs-prod-006.grafana.net
    basicAuth:
      username: "789012"
      password: ${GRAFANA_CLOUD_API_KEY}
  tempo:
    host: https://tempo-us-central1.grafana.net:443
    basicAuth:
      username: "345678"
      password: ${GRAFANA_CLOUD_API_KEY}

metrics:
  enabled: true
  alloy:
    instances:
      - name: alloy-metrics
        replicas: 2
        resources:
          requests:
            cpu: 100m
            memory: 256Mi
  cost:
    enabled: true
  node-exporter:
    enabled: true
  kube-state-metrics:
    enabled: true

logs:
  enabled: true
  pod_logs:
    enabled: true
  cluster_events:
    enabled: true

traces:
  enabled: true

receivers:
  grpc:
    enabled: true
    port: 4317
  http:
    enabled: true
    port: 4318

# Fleet management (optional)
fleet:
  enabled: false
  # api_url: https://fleet.grafana.net
```

---

## Grafana Alloy Configuration Examples

### Basic Alloy Config

```alloy
// config.alloy - Basic metrics and logs collection

// Prometheus scrape
prometheus.scrape "default" {
  targets = [
    {"__address__" = "localhost:9090", "job" = "prometheus"},
    {"__address__" = "localhost:3000", "job" = "grafana"},
  ]
  forward_to = [prometheus.remote_write.default.receiver]
  scrape_interval = "15s"
}

// Kubernetes service discovery
discovery.kubernetes "pods" {
  role = "pod"
}

prometheus.scrape "kubernetes" {
  targets    = discovery.kubernetes.pods.targets
  forward_to = [prometheus.remote_write.default.receiver]

  clustering {
    enabled = true
  }
}

// Remote write to Prometheus/Mimir
prometheus.remote_write "default" {
  endpoint {
    url = "http://prometheus:9090/api/v1/write"

    queue_config {
      capacity = 10000
      max_samples_per_send = 5000
    }
  }
}

// Log collection
local.file_match "logs" {
  path_targets = [{"__path__" = "/var/log/*.log"}]
}

loki.source.file "local_logs" {
  targets    = local.file_match.logs.targets
  forward_to = [loki.write.default.receiver]
}

loki.write "default" {
  endpoint {
    url = "http://loki:3100/loki/api/v1/push"
  }
}
```

### Production Alloy Config with OTLP

```alloy
// config.alloy - Production setup with OpenTelemetry

// OTLP receiver for traces and metrics
otelcol.receiver.otlp "default" {
  grpc {
    endpoint = "0.0.0.0:4317"
  }
  http {
    endpoint = "0.0.0.0:4318"
  }

  output {
    metrics = [otelcol.processor.batch.default.input]
    logs    = [otelcol.processor.batch.default.input]
    traces  = [otelcol.processor.batch.default.input]
  }
}

// Batch processor
otelcol.processor.batch "default" {
  timeout = "5s"
  send_batch_size = 1000

  output {
    metrics = [otelcol.exporter.prometheus.default.input]
    logs    = [otelcol.exporter.loki.default.input]
    traces  = [otelcol.exporter.otlp.tempo.input]
  }
}

// Export metrics to Prometheus
otelcol.exporter.prometheus "default" {
  forward_to = [prometheus.remote_write.grafana_cloud.receiver]
}

// Export logs to Loki
otelcol.exporter.loki "default" {
  forward_to = [loki.write.grafana_cloud.receiver]
}

// Export traces to Tempo
otelcol.exporter.otlp "tempo" {
  client {
    endpoint = "tempo.monitoring.svc.cluster.local:4317"
    tls {
      insecure = true
    }
  }
}

// Prometheus remote write to Grafana Cloud
prometheus.remote_write "grafana_cloud" {
  endpoint {
    url = env("PROMETHEUS_REMOTE_WRITE_URL")

    basic_auth {
      username = env("GRAFANA_CLOUD_PROMETHEUS_USERNAME")
      password = env("GRAFANA_CLOUD_API_KEY")
    }
  }
}

// Loki write to Grafana Cloud
loki.write "grafana_cloud" {
  endpoint {
    url = env("LOKI_URL")

    basic_auth {
      username = env("GRAFANA_CLOUD_LOKI_USERNAME")
      password = env("GRAFANA_CLOUD_API_KEY")
    }
  }
}

// Kubernetes monitoring
discovery.kubernetes "nodes" {
  role = "node"
}

prometheus.scrape "node_exporter" {
  targets = discovery.kubernetes.nodes.targets
  forward_to = [prometheus.remote_write.grafana_cloud.receiver]

  scrape_config {
    job_name = "node-exporter"
    metrics_path = "/metrics"
    scheme = "http"

    relabel_configs = [
      {
        source_labels = ["__meta_kubernetes_node_name"]
        target_label  = "node"
      },
    ]
  }
}
```

---

## Grafonnet Dashboard Examples

### Application Overview Dashboard

```jsonnet
// dashboards/app-overview.jsonnet
local grafana = import 'grafonnet/grafana.libsonnet';
local dashboard = grafana.dashboard;
local row = grafana.row;
local prometheus = grafana.prometheus;
local graphPanel = grafana.graphPanel;
local statPanel = grafana.statPanel;
local tablePanel = grafana.tablePanel;

local promDatasource = 'Prometheus';

dashboard.new(
  'Application Overview',
  schemaVersion=39,
  tags=['application', 'sre'],
  time_from='now-1h',
  time_to='now',
  refresh='30s',
  uid='app-overview',
)
.addTemplate(
  grafana.template.datasource(
    'datasource',
    'prometheus',
    promDatasource,
  )
)
.addTemplate(
  grafana.template.query(
    name='namespace',
    datasource='$datasource',
    query='label_values(kube_pod_info, namespace)',
    refresh='load',
    includeAll=true,
    multi=true,
  )
)
.addTemplate(
  grafana.template.query(
    name='service',
    datasource='$datasource',
    query='label_values(kube_service_info{namespace=~"$namespace"}, service)',
    refresh='load',
    includeAll=true,
    multi=true,
  )
)
.addRow(
  row.new(title='Service Health')
  .addPanel(
    statPanel.new(
      'Request Rate',
      datasource='$datasource',
      unit='reqps',
      colorMode='value',
    )
    .addTarget(
      prometheus.target(
        'sum(rate(http_requests_total{namespace=~"$namespace",service=~"$service"}[5m]))',
        legendFormat='Total',
      )
    )
    .addThreshold({color: 'green', value: null})
    .addThreshold({color: 'yellow', value: 1000})
    .addThreshold({color: 'red', value: 5000}),
    gridPos={h: 4, w: 4, x: 0, y: 0}
  )
  .addPanel(
    statPanel.new(
      'Error Rate',
      datasource='$datasource',
      unit='percent',
      colorMode='value',
    )
    .addTarget(
      prometheus.target(
        'sum(rate(http_requests_total{namespace=~"$namespace",service=~"$service",status=~"5.."}[5m])) / sum(rate(http_requests_total{namespace=~"$namespace",service=~"$service"}[5m])) * 100',
        legendFormat='Errors',
      )
    )
    .addThreshold({color: 'green', value: null})
    .addThreshold({color: 'yellow', value: 1})
    .addThreshold({color: 'red', value: 5}),
    gridPos={h: 4, w: 4, x: 4, y: 0}
  )
  .addPanel(
    statPanel.new(
      'P99 Latency',
      datasource='$datasource',
      unit='s',
      colorMode='value',
    )
    .addTarget(
      prometheus.target(
        'histogram_quantile(0.99, sum(rate(http_request_duration_seconds_bucket{namespace=~"$namespace",service=~"$service"}[5m])) by (le))',
        legendFormat='P99',
      )
    )
    .addThreshold({color: 'green', value: null})
    .addThreshold({color: 'yellow', value: 0.5})
    .addThreshold({color: 'red', value: 1}),
    gridPos={h: 4, w: 4, x: 8, y: 0}
  )
  .addPanel(
    statPanel.new(
      'Available Replicas',
      datasource='$datasource',
      unit='short',
      colorMode='value',
    )
    .addTarget(
      prometheus.target(
        'sum(kube_deployment_status_replicas_available{namespace=~"$namespace"})',
        legendFormat='Replicas',
      )
    )
    .addThreshold({color: 'red', value: null})
    .addThreshold({color: 'yellow', value: 2})
    .addThreshold({color: 'green', value: 3}),
    gridPos={h: 4, w: 4, x: 12, y: 0}
  )
)
.addRow(
  row.new(title='Traffic')
  .addPanel(
    graphPanel.new(
      'Request Rate by Status',
      datasource='$datasource',
      span=12,
      fill=1,
      legend_show=true,
      legend_values=true,
      legend_current=true,
      legend_alignAsTable=true,
    )
    .addTarget(
      prometheus.target(
        'sum(rate(http_requests_total{namespace=~"$namespace",service=~"$service"}[5m])) by (status)',
        legendFormat='{{status}}',
      )
    ),
    gridPos={h: 8, w: 12, x: 0, y: 4}
  )
  .addPanel(
    graphPanel.new(
      'Latency Distribution',
      datasource='$datasource',
      span=12,
      fill=1,
    )
    .addTarget(
      prometheus.target(
        'histogram_quantile(0.50, sum(rate(http_request_duration_seconds_bucket{namespace=~"$namespace",service=~"$service"}[5m])) by (le))',
        legendFormat='P50',
      )
    )
    .addTarget(
      prometheus.target(
        'histogram_quantile(0.90, sum(rate(http_request_duration_seconds_bucket{namespace=~"$namespace",service=~"$service"}[5m])) by (le))',
        legendFormat='P90',
      )
    )
    .addTarget(
      prometheus.target(
        'histogram_quantile(0.99, sum(rate(http_request_duration_seconds_bucket{namespace=~"$namespace",service=~"$service"}[5m])) by (le))',
        legendFormat='P99',
      )
    ),
    gridPos={h: 8, w: 12, x: 12, y: 4}
  )
)
.addRow(
  row.new(title='Resources')
  .addPanel(
    graphPanel.new(
      'CPU Usage',
      datasource='$datasource',
      span=6,
      fill=1,
      format='short',
    )
    .addTarget(
      prometheus.target(
        'sum(rate(container_cpu_usage_seconds_total{namespace=~"$namespace",container!="",container!="POD"}[5m])) by (pod)',
        legendFormat='{{pod}}',
      )
    ),
    gridPos={h: 8, w: 12, x: 0, y: 12}
  )
  .addPanel(
    graphPanel.new(
      'Memory Usage',
      datasource='$datasource',
      span=6,
      fill=1,
      format='bytes',
    )
    .addTarget(
      prometheus.target(
        'sum(container_memory_working_set_bytes{namespace=~"$namespace",container!="",container!="POD"}) by (pod)',
        legendFormat='{{pod}}',
      )
    ),
    gridPos={h: 8, w: 12, x: 12, y: 12}
  )
)
```

### Generate Dashboard

```bash
# Install dependencies
brew install jsonnet  # macOS
# or: apt install jsonnet  # Ubuntu

# Clone grafonnet
git clone https://github.com/grafana/grafonnet-lib.git

# Generate dashboard JSON
jsonnet -J grafonnet-lib dashboards/app-overview.jsonnet > dashboards/json/app-overview.json

# Import to Grafana via API
curl -X POST http://admin:admin@localhost:3000/api/dashboards/db \
  -H "Content-Type: application/json" \
  -d "{\"dashboard\": $(cat dashboards/json/app-overview.json), \"overwrite\": true}"
```

---

## Nginx Load Balancer Example

```nginx
# nginx.conf for Grafana HA
upstream grafana {
    least_conn;
    server grafana-1:3000 weight=1 max_fails=3 fail_timeout=30s;
    server grafana-2:3000 weight=1 max_fails=3 fail_timeout=30s;
    keepalive 32;
}

server {
    listen 80;
    server_name grafana.example.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name grafana.example.com;

    ssl_certificate /etc/nginx/certs/fullchain.pem;
    ssl_certificate_key /etc/nginx/certs/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256;
    ssl_prefer_server_ciphers off;

    # Security headers
    add_header Strict-Transport-Security "max-age=63072000" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;

    location / {
        proxy_pass http://grafana;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header Connection "";

        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }

    # WebSocket support for Live features
    location /api/live/ {
        proxy_pass http://grafana;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
    }

    # Health check endpoint
    location /health {
        proxy_pass http://grafana/api/health;
        proxy_http_version 1.1;
        access_log off;
    }
}
```
