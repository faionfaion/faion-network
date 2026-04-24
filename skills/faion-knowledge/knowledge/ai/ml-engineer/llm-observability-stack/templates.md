---
id: llm-observability-stack-templates
name: "LLM Observability Stack Templates"
domain: ML
skill: faion-ml-engineer
category: "best-practices-2026"
---

# LLM Observability Stack Templates

## Docker Compose: Complete Stack

### Langfuse + Prometheus + Grafana

```yaml
# docker-compose.yml - Self-hosted observability stack
version: '3.8'

services:
  # Langfuse - LLM tracing and evaluation
  langfuse:
    image: langfuse/langfuse:latest
    ports:
      - "3000:3000"
    environment:
      DATABASE_URL: postgresql://postgres:postgres@postgres:5432/langfuse
      NEXTAUTH_SECRET: ${NEXTAUTH_SECRET}
      NEXTAUTH_URL: http://localhost:3000
      SALT: ${SALT}
      TELEMETRY_ENABLED: "false"
    depends_on:
      - postgres
    restart: unless-stopped

  # PostgreSQL for Langfuse
  postgres:
    image: postgres:16
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: langfuse
    volumes:
      - langfuse_data:/var/lib/postgresql/data
    restart: unless-stopped

  # Prometheus - metrics collection
  prometheus:
    image: prom/prometheus:latest
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
      - ./alert_rules.yml:/etc/prometheus/alert_rules.yml
      - prometheus_data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
      - '--web.enable-lifecycle'
    restart: unless-stopped

  # Grafana - dashboards
  grafana:
    image: grafana/grafana:latest
    ports:
      - "3001:3000"
    environment:
      GF_SECURITY_ADMIN_PASSWORD: ${GRAFANA_PASSWORD:-admin}
      GF_INSTALL_PLUGINS: grafana-piechart-panel
    volumes:
      - ./grafana/provisioning:/etc/grafana/provisioning
      - grafana_data:/var/lib/grafana
    depends_on:
      - prometheus
    restart: unless-stopped

  # Alertmanager - alert routing
  alertmanager:
    image: prom/alertmanager:latest
    ports:
      - "9093:9093"
    volumes:
      - ./alertmanager.yml:/etc/alertmanager/alertmanager.yml
    restart: unless-stopped

  # OTEL Collector - telemetry aggregation
  otel-collector:
    image: otel/opentelemetry-collector-contrib:latest
    ports:
      - "4317:4317"   # OTLP gRPC
      - "4318:4318"   # OTLP HTTP
      - "8889:8889"   # Prometheus metrics
    volumes:
      - ./otel-collector.yml:/etc/otelcol-contrib/config.yaml
    restart: unless-stopped

volumes:
  langfuse_data:
  prometheus_data:
  grafana_data:
```

### Prometheus Configuration

```yaml
# prometheus.yml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

alerting:
  alertmanagers:
    - static_configs:
        - targets:
          - alertmanager:9093

rule_files:
  - /etc/prometheus/alert_rules.yml

scrape_configs:
  # Application metrics
  - job_name: 'llm-app'
    static_configs:
      - targets: ['app:8000']
    metrics_path: /metrics

  # OTEL Collector metrics
  - job_name: 'otel-collector'
    static_configs:
      - targets: ['otel-collector:8889']

  # Prometheus self-monitoring
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']
```

### OTEL Collector Configuration

```yaml
# otel-collector.yml
receivers:
  otlp:
    protocols:
      grpc:
        endpoint: 0.0.0.0:4317
      http:
        endpoint: 0.0.0.0:4318

processors:
  batch:
    timeout: 1s
    send_batch_size: 1024

  # Add LLM-specific attributes
  attributes:
    actions:
      - key: service.name
        value: llm-observability
        action: upsert

exporters:
  # Prometheus for metrics
  prometheus:
    endpoint: "0.0.0.0:8889"
    namespace: llm

  # Langfuse for traces (via OTLP)
  otlp/langfuse:
    endpoint: "https://cloud.langfuse.com/api/public/otel"
    headers:
      Authorization: "Bearer ${LANGFUSE_PUBLIC_KEY}"

  # Debug logging
  logging:
    loglevel: info

service:
  pipelines:
    traces:
      receivers: [otlp]
      processors: [batch, attributes]
      exporters: [otlp/langfuse, logging]

    metrics:
      receivers: [otlp]
      processors: [batch]
      exporters: [prometheus]
```

