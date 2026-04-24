# FinOps Cloud Cost Optimization Templates

## 1. Cost Analysis Report Template

```markdown
# Cloud Cost Analysis Report

**Period:** [Month/Quarter YYYY]
**Prepared by:** [Name]
**Date:** [Date]

## Executive Summary

| Metric | Current | Previous | Change |
|--------|---------|----------|--------|
| Total Spend | $XXX,XXX | $XXX,XXX | +/-X% |
| Compute | $XX,XXX | $XX,XXX | +/-X% |
| Storage | $XX,XXX | $XX,XXX | +/-X% |
| Network | $XX,XXX | $XX,XXX | +/-X% |
| Database | $XX,XXX | $XX,XXX | +/-X% |

## Cost by Environment

| Environment | Spend | % of Total |
|-------------|-------|------------|
| Production | $XX,XXX | XX% |
| Staging | $X,XXX | XX% |
| Development | $X,XXX | XX% |
| Other | $X,XXX | XX% |

## Cost by Team

| Team | Spend | Trend | Notes |
|------|-------|-------|-------|
| [Team A] | $XX,XXX | [up/down/stable] | |
| [Team B] | $XX,XXX | [up/down/stable] | |

## Top Cost Drivers

1. **[Service/Resource]** - $X,XXX (+X% MoM)
   - Root cause: [explanation]
   - Action: [recommendation]

2. **[Service/Resource]** - $X,XXX (+X% MoM)
   - Root cause: [explanation]
   - Action: [recommendation]

## Optimization Opportunities

| Opportunity | Estimated Savings | Effort | Priority |
|-------------|-------------------|--------|----------|
| [Rightsizing] | $X,XXX/month | Low | High |
| [RI purchase] | $X,XXX/month | Medium | High |
| [Spot migration] | $X,XXX/month | Medium | Medium |

## Commitment Coverage

| Type | Coverage | Target | Gap |
|------|----------|--------|-----|
| Reserved Instances | XX% | 70% | XX% |
| Savings Plans | XX% | - | - |
| Spot Instances | XX% | 20% | XX% |

## Anomalies Detected

| Date | Service | Expected | Actual | Root Cause |
|------|---------|----------|--------|------------|
| [Date] | [Service] | $X,XXX | $X,XXX | [Cause] |

## Actions for Next Period

- [ ] [Action 1]
- [ ] [Action 2]
- [ ] [Action 3]
```

---

## 2. Rightsizing Recommendation Template

```markdown
# Rightsizing Recommendations

**Analysis Period:** [Start Date] - [End Date]
**Environment:** [Production/Staging/Dev]

## Summary

| Metric | Value |
|--------|-------|
| Instances Analyzed | XX |
| Instances Flagged | XX |
| Potential Savings | $X,XXX/month |

## Recommendations

### High Confidence (Safe to Implement)

| Instance ID | Current Type | Recommended | Avg CPU | Avg Memory | Monthly Savings |
|-------------|--------------|-------------|---------|------------|-----------------|
| i-xxx | m5.2xlarge | m5.xlarge | 12% | 25% | $XXX |
| i-yyy | r5.xlarge | r5.large | 18% | 32% | $XXX |

### Medium Confidence (Review Before Implementing)

| Instance ID | Current Type | Recommended | Avg CPU | Peak CPU | Monthly Savings |
|-------------|--------------|-------------|---------|----------|-----------------|
| i-zzz | c5.4xlarge | c5.2xlarge | 28% | 65% | $XXX |

### Architecture Changes Recommended

| Instance ID | Current Type | Issue | Recommendation |
|-------------|--------------|-------|----------------|
| i-aaa | m5.4xlarge | Memory bound | Consider r5 family |
| i-bbb | c5.xlarge | Network bound | Consider enhanced networking |

## Implementation Plan

**Phase 1 - Low Risk (Week 1-2)**
- [ ] Development environment instances
- [ ] Non-critical background workers

**Phase 2 - Medium Risk (Week 3-4)**
- [ ] Staging environment
- [ ] Production non-critical services

**Phase 3 - Production Critical (Week 5+)**
- [ ] Production APIs (with monitoring)
- [ ] Database instances (with approval)

## Rollback Plan

1. Monitor CloudWatch metrics for 24 hours post-change
2. Alert thresholds: CPU > 70%, Memory > 80%
3. Rollback procedure: [document steps]
4. Escalation contact: [name/team]
```

---

## 3. Reserved Instance Purchase Plan

