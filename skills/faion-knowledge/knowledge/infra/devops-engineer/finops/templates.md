# FinOps Templates

Reusable templates for cloud cost optimization implementation.

## Template 1: Tagging Policy

```yaml
# Mandatory Tags Schema
tags:
  mandatory:
    - key: Environment
      allowed_values:
        - production
        - staging
        - development
        - test
        - sandbox
      description: Deployment environment

    - key: Owner
      format: "email"
      description: Team or individual responsible

    - key: Project
      format: "alphanumeric-dash"
      description: Project or application name

    - key: CostCenter
      format: "CC-[0-9]{4}"
      description: Finance cost center code

  recommended:
    - key: Team
      description: Owning team name

    - key: Component
      description: Application component

    - key: DataClassification
      allowed_values:
        - public
        - internal
        - confidential
        - restricted
      description: Data sensitivity level

  automation:
    - key: AutoShutdown
      allowed_values:
        - "true"
        - "false"
      description: Enable automatic shutdown

    - key: BackupSchedule
      allowed_values:
        - daily
        - weekly
        - none
      description: Backup frequency
```

---

## Template 2: Cost Allocation Report

```markdown
# Monthly Cloud Cost Report

**Period:** [MONTH YEAR]
**Report Date:** [DATE]

## Executive Summary

| Metric | This Month | Last Month | Trend |
|--------|------------|------------|-------|
| Total Spend | $XXX,XXX | $XXX,XXX | +X% |
| Budget | $XXX,XXX | - | - |
| Variance | $X,XXX | - | - |
| Waste Identified | $X,XXX | $X,XXX | -X% |
| Savings Achieved | $X,XXX | $X,XXX | +X% |

## Cost by Environment

| Environment | Spend | % of Total |
|-------------|-------|------------|
| Production | $XXX,XXX | XX% |
| Staging | $XX,XXX | XX% |
| Development | $XX,XXX | XX% |
| Test | $X,XXX | XX% |
| Untagged | $X,XXX | XX% |

## Cost by Team

| Team | Budget | Actual | Variance | Status |
|------|--------|--------|----------|--------|
| Team A | $XX,XXX | $XX,XXX | +$X,XXX | Over |
| Team B | $XX,XXX | $XX,XXX | -$X,XXX | Under |
| Team C | $XX,XXX | $XX,XXX | $0 | On Track |

## Top Cost Drivers

| Resource | Cost | Change | Owner |
|----------|------|--------|-------|
| [Resource 1] | $X,XXX | +XX% | Team A |
| [Resource 2] | $X,XXX | +XX% | Team B |
| [Resource 3] | $X,XXX | -XX% | Team C |

## Optimization Opportunities

| Recommendation | Potential Savings | Effort | Priority |
|----------------|-------------------|--------|----------|
| Rightsize EC2 instances | $X,XXX/mo | Low | High |
| Purchase Savings Plans | $X,XXX/mo | Medium | High |
| Delete idle resources | $X,XXX/mo | Low | Medium |

## Action Items

- [ ] [Action 1] - Owner: [Name] - Due: [Date]
- [ ] [Action 2] - Owner: [Name] - Due: [Date]
- [ ] [Action 3] - Owner: [Name] - Due: [Date]

## Appendix: Detailed Breakdown

[Attach detailed CSV/Excel export]
```

---

## Template 3: Budget Configuration

```terraform
# Terraform AWS Budget Template
resource "aws_budgets_budget" "team_budget" {
  name              = "${var.team_name}-monthly-budget"
  budget_type       = "COST"
  limit_amount      = var.monthly_limit
  limit_unit        = "USD"
  time_unit         = "MONTHLY"
  time_period_start = "2025-01-01_00:00"

  cost_filter {
    name   = "TagKeyValue"
    values = ["user:team$${var.team_name}"]
  }

  notification {
    comparison_operator        = "GREATER_THAN"
    threshold                  = 50
    threshold_type             = "PERCENTAGE"
    notification_type          = "ACTUAL"
    subscriber_email_addresses = [var.team_email]
  }

  notification {
    comparison_operator        = "GREATER_THAN"
    threshold                  = 80
    threshold_type             = "PERCENTAGE"
    notification_type          = "ACTUAL"
    subscriber_email_addresses = [var.team_email, var.finops_email]
  }

  notification {
    comparison_operator        = "GREATER_THAN"
    threshold                  = 100
    threshold_type             = "PERCENTAGE"
    notification_type          = "ACTUAL"
    subscriber_email_addresses = [var.team_email, var.finops_email, var.finance_email]
  }

  notification {
    comparison_operator        = "GREATER_THAN"
    threshold                  = 100
    threshold_type             = "PERCENTAGE"
    notification_type          = "FORECASTED"
    subscriber_email_addresses = [var.finops_email]
  }
}

variable "team_name" {
  description = "Team identifier"
  type        = string
}

variable "monthly_limit" {
  description = "Monthly budget limit in USD"
  type        = number
}

variable "team_email" {
  description = "Team notification email"
  type        = string
}

variable "finops_email" {
  description = "FinOps team email"
  type        = string
  default     = "finops@company.com"
}

variable "finance_email" {
  description = "Finance team email"
  type        = string
  default     = "finance@company.com"
}
```

