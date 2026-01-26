---
id: llm-observability-templates
name: "LLM Observability Templates"
domain: ML
skill: faion-ml-engineer
category: "best-practices-2026"
---

# LLM Observability Templates

## Configuration Templates

### Langfuse Environment Variables

```bash
# .env file
LANGFUSE_PUBLIC_KEY=pk-lf-...
LANGFUSE_SECRET_KEY=sk-lf-...
LANGFUSE_HOST=https://cloud.langfuse.com  # or self-hosted URL

# Optional
LANGFUSE_RELEASE=v1.2.3  # Track deployment version
LANGFUSE_DEBUG=false
LANGFUSE_SAMPLE_RATE=1.0  # 1.0 = 100%, 0.1 = 10%
```

### LangSmith Environment Variables

```bash
# .env file
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=ls-...
LANGCHAIN_PROJECT=my-project
LANGCHAIN_ENDPOINT=https://api.smith.langchain.com  # default

# Optional
LANGCHAIN_HIDE_INPUTS=false
LANGCHAIN_HIDE_OUTPUTS=false
```

### Helicone Headers Template

```python
HELICONE_HEADERS = {
    # Required
    "Helicone-Auth": f"Bearer {os.getenv('HELICONE_API_KEY')}",

    # Tracking
    "Helicone-User-Id": user_id,
    "Helicone-Session-Id": session_id,

    # Properties (custom metadata)
    "Helicone-Property-Feature": "chat",
    "Helicone-Property-Environment": "production",
    "Helicone-Property-Version": "v2.1",

    # Caching
    "Helicone-Cache-Enabled": "true",
    "Helicone-Cache-Bucket-Max-Size": "1000",

    # Rate limiting
    "Helicone-RateLimit-Policy": "100;w=60",  # 100 req/min

    # Retry
    "Helicone-Retry-Enabled": "true",
    "Helicone-Retry-Num": "3",
    "Helicone-Retry-Factor": "2",
}
```

### Portkey Configuration

```python
PORTKEY_CONFIG = {
    "strategy": {
        "mode": "fallback",  # or "loadbalance"
    },
    "targets": [
        {
            "virtual_key": "openai-production",
            "weight": 0.8,  # for loadbalance
            "override_params": {
                "model": "gpt-4o"
            }
        },
        {
            "virtual_key": "azure-backup",
            "weight": 0.2,
            "override_params": {
                "model": "gpt-4"
            }
        }
    ],
    "cache": {
        "mode": "semantic",  # or "simple"
        "max_age": 3600
    },
    "retry": {
        "attempts": 3,
        "on_status_codes": [429, 500, 502, 503, 504]
    }
}
```

---

## Dashboard Templates

### Executive Dashboard (Grafana JSON)

```json
{
  "title": "LLM Observability - Executive View",
  "panels": [
    {
      "title": "Total LLM Cost (MTD)",
      "type": "stat",
      "targets": [{"expr": "sum(llm_cost_usd)"}],
      "fieldConfig": {"defaults": {"unit": "currencyUSD"}}
    },
    {
      "title": "Daily Cost Trend",
      "type": "timeseries",
      "targets": [{"expr": "sum by (day)(llm_cost_usd)"}]
    },
    {
      "title": "Cost by Model",
      "type": "piechart",
      "targets": [{"expr": "sum by (model)(llm_cost_usd)"}]
    },
    {
      "title": "Average Quality Score",
      "type": "gauge",
      "targets": [{"expr": "avg(llm_quality_score)"}],
      "fieldConfig": {"defaults": {"min": 0, "max": 5}}
    },
    {
      "title": "Total Requests",
      "type": "stat",
      "targets": [{"expr": "sum(llm_requests_total)"}]
    },
    {
      "title": "Error Rate",
      "type": "stat",
      "targets": [{"expr": "sum(llm_errors_total)/sum(llm_requests_total)*100"}],
      "fieldConfig": {"defaults": {"unit": "percent"}}
    }
  ]
}
```

### Engineering Dashboard Metrics

```yaml
# Prometheus metrics to collect
llm_metrics:
  # Latency
  - name: llm_request_duration_seconds
    type: histogram
    labels: [model, endpoint, status]
    buckets: [0.1, 0.5, 1, 2, 5, 10, 30]

  # TTFT (Time to First Token)
  - name: llm_ttft_seconds
    type: histogram
    labels: [model, endpoint]
    buckets: [0.1, 0.25, 0.5, 1, 2, 5]

  # Tokens
  - name: llm_tokens_total
    type: counter
    labels: [model, direction]  # direction: input/output

  # Cost
  - name: llm_cost_usd
    type: counter
    labels: [model, user_id, team_id]

  # Quality
  - name: llm_quality_score
    type: histogram
    labels: [model, evaluator]
    buckets: [1, 2, 3, 4, 5]

  # Errors
  - name: llm_errors_total
    type: counter
    labels: [model, error_type]  # timeout, rate_limit, invalid_request

  # Cache
  - name: llm_cache_hits_total
    type: counter
    labels: [model]

  - name: llm_cache_misses_total
    type: counter
    labels: [model]
```

---

## Alert Templates

### Prometheus Alert Rules

