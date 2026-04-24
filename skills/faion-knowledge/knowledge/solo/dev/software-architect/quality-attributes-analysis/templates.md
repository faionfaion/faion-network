# Quality Attributes Analysis Templates

Copy-paste templates for quality attribute scenarios, utility trees, ATAM documentation, and NFR specifications.

---

## Quality Attribute Scenario Template

### Basic Scenario Format

```markdown
## Scenario: [ID] - [Short Name]

| Part | Value |
|------|-------|
| **Source** | [Who/what triggers the stimulus] |
| **Stimulus** | [The event or condition] |
| **Environment** | [Context: normal, overload, failure, attack] |
| **Artifact** | [System component affected] |
| **Response** | [Expected system behavior] |
| **Response Measure** | [Quantifiable success criteria] |

**Priority**: (Importance: H/M/L, Difficulty: H/M/E)
**Status**: Draft | Reviewed | Approved
**Owner**: [Name]
```

### Performance Scenario Template

```markdown
## PERF-[XXX]: [Performance Aspect]

| Part | Value |
|------|-------|
| **Source** | [User type / System component / External service] |
| **Stimulus** | [Action: request, query, process, etc.] |
| **Environment** | [Normal load / Peak load (Nx) / Degraded mode] |
| **Artifact** | [Service name, API endpoint, database] |
| **Response** | [Complete action, queue, reject, cache hit] |
| **Response Measure** | [Latency: p50/p95/p99 < Xms, Throughput: Y RPS] |

**Priority**: (H/M/L, H/M/E)
**Test Strategy**: [Load test, benchmark, synthetic monitoring]
**Current State**: [If known]
**Target State**: [Goal]
```

### Availability Scenario Template

```markdown
## AVAIL-[XXX]: [Availability Aspect]

| Part | Value |
|------|-------|
| **Source** | [Infrastructure / External dependency / Operator] |
| **Stimulus** | [Failure: crash, network partition, resource exhaustion] |
| **Environment** | [Peak hours / Off-peak / Maintenance window] |
| **Artifact** | [Service, region, data center] |
| **Response** | [Failover, degrade gracefully, queue, retry] |
| **Response Measure** | [Uptime: XX.XX%, MTTR: X min, RTO: X min, RPO: X min] |

**Priority**: (H/M/L, H/M/E)
**Redundancy**: [Active-active / Active-passive / None]
**Monitoring**: [Health checks, alerting threshold]
```

### Security Scenario Template

```markdown
## SEC-[XXX]: [Security Aspect]

| Part | Value |
|------|-------|
| **Source** | [Attacker / Insider / Automated scan] |
| **Stimulus** | [Attack: injection, brute force, data exfiltration] |
| **Environment** | [Public internet / Internal network / VPN] |
| **Artifact** | [Authentication, API, database, file storage] |
| **Response** | [Block, alert, log, rate limit, revoke access] |
| **Response Measure** | [Detection time, false positive rate, compliance %] |

**Priority**: (H/M/L, H/M/E)
**Threat Model Reference**: [Link to threat model]
**Compliance**: [GDPR, HIPAA, PCI-DSS, SOC2]
```

### Scalability Scenario Template

```markdown
## SCALE-[XXX]: [Scalability Aspect]

| Part | Value |
|------|-------|
| **Source** | [Growth event: campaign, viral, seasonal] |
| **Stimulus** | [Load increase: Nx current load] |
| **Environment** | [Capacity: current / max provisioned] |
| **Artifact** | [Stateless services / Database / Cache] |
| **Response** | [Auto-scale, queue, shed load, reject] |
| **Response Measure** | [Scale time, cost increase, latency during scaling] |

**Priority**: (H/M/L, H/M/E)
**Scaling Strategy**: [Horizontal / Vertical / Elastic]
**Bottleneck**: [Known limiting factor]
```

### Maintainability Scenario Template

```markdown
## MAINT-[XXX]: [Maintainability Aspect]

| Part | Value |
|------|-------|
| **Source** | [Developer / DevOps / External contributor] |
| **Stimulus** | [Change: feature, bugfix, config, dependency update] |
| **Environment** | [Development / Staging / Production] |
| **Artifact** | [Module, service, shared library] |
| **Response** | [Build, test, deploy, rollback] |
| **Response Measure** | [Deploy time, test coverage %, rollback time] |

**Priority**: (H/M/L, H/M/E)
**Deployment Frequency**: [Per day / Per week / Per month]
**Change Failure Rate**: [Target %]
```

