# LLM Observability Stack

## Summary

**One-sentence:** Produces a production LLM observability stack config: OpenTelemetry collectors, Langfuse / Prometheus / Grafana wiring, alert rules, and PII-redaction pipeline.

**One-paragraph:** Produces a production LLM observability stack config. Vendor-neutral OpenTelemetry-first approach for 2026: OTel collectors, Langfuse for LLM-specific tracing + cost analytics, Prometheus + Grafana for metrics, Alertmanager for paging, and a PII-redaction pipeline at the collector. The methodology pins the stack components, their versions, and the integration recipes for OpenAI / Anthropic / Gemini / LangGraph / LlamaIndex.

**Ефективно для:** SRE / Platform engineer для production LLM observability — fixed stack YAML з components + versions + alert rules.

## Applies If (ALL must hold)

- Deploying LLM in production with multi-step chains / agents.
- Need vendor-neutral OTel-first stack (avoid lock-in).
- Have Kubernetes / Docker compose infra to host OTel + Langfuse + Prom + Grafana.
- Compliance requires EU-resident self-hosted observability.
- Multiple LLM providers (OpenAI + Anthropic + Gemini) in one product.

## Skip If (ANY kills it)

- Single-provider deployment with provider-native dashboard adequate.
- Sub-scale workload — vendor SaaS (LangSmith) is cheaper than running the stack.
- Air-gapped environment with no GitHub/upstream access — vendor offline support needed.
- Cannot dedicate one engineer to operate the stack.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| k8s/docker infra | yaml | platform |
| Data-residency policy | yaml | trust+safety |
| LLM-provider catalogue | yaml | ML lead |
| Cost budget for stack | yaml | finance |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/ai/ml-engineer/llm-observability` | Parent spec — this is its concrete impl. |
| `geek/ai/ml-engineer/cost-optimization` | Cost-rule sources. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules each with rationale + source. | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid/invalid examples + self-check. | ~800 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom/root-cause/fix. | ~800 |
| `content/04-procedure.xml` | essential | 6-step procedure: deploy-otel → deploy-langfuse → deploy-prom → wire-instrumentation → wire-pricing → wire-alerts. | ~800 |
| `content/06-decision-tree.xml` | essential | Branch by deployment topology + integration matrix. | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scaffold-yaml` | haiku | Fill langfuse-stack.yaml + alert-rules.yaml + pricing.yaml. |
| `design-integration` | sonnet | Wire SDKs (langfuse / openllmetry / native OTel) per provider. |
| `debug-collector` | opus | OTel collector pipeline triage. |

## Templates

| File | Purpose |
|------|---------|
| `templates/langfuse-stack.yaml` | Docker / k8s spec for Langfuse self-host. |
| `templates/alert-rules.yaml` | Alertmanager rules: cost / latency / quality. |
| `templates/pricing.yaml` | Per-provider per-model token-price book. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-llm-observability-stack.py` | Validate the stack config (versions, components, alert rules, pricing). | Pre-merge of every stack-config PR. |

## Related

- [[llm-observability]] — parent spec.
- [[cost-optimization]] — cost-rule inputs.
- [[claude-api]] / [[gemini-api]] — provider SDKs to instrument.

## Decision tree

Decision tree at `content/06-decision-tree.xml` picks deployment topology (docker compose dev / k8s prod / managed) and integration choice per provider.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/langfuse-stack.yaml`

```yaml
# docker-compose.yml — Self-hosted LLM observability stack
# Services: Langfuse + PostgreSQL + Prometheus + Grafana + Alertmanager + OTEL Collector
# Requires: .env with NEXTAUTH_SECRET, SALT, GRAFANA_PASSWORD, LANGFUSE_PUBLIC_KEY

version: '3.8'

services:
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

  postgres:
    image: postgres:16
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: langfuse
    volumes:
      - langfuse_data:/var/lib/postgresql/data
    restart: unless-stopped

  prometheus:
    image: prom/prometheus:latest
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
      - ./alert-rules.yaml:/etc/prometheus/alert_rules.yml
      - prometheus_data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
      - '--web.enable-lifecycle'
    restart: unless-stopped

  grafana:
    image: grafana/grafana:latest
    ports:
      - "3001:3000"
    environment:
      GF_SECURITY_ADMIN_PASSWORD: ${GRAFANA_PASSWORD:-admin}
      GF_INSTALL_PLUGINS: grafana-piechart-panel
    volumes:
      - grafana_data:/var/lib/grafana
    depends_on:
      - prometheus
    restart: unless-stopped

  alertmanager:
    image: prom/alertmanager:latest
    ports:
      - "9093:9093"
    volumes:
      - ./alertmanager.yml:/etc/alertmanager/alertmanager.yml
    restart: unless-stopped

  otel-collector:
    image: otel/opentelemetry-collector-contrib:latest
    ports:
      - "4317:4317"   # OTLP gRPC
      - "4318:4318"   # OTLP HTTP
      - "8889:8889"   # Prometheus metrics export
    volumes:
      - ./otel-collector.yml:/etc/otelcol-contrib/config.yaml
    restart: unless-stopped

volumes:
  langfuse_data:
  prometheus_data:
  grafana_data:

---
# prometheus.yml
# global:
#   scrape_interval: 15s
#   evaluation_interval: 15s
# alerting:
#   alertmanagers:
#     - static_configs:
#         - targets: [alertmanager:9093]
# rule_files:
#   - /etc/prometheus/alert_rules.yml
# scrape_configs:
#   - job_name: llm-app
#     static_configs:
#       - targets: [app:8000]
#   - job_name: otel-collector
#     static_configs:
#       - targets: [otel-collector:8889]

---
# otel-collector.yml
# receivers:
#   otlp:
#     protocols:
#       grpc:
#         endpoint: 0.0.0.0:4317
#       http:
#         endpoint: 0.0.0.0:4318
# processors:
#   batch:
#     timeout: 1s
#     send_batch_size: 1024
# exporters:
#   prometheus:
#     endpoint: "0.0.0.0:8889"
#     namespace: llm
#   otlp/langfuse:
#     endpoint: "https://cloud.langfuse.com/api/public/otel"
#     headers:
#       Authorization: "Bearer ${LANGFUSE_PUBLIC_KEY}"
# service:
#   pipelines:
#     traces:
#       receivers: [otlp]
#       processors: [batch]
#       exporters: [otlp/langfuse]
#     metrics:
#       receivers: [otlp]
#       processors: [batch]
#       exporters: [prometheus]
```

