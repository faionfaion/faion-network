# Database Selection Templates

Templates for documenting database decisions.

---

## Decision Matrix Template

### Weighted Scoring Matrix

```markdown
## Database Selection: [Project Name]

**Date:** YYYY-MM-DD
**Author:** [Name]
**Reviewers:** [Names]

### Candidates

| Option | Description |
|--------|-------------|
| Option A | [Database name and brief description] |
| Option B | [Database name and brief description] |
| Option C | [Database name and brief description] |

### Evaluation Criteria

| Criterion | Weight | Option A | Option B | Option C |
|-----------|--------|----------|----------|----------|
| Data model fit | 25% | 4/5 | 3/5 | 5/5 |
| Query performance | 20% | 4/5 | 5/5 | 3/5 |
| Scalability | 15% | 3/5 | 5/5 | 4/5 |
| Team expertise | 15% | 5/5 | 2/5 | 3/5 |
| Total cost (3yr) | 15% | 4/5 | 3/5 | 4/5 |
| Ecosystem/tooling | 10% | 5/5 | 4/5 | 4/5 |
| **Weighted Score** | 100% | **4.05** | **3.65** | **3.95** |

### Scoring Guide

- 5: Excellent - Exceeds requirements
- 4: Good - Meets all requirements
- 3: Acceptable - Meets most requirements
- 2: Poor - Significant gaps
- 1: Unacceptable - Does not meet requirements

### Decision

**Selected:** Option A ([Database Name])

**Rationale:**
[2-3 sentences explaining why this option was selected]

**Trade-offs Accepted:**
- [Trade-off 1]
- [Trade-off 2]

**Risks & Mitigations:**
| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| [Risk 1] | Medium | High | [Mitigation] |
| [Risk 2] | Low | Medium | [Mitigation] |
```

---

## Requirements Capture Template

```markdown
## Database Requirements: [Feature/System]

### Data Characteristics

| Attribute | Value |
|-----------|-------|
| Data model type | [Relational / Document / Graph / Time-series / Vector] |
| Current data volume | [X GB/TB] |
| 3-year projected volume | [X GB/TB] |
| Average record size | [X KB] |
| Schema stability | [Fixed / Evolves frequently] |

### Access Patterns

| Pattern | Frequency | Latency Requirement |
|---------|-----------|---------------------|
| Read single record | [X/sec] | [X ms] |
| Read range/list | [X/sec] | [X ms] |
| Write single record | [X/sec] | [X ms] |
| Bulk write | [X/min] | [X sec] |
| Complex query/aggregation | [X/min] | [X sec] |
| Full-text search | [X/sec] | [X ms] |

### Consistency Requirements

| Requirement | Value |
|-------------|-------|
| Transaction scope | [Single-row / Multi-row / Multi-table] |
| Consistency model | [Strong / Eventual / Configurable] |
| Durability requirement | [Sync / Async replication] |

### Availability Requirements

| Requirement | Value |
|-------------|-------|
| Uptime SLA | [99.9% / 99.99% / 99.999%] |
| RTO (Recovery Time Objective) | [X minutes/hours] |
| RPO (Recovery Point Objective) | [Zero / X minutes] |
| Multi-region required | [Yes / No] |

### Constraints

| Constraint | Details |
|------------|---------|
| Cloud provider | [AWS / GCP / Azure / Multi-cloud / On-prem] |
| Compliance | [GDPR / HIPAA / PCI-DSS / SOC2 / None] |
| Budget (monthly) | [$X - $Y] |
| Team expertise | [List known databases] |
```

---

## Architecture Decision Record (ADR) Template

```markdown
# ADR-XXX: Database Selection for [Component]

## Status

[Proposed | Accepted | Deprecated | Superseded by ADR-YYY]

## Context

[Describe the issue that motivates this decision]

We need to select a database for [component/feature] which requires:
- [Requirement 1]
- [Requirement 2]
- [Requirement 3]

### Current State

[Describe current situation, if applicable]

### Constraints

- [Constraint 1]
- [Constraint 2]

## Options Considered

### Option 1: [Database Name]

**Pros:**
- [Pro 1]
- [Pro 2]

**Cons:**
- [Con 1]
- [Con 2]

**Estimated Cost:** $X/month

### Option 2: [Database Name]

**Pros:**
- [Pro 1]
- [Pro 2]

**Cons:**
- [Con 1]
- [Con 2]

**Estimated Cost:** $X/month

### Option 3: [Database Name]

**Pros:**
- [Pro 1]
- [Pro 2]

**Cons:**
- [Con 1]
- [Con 2]

**Estimated Cost:** $X/month

## Decision

We will use **[Database Name]** because:
1. [Reason 1]
2. [Reason 2]
3. [Reason 3]

## Consequences

### Positive

- [Positive consequence 1]
- [Positive consequence 2]

### Negative

- [Negative consequence 1]
- [Negative consequence 2]

### Neutral

- [Neutral consequence 1]

## Implementation Notes

- [Note 1]
- [Note 2]

## References

- [Link 1]
- [Link 2]
```

---

## Cost Comparison Template