---

## Utility Tree Templates

### Basic Utility Tree

```markdown
# Utility Tree: [System Name]

## Root: UTILITY (Overall System Value)

### 1. Performance
- 1.1 Latency
  - 1.1.1 API response time (H, M) - p99 < 200ms
  - 1.1.2 Page load time (M, L) - < 3s
- 1.2 Throughput
  - 1.2.1 Peak request handling (H, H) - 10K RPS
  - 1.2.2 Batch processing (M, M) - 1M records/hour

### 2. Availability
- 2.1 Uptime
  - 2.1.1 Core services (H, H) - 99.99%
  - 2.1.2 Non-critical features (M, L) - 99.9%
- 2.2 Recovery
  - 2.2.1 Failover time (H, M) - < 30s
  - 2.2.2 Data recovery (H, H) - RPO < 5 min

### 3. Security
- 3.1 Authentication
  - 3.1.1 Multi-factor auth (H, M) - Required for admin
  - 3.1.2 Session management (M, L) - 30 min timeout
- 3.2 Data Protection
  - 3.2.1 Encryption at rest (H, M) - AES-256
  - 3.2.2 Encryption in transit (H, L) - TLS 1.3

### 4. Scalability
- 4.1 Elastic Scaling
  - 4.1.1 Auto-scale on demand (H, H) - 10x in 5 min
- 4.2 Data Scaling
  - 4.2.1 Database sharding (M, H) - Support 10TB

### 5. Maintainability
- 5.1 Deployability
  - 5.1.1 Zero-downtime deploys (H, M) - Blue-green
- 5.2 Observability
  - 5.2.1 Distributed tracing (M, M) - All services

---

## Priority Legend
- Importance: (H)igh, (M)edium, (L)ow
- Difficulty: (H)ard, (M)edium, (E)asy
- Focus on (H, H) and (H, M) scenarios as architectural drivers
```

### Utility Tree as ASCII Diagram

```
                                    UTILITY
                                       │
           ┌───────────┬───────────┬───┴───┬───────────┬───────────┐
           │           │           │       │           │           │
      Performance  Availability  Security  Scalability  Maintainability
           │           │           │       │           │
     ┌─────┴─────┐     │     ┌─────┴─────┐ │     ┌─────┴─────┐
     │           │     │     │           │ │     │           │
  Latency   Throughput │   Auth      Data │ │  Deploy    Observe
     │           │     │     │           │ │     │           │
  ┌──┴──┐   ┌──┴──┐   │  ┌──┴──┐   ┌──┴──┐│  ┌──┴──┐   ┌──┴──┐
 API  Page Peak Batch  │ MFA  Session Encrypt│Zero  CI/CD Trace Log
(H,M) (M,L)(H,H)(M,M)  │(H,M) (M,L) (H,M)   │(H,M) (M,L)(M,M)(M,L)
                       │                    │
                 ┌─────┴─────┐        ┌─────┴─────┐
                 │           │        │           │
              Uptime     Recovery   Elastic    Data
                 │           │        │           │
            ┌────┴────┐ ┌────┴────┐   │      ┌────┴────┐
          Core   Non-crit Fail  DR   Auto   Shard   Archive
         (H,H)   (M,L)  (H,M)(H,H) (H,H)   (M,H)   (L,M)
```

---

## ATAM Documentation Templates

### ATAM Evaluation Report Template

