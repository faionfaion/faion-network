# FinOps Templates

## Tagging Policy Template

```yaml
# finops-tagging-policy.yaml
apiVersion: v1
kind: TaggingPolicy
metadata:
  name: organization-tagging-standard
  version: "1.0"
  last_updated: "2025-01-26"

mandatory_tags:
  - key: project
    description: "Project or product name"
    pattern: "^[a-z][a-z0-9-]{2,32}$"
    examples:
      - "ecommerce-platform"
      - "data-pipeline"

  - key: environment
    description: "Deployment environment"
    allowed_values:
      - prod
      - staging
      - dev
      - test
      - sandbox

  - key: owner
    description: "Team responsible for the resource"
    pattern: "^[a-z][a-z0-9-]{2,20}-team$"
    examples:
      - "platform-team"
      - "ml-team"

  - key: cost-center
    description: "Financial cost center code"
    pattern: "^CC-[0-9]{4,6}$"
    examples:
      - "CC-1234"
      - "CC-567890"

recommended_tags:
  - key: application
    description: "Application name within project"

  - key: component
    description: "Component or microservice name"

  - key: data-classification
    description: "Data sensitivity level"
    allowed_values:
      - public
      - internal
      - confidential
      - restricted

  - key: managed-by
    description: "IaC tool managing resource"
    allowed_values:
      - terraform
      - pulumi
      - cloudformation
      - manual

  - key: backup
    description: "Backup requirement"
    allowed_values:
      - daily
      - weekly
      - none

enforcement:
  grace_period_days: 7
  non_compliance_action: alert  # alert | prevent | terminate
  notification_channel: "#finops-alerts"
```

## Budget Template

```yaml
# finops-budget.yaml
apiVersion: v1
kind: FinOpsBudget
metadata:
  name: production-environment-budget
  fiscal_year: "2025"

budget:
  total_annual: 120000  # USD
  monthly_target: 10000

  breakdown:
    compute:
      allocation: 40%  # $4,000/month
      services:
        - ec2
        - lambda
        - ecs

    storage:
      allocation: 20%  # $2,000/month
      services:
        - s3
        - ebs
        - rds-storage

    database:
      allocation: 25%  # $2,500/month
      services:
        - rds
        - dynamodb
        - elasticache

    network:
      allocation: 10%  # $1,000/month
      services:
        - data-transfer
        - nat-gateway
        - cloudfront

    other:
      allocation: 5%   # $500/month

alerts:
  - threshold: 50%
    type: forecast
    recipients:
      - finops@company.com

  - threshold: 75%
    type: forecast
    recipients:
      - finops@company.com
      - engineering-leads@company.com

  - threshold: 90%
    type: actual
    recipients:
      - finops@company.com
      - engineering-leads@company.com
      - cto@company.com

  - threshold: 100%
    type: actual
    recipients:
      - finops@company.com
      - engineering-leads@company.com
      - cto@company.com
      - cfo@company.com
    escalation: true
```

## Cost Report Template

