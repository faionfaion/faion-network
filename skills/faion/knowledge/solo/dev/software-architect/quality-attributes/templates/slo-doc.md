# SLO Definition: {Service Name}

**Service:** {service-name}
**Owner:** {team-name}
**Review cycle:** monthly
**Last reviewed:** YYYY-MM-DD

---

## SLIs (What We Measure)

| SLI | Metric | Data Source |
|-----|--------|-------------|
| Availability | % of HTTP requests returning non-5xx | Prometheus `http_requests_total` |
| Latency | p99 response time of successful requests | Prometheus `http_request_duration_seconds` |
| Error rate | % of requests returning 5xx | Prometheus `http_requests_total{code=~"5.."}` |

---

## SLOs (Targets)

| SLO | Target | Window |
|-----|--------|--------|
| Availability | ≥ 99.9% | 30 days rolling |
| p99 Latency | ≤ 500ms | 30 days rolling |
| Error rate | ≤ 0.1% | 30 days rolling |

---

## Error Budget

| SLO | Monthly budget | Minutes of downtime allowed |
|-----|---------------|-----------------------------|
| Availability (99.9%) | 0.1% | 43.8 min/month |
| Error rate (0.1%) | 0.1% | 43.8 min/month |

**Budget consumption:** reviewed in weekly SRE sync.
**Action when budget is 50% consumed:** investigate and address root cause.
**Action when budget is exhausted:** feature freeze until budget is replenished.

---

## Alerting

| Alert | Condition | Severity |
|-------|-----------|----------|
| AvailabilityBurnHigh | Burn rate > 14x over 1h (budget exhausted in <2h) | PagerDuty — page on-call |
| AvailabilityBurnMedium | Burn rate > 6x over 6h (budget exhausted in <1d) | Slack #alerts — ticket |
| LatencyP99High | p99 > 500ms for 5 min | Slack #alerts — investigate |

---

## SLA (Customer Commitment)

**Contractual SLA:** 99.5% monthly uptime (more conservative than internal SLO)
**SLA breach threshold:** < 99.5% availability in any calendar month
**Customer remedies:** service credits per contract terms

---

## Notes

<!-- Architecture decisions that affect this SLO, dependencies, exclusions (e.g. planned maintenance windows excluded) -->