```markdown
# ATAM Evaluation Report

**System**: [System Name]
**Version**: [Architecture Version]
**Date**: [Evaluation Date]
**Evaluation Team**: [Names]

---

## 1. Executive Summary

[Brief overview of findings, key risks, and recommendations]

### Key Findings
- [Finding 1]
- [Finding 2]
- [Finding 3]

### Risk Summary
| Severity | Count | Theme |
|----------|-------|-------|
| High | X | [Theme] |
| Medium | Y | [Theme] |
| Low | Z | [Theme] |

---

## 2. Business Drivers

### Primary Goals
1. [Business Goal 1]
2. [Business Goal 2]

### Constraints
- [Constraint 1]
- [Constraint 2]

### Key Stakeholders
| Stakeholder | Role | Quality Priorities |
|-------------|------|-------------------|
| [Name] | [Role] | [Attributes] |

---

## 3. Architecture Overview

### System Context
[High-level description]

### Key Architectural Decisions
| Decision | Rationale | Trade-offs |
|----------|-----------|------------|
| [Decision] | [Why] | [What's sacrificed] |

### Technology Stack
- [Component]: [Technology]

---

## 4. Utility Tree

[Include utility tree diagram or table]

### Architectural Drivers (High Priority)
| ID | Attribute | Scenario | Priority |
|----|-----------|----------|----------|
| AD-1 | [Attribute] | [Scenario] | (H, H) |

---

## 5. Scenario Analysis

### Scenario: [ID]
**Attribute**: [Quality Attribute]
**Priority**: [Importance, Difficulty]

**Scenario Description**:
[Full scenario with all 6 parts]

**Architectural Approach**:
[How architecture addresses this]

**Analysis**:
- Sensitivity Points: [List]
- Trade-off Points: [List]
- Risks: [List]
- Non-risks: [List]

---

## 6. Risks

### R-[XXX]: [Risk Title]
- **Description**: [Detailed description]
- **Quality Attributes Affected**: [List]
- **Business Impact**: [High/Medium/Low]
- **Likelihood**: [High/Medium/Low]
- **Mitigation**: [Recommended action]
- **Owner**: [Responsible party]

---

## 7. Sensitivity Points

| ID | Component | Parameter | Affected Attributes | Notes |
|----|-----------|-----------|---------------------|-------|
| SP-1 | [Component] | [Parameter] | [Attributes] | [Notes] |

---

## 8. Trade-off Points

| ID | Decision | Attributes in Tension | Current Balance | Notes |
|----|----------|----------------------|-----------------|-------|
| TP-1 | [Decision] | [Attr1 vs Attr2] | [Choice] | [Rationale] |

---

## 9. Risk Themes

### Theme 1: [Name]
**Description**: [Pattern description]
**Related Risks**: R-X, R-Y, R-Z
**Business Impact**: [Description]
**Recommendations**: [Actions]

---

## 10. Recommendations

### Immediate Actions (0-30 days)
1. [Action]

### Short-term (1-3 months)
1. [Action]

### Long-term (3-12 months)
1. [Action]

---

## Appendices

### A. Participants
| Name | Role | Organization |
|------|------|--------------|

### B. Documents Reviewed
- [Document]

### C. Glossary
| Term | Definition |
|------|------------|
```

### Risk Register Template

```markdown
# Risk Register

## Risks

| ID | Title | Description | Attributes | Likelihood | Impact | Priority | Status | Owner | Mitigation |
|----|-------|-------------|------------|------------|--------|----------|--------|-------|------------|
| R-001 | [Title] | [Description] | [Attrs] | H/M/L | H/M/L | [LxI] | Open | [Name] | [Action] |

## Risk Matrix

|            | Low Impact | Medium Impact | High Impact |
|------------|------------|---------------|-------------|
| **High**   | Medium     | High          | Critical    |
| **Medium** | Low        | Medium        | High        |
| **Low**    | Low        | Low           | Medium      |

## Risk Themes

| Theme | Related Risks | Overall Priority |
|-------|---------------|------------------|
| [Theme Name] | R-001, R-003 | High |
```

### Sensitivity Point Analysis Template

```markdown
# Sensitivity Point Analysis

## SP-[XXX]: [Component] - [Parameter]

### Description
[What this sensitivity point is]

### Parameter Details
- **Current Value**: [Value]
- **Range**: [Min - Max]
- **Default**: [Default value]

### Impact Analysis

| Change | Attribute | Impact |
|--------|-----------|--------|
| Increase by 10% | Performance | +15% throughput |
| Decrease by 10% | Performance | -20% throughput |
| Increase by 10% | Cost | +5% infra cost |

### Scenarios Affected
- [Scenario ID]: [How affected]

### Monitoring
- **Metric**: [Metric name]
- **Alert Threshold**: [Value]
- **Dashboard**: [Link]

### Recommendations
- [Recommendation]
```

### Trade-off Point Analysis Template

