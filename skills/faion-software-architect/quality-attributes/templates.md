# Quality Attributes Templates

Copy-paste templates for documenting quality requirements, SLOs, and NFRs.

---

## Quality Attribute Scenario Template

Use the 6-part SEI format for every quality requirement.

### Basic Template

```markdown
## QA-{ID}: {Quality Attribute} - {Short Description}

**Source:** {Who/what generates the stimulus}
**Stimulus:** {The event or condition}
**Environment:** {System state when stimulus occurs}
**Artifact:** {Component being stimulated}
**Response:** {What the system does}
**Response Measure:** {How to verify the response}

### Context
{Why this scenario matters}

### Acceptance Criteria
- [ ] {Measurable criterion 1}
- [ ] {Measurable criterion 2}

### Architectural Tactics
- {Tactic 1}
- {Tactic 2}
```

### Filled Example

```markdown
## QA-001: Performance - Product Search Latency

**Source:** End user
**Stimulus:** Submits product search with filters
**Environment:** Normal operations (50K concurrent users)
**Artifact:** Product Search API
**Response:** Returns paginated product list
**Response Measure:** p95 latency < 300ms, p99 < 1s

### Context
Fast search is critical for conversion. Users abandon after 3 seconds.

### Acceptance Criteria
- [ ] p95 latency < 300ms under normal load
- [ ] p99 latency < 1s under peak load
- [ ] Zero timeouts under normal load

### Architectural Tactics
- Elasticsearch for full-text search
- Redis caching for popular queries (1h TTL)
- Query result pagination (max 100 items)
```

---

## NFR Specification Template

### Document Header

```markdown
# Non-Functional Requirements Specification

**Project:** {Project Name}
**Version:** {1.0}
**Last Updated:** {YYYY-MM-DD}
**Author:** {Name}
**Status:** {Draft | Review | Approved}

## Document History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | YYYY-MM-DD | Name | Initial draft |

## Stakeholder Sign-off

| Stakeholder | Role | Date | Signature |
|-------------|------|------|-----------|
| | | | |
```

### Performance Requirements Section

```markdown
## Performance Requirements

### PERF-001: API Response Time

| Parameter | Value |
|-----------|-------|
| **Requirement ID** | PERF-001 |
| **Category** | Performance |
| **Priority** | Critical |
| **Description** | API endpoints must respond within acceptable time |

| Metric | Target | Threshold | Measurement |
|--------|--------|-----------|-------------|
| Latency p50 | < 100ms | < 150ms | Prometheus |
| Latency p95 | < 300ms | < 500ms | Prometheus |
| Latency p99 | < 1s | < 2s | Prometheus |

**Conditions:**
- Under normal load (1,000 RPS)
- Under peak load (5,000 RPS)

**Verification Method:** Load testing with k6

**Related FRs:** FR-001, FR-002, FR-003
```

### Scalability Requirements Section

```markdown
## Scalability Requirements

### SCALE-001: Horizontal Scaling

| Parameter | Value |
|-----------|-------|
| **Requirement ID** | SCALE-001 |
| **Category** | Scalability |
| **Priority** | High |
| **Description** | System must scale horizontally to handle growth |

| Metric | Current | 6 Months | 1 Year |
|--------|---------|----------|--------|
| Concurrent Users | 10K | 30K | 100K |
| Requests/second | 1K | 3K | 10K |
| Data Volume | 100GB | 300GB | 1TB |

**Constraints:**
- Linear cost increase (not exponential)
- No architecture changes required
- Auto-scaling response < 5 minutes

**Verification Method:** Load testing at projected scale
```

### Availability Requirements Section

```markdown
## Availability Requirements

### AVAIL-001: System Uptime

| Parameter | Value |
|-----------|-------|
| **Requirement ID** | AVAIL-001 |
| **Category** | Availability |
| **Priority** | Critical |
| **Description** | System must maintain high availability |

| Component | SLA Target | Downtime/Month |
|-----------|------------|----------------|
| Core API | 99.9% | 43.8 minutes |
| Database | 99.95% | 21.9 minutes |
| CDN | 99.99% | 4.3 minutes |

**Maintenance Windows:**
- Planned: Sundays 02:00-04:00 UTC
- Emergency: Anytime with 30-min notice

**Recovery Objectives:**
- RTO: 15 minutes
- RPO: 1 minute

**Verification Method:** Uptime monitoring (Datadog)
```