---

## Alert Rules

### Prometheus Alert Rules

```yaml
# alert_rules.yml
groups:
  - name: llm_alerts
    rules:
      # High Error Rate
      - alert: LLMHighErrorRate
        expr: |
          sum(rate(llm_requests_total{status="error"}[5m]))
          / sum(rate(llm_requests_total[5m])) > 0.05
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "LLM error rate above 5%"
          description: "Error rate is {{ $value | humanizePercentage }}"
          runbook_url: "https://wiki.example.com/runbooks/llm-high-error-rate"

      # High Latency P99
      - alert: LLMHighLatencyP99
        expr: |
          histogram_quantile(0.99,
            sum(rate(llm_request_duration_seconds_bucket[5m])) by (le, model)
          ) > 10
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "LLM P99 latency above 10s"
          description: "Model {{ $labels.model }} P99 latency: {{ $value }}s"

      # Slow TTFT
      - alert: LLMSlowTTFT
        expr: |
          histogram_quantile(0.95,
            sum(rate(llm_ttft_seconds_bucket[5m])) by (le)
          ) > 2
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "Time to First Token P95 above 2s"
          description: "TTFT P95: {{ $value }}s"

      # Cost Spike (150% of daily average)
      - alert: LLMCostSpike
        expr: |
          sum(increase(llm_cost_usd[1h]))
          > 1.5 * avg_over_time(sum(increase(llm_cost_usd[1h]))[7d:1h])
        for: 30m
        labels:
          severity: warning
        annotations:
          summary: "LLM cost spike detected"
          description: "Hourly cost 50% above weekly average"

      # Daily Budget Warning (80%)
      - alert: LLMDailyBudgetWarning
        expr: |
          sum(increase(llm_cost_usd[24h])) > 80
        labels:
          severity: warning
        annotations:
          summary: "LLM daily spend approaching budget"
          description: "Daily spend: ${{ $value | humanize }}"

      # Daily Budget Critical (95%)
      - alert: LLMDailyBudgetCritical
        expr: |
          sum(increase(llm_cost_usd[24h])) > 95
        labels:
          severity: critical
        annotations:
          summary: "LLM daily budget nearly exhausted"
          description: "Daily spend: ${{ $value | humanize }}"

      # Quality Degradation
      - alert: LLMQualityDrop
        expr: |
          avg(llm_quality_score) < 3.5
        for: 15m
        labels:
          severity: warning
        annotations:
          summary: "LLM quality score below threshold"
          description: "Average quality: {{ $value }}/5"

      # High Hallucination Rate
      - alert: LLMHighHallucinationRate
        expr: |
          sum(rate(llm_hallucination_total[15m]))
          / sum(rate(llm_requests_total[15m])) > 0.1
        for: 10m
        labels:
          severity: high
        annotations:
          summary: "Hallucination rate above 10%"
          description: "Hallucination rate: {{ $value | humanizePercentage }}"

      # Low Cache Hit Rate
      - alert: LLMLowCacheHitRate
        expr: |
          sum(rate(llm_cache_hits_total[1h]))
          / (sum(rate(llm_cache_hits_total[1h])) + sum(rate(llm_cache_misses_total[1h]))) < 0.2
        for: 30m
        labels:
          severity: info
        annotations:
          summary: "Cache hit rate below 20%"
          description: "Consider optimizing caching strategy"
```

### Alertmanager Configuration

```yaml
# alertmanager.yml
global:
  resolve_timeout: 5m
  slack_api_url: ${SLACK_WEBHOOK_URL}

route:
  receiver: 'slack-notifications'
  group_by: ['alertname', 'severity']
  group_wait: 30s
  group_interval: 5m
  repeat_interval: 4h

  routes:
    - match:
        severity: critical
      receiver: 'pagerduty-critical'
      continue: true

    - match:
        severity: warning
      receiver: 'slack-notifications'

receivers:
  - name: 'slack-notifications'
    slack_configs:
      - channel: '#llm-alerts'
        send_resolved: true
        title: '{{ if eq .Status "firing" }}:fire:{{ else }}:white_check_mark:{{ end }} {{ .CommonAnnotations.summary }}'
        text: '{{ .CommonAnnotations.description }}'
        actions:
          - type: button
            text: 'View Dashboard'
            url: 'http://grafana:3000/d/llm-observability'
          - type: button
            text: 'Runbook'
            url: '{{ .CommonAnnotations.runbook_url }}'

  - name: 'pagerduty-critical'
    pagerduty_configs:
      - service_key: ${PAGERDUTY_SERVICE_KEY}
        severity: critical
```