```markdown
# Trade-off Point Analysis

## TP-[XXX]: [Decision Name]

### Description
[What decision involves trade-offs]

### Attributes in Tension

| Attribute A | vs | Attribute B |
|-------------|:--:|-------------|
| [Attribute] | vs | [Attribute] |

### Options Analysis

| Option | Attr A Impact | Attr B Impact | Other Impacts |
|--------|---------------|---------------|---------------|
| Option 1 | Favors (+) | Sacrifices (-) | [Notes] |
| Option 2 | Neutral (=) | Neutral (=) | [Notes] |
| Option 3 | Sacrifices (-) | Favors (+) | [Notes] |

### Current Decision
**Chosen Option**: [Option X]

**Rationale**: [Why this option]

**Stakeholder Agreement**: [Who agreed]

### Consequences
- **Positive**: [Benefits]
- **Negative**: [Drawbacks]
- **Neutral**: [Unchanged aspects]

### Reversal Conditions
[When this decision should be revisited]
```

---

## NFR Specification Templates

### NFR Document Template

```markdown
# Non-Functional Requirements Specification

**Project**: [Project Name]
**Version**: [Version]
**Last Updated**: [Date]
**Author**: [Name]

---

## 1. Performance Requirements

### 1.1 Response Time
| Metric | Target | Measurement |
|--------|--------|-------------|
| API p50 latency | < 100ms | Continuous monitoring |
| API p99 latency | < 500ms | Continuous monitoring |
| Page load time | < 3s | Synthetic monitoring |

### 1.2 Throughput
| Metric | Target | Measurement |
|--------|--------|-------------|
| Peak requests/second | 10,000 RPS | Load testing |
| Concurrent users | 50,000 | Load testing |

### 1.3 Resource Utilization
| Resource | Normal | Peak | Alert |
|----------|--------|------|-------|
| CPU | < 50% | < 80% | > 85% |
| Memory | < 60% | < 85% | > 90% |
| Disk I/O | < 40% | < 70% | > 80% |

---

## 2. Availability Requirements

### 2.1 Uptime
| Service Tier | Target | Measurement Period |
|--------------|--------|-------------------|
| Tier 1 (Critical) | 99.99% | Monthly |
| Tier 2 (Important) | 99.9% | Monthly |
| Tier 3 (Standard) | 99% | Monthly |

### 2.2 Recovery
| Metric | Target |
|--------|--------|
| RTO (Recovery Time Objective) | 30 minutes |
| RPO (Recovery Point Objective) | 5 minutes |
| MTTR (Mean Time to Recovery) | 15 minutes |
| MTBF (Mean Time Between Failures) | 720 hours |

---

## 3. Security Requirements

### 3.1 Authentication
| Requirement | Specification |
|-------------|---------------|
| Protocol | OAuth 2.0 / OIDC |
| MFA | Required for admin, optional for users |
| Session timeout | 30 minutes inactive, 8 hours absolute |
| Password policy | 12+ chars, complexity requirements |

### 3.2 Data Protection
| Data Type | At Rest | In Transit | Retention |
|-----------|---------|------------|-----------|
| PII | AES-256 | TLS 1.3 | 7 years |
| Credentials | Argon2 hash | TLS 1.3 | Until changed |
| Logs | AES-256 | TLS 1.3 | 90 days |

---

## 4. Scalability Requirements

### 4.1 Capacity
| Dimension | Current | 1 Year | 3 Year |
|-----------|---------|--------|--------|
| Users | 100K | 500K | 2M |
| Data volume | 1TB | 10TB | 100TB |
| Requests/day | 10M | 50M | 200M |

### 4.2 Elasticity
| Trigger | Action | Time |
|---------|--------|------|
| CPU > 70% for 5 min | Scale out | < 2 min |
| CPU < 30% for 15 min | Scale in | < 5 min |
| Queue depth > 1000 | Scale workers | < 1 min |

---

## 5. Maintainability Requirements

### 5.1 Deployment
| Metric | Target |
|--------|--------|
| Deployment frequency | Daily |
| Lead time for changes | < 1 day |
| Change failure rate | < 5% |
| Rollback time | < 5 minutes |

### 5.2 Observability
| Capability | Requirement |
|------------|-------------|
| Logging | Structured, centralized, 90-day retention |
| Metrics | 15s resolution, 30-day retention |
| Tracing | Distributed, 100% sampling in dev, 10% in prod |
| Alerting | < 5 min detection, PagerDuty integration |

---

## 6. Compliance Requirements

| Standard | Scope | Audit Frequency |
|----------|-------|-----------------|
| SOC 2 Type II | All systems | Annual |
| GDPR | EU user data | Continuous |
| PCI-DSS | Payment processing | Annual |

---

## Appendix: Quality Attribute Scenarios

[Include key scenarios from utility tree]
```