```markdown
## Database Cost Analysis: [Options]

### Assumptions

| Parameter | Value |
|-----------|-------|
| Data volume | X TB |
| Read requests/month | X million |
| Write requests/month | X million |
| Compute needs | X vCPUs, X GB RAM |
| Replication | [Single-AZ / Multi-AZ / Multi-region] |
| Environment count | [Prod + Staging + Dev] |

### 3-Year TCO Comparison

| Cost Category | Option A | Option B | Option C |
|---------------|----------|----------|----------|
| **Year 1** | | | |
| License/Subscription | $X | $X | $X |
| Infrastructure | $X | $X | $X |
| Data transfer | $X | $X | $X |
| Setup/Migration | $X | $X | $X |
| Training | $X | $X | $X |
| **Year 1 Total** | **$X** | **$X** | **$X** |
| | | | |
| **Year 2** | | | |
| License/Subscription | $X | $X | $X |
| Infrastructure | $X | $X | $X |
| Data transfer | $X | $X | $X |
| Operations | $X | $X | $X |
| **Year 2 Total** | **$X** | **$X** | **$X** |
| | | | |
| **Year 3** | | | |
| License/Subscription | $X | $X | $X |
| Infrastructure | $X | $X | $X |
| Data transfer | $X | $X | $X |
| Operations | $X | $X | $X |
| **Year 3 Total** | **$X** | **$X** | **$X** |
| | | | |
| **3-Year TCO** | **$X** | **$X** | **$X** |

### Cost Optimization Opportunities

| Option | Optimization | Potential Savings |
|--------|--------------|-------------------|
| Option A | Reserved instances | X% |
| Option A | Right-sizing | X% |
| Option B | Serverless tier | X% |
```

---

## Migration Plan Template

```markdown
## Database Migration Plan: [Source] to [Target]

### Overview

| Attribute | Value |
|-----------|-------|
| Source database | [Name, version] |
| Target database | [Name, version] |
| Data volume | [X TB] |
| Estimated downtime | [X minutes/hours] |
| Rollback window | [X hours/days] |

### Phase 1: Preparation

| Task | Owner | Duration | Status |
|------|-------|----------|--------|
| Schema mapping | [Name] | [X days] | [ ] |
| Data type conversion plan | [Name] | [X days] | [ ] |
| Application code changes | [Name] | [X days] | [ ] |
| Test environment setup | [Name] | [X days] | [ ] |

### Phase 2: Testing

| Task | Owner | Duration | Status |
|------|-------|----------|--------|
| Data migration test | [Name] | [X days] | [ ] |
| Application integration test | [Name] | [X days] | [ ] |
| Performance benchmarking | [Name] | [X days] | [ ] |
| Rollback procedure test | [Name] | [X days] | [ ] |

### Phase 3: Migration

| Step | Time | Action | Verification |
|------|------|--------|--------------|
| T-60min | [Time] | Notify stakeholders | [Check] |
| T-30min | [Time] | Stop write traffic | [Check] |
| T-15min | [Time] | Final data sync | [Check] |
| T-0 | [Time] | Switch application config | [Check] |
| T+5min | [Time] | Verify connectivity | [Check] |
| T+15min | [Time] | Run smoke tests | [Check] |
| T+30min | [Time] | Enable write traffic | [Check] |
| T+60min | [Time] | Monitor metrics | [Check] |

### Rollback Plan

| Trigger | Action |
|---------|--------|
| Migration fails before cutover | Retry or abort, no impact |
| Application errors after cutover | Revert config to source DB |
| Data corruption detected | Restore from backup |
| Performance degradation | Scale up or rollback |

### Success Criteria

- [ ] All data migrated with checksum verification
- [ ] Application response times within SLA
- [ ] No data loss or corruption
- [ ] All integrations functioning
- [ ] Monitoring and alerting operational
```

---

## PoC Evaluation Template

```markdown
## Database PoC Evaluation: [Database Name]

### Test Environment

| Parameter | Value |
|-----------|-------|
| Database version | [X.Y.Z] |
| Instance type | [e.g., db.r5.large] |
| Storage | [X GB, type] |
| Test data volume | [X GB / X million records] |
| Test duration | [X days] |

### Functional Evaluation

| Feature | Requirement | Result | Notes |
|---------|-------------|--------|-------|
| Schema support | [Requirement] | Pass/Fail | [Notes] |
| Query types | [Requirement] | Pass/Fail | [Notes] |
| Transactions | [Requirement] | Pass/Fail | [Notes] |
| Indexing | [Requirement] | Pass/Fail | [Notes] |
| Full-text search | [Requirement] | Pass/Fail | [Notes] |

### Performance Evaluation

| Metric | Target | Achieved | Notes |
|--------|--------|----------|-------|
| Read latency (p50) | [X ms] | [X ms] | [Notes] |
| Read latency (p99) | [X ms] | [X ms] | [Notes] |
| Write latency (p50) | [X ms] | [X ms] | [Notes] |
| Write latency (p99) | [X ms] | [X ms] | [Notes] |
| Read throughput | [X/sec] | [X/sec] | [Notes] |
| Write throughput | [X/sec] | [X/sec] | [Notes] |

### Operational Evaluation

| Aspect | Rating (1-5) | Notes |
|--------|--------------|-------|
| Setup complexity | [X] | [Notes] |
| Documentation quality | [X] | [Notes] |
| Monitoring/Metrics | [X] | [Notes] |
| Backup/Restore | [X] | [Notes] |
| Scaling ease | [X] | [Notes] |
| Troubleshooting | [X] | [Notes] |

### Issues Encountered

| Issue | Severity | Resolution | Impact on Decision |
|-------|----------|------------|-------------------|
| [Issue 1] | [High/Med/Low] | [Resolution] | [Impact] |
| [Issue 2] | [High/Med/Low] | [Resolution] | [Impact] |

### Recommendation

**Proceed:** Yes / No / With conditions

**Conditions (if applicable):**
- [Condition 1]
- [Condition 2]
```

---

## Related

- [README.md](README.md) - Database categories overview
- [checklist.md](checklist.md) - Selection checklist
- [examples.md](examples.md) - Real-world use cases
- [llm-prompts.md](llm-prompts.md) - AI-assisted selection