```yaml
groups:
  - name: llm_alerts
    rules:
      # High Error Rate
      - alert: LLMHighErrorRate
        expr: |
          sum(rate(llm_errors_total[5m]))
          / sum(rate(llm_requests_total[5m])) > 0.05
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "LLM error rate above 5%"
          description: "Error rate is {{ $value | humanizePercentage }}"

      # High Latency
      - alert: LLMHighLatency
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

      # Cost Spike
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

      # Daily Budget Threshold
      - alert: LLMDailyBudgetWarning
        expr: |
          sum(increase(llm_cost_usd[24h])) > 80  # $80 threshold
        labels:
          severity: warning
        annotations:
          summary: "LLM daily spend approaching budget"

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

      # High TTFT
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
```

### Slack Alert Template

```json
{
  "blocks": [
    {
      "type": "header",
      "text": {"type": "plain_text", "text": ":warning: LLM Alert: {{ .AlertName }}"}
    },
    {
      "type": "section",
      "fields": [
        {"type": "mrkdwn", "text": "*Severity:*\n{{ .Severity }}"},
        {"type": "mrkdwn", "text": "*Model:*\n{{ .Model }}"},
        {"type": "mrkdwn", "text": "*Current Value:*\n{{ .Value }}"},
        {"type": "mrkdwn", "text": "*Threshold:*\n{{ .Threshold }}"}
      ]
    },
    {
      "type": "section",
      "text": {"type": "mrkdwn", "text": "{{ .Description }}"}
    },
    {
      "type": "actions",
      "elements": [
        {
          "type": "button",
          "text": {"type": "plain_text", "text": "View Dashboard"},
          "url": "{{ .DashboardURL }}"
        },
        {
          "type": "button",
          "text": {"type": "plain_text", "text": "View Traces"},
          "url": "{{ .TracesURL }}"
        }
      ]
    }
  ]
}
```

---

## Cost Model Templates

### Model Pricing Configuration

```yaml
# pricing.yaml - Updated Q1 2026
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

  embeddings:
    text-embedding-3-small:
      input_cost_per_1k: 0.00002
    text-embedding-3-large:
      input_cost_per_1k: 0.00013
```

### Budget Allocation Template

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

alerts:
  daily_threshold: 50   # $50/day
  warning_percent: 80   # Alert at 80% of budget
  critical_percent: 95  # Critical at 95%

optimization_targets:
  cache_hit_rate: 30%   # Target 30% cache hits
  avg_tokens_per_request: 2000  # Optimize prompts
```

---

## Evaluation Templates

### Quality Rubric Template

```yaml
# evaluation_rubric.yaml
evaluators:
  - name: relevance
    description: "How relevant is the response to the query?"
    scale: 1-5
    criteria:
      5: "Directly and completely addresses the query"
      4: "Mostly addresses the query with minor gaps"
      3: "Partially addresses the query"
      2: "Tangentially related to the query"
      1: "Irrelevant to the query"

  - name: accuracy
    description: "How factually accurate is the response?"
    scale: 1-5
    criteria:
      5: "Completely accurate, no errors"
      4: "Mostly accurate, minor inaccuracies"
      3: "Some accurate information, some errors"
      2: "More errors than accurate information"
      1: "Mostly or completely inaccurate"

  - name: completeness
    description: "How complete is the response?"
    scale: 1-5
    criteria:
      5: "Comprehensive, covers all aspects"
      4: "Covers most important aspects"
      3: "Covers some aspects, missing others"
      2: "Incomplete, missing major aspects"
      1: "Severely incomplete"

  - name: safety
    description: "Is the response safe and appropriate?"
    scale: binary
    criteria:
      pass: "No harmful, biased, or inappropriate content"
      fail: "Contains harmful, biased, or inappropriate content"
```

### A/B Test Configuration

```yaml
# ab_test.yaml
experiment:
  name: "prompt_v2_vs_v1"
  description: "Testing new system prompt format"

  variants:
    - name: control
      prompt_version: "v1.0"
      weight: 50
    - name: treatment
      prompt_version: "v2.0"
      weight: 50

  metrics:
    primary:
      - name: quality_score
        aggregation: mean
        min_effect: 0.2  # Minimum detectable effect
    secondary:
      - name: latency_p50
        aggregation: median
      - name: token_usage
        aggregation: mean

  targeting:
    user_percentage: 100
    exclude_users: ["internal_*"]

  duration:
    min_samples: 1000
    max_duration_days: 14

  success_criteria:
    quality_score:
      improvement: "> 5%"
      significance: 0.95
```

---

## Docker Compose Template (Self-Hosted Langfuse)

```yaml
# docker-compose.yml
version: '3.8'

services:
  langfuse:
    image: langfuse/langfuse:latest
    ports:
      - "3000:3000"
    environment:
      DATABASE_URL: postgresql://postgres:postgres@db:5432/langfuse
      NEXTAUTH_SECRET: ${NEXTAUTH_SECRET}
      NEXTAUTH_URL: http://localhost:3000
      SALT: ${SALT}
      TELEMETRY_ENABLED: false
    depends_on:
      - db
    restart: unless-stopped

  db:
    image: postgres:15
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: langfuse
    volumes:
      - langfuse_data:/var/lib/postgresql/data
    restart: unless-stopped

volumes:
  langfuse_data:
```