```markdown
# Monthly FinOps Report - [Month Year]

## Executive Summary

| Metric | Value | vs Last Month | vs Budget |
|--------|-------|---------------|-----------|
| Total Spend | $XX,XXX | +/-X% | +/-X% |
| Waste Identified | $X,XXX | +/-X% | - |
| Savings Realized | $X,XXX | +/-X% | - |
| Commitment Coverage | XX% | +/-X% | Target: 75% |

## Key Highlights

1. **[Highlight 1]** - Brief description of notable change
2. **[Highlight 2]** - Brief description of optimization
3. **[Highlight 3]** - Brief description of issue/concern

## Cost Breakdown by Environment

| Environment | Spend | % of Total | Trend |
|-------------|-------|------------|-------|
| Production | $X,XXX | XX% | +/-X% |
| Staging | $X,XXX | XX% | +/-X% |
| Development | $X,XXX | XX% | +/-X% |
| Other | $X,XXX | XX% | +/-X% |

## Cost Breakdown by Service

| Service | Spend | % of Total | Optimization Opportunity |
|---------|-------|------------|-------------------------|
| EC2/Compute | $X,XXX | XX% | [Notes] |
| RDS/Database | $X,XXX | XX% | [Notes] |
| S3/Storage | $X,XXX | XX% | [Notes] |
| Data Transfer | $X,XXX | XX% | [Notes] |
| Other | $X,XXX | XX% | [Notes] |

## Optimization Progress

### Completed This Month
- [ ] Action 1 - Savings: $XXX
- [ ] Action 2 - Savings: $XXX
- [ ] Action 3 - Savings: $XXX

### In Progress
- [ ] Action 4 - Expected Savings: $XXX
- [ ] Action 5 - Expected Savings: $XXX

### Planned Next Month
- [ ] Action 6 - Expected Savings: $XXX
- [ ] Action 7 - Expected Savings: $XXX

## Anomalies Detected

| Date | Description | Impact | Resolution |
|------|-------------|--------|------------|
| MM/DD | [Description] | $XXX | [Status] |

## Recommendations

1. **[Recommendation 1]**
   - Current state: [Description]
   - Proposed action: [Description]
   - Expected savings: $XXX/month

2. **[Recommendation 2]**
   - Current state: [Description]
   - Proposed action: [Description]
   - Expected savings: $XXX/month

## Next Month Forecast

| Metric | Forecast | Confidence |
|--------|----------|------------|
| Total Spend | $XX,XXX | High/Medium/Low |
| Waste | $X,XXX | High/Medium/Low |

---
Report generated: [Date]
Next review: [Date]
```

## FinOps Team Charter Template

```markdown
# FinOps Team Charter

## Mission
Enable the organization to achieve maximum business value from cloud investments through financial accountability, operational efficiency, and continuous optimization.

## Team Composition

| Role | Name | Department | Responsibility |
|------|------|------------|----------------|
| FinOps Lead | [Name] | [Dept] | Strategy, coordination, reporting |
| Cloud Architect | [Name] | Engineering | Technical optimization, architecture |
| Finance Analyst | [Name] | Finance | Budget, forecasting, chargeback |
| Engineering Lead | [Name] | Engineering | Implementation, automation |
| Product Representative | [Name] | Product | Business alignment, priorities |

## Responsibilities

### FinOps Lead
- Chair weekly FinOps meetings
- Report to executive stakeholders
- Define and track KPIs
- Coordinate cross-functional initiatives

### Cloud Architect
- Identify optimization opportunities
- Design cost-efficient architectures
- Implement automation
- Technical decision authority

### Finance Analyst
- Manage budgets and forecasts
- Process chargebacks
- Financial reporting
- Cost allocation accuracy

## Meeting Cadence

| Meeting | Frequency | Duration | Attendees |
|---------|-----------|----------|-----------|
| FinOps Standup | Weekly | 30 min | Core team |
| Optimization Review | Bi-weekly | 60 min | Core team + engineers |
| Executive Update | Monthly | 30 min | Lead + executives |
| Strategy Review | Quarterly | 2 hours | Full team |

## KPIs

| KPI | Target | Current | Owner |
|-----|--------|---------|-------|
| Total Cloud Spend | Stay within budget | $XXX | Finance |
| Waste Percentage | <10% | XX% | Cloud Architect |
| Commitment Coverage | 70-80% | XX% | Finance |
| Tag Compliance | >95% | XX% | Cloud Architect |
| Cost Per Customer | Trending down | $X.XX | Product |

## Decision Authority

| Decision Type | Authority | Escalation |
|---------------|-----------|------------|
| <$1,000 savings | Team member | None |
| $1,000-$10,000 | FinOps Lead | Engineering Lead |
| $10,000-$50,000 | FinOps Lead + Finance | VP Engineering |
| >$50,000 | Executive approval | CTO/CFO |

## Communication

- Slack channel: #finops
- Email: finops@company.com
- Dashboard: [Link to cost dashboard]
- Documentation: [Link to wiki]

---
Approved by: [Name], [Date]
Next review: [Date]
```

## Optimization Playbook Template

