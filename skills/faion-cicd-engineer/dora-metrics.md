---
id: dora-metrics
name: "DORA Metrics"
domain: OPS
skill: faion-devops-engineer
category: "best-practices-2026"
---

# DORA Metrics

DORA (DevOps Research and Assessment) metrics measure software delivery performance.

## Four Key Metrics

| Metric | Elite | High | Medium | Low |
|--------|-------|------|--------|-----|
| Deployment Frequency | Multiple/day | Weekly-monthly | Monthly-6mo | 6mo+ |
| Lead Time for Changes | <1 hour | 1 day-1 week | 1-6 months | 6mo+ |
| Change Failure Rate | 0-15% | 16-30% | 16-30% | 16-30% |
| Time to Restore Service | <1 hour | <1 day | 1 day-1 week | 1 week-1 month |

## Why It Matters

- Elite performers are 2x more likely to exceed organizational goals
- High-performing teams deploy 208x more frequently than low performers
- Elite teams have 106x faster lead times

## Implementation

**Deployment Frequency:**
```yaml
# Track via CI/CD pipeline
deployment_count:
  source: GitHub Actions/GitLab CI
  query: "count(deployments) / time_period"
  aggregation: daily, weekly, monthly
```

**Lead Time:**
```yaml
# Time from commit to production
lead_time:
  start: git_commit_timestamp
  end: deployment_timestamp
  query: "avg(deployment_time - commit_time)"
```

**Change Failure Rate:**
```yaml
# Failed deployments requiring hotfix/rollback
failure_rate:
  failed_deployments: rollback_count + hotfix_count
  total_deployments: all_deployments
  query: "failed / total * 100"
```

**MTTR (Time to Restore):**
```yaml
# Incident creation to resolution
mttr:
  start: incident_detected_timestamp
  end: incident_resolved_timestamp
  query: "avg(resolved_time - detected_time)"
```

## Monitoring Tools

| Tool | Integration |
|------|-------------|
| Sleuth | GitHub, GitLab, Jira, PagerDuty |
| Haystack | CI/CD pipelines, incident mgmt |
| LinearB | Git, Jira, CI/CD, incidents |
| Jellyfish | Multi-platform aggregation |
| Swarmia | Engineering analytics |

## Dashboard Example

```yaml
dashboards:
  grafana:
    - deployment_frequency_chart
    - lead_time_histogram
    - change_failure_rate_gauge
    - mttr_trend_line

  queries:
    - source: prometheus
    - source: loki (logs)
    - source: github_api
    - source: pagerduty_api
```

## 2026 Evolution

- AI-driven insights: predict bottlenecks before they impact metrics
- Automated correlation: link metrics to code changes/team changes
- Business outcome mapping: tie DORA metrics to revenue/user satisfaction

## Best Practices

1. Start with baseline measurement (no targets initially)
2. Focus on trends over absolute numbers
3. Use metrics for improvement, not punishment
4. Automate data collection
5. Review metrics weekly with team

## Sources

- [DORA State of DevOps Report 2024](https://dora.dev/research/)
- [Google Cloud DORA Metrics Guide](https://cloud.google.com/blog/products/devops-sre/using-the-four-keys-to-measure-your-devops-performance)
- [Four Keys Project (GitHub)](https://github.com/GoogleCloudPlatform/fourkeys)
- [Sleuth DORA Metrics](https://www.sleuth.io/dora-metrics)
- [Accelerate (Book by Dr. Nicole Forsgren)](https://itrevolution.com/product/accelerate/)