---

## Template 4: Savings Plan Analysis

```markdown
# Savings Plan Analysis

**Analysis Date:** [DATE]
**Analysis Period:** [START_DATE] to [END_DATE]

## Current State

| Metric | Value |
|--------|-------|
| Total Compute Spend | $XXX,XXX/month |
| On-Demand Spend | $XXX,XXX (XX%) |
| Existing Commitments | $XX,XXX (XX%) |
| Spot/Preemptible | $X,XXX (XX%) |

## Usage Pattern Analysis

### Baseline Usage (Steady State)

| Service | Average Usage | Hourly Cost |
|---------|--------------|-------------|
| EC2 | XXX instances | $XXX |
| Fargate | XXX vCPU | $XXX |
| Lambda | XXX GB-seconds | $XXX |

### Variable Usage

| Time Period | Usage Pattern | % of Total |
|-------------|---------------|------------|
| Business hours | Peak | XX% |
| Nights/weekends | Trough | XX% |
| Monthly spikes | Variable | XX% |

## Recommendation

### Compute Savings Plan

| Term | Payment | Commitment | Discount | Annual Savings |
|------|---------|------------|----------|----------------|
| 1 Year | No Upfront | $XX/hour | 22% | $XX,XXX |
| 1 Year | Partial Upfront | $XX/hour | 25% | $XX,XXX |
| 1 Year | All Upfront | $XX/hour | 27% | $XX,XXX |
| 3 Year | No Upfront | $XX/hour | 36% | $XX,XXX |
| 3 Year | All Upfront | $XX/hour | 52% | $XX,XXX |

### Recommended Configuration

| Commitment Type | Hourly Amount | Term | Payment | Expected Utilization |
|-----------------|---------------|------|---------|---------------------|
| Compute SP | $XX | 1 Year | Partial Upfront | 95%+ |
| EC2 Instance SP | $XX | 1 Year | No Upfront | 90%+ |

## Risk Assessment

| Risk | Mitigation |
|------|------------|
| Usage decrease | Conservative commitment (80% of baseline) |
| Region change | Use Compute SP (region-flexible) |
| Instance family change | Use Compute SP (instance-flexible) |

## Financial Summary

| Metric | Before | After | Delta |
|--------|--------|-------|-------|
| Monthly Spend | $XXX,XXX | $XXX,XXX | -$XX,XXX |
| Annual Spend | $X,XXX,XXX | $X,XXX,XXX | -$XXX,XXX |
| Effective Discount | 0% | XX% | +XX% |
```

---

## Template 5: Rightsizing Report