### Security Requirements Section

```markdown
## Security Requirements

### SEC-001: Authentication

| Parameter | Value |
|-----------|-------|
| **Requirement ID** | SEC-001 |
| **Category** | Security |
| **Priority** | Critical |
| **Description** | Secure user authentication |

| Control | Requirement |
|---------|-------------|
| Protocol | OAuth 2.0 with PKCE |
| MFA | Required for admin, optional for users |
| Session | 15-minute idle timeout |
| Password | Min 12 chars, complexity enforced |
| Lockout | 5 failed attempts, 15-min lockout |

**Compliance:** SOC 2 Type II, GDPR

**Verification Method:** Security audit, penetration testing

### SEC-002: Data Protection

| Parameter | Value |
|-----------|-------|
| **Requirement ID** | SEC-002 |
| **Category** | Security |
| **Priority** | Critical |
| **Description** | Protect sensitive data |

| Data Type | At Rest | In Transit |
|-----------|---------|------------|
| PII | AES-256 | TLS 1.3 |
| Credentials | Argon2id hash | TLS 1.3 |
| Logs | AES-256 | TLS 1.3 |

**Key Management:**
- AWS KMS for key storage
- 90-day key rotation
- Separate keys per environment
```

---

## SLO Document Template

```markdown
# Service Level Objectives

**Service:** {Service Name}
**Version:** {1.0}
**Effective Date:** {YYYY-MM-DD}
**Review Cadence:** Quarterly

## SLO Summary

| SLI | SLO Target | Error Budget |
|-----|------------|--------------|
| Availability | 99.9% | 0.1% (43.8 min/month) |
| Latency p95 | < 200ms | 0.5% above threshold |
| Error Rate | < 0.1% | 0.1% (43.8 min/month) |

## Detailed SLOs

### SLO-001: Availability

**Definition:**
Percentage of successful HTTP requests (non-5xx) over total requests.

**Target:** 99.9% over rolling 30-day window

**Measurement:**
```promql
sum(rate(http_requests_total{status!~"5.."}[30d])) /
sum(rate(http_requests_total[30d]))
```

**Error Budget:**
- Monthly: 43.8 minutes
- Burn rate alert: > 2x hourly

**Exclusions:**
- Planned maintenance (announced 48h in advance)
- Requests from blocked IPs

### SLO-002: Latency

**Definition:**
95th percentile of request duration for successful requests.

**Target:** p95 < 200ms for 99.5% of time windows

**Measurement:**
```promql
histogram_quantile(0.95,
  sum(rate(http_request_duration_seconds_bucket{status!~"5.."}[5m]))
  by (le)
)
```

**Error Budget:**
- Monthly: 3.65 hours above threshold

### SLO-003: Error Rate

**Definition:**
Percentage of 5xx responses over total responses.

**Target:** < 0.1% over rolling 30-day window

**Measurement:**
```promql
sum(rate(http_requests_total{status=~"5.."}[30d])) /
sum(rate(http_requests_total[30d]))
```

## Error Budget Policy

| Budget Remaining | Action |
|------------------|--------|
| > 50% | Normal development |
| 25-50% | Increased testing, slower rollouts |
| 10-25% | Feature freeze, focus on reliability |
| < 10% | Incident mode, all hands on reliability |

## Review Schedule

- **Weekly:** Error budget consumption review
- **Monthly:** SLO target review
- **Quarterly:** SLI/SLO definition review
```

---

## Utility Tree Template

For Architecture Tradeoff Analysis Method (ATAM).