```markdown
# Reserved Instance Purchase Plan

**Analysis Date:** [Date]
**Commitment Period:** [1 year / 3 years]
**Provider:** [AWS/GCP/Azure]

## Current State

| Metric | Value |
|--------|-------|
| Total On-Demand Spend | $XX,XXX/month |
| Current RI Coverage | XX% |
| Current RI Utilization | XX% |

## Usage Analysis

### Steady-State Workloads (24/7)

| Instance Type | Count | Avg Hours/Month | On-Demand Cost |
|---------------|-------|-----------------|----------------|
| m5.xlarge | XX | 720 | $X,XXX |
| c5.2xlarge | XX | 720 | $X,XXX |
| r5.large | XX | 720 | $X,XXX |

### Variable Workloads (Exclude from RI)

| Instance Type | Count | Pattern | Reason |
|---------------|-------|---------|--------|
| m5.2xlarge | XX | Business hours | Scheduled dev |
| c5.xlarge | XX | Batch jobs | Spot candidate |

## Purchase Recommendations

### Standard RIs (Maximum Savings)

| Instance Type | Quantity | Term | Payment | Monthly | Total Savings |
|---------------|----------|------|---------|---------|---------------|
| m5.xlarge | XX | 3-year | All Upfront | $XXX | $XX,XXX/year |
| c5.2xlarge | XX | 3-year | All Upfront | $XXX | $XX,XXX/year |

### Convertible RIs (Flexibility)

| Instance Type | Quantity | Term | Payment | Monthly | Total Savings |
|---------------|----------|------|---------|---------|---------------|
| r5.large | XX | 1-year | Partial Upfront | $XXX | $X,XXX/year |

## Financial Summary

| Metric | Value |
|--------|-------|
| Upfront Investment | $XX,XXX |
| Monthly Commitment | $X,XXX |
| Break-Even Point | X months |
| 1-Year Savings | $XX,XXX |
| 3-Year Savings | $XXX,XXX |

## Risk Mitigation

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| Workload decrease | Medium | Use Convertible RIs, sell on Marketplace |
| Instance family change | Low | Convertible RIs allow exchange |
| Provider migration | Low | Start with 1-year terms |

## Approval Required

- [ ] Engineering Lead
- [ ] Finance
- [ ] CTO/VP Engineering
```

---

## 4. Spot Instance Migration Plan

```markdown
# Spot Instance Migration Plan

**Workload:** [Name]
**Current Instance Type:** [Type]
**Target Savings:** XX%

## Workload Assessment

| Criteria | Status | Notes |
|----------|--------|-------|
| Fault Tolerant | Yes/No | |
| Stateless | Yes/No | |
| Can Checkpoint | Yes/No | |
| Auto-Scaling Enabled | Yes/No | |
| Interruption Handling | Yes/No | |

## Spot Fitness Score: [High/Medium/Low]

## Architecture Changes Required

### Checkpointing (if needed)
```yaml
checkpoint_config:
  interval: every X minutes/steps
  storage: s3://bucket/checkpoints/
  retention: X days
```

### Interruption Handling
```yaml
interruption_handler:
  type: [graceful_shutdown/checkpoint_and_exit]
  timeout: 120 seconds
  fallback: on-demand
```

## Instance Diversification

| Priority | Instance Type | vCPU | Memory | Spot Price |
|----------|---------------|------|--------|------------|
| 1 | c5.2xlarge | 8 | 16GB | $0.XX |
| 2 | c5a.2xlarge | 8 | 16GB | $0.XX |
| 3 | c6i.2xlarge | 8 | 16GB | $0.XX |
| 4 | m5.2xlarge | 8 | 32GB | $0.XX |

## Launch Template

```json
{
  "LaunchTemplateData": {
    "InstanceMarketOptions": {
      "MarketType": "spot",
      "SpotOptions": {
        "SpotInstanceType": "persistent",
        "InstanceInterruptionBehavior": "stop"
      }
    }
  }
}
```

## Testing Plan

| Phase | Environment | Duration | Success Criteria |
|-------|-------------|----------|------------------|
| 1 | Dev | 1 week | No data loss on interruption |
| 2 | Staging | 2 weeks | 95% job completion rate |
| 3 | Production | Gradual | Match on-demand reliability |

## Monitoring

| Metric | Alert Threshold |
|--------|-----------------|
| Interruption rate | > 10% |
| Job failure rate | > 5% |
| Fallback to on-demand | > 20% |
```

---

## 5. Cost Allocation Tagging Policy