---

## Environment Variables

### Complete .env Template

```bash
# .env - LLM Observability Stack

# Langfuse
LANGFUSE_PUBLIC_KEY=pk-lf-...
LANGFUSE_SECRET_KEY=sk-lf-...
LANGFUSE_HOST=https://cloud.langfuse.com
NEXTAUTH_SECRET=your-nextauth-secret
SALT=your-salt-value

# LangSmith (if using)
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=ls-...
LANGCHAIN_PROJECT=production

# Helicone
HELICONE_API_KEY=sk-helicone-...

# Portkey
PORTKEY_API_KEY=pk-...

# OpenAI
OPENAI_API_KEY=sk-...

# Anthropic
ANTHROPIC_API_KEY=sk-ant-...

# Grafana
GRAFANA_PASSWORD=your-secure-password

# Alerting
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/...
PAGERDUTY_SERVICE_KEY=...

# Application
APP_ENVIRONMENT=production
APP_VERSION=v2.1.0
```

---

## Model Pricing Configuration

```yaml
# pricing.yaml - Q1 2026 Pricing
models:
  openai:
    gpt-4o:
      input_cost_per_1k: 0.0025
      output_cost_per_1k: 0.01
      cached_input_cost_per_1k: 0.00125
    gpt-4o-mini:
      input_cost_per_1k: 0.00015
      output_cost_per_1k: 0.0006
    gpt-4-turbo:
      input_cost_per_1k: 0.01
      output_cost_per_1k: 0.03
    o1:
      input_cost_per_1k: 0.015
      output_cost_per_1k: 0.06
    o1-mini:
      input_cost_per_1k: 0.003
      output_cost_per_1k: 0.012
    o3-mini:
      input_cost_per_1k: 0.001
      output_cost_per_1k: 0.004

  anthropic:
    claude-sonnet-4-20250514:
      input_cost_per_1k: 0.003
      output_cost_per_1k: 0.015
    claude-opus-4-20250514:
      input_cost_per_1k: 0.015
      output_cost_per_1k: 0.075
    claude-3-5-haiku:
      input_cost_per_1k: 0.0008
      output_cost_per_1k: 0.004

  google:
    gemini-2.0-flash:
      input_cost_per_1k: 0.000075
      output_cost_per_1k: 0.0003
    gemini-2.0-pro:
      input_cost_per_1k: 0.00125
      output_cost_per_1k: 0.005
    gemini-2.5-pro:
      input_cost_per_1k: 0.00125
      output_cost_per_1k: 0.01

  embeddings:
    text-embedding-3-small:
      input_cost_per_1k: 0.00002
    text-embedding-3-large:
      input_cost_per_1k: 0.00013
```

---

## Budget Allocation Template

```yaml
# budget.yaml
monthly_budget_usd: 1000

allocation:
  by_team:
    engineering: 40%    # $400
    product: 30%        # $300
    support: 20%        # $200
    experiments: 10%    # $100

  by_environment:
    production: 70%
    staging: 20%
    development: 10%

  by_model_tier:
    reasoning: 30%      # o1, o3
    flagship: 40%       # GPT-4o, Claude Sonnet
    efficient: 30%      # GPT-4o-mini, Haiku

alerts:
  daily_threshold: 50   # $50/day warning
  hourly_spike: 10      # $10/hour anomaly
  warning_percent: 80   # Alert at 80% of budget
  critical_percent: 95  # Critical at 95%

optimization:
  cache_hit_target: 30%
  avg_tokens_per_request: 2000
  model_fallback_enabled: true
```

---

## Grafana Dashboard JSON