```markdown
# Quality Attribute Utility Tree

**System:** {System Name}
**Date:** {YYYY-MM-DD}
**Participants:** {Names}

## Utility Tree

| Quality Attribute | Refinement | Scenario | Business (H/M/L) | Technical (H/M/L) |
|-------------------|------------|----------|------------------|-------------------|
| **Performance** | Latency | Search returns < 300ms at p95 | H | M |
| | | Page load < 2s on 3G | H | H |
| | Throughput | Handle 10K RPS at peak | M | H |
| **Availability** | Uptime | 99.9% monthly availability | H | M |
| | Recovery | Failover < 30 seconds | H | H |
| **Security** | Authentication | MFA for all admin access | H | L |
| | Data Protection | PII encrypted at rest | H | L |
| **Scalability** | Growth | Support 10x user growth | M | H |
| | Elasticity | Auto-scale within 5 min | M | M |
| **Maintainability** | Deployment | Daily deployments possible | M | L |
| | Modularity | Independent service deployment | M | M |

## Priority Scenarios (H,H)

1. **Page load < 2s on 3G** (Performance)
   - Critical for mobile users (60% of traffic)
   - Requires CDN, image optimization, code splitting

2. **Failover < 30 seconds** (Availability)
   - Business continuity requirement
   - Requires active-passive or active-active

## Trade-off Points Identified

| Trade-off | Decision | Rationale |
|-----------|----------|-----------|
| Consistency vs Latency | Eventual consistency | p95 latency more critical |
| Security vs UX | Risk-based auth | MFA only for sensitive operations |
```

---

## ADR Template for Quality Decisions

```markdown
# ADR-{NUMBER}: {Title}

**Status:** {Proposed | Accepted | Deprecated | Superseded}
**Date:** {YYYY-MM-DD}
**Decision Makers:** {Names}

## Context

{What is the issue that we're addressing? What quality attribute is involved?}

## Quality Attributes Affected

| Attribute | Impact | Direction |
|-----------|--------|-----------|
| Performance | High | Positive |
| Security | Medium | Negative |
| Cost | Low | Neutral |

## Decision

{What is the change that we're proposing/making?}

## Options Considered

### Option 1: {Name}
- **Pros:** {List}
- **Cons:** {List}
- **Quality Impact:** {Assessment}

### Option 2: {Name}
- **Pros:** {List}
- **Cons:** {List}
- **Quality Impact:** {Assessment}

## Consequences

### Positive
- {Positive consequence 1}

### Negative
- {Negative consequence 1}

### Risks
- {Risk 1}: {Mitigation}

## Metrics to Monitor

| Metric | Before | Expected After | Alert Threshold |
|--------|--------|----------------|-----------------|
| Latency p95 | 500ms | 200ms | > 300ms |

## Related Decisions

- ADR-{XX}: {Related decision}
```

---

## Quality Requirements Traceability Matrix

```markdown
# Quality Requirements Traceability Matrix

**Project:** {Name}
**Version:** {1.0}

| QA ID | Description | Architectural Decision | Implementation | Test | Status |
|-------|-------------|------------------------|----------------|------|--------|
| QA-001 | p95 < 300ms | Caching layer (ADR-05) | Redis cache | PERF-01 | Done |
| QA-002 | 99.9% uptime | Multi-AZ (ADR-03) | AWS deployment | AVAIL-01 | Done |
| QA-003 | MFA required | OAuth + TOTP (ADR-08) | Auth service | SEC-01 | In Progress |
| QA-004 | Auto-scale | K8s HPA (ADR-12) | HPA config | SCALE-01 | Planned |
```

---

## Quality Attribute Workshop Agenda

```markdown
# Quality Attribute Workshop

**Date:** {YYYY-MM-DD}
**Duration:** 4 hours
**Facilitator:** {Name}

## Attendees

| Name | Role | Quality Focus |
|------|------|---------------|
| | Architect | Overall |
| | Product | Business impact |
| | Security | Security |
| | Ops | Availability, Performance |

## Agenda

| Time | Activity | Output |
|------|----------|--------|
| 0:00-0:15 | Introduction, goals | Shared understanding |
| 0:15-0:45 | Business drivers review | Priority list |
| 0:45-1:30 | Scenario brainstorming | Raw scenarios |
| 1:30-1:45 | Break | |
| 1:45-2:30 | Scenario prioritization | Utility tree |
| 2:30-3:15 | Trade-off discussion | Trade-off points |
| 3:15-3:45 | Architectural approach mapping | Tactics list |
| 3:45-4:00 | Next steps, actions | Action items |

## Preparation Required

- [ ] Architecture overview document
- [ ] Business requirements document
- [ ] Existing NFR documentation
- [ ] Performance/incident reports
```

---

## Prometheus Alert Templates