```markdown
# Cost Allocation Tagging Policy

**Version:** 1.0
**Effective Date:** [Date]
**Owner:** [FinOps Team]

## Required Tags

| Tag Key | Description | Allowed Values | Example |
|---------|-------------|----------------|---------|
| Environment | Deployment environment | prod, staging, dev, sandbox | prod |
| Team | Owning team | [list teams] | platform |
| Service | Application/service name | [freeform] | payment-api |
| CostCenter | Finance cost center | CC-XXX format | CC-100 |
| Owner | Technical owner email | email format | dev@company.com |

## Optional Tags

| Tag Key | Description | When to Use |
|---------|-------------|-------------|
| Project | Project name | Time-bound projects |
| Compliance | Compliance requirement | PCI, HIPAA resources |
| DataClass | Data classification | Data-sensitive resources |

## Enforcement

### AWS Service Control Policy
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "RequireTags",
      "Effect": "Deny",
      "Action": [
        "ec2:RunInstances",
        "rds:CreateDBInstance"
      ],
      "Resource": "*",
      "Condition": {
        "Null": {
          "aws:RequestTag/Environment": "true",
          "aws:RequestTag/Team": "true",
          "aws:RequestTag/Service": "true"
        }
      }
    }
  ]
}
```

## Compliance Targets

| Metric | Target | Measurement |
|--------|--------|-------------|
| Required tag coverage | > 98% | Weekly audit |
| Untagged resources | < 5% | Monthly report |
| Invalid tag values | < 2% | Automated validation |

## Remediation Process

1. **Week 1:** Warning email to resource owner
2. **Week 2:** Escalation to team lead
3. **Week 3:** Escalation to engineering manager
4. **Week 4:** Resource terminated (non-prod) or exception required (prod)
```

---

## 6. Weekly Cost Review Agenda

```markdown
# Weekly FinOps Review

**Date:** [Date]
**Attendees:** [List]

## Agenda (30 min)

### 1. Cost Dashboard Review (5 min)
- [ ] Week-over-week change
- [ ] Month-to-date vs budget
- [ ] Forecast for month-end

### 2. Anomalies & Spikes (10 min)
| Service | Expected | Actual | Owner | Status |
|---------|----------|--------|-------|--------|
| | | | | |

### 3. Optimization Progress (10 min)
| Initiative | Status | Savings Realized |
|------------|--------|------------------|
| Rightsizing Phase 1 | | |
| Spot Migration | | |
| RI Purchase | | |

### 4. Action Items (5 min)
| Action | Owner | Due Date |
|--------|-------|----------|
| | | |

## Metrics Dashboard Links
- AWS Cost Explorer: [link]
- Team Dashboard: [link]
- RI Utilization: [link]
```

---

## 7. FinOps Maturity Assessment

```markdown
# FinOps Maturity Assessment

**Date:** [Date]
**Assessed by:** [Name]

## Scoring Guide
- **1 (Crawl):** Manual, ad-hoc, reactive
- **2 (Walk):** Documented, partially automated
- **3 (Run):** Fully automated, proactive, continuous

## Assessment

### Cost Visibility
| Capability | Score | Notes |
|------------|-------|-------|
| Tagging coverage | 1/2/3 | |
| Real-time dashboards | 1/2/3 | |
| Team-level attribution | 1/2/3 | |
| Anomaly detection | 1/2/3 | |

### Optimization
| Capability | Score | Notes |
|------------|-------|-------|
| Rightsizing | 1/2/3 | |
| Commitment management | 1/2/3 | |
| Waste elimination | 1/2/3 | |
| Spot adoption | 1/2/3 | |

### Governance
| Capability | Score | Notes |
|------------|-------|-------|
| Budget management | 1/2/3 | |
| Policy enforcement | 1/2/3 | |
| Chargeback/showback | 1/2/3 | |
| Executive reporting | 1/2/3 | |

### Culture
| Capability | Score | Notes |
|------------|-------|-------|
| Engineer awareness | 1/2/3 | |
| Cost in CI/CD | 1/2/3 | |
| Proactive optimization | 1/2/3 | |
| FinOps team | 1/2/3 | |

## Overall Score: XX/48

| Level | Score Range | Status |
|-------|-------------|--------|
| Crawl | 16-26 | |
| Walk | 27-37 | |
| Run | 38-48 | |

## Priority Improvements
1. [Highest impact improvement]
2. [Second priority]
3. [Third priority]
```

---

*Templates should be customized to your organization's specific needs and tools.*