### SLO Document Template

```markdown
# Service Level Objectives

**Service**: [Service Name]
**Version**: [Version]
**Owner**: [Team]

---

## SLIs (Service Level Indicators)

### Availability SLI
```
availability = (successful_requests / total_requests) * 100
```

### Latency SLI
```
latency_sli = (requests_under_threshold / total_requests) * 100
```

### Error Rate SLI
```
error_rate = (error_responses / total_responses) * 100
```

---

## SLOs (Service Level Objectives)

| SLI | SLO Target | Window | Current |
|-----|------------|--------|---------|
| Availability | 99.9% | 30 days | [Value] |
| Latency p99 | < 500ms | 30 days | [Value] |
| Error rate | < 0.1% | 30 days | [Value] |

---

## Error Budget

| SLO | Budget (30 days) | Consumed | Remaining |
|-----|------------------|----------|-----------|
| Availability (99.9%) | 43.2 min | [Value] | [Value] |
| Latency | 0.1% requests | [Value] | [Value] |

---

## Alerting Thresholds

| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Error budget 50% consumed | budget_remaining < 50% | Warning | Review |
| Error budget 75% consumed | budget_remaining < 25% | Critical | Freeze deploys |
| SLO breach | current < target | Critical | Incident |

---

## Escalation

| Level | Time | Contact |
|-------|------|---------|
| L1 | 0-15 min | On-call engineer |
| L2 | 15-30 min | Team lead |
| L3 | 30+ min | Engineering manager |
```

---

## Stakeholder Analysis Template

```markdown
# Stakeholder Analysis

## Stakeholder Registry

| ID | Name/Role | Organization | Interest Level | Influence | Quality Priorities |
|----|-----------|--------------|----------------|-----------|-------------------|
| S-1 | [Name] | [Org] | High/Medium/Low | High/Medium/Low | [Attributes] |

## Stakeholder-Attribute Matrix

| Stakeholder | Performance | Availability | Security | Scalability | Maintainability | Cost |
|-------------|:-----------:|:------------:|:--------:|:-----------:|:---------------:|:----:|
| End Users | 3 | 3 | 1 | 0 | 0 | 0 |
| Operations | 2 | 3 | 2 | 1 | 3 | 2 |
| Security | 0 | 2 | 3 | 0 | 1 | 0 |
| Business | 2 | 3 | 2 | 2 | 0 | 3 |
| Dev Team | 1 | 0 | 1 | 1 | 3 | 0 |

**Scale**: 0 = Not relevant, 1 = Nice to have, 2 = Important, 3 = Critical

## Conflict Resolution

| Conflict | Stakeholders | Resolution Strategy |
|----------|--------------|---------------------|
| [Description] | [S-1, S-2] | [How to resolve] |

## Communication Plan

| Stakeholder | Frequency | Format | Owner |
|-------------|-----------|--------|-------|
| [Stakeholder] | [Weekly] | [Status report] | [Name] |
```

---

## Quick Reference Card

```markdown
# QA Analysis Quick Reference

## Scenario Parts (6)
1. **Source** - Who/what triggers
2. **Stimulus** - What happens
3. **Environment** - Context
4. **Artifact** - What's affected
5. **Response** - System behavior
6. **Measure** - Success criteria

## Priority Notation
- **(H,H)** - High importance, Hard to achieve = Focus here
- **(H,M)** - High importance, Medium difficulty = Key driver
- **(M,H)** - Medium importance, Hard = Consider alternatives
- **(M,M)** - Medium importance, Medium difficulty = Standard
- Others - Lower priority

## Common Tactics
- **Performance**: Cache, async, pool, batch
- **Availability**: Replicate, failover, health check
- **Security**: Encrypt, authenticate, authorize, audit
- **Scalability**: Shard, stateless, queue, CDN
- **Maintainability**: Modularize, test, document, monitor

## Red Flags
- No quantified measures
- Missing failure scenarios
- Conflicting priorities unresolved
- Single points of failure
- No monitoring strategy
```