```yaml
# Quality Attribute Alerts

groups:
  - name: quality_attributes
    rules:
      # Availability SLO
      - alert: HighErrorRate
        expr: |
          sum(rate(http_requests_total{status=~"5.."}[5m])) /
          sum(rate(http_requests_total[5m])) > 0.001
        for: 5m
        labels:
          severity: critical
          quality_attribute: availability
        annotations:
          summary: "Error rate above SLO threshold"
          description: "Error rate is {{ $value | humanizePercentage }}"

      # Performance SLO
      - alert: HighLatency
        expr: |
          histogram_quantile(0.95,
            sum(rate(http_request_duration_seconds_bucket[5m])) by (le)
          ) > 0.3
        for: 5m
        labels:
          severity: warning
          quality_attribute: performance
        annotations:
          summary: "p95 latency above 300ms"
          description: "Current p95: {{ $value | humanizeDuration }}"

      # Error Budget Burn Rate
      - alert: ErrorBudgetBurn
        expr: |
          (
            1 - (
              sum(rate(http_requests_total{status!~"5.."}[1h])) /
              sum(rate(http_requests_total[1h]))
            )
          ) / (1 - 0.999) > 2
        for: 15m
        labels:
          severity: warning
          quality_attribute: availability
        annotations:
          summary: "Error budget burning too fast"
          description: "Burn rate: {{ $value }}x"
```

---

## Grafana Dashboard JSON Snippet

```json
{
  "title": "Quality Attributes Overview",
  "panels": [
    {
      "title": "Availability (30d)",
      "type": "stat",
      "targets": [
        {
          "expr": "sum(rate(http_requests_total{status!~\"5..\"}[30d])) / sum(rate(http_requests_total[30d])) * 100",
          "legendFormat": "Availability %"
        }
      ],
      "fieldConfig": {
        "defaults": {
          "thresholds": {
            "steps": [
              {"value": 99, "color": "red"},
              {"value": 99.9, "color": "yellow"},
              {"value": 99.95, "color": "green"}
            ]
          },
          "unit": "percent"
        }
      }
    },
    {
      "title": "Latency p95",
      "type": "timeseries",
      "targets": [
        {
          "expr": "histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))",
          "legendFormat": "p95"
        },
        {
          "expr": "0.3",
          "legendFormat": "SLO Target"
        }
      ]
    },
    {
      "title": "Error Budget Remaining",
      "type": "gauge",
      "targets": [
        {
          "expr": "(1 - (1 - sum(rate(http_requests_total{status!~\"5..\"}[30d])) / sum(rate(http_requests_total[30d]))) / 0.001) * 100"
        }
      ],
      "fieldConfig": {
        "defaults": {
          "min": 0,
          "max": 100,
          "thresholds": {
            "steps": [
              {"value": 0, "color": "red"},
              {"value": 25, "color": "orange"},
              {"value": 50, "color": "yellow"},
              {"value": 75, "color": "green"}
            ]
          },
          "unit": "percent"
        }
      }
    }
  ]
}
```

---

## k6 Load Test Template

```javascript
// quality-attribute-test.js
import http from 'k6/http';
import { check, sleep } from 'k6';
import { Rate, Trend } from 'k6/metrics';

// Custom metrics for quality attributes
const errorRate = new Rate('errors');
const latencyP95 = new Trend('latency_p95', true);

// Test configuration matching SLOs
export const options = {
  stages: [
    { duration: '2m', target: 100 },   // Ramp up
    { duration: '5m', target: 100 },   // Steady state
    { duration: '2m', target: 500 },   // Peak load
    { duration: '5m', target: 500 },   // Sustained peak
    { duration: '2m', target: 0 },     // Ramp down
  ],
  thresholds: {
    // Performance SLOs
    http_req_duration: ['p(95)<300', 'p(99)<1000'],
    // Availability SLO
    errors: ['rate<0.001'],
    // Custom thresholds
    latency_p95: ['p(95)<300'],
  },
};

export default function () {
  const res = http.get('https://api.example.com/products/search?q=test');

  // Track quality metrics
  errorRate.add(res.status >= 500);
  latencyP95.add(res.timings.duration);

  // Validate response
  check(res, {
    'status is 200': (r) => r.status === 200,
    'response time < 300ms': (r) => r.timings.duration < 300,
    'has results': (r) => JSON.parse(r.body).results.length > 0,
  });

  sleep(1);
}
```

---

*Part of [quality-attributes](README.md) | [faion-software-architect](../CLAUDE.md)*
