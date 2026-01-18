# M-DO-028: SLOs, SLIs, and Error Budgets

## Metadata
- **Category:** Development/DevOps
- **Difficulty:** Intermediate
- **Tags:** #devops, #sre, #slo, #sli, #reliability, #methodology
- **Agent:** faion-devops-agent

---

## Problem

"The system is reliable enough" is subjective. Teams don't know when to focus on features vs reliability. Outages cause finger-pointing, not learning.

## Promise

After this methodology, you will define and measure reliability objectively. Error budgets will guide decisions about velocity vs stability.

## Overview

SLIs measure service behavior, SLOs set targets, and error budgets quantify acceptable unreliability. This creates a shared language for reliability.

---

## Framework

### Step 1: Core Definitions

```
SLI (Service Level Indicator)
├── Quantitative measure of service behavior
├── Examples: latency, error rate, throughput
└── "What we measure"

SLO (Service Level Objective)
├── Target value for an SLI
├── Example: 99.9% requests < 200ms
└── "What we aim for"

SLA (Service Level Agreement)
├── Contract with consequences
├── Example: 99.9% uptime or credit
└── "What we promise externally"

Error Budget
├── 100% - SLO = allowed unreliability
├── Example: 0.1% errors allowed (99.9% SLO)
└── "How much failure is acceptable"
```

### Step 2: Common SLIs

```yaml
# Availability SLI
name: availability
description: Percentage of successful requests
formula: |
  (successful_requests / total_requests) * 100
good_event: status_code < 500
total_event: all requests

# Latency SLI
name: latency
description: Percentage of requests under threshold
formula: |
  (requests_under_threshold / total_requests) * 100
thresholds:
  - p50: 100ms
  - p95: 200ms
  - p99: 500ms

# Throughput SLI
name: throughput
description: Requests processed per second
formula: rate(requests_total[1m])
target: ">= 1000 rps"

# Freshness SLI (for data pipelines)
name: freshness
description: Age of data
formula: now() - last_updated_at
target: "< 5 minutes"

# Correctness SLI
name: correctness
description: Percentage of correct responses
formula: |
  (correct_responses / total_responses) * 100
```

### Step 3: Defining SLOs

```yaml
# SLO Document
service: api-service
owner: platform-team
last_reviewed: 2024-01-15

slos:
  - name: Availability
    sli: availability
    target: 99.9%
    window: 30 days
    consequences:
      - "If breached, freeze non-critical deploys"
      - "Allocate 50% of sprint to reliability"

  - name: Latency P95
    sli: latency_p95
    target: 99% of requests < 200ms
    window: 30 days

  - name: Latency P99
    sli: latency_p99
    target: 99% of requests < 500ms
    window: 30 days

error_budget:
  availability:
    monthly_budget: 43.2 minutes  # 30 days * 0.1%
    current_remaining: 38.5 minutes
    burn_rate: normal

  latency:
    monthly_budget: 1%
    current_remaining: 0.8%
    burn_rate: elevated
```

### Step 4: Prometheus SLO Metrics

```yaml
# Recording rules for SLIs
groups:
  - name: sli-recording
    rules:
      # Availability SLI
      - record: sli:availability:ratio
        expr: |
          sum(rate(http_requests_total{status!~"5.."}[5m]))
          /
          sum(rate(http_requests_total[5m]))

      # Latency SLI (P95 under 200ms)
      - record: sli:latency_p95:ratio
        expr: |
          histogram_quantile(0.95,
            sum(rate(http_request_duration_seconds_bucket[5m])) by (le)
          ) < 0.2

      # Error budget remaining (30 day window)
      - record: slo:availability:error_budget_remaining
        expr: |
          1 - (
            (1 - avg_over_time(sli:availability:ratio[30d]))
            /
            (1 - 0.999)
          )
```

### Step 5: Error Budget Alerts

```yaml
# Alert rules for SLO burn rate
groups:
  - name: slo-alerts
    rules:
      # Fast burn - exhausts 2% budget in 1 hour
      - alert: HighErrorBudgetBurn
        expr: |
          sli:availability:ratio < 0.99
        for: 5m
        labels:
          severity: critical
          slo: availability
        annotations:
          summary: "High error budget burn rate"
          description: "Burning error budget at >2% per hour"

      # Slow burn - exhausts budget before month end
      - alert: SlowErrorBudgetBurn
        expr: |
          predict_linear(slo:availability:error_budget_remaining[6h], 86400 * 7) < 0
        for: 30m
        labels:
          severity: warning
          slo: availability
        annotations:
          summary: "Error budget will be exhausted"
          description: "At current rate, budget exhausted in 7 days"

      # Budget exhausted
      - alert: ErrorBudgetExhausted
        expr: |
          slo:availability:error_budget_remaining < 0
        for: 5m
        labels:
          severity: critical
          slo: availability
        annotations:
          summary: "Error budget exhausted"
          description: "SLO breached, freeze deployments"
```