```json
{
  "dashboard": {
    "title": "LLM Observability Stack",
    "uid": "llm-observability",
    "panels": [
      {
        "title": "Total Cost (MTD)",
        "type": "stat",
        "gridPos": {"h": 4, "w": 6, "x": 0, "y": 0},
        "targets": [{"expr": "sum(llm_cost_usd)"}],
        "fieldConfig": {"defaults": {"unit": "currencyUSD"}}
      },
      {
        "title": "Request Rate",
        "type": "stat",
        "gridPos": {"h": 4, "w": 6, "x": 6, "y": 0},
        "targets": [{"expr": "sum(rate(llm_requests_total[5m]))"}],
        "fieldConfig": {"defaults": {"unit": "reqps"}}
      },
      {
        "title": "Error Rate",
        "type": "gauge",
        "gridPos": {"h": 4, "w": 6, "x": 12, "y": 0},
        "targets": [{"expr": "sum(rate(llm_requests_total{status='error'}[5m])) / sum(rate(llm_requests_total[5m])) * 100"}],
        "fieldConfig": {"defaults": {"unit": "percent", "max": 10}}
      },
      {
        "title": "Quality Score",
        "type": "gauge",
        "gridPos": {"h": 4, "w": 6, "x": 18, "y": 0},
        "targets": [{"expr": "avg(llm_quality_score)"}],
        "fieldConfig": {"defaults": {"min": 0, "max": 5}}
      },
      {
        "title": "Daily Cost Trend",
        "type": "timeseries",
        "gridPos": {"h": 8, "w": 12, "x": 0, "y": 4},
        "targets": [{"expr": "sum(increase(llm_cost_usd[1h]))"}]
      },
      {
        "title": "Latency Distribution",
        "type": "heatmap",
        "gridPos": {"h": 8, "w": 12, "x": 12, "y": 4},
        "targets": [{"expr": "sum(rate(llm_request_duration_seconds_bucket[5m])) by (le)"}]
      },
      {
        "title": "Cost by Model",
        "type": "piechart",
        "gridPos": {"h": 8, "w": 8, "x": 0, "y": 12},
        "targets": [{"expr": "sum by (model)(llm_cost_usd)"}]
      },
      {
        "title": "Token Usage",
        "type": "timeseries",
        "gridPos": {"h": 8, "w": 8, "x": 8, "y": 12},
        "targets": [
          {"expr": "sum(rate(llm_tokens_total{direction='input'}[5m]))", "legendFormat": "Input"},
          {"expr": "sum(rate(llm_tokens_total{direction='output'}[5m]))", "legendFormat": "Output"}
        ]
      },
      {
        "title": "Cache Hit Rate",
        "type": "stat",
        "gridPos": {"h": 4, "w": 4, "x": 16, "y": 12},
        "targets": [{"expr": "sum(rate(llm_cache_hits_total[1h])) / (sum(rate(llm_cache_hits_total[1h])) + sum(rate(llm_cache_misses_total[1h])))"}],
        "fieldConfig": {"defaults": {"unit": "percentunit"}}
      },
      {
        "title": "TTFT P95",
        "type": "stat",
        "gridPos": {"h": 4, "w": 4, "x": 20, "y": 12},
        "targets": [{"expr": "histogram_quantile(0.95, sum(rate(llm_ttft_seconds_bucket[5m])) by (le))"}],
        "fieldConfig": {"defaults": {"unit": "s"}}
      }
    ]
  }
}
```

---

## Kubernetes Deployment

```yaml
# k8s/observability-stack.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: llm-observability
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: langfuse
  namespace: llm-observability
spec:
  replicas: 2
  selector:
    matchLabels:
      app: langfuse
  template:
    metadata:
      labels:
        app: langfuse
    spec:
      containers:
        - name: langfuse
          image: langfuse/langfuse:latest
          ports:
            - containerPort: 3000
          env:
            - name: DATABASE_URL
              valueFrom:
                secretKeyRef:
                  name: langfuse-secrets
                  key: database-url
            - name: NEXTAUTH_SECRET
              valueFrom:
                secretKeyRef:
                  name: langfuse-secrets
                  key: nextauth-secret
          resources:
            requests:
              memory: "512Mi"
              cpu: "250m"
            limits:
              memory: "1Gi"
              cpu: "500m"
---
apiVersion: v1
kind: Service
metadata:
  name: langfuse
  namespace: llm-observability
spec:
  selector:
    app: langfuse
  ports:
    - port: 3000
      targetPort: 3000
  type: ClusterIP
```