```markdown
# FinOps Optimization Playbook

## [Optimization Name]

### Overview
Brief description of the optimization technique.

### Applicability
- Resource types: [EC2, RDS, etc.]
- Environments: [Prod, Dev, All]
- Risk level: [Low/Medium/High]
- Effort: [Low/Medium/High]

### Prerequisites
- [ ] Prerequisite 1
- [ ] Prerequisite 2

### Procedure

#### Step 1: Analysis
```bash
# Commands or steps to analyze current state
```

#### Step 2: Validation
- [ ] Validate assumption 1
- [ ] Validate assumption 2

#### Step 3: Implementation
```bash
# Commands or steps to implement
```

#### Step 4: Verification
- [ ] Verify outcome 1
- [ ] Verify outcome 2

### Rollback Plan
```bash
# Commands or steps to rollback if needed
```

### Expected Savings
- Monthly: $XXX
- Annual: $X,XXX

### Risks and Mitigations
| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| [Risk 1] | Low/Med/High | Low/Med/High | [Action] |

### Success Metrics
- Metric 1: [Before] to [After]
- Metric 2: [Before] to [After]

---
Last updated: [Date]
Owner: [Name]
```

## AWS Policy Templates

### IAM Policy for FinOps Read Access

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "FinOpsReadAccess",
      "Effect": "Allow",
      "Action": [
        "ce:*",
        "cur:Describe*",
        "aws-portal:ViewBilling",
        "aws-portal:ViewUsage",
        "budgets:View*",
        "budgets:Describe*",
        "pricing:*",
        "compute-optimizer:Get*",
        "compute-optimizer:Describe*",
        "savingsplans:Describe*",
        "ec2:Describe*",
        "rds:Describe*",
        "s3:GetBucketLocation",
        "s3:ListAllMyBuckets",
        "organizations:Describe*",
        "organizations:List*"
      ],
      "Resource": "*"
    }
  ]
}
```

### SCP to Prevent Untagged Resources

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "RequireTags",
      "Effect": "Deny",
      "Action": [
        "ec2:RunInstances",
        "rds:CreateDBInstance",
        "s3:CreateBucket"
      ],
      "Resource": "*",
      "Condition": {
        "Null": {
          "aws:RequestTag/project": "true",
          "aws:RequestTag/environment": "true",
          "aws:RequestTag/owner": "true"
        }
      }
    }
  ]
}
```

## Terraform Module Template

### Cost-Optimized EC2 Instance

```hcl
# modules/cost-optimized-ec2/main.tf

variable "name" {
  type = string
}

variable "instance_type" {
  type    = string
  default = "t3.micro"
}

variable "environment" {
  type = string
}

variable "project" {
  type = string
}

variable "owner" {
  type = string
}

variable "cost_center" {
  type = string
}

variable "enable_spot" {
  type    = bool
  default = false
}

locals {
  mandatory_tags = {
    project      = var.project
    environment  = var.environment
    owner        = var.owner
    cost-center  = var.cost_center
    managed-by   = "terraform"
  }
}

resource "aws_instance" "this" {
  ami           = data.aws_ami.amazon_linux.id
  instance_type = var.instance_type

  # Use spot if enabled (for non-prod)
  instance_market_options {
    market_type = var.enable_spot ? "spot" : null

    dynamic "spot_options" {
      for_each = var.enable_spot ? [1] : []
      content {
        instance_interruption_behavior = "stop"
        spot_instance_type             = "persistent"
      }
    }
  }

  # Enable detailed monitoring for optimization insights
  monitoring = true

  # Mandatory tags
  tags = merge(local.mandatory_tags, {
    Name = var.name
  })

  # Cost-saving: stop instance on termination (for spot)
  instance_initiated_shutdown_behavior = "stop"
}

output "instance_id" {
  value = aws_instance.this.id
}

output "monthly_cost_estimate" {
  value = var.enable_spot ? "~$${var.instance_type == "t3.micro" ? "3" : "varies"}/month (spot)" : "~$${var.instance_type == "t3.micro" ? "8" : "varies"}/month (on-demand)"
}
```

---

*FinOps Templates | faion-cicd-engineer*