### Step 6: Error Budget Policy

```markdown
# Error Budget Policy

## Budget Status Actions

### Green (>50% remaining)
- Normal development velocity
- Feature work prioritized
- Experiments allowed

### Yellow (20-50% remaining)
- Increased monitoring
- Review recent changes
- Limit risky deployments

### Red (0-20% remaining)
- Reliability focus
- Feature freeze optional
- Post-mortems for all incidents

### Exhausted (<0%)
- Feature freeze mandatory
- All hands on reliability
- Daily SLO review meetings

## Budget Allocation

- 70% for planned work (deploys, experiments)
- 30% for unplanned work (incidents)

## Review Cadence

- Weekly: Check burn rate
- Monthly: Review SLO targets
- Quarterly: Adjust SLOs if needed
```

---

## Templates

### Grafana Dashboard

```json
{
  "title": "SLO Dashboard",
  "panels": [
    {
      "title": "Availability SLO",
      "type": "gauge",
      "targets": [
        {
          "expr": "sli:availability:ratio",
          "legendFormat": "Current"
        }
      ],
      "fieldConfig": {
        "defaults": {
          "thresholds": {
            "steps": [
              { "color": "red", "value": 0 },
              { "color": "yellow", "value": 0.99 },
              { "color": "green", "value": 0.999 }
            ]
          },
          "min": 0.99,
          "max": 1
        }
      }
    },
    {
      "title": "Error Budget Remaining",
      "type": "stat",
      "targets": [
        {
          "expr": "slo:availability:error_budget_remaining * 100",
          "legendFormat": "Remaining"
        }
      ],
      "fieldConfig": {
        "defaults": {
          "unit": "percent",
          "thresholds": {
            "steps": [
              { "color": "red", "value": 0 },
              { "color": "yellow", "value": 20 },
              { "color": "green", "value": 50 }
            ]
          }
        }
      }
    },
    {
      "title": "Budget Burn Rate (7 day projection)",
      "type": "timeseries",
      "targets": [
        {
          "expr": "predict_linear(slo:availability:error_budget_remaining[6h], 86400 * 7)",
          "legendFormat": "Projected"
        }
      ]
    }
  ]
}
```

### SLO Document Template

```markdown
# SLO: [Service Name]

## Service Description
Brief description of what the service does.

## SLIs

### Availability
- **Definition:** Successful requests / Total requests
- **Good event:** HTTP status < 500
- **Measurement:** Prometheus

### Latency
- **Definition:** Requests under threshold
- **Threshold:** P95 < 200ms
- **Measurement:** Prometheus histogram

## SLO Targets

| SLI | Target | Window | Error Budget |
|-----|--------|--------|--------------|
| Availability | 99.9% | 30 days | 43.2 min/month |
| Latency P95 | 99% | 30 days | 1% requests |

## Error Budget Policy

See central policy document.

## Stakeholders
- Owner: @team-lead
- On-call: platform-team
- Review: Monthly

## Review History
- 2024-01-15: Initial SLOs defined
- 2024-04-15: Adjusted latency target
```

---

## Common Mistakes

1. **Too many SLOs** - Start with 2-3 per service
2. **Unrealistic targets** - Base on historical data
3. **No consequences** - Policy must be enforced
4. **Set and forget** - Review quarterly
5. **Ignoring user impact** - SLOs should reflect UX

---

## Checklist

- [ ] SLIs defined for key user journeys
- [ ] SLO targets based on historical data
- [ ] Error budget calculated
- [ ] Alerts for budget burn rate
- [ ] Dashboard for visibility
- [ ] Policy document created
- [ ] Stakeholder buy-in
- [ ] Quarterly review scheduled

---

## Next Steps

- M-DO-011: Prometheus Monitoring
- M-DO-025: Incident Management
- M-DO-010: Infrastructure Patterns

---

*Methodology M-DO-028 v1.0*