### `templates/alert-rules.yaml`

```yaml
# alert_rules.yml — Prometheus alert rules for LLM observability
# Thresholds: error rate >5%, P99 latency >10s, TTFT P95 >2s,
# hallucination >10%, daily budget 80%/95%, quality score <3.5, cache hit <20%

groups:
  - name: llm_alerts
    rules:

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
          description: "Model {{ $labels.model }} P99: {{ $value }}s"

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

      - alert: LLMCostSpike
        expr: |
          sum(increase(llm_cost_usd[1h]))
          > 1.5 * avg_over_time(sum(increase(llm_cost_usd[1h]))[7d:1h])
        for: 30m
        labels:
          severity: warning
        annotations:
          summary: "LLM cost spike detected (>150% of 7-day avg)"
          description: "Hourly cost 50% above weekly average"

      - alert: LLMDailyBudgetWarning
        expr: sum(increase(llm_cost_usd[24h])) > 80
        labels:
          severity: warning
        annotations:
          summary: "LLM daily spend at 80% of $100 budget"
          description: "Daily spend: ${{ $value | humanize }}"

      - alert: LLMDailyBudgetCritical
        expr: sum(increase(llm_cost_usd[24h])) > 95
        labels:
          severity: critical
        annotations:
          summary: "LLM daily budget nearly exhausted (>95%)"
          description: "Daily spend: ${{ $value | humanize }}"

      - alert: LLMQualityDrop
        expr: avg(llm_quality_score) < 3.5
        for: 15m
        labels:
          severity: warning
        annotations:
          summary: "LLM quality score below 3.5/5"
          description: "Average quality: {{ $value }}/5"

      - alert: LLMHighHallucinationRate
        expr: |
          sum(rate(llm_hallucination_total[15m]))
          / sum(rate(llm_requests_total[15m])) > 0.1
        for: 10m
        labels:
          severity: high
        annotations:
          summary: "Hallucination rate above 10%"
          description: "Rate: {{ $value | humanizePercentage }}"

      - alert: LLMLowCacheHitRate
        expr: |
          sum(rate(llm_cache_hits_total[1h]))
          / (sum(rate(llm_cache_hits_total[1h])) + sum(rate(llm_cache_misses_total[1h]))) < 0.2
        for: 30m
        labels:
          severity: info
        annotations:
          summary: "Cache hit rate below 20%"
          description: "Consider reviewing prompt caching strategy"
```

### `templates/pricing.yaml`

```yaml
# pricing.yaml — LLM model pricing config (Q1 2026)
# All costs in USD per 1K tokens.
# Update quarterly; import in cost-tracking code instead of hardcoding rates.

models:
  openai:
    gpt-4o:
      input_cost_per_1k: 0.0025
      output_cost_per_1k: 0.01
      cached_input_cost_per_1k: 0.00125
    gpt-4o-mini:
      input_cost_per_1k: 0.00015
      output_cost_per_1k: 0.0006
    o1:
      input_cost_per_1k: 0.015
      output_cost_per_1k: 0.06
    o3-mini:
      input_cost_per_1k: 0.001
      output_cost_per_1k: 0.004

  anthropic:
    claude-sonnet-4:
      input_cost_per_1k: 0.003
      output_cost_per_1k: 0.015
      cached_input_cost_per_1k: 0.0003
    claude-opus-4:
      input_cost_per_1k: 0.015
      output_cost_per_1k: 0.075
    claude-3-5-haiku:
      input_cost_per_1k: 0.0008
      output_cost_per_1k: 0.004

  google:
    gemini-2.0-flash:
      input_cost_per_1k: 0.000075
      output_cost_per_1k: 0.0003
    gemini-2.5-pro:
      input_cost_per_1k: 0.00125
      output_cost_per_1k: 0.01

  embeddings:
    text-embedding-3-small:
      input_cost_per_1k: 0.00002
    text-embedding-3-large:
      input_cost_per_1k: 0.00013

budget:
  monthly_usd: 1000
  daily_warning_usd: 80
  daily_critical_usd: 95
  allocation:
    production: 0.70
    staging: 0.20
    development: 0.10
```