```markdown
# Rightsizing Analysis Report

**Analysis Date:** [DATE]
**Resources Analyzed:** [COUNT]
**Analysis Period:** [DAYS] days

## Summary

| Category | Count | Current Cost | Recommended Cost | Savings |
|----------|-------|--------------|------------------|---------|
| Oversized | XX | $XX,XXX | $X,XXX | $X,XXX |
| Idle | XX | $X,XXX | $0 | $X,XXX |
| Optimal | XX | $XX,XXX | $XX,XXX | $0 |
| **Total** | XXX | $XXX,XXX | $XX,XXX | $XX,XXX |

## Oversized Instances

| Instance ID | Current Type | Avg CPU | Avg Memory | Recommended | Monthly Savings |
|-------------|--------------|---------|------------|-------------|-----------------|
| i-xxxxx1 | m5.2xlarge | 5% | 12% | m5.large | $XXX |
| i-xxxxx2 | r5.4xlarge | 8% | 25% | r5.xlarge | $XXX |
| i-xxxxx3 | c5.2xlarge | 15% | 10% | c5.large | $XXX |

## Idle Instances (Termination Candidates)

| Instance ID | Type | Avg CPU | Last Activity | Owner | Monthly Cost |
|-------------|------|---------|---------------|-------|--------------|
| i-yyyyy1 | t3.large | <1% | 30+ days ago | Team A | $XX |
| i-yyyyy2 | m5.xlarge | <1% | 45+ days ago | Team B | $XXX |

## Recommendations

### Immediate Actions (Low Risk)

1. [ ] Terminate idle instances (list attached)
2. [ ] Rightsize dev/test instances
3. [ ] Apply auto-scaling to variable workloads

### Planned Actions (Requires Testing)

1. [ ] Rightsize production instances during maintenance window
2. [ ] Migrate to newer instance families
3. [ ] Evaluate Graviton instances for compatible workloads

## Implementation Timeline

| Week | Action | Resources | Expected Savings |
|------|--------|-----------|------------------|
| 1 | Terminate idle | XX instances | $X,XXX |
| 2 | Rightsize dev | XX instances | $X,XXX |
| 3-4 | Rightsize staging | XX instances | $X,XXX |
| 5-6 | Rightsize production | XX instances | $X,XXX |
```

---

## Template 6: FinOps RACI Matrix

```markdown
# FinOps RACI Matrix

| Activity | Engineering | Finance | FinOps | Leadership |
|----------|-------------|---------|--------|------------|
| **INFORM** |
| Enable billing exports | R | I | A | I |
| Define tagging standards | C | C | A/R | I |
| Implement tags | R | I | A | I |
| Create dashboards | C | C | A/R | I |
| **OPTIMIZE** |
| Rightsizing analysis | C | I | R | A |
| Commitment purchases | C | R | A | C |
| Resource cleanup | R | I | A | I |
| Architecture optimization | A/R | I | C | I |
| **OPERATE** |
| Budget setting | C | A/R | C | C |
| Cost reviews | R | C | A | C |
| Anomaly response | R | I | A | I |
| Policy enforcement | C | I | A/R | C |

**Legend:**
- R = Responsible (does the work)
- A = Accountable (owns the outcome)
- C = Consulted (provides input)
- I = Informed (kept up to date)
```

---

## Template 7: Cost Anomaly Investigation

```markdown
# Cost Anomaly Investigation

**Alert ID:** [ID]
**Detected:** [DATETIME]
**Investigated By:** [NAME]

## Alert Details

| Field | Value |
|-------|-------|
| Anomaly Type | [Spike/Drift/New] |
| Service | [Service Name] |
| Account | [Account ID/Name] |
| Region | [Region] |
| Expected Cost | $X,XXX |
| Actual Cost | $X,XXX |
| Variance | +$X,XXX (+XX%) |

## Investigation

### Timeline of Events

| Timestamp | Event | Source |
|-----------|-------|--------|
| [TIME] | [Event description] | [CloudTrail/Logs] |
| [TIME] | [Event description] | [CloudTrail/Logs] |

### Root Cause

[Description of root cause]

| Factor | Details |
|--------|---------|
| What changed | [Description] |
| Who made change | [User/Role] |
| Why | [Reason if known] |

## Impact Assessment

| Metric | Value |
|--------|-------|
| Total additional cost | $X,XXX |
| Duration | [Hours/Days] |
| Projected monthly impact | $XX,XXX |
| Business impact | [High/Medium/Low] |

## Resolution

| Action | Status | Owner |
|--------|--------|-------|
| [Action 1] | Done | [Name] |
| [Action 2] | In Progress | [Name] |
| [Action 3] | Pending | [Name] |

## Prevention

| Control | Implementation |
|---------|---------------|
| Policy change | [Description] |
| Alert tuning | [Description] |
| Process improvement | [Description] |

## Lessons Learned

[Summary of what was learned and how to prevent recurrence]
```

## Sources

- [FinOps Foundation Templates](https://www.finops.org/resources/)
- [AWS Well-Architected Cost Optimization](https://docs.aws.amazon.com/wellarchitected/latest/cost-optimization-pillar/)
- [Google Cloud Cost Management](https://cloud.google.com/cost-management)
