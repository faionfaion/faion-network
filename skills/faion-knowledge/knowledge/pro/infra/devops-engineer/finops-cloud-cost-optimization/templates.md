# FinOps Templates

## 1. Tagging Policy Template

### Mandatory Tags

```yaml
# tagging-policy.yaml
# Required for all cloud resources

mandatory_tags:
  project:
    description: "Project or product identifier"
    validation: "^[a-z0-9-]{3,30}$"
    examples: ["ecommerce-platform", "data-pipeline", "auth-service"]

  environment:
    description: "Deployment environment"
    allowed_values:
      - prod
      - staging
      - dev
      - sandbox
      - dr

  owner:
    description: "Team or individual responsible"
    validation: "^[a-z0-9-@.]{3,50}$"
    examples: ["platform-team", "john.doe@company.com"]

  cost-center:
    description: "Finance cost allocation code"
    validation: "^CC[0-9]{4,6}$"
    examples: ["CC1234", "CC567890"]
```

### Recommended Tags

```yaml
recommended_tags:
  application:
    description: "Application name"
    examples: ["api-gateway", "web-frontend", "ml-pipeline"]

  service:
    description: "Service or microservice name"
    examples: ["user-service", "payment-processor"]

  data-classification:
    description: "Data sensitivity level"
    allowed_values:
      - public
      - internal
      - confidential
      - restricted

  managed-by:
    description: "Infrastructure management method"
    allowed_values:
      - terraform
      - pulumi
      - cloudformation
      - manual

  created-by:
    description: "Creator for manual resources"
    examples: ["john.doe", "ci-pipeline"]

  expiry-date:
    description: "Auto-termination date for temporary resources"
    validation: "^[0-9]{4}-[0-9]{2}-[0-9]{2}$"
    examples: ["2026-03-15"]
```

---

## 2. AWS Tag Enforcement (Terraform)

### Service Control Policy

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "RequireMandatoryTags",
      "Effect": "Deny",
      "Action": [
        "ec2:RunInstances",
        "ec2:CreateVolume",
        "rds:CreateDBInstance",
        "s3:CreateBucket"
      ],
      "Resource": "*",
      "Condition": {
        "Null": {
          "aws:RequestTag/project": "true",
          "aws:RequestTag/environment": "true",
          "aws:RequestTag/owner": "true",
          "aws:RequestTag/cost-center": "true"
        }
      }
    }
  ]
}
```

### AWS Config Rule

```hcl
# required-tags-config-rule.tf

resource "aws_config_config_rule" "required_tags" {
  name = "required-tags"

  source {
    owner             = "AWS"
    source_identifier = "REQUIRED_TAGS"
  }

  input_parameters = jsonencode({
    tag1Key   = "project"
    tag2Key   = "environment"
    tag3Key   = "owner"
    tag4Key   = "cost-center"
  })

  scope {
    compliance_resource_types = [
      "AWS::EC2::Instance",
      "AWS::EC2::Volume",
      "AWS::RDS::DBInstance",
      "AWS::S3::Bucket",
      "AWS::Lambda::Function"
    ]
  }
}
```

---

## 3. Azure Tag Enforcement (Policy)

```json
{
  "mode": "Indexed",
  "policyRule": {
    "if": {
      "anyOf": [
        {
          "field": "[concat('tags[', parameters('tagName1'), ']')]",
          "exists": "false"
        },
        {
          "field": "[concat('tags[', parameters('tagName2'), ']')]",
          "exists": "false"
        },
        {
          "field": "[concat('tags[', parameters('tagName3'), ']')]",
          "exists": "false"
        },
        {
          "field": "[concat('tags[', parameters('tagName4'), ']')]",
          "exists": "false"
        }
      ]
    },
    "then": {
      "effect": "deny"
    }
  },
  "parameters": {
    "tagName1": {
      "type": "String",
      "defaultValue": "project"
    },
    "tagName2": {
      "type": "String",
      "defaultValue": "environment"
    },
    "tagName3": {
      "type": "String",
      "defaultValue": "owner"
    },
    "tagName4": {
      "type": "String",
      "defaultValue": "cost-center"
    }
  }
}
```

---

## 4. GCP Label Enforcement (Terraform)

```hcl
# gcp-label-policy.tf

resource "google_project_organization_policy" "require_labels" {
  project    = var.project_id
  constraint = "constraints/compute.requireLabels"

  list_policy {
    allow {
      values = [
        "project",
        "environment",
        "owner",
        "cost-center"
      ]
    }
  }
}

# Module with enforced labels
module "compute_instance" {
  source = "./modules/compute"

  labels = merge(var.required_labels, {
    project      = var.project_name
    environment  = var.environment
    owner        = var.owner
    cost-center  = var.cost_center
  })
}
```

---

## 5. Budget Alert Template

### AWS Budget (Terraform)

```hcl
# aws-budget.tf

resource "aws_budgets_budget" "monthly" {
  name              = "monthly-budget"
  budget_type       = "COST"
  limit_amount      = "10000"
  limit_unit        = "USD"
  time_unit         = "MONTHLY"
  time_period_start = "2026-01-01_00:00"

  cost_filter {
    name   = "TagKeyValue"
    values = ["project$${var.project_name}"]
  }

  notification {
    comparison_operator        = "GREATER_THAN"
    threshold                  = 50
    threshold_type             = "PERCENTAGE"
    notification_type          = "ACTUAL"
    subscriber_email_addresses = var.alert_emails
  }

  notification {
    comparison_operator        = "GREATER_THAN"
    threshold                  = 75
    threshold_type             = "PERCENTAGE"
    notification_type          = "ACTUAL"
    subscriber_email_addresses = var.alert_emails
  }

  notification {
    comparison_operator        = "GREATER_THAN"
    threshold                  = 90
    threshold_type             = "PERCENTAGE"
    notification_type          = "ACTUAL"
    subscriber_email_addresses = concat(var.alert_emails, var.escalation_emails)
  }

  notification {
    comparison_operator        = "GREATER_THAN"
    threshold                  = 100
    threshold_type             = "PERCENTAGE"
    notification_type          = "ACTUAL"
    subscriber_email_addresses = concat(var.alert_emails, var.escalation_emails)
  }
}
```

### Azure Budget

```hcl
# azure-budget.tf

resource "azurerm_consumption_budget_resource_group" "monthly" {
  name              = "monthly-budget"
  resource_group_id = azurerm_resource_group.main.id

  amount     = 10000
  time_grain = "Monthly"

  time_period {
    start_date = "2026-01-01T00:00:00Z"
    end_date   = "2026-12-31T23:59:59Z"
  }

  filter {
    tag {
      name   = "project"
      values = [var.project_name]
    }
  }

  notification {
    enabled   = true
    threshold = 50.0
    operator  = "GreaterThan"
    contact_emails = var.alert_emails
  }

  notification {
    enabled   = true
    threshold = 75.0
    operator  = "GreaterThan"
    contact_emails = var.alert_emails
  }

  notification {
    enabled   = true
    threshold = 90.0
    operator  = "GreaterThan"
    contact_emails = concat(var.alert_emails, var.escalation_emails)
  }
}
```

---

## 6. Rightsizing Review Template

### Weekly Review Checklist

```markdown
# Rightsizing Review - Week of [DATE]

## Summary

| Metric | Value |
|--------|-------|
| Instances reviewed | |
| Recommendations generated | |
| Recommendations implemented | |
| Estimated monthly savings | |

## Recommendations

### High Priority (>$500/month savings)

| Instance ID | Current Type | Recommended | Avg CPU | Avg Memory | Est. Savings |
|-------------|--------------|-------------|---------|------------|--------------|
| | | | | | |

### Medium Priority ($100-500/month)

| Instance ID | Current Type | Recommended | Avg CPU | Avg Memory | Est. Savings |
|-------------|--------------|-------------|---------|------------|--------------|
| | | | | | |

### Deferred (Needs Investigation)

| Instance ID | Current Type | Reason for Deferral |
|-------------|--------------|---------------------|
| | | |

## Blockers

- [ ]

## Next Steps

1.
2.
3.

## Approvals

- [ ] Engineering lead
- [ ] Application owner
- [ ] Change approved
```

---

## 7. Commitment Coverage Report

```markdown
# Commitment Coverage Report - [MONTH YEAR]

## Overview

| Provider | Total Spend | Committed | On-Demand | Spot | Coverage % |
|----------|-------------|-----------|-----------|------|------------|
| AWS | | | | | |
| Azure | | | | | |
| GCP | | | | | |
| **Total** | | | | | |

## AWS Savings Plans

| Plan Type | Hourly Commitment | Utilization | Coverage | Savings |
|-----------|-------------------|-------------|----------|---------|
| Compute SP | | | | |
| EC2 Instance SP | | | | |
| **Total** | | | | |

## AWS Reserved Instances

| Instance Family | RIs Owned | RIs Used | Utilization % | Expiring (90d) |
|-----------------|-----------|----------|---------------|----------------|
| | | | | |

## Azure Reservations

| Resource Type | Reservations | Utilization % | Savings |
|---------------|--------------|---------------|---------|
| VM | | | |
| SQL | | | |
| Storage | | | |

## GCP Commitments

| Commitment Type | vCPUs | Memory (GB) | Utilization % |
|-----------------|-------|-------------|---------------|
| | | | |

## Recommendations

### Increase Commitments

| Provider | Resource | Recommended | Estimated Savings |
|----------|----------|-------------|-------------------|
| | | | |

### Reduce/Modify Commitments

| Provider | Resource | Current | Recommended | Reason |
|----------|----------|---------|-------------|--------|
| | | | | |

## Expiring Commitments (Next 90 Days)

| Provider | Resource | Expiry Date | Current Cost | Recommendation |
|----------|----------|-------------|--------------|----------------|
| | | | | |
```

---

## 8. Cost Anomaly Investigation

```markdown
# Cost Anomaly Investigation

## Anomaly Details

| Field | Value |
|-------|-------|
| Date detected | |
| Provider | |
| Service | |
| Account/Subscription | |
| Expected daily cost | |
| Actual daily cost | |
| Variance | |
| Variance % | |

## Initial Analysis

### Resource Changes

| Resource | Change Type | Timestamp | Changed By |
|----------|-------------|-----------|------------|
| | | | |

### Usage Changes

| Metric | Previous Avg | Current | Change % |
|--------|--------------|---------|----------|
| | | | |

## Root Cause

[ ] New deployment
[ ] Configuration change
[ ] Traffic spike
[ ] Data transfer increase
[ ] Storage growth
[ ] Pricing change
[ ] Attack/abuse
[ ] Other: _______________

## Details

```
[Detailed explanation of root cause]
```

## Resolution

| Action | Owner | Status | Completion Date |
|--------|-------|--------|-----------------|
| | | | |

## Prevention

- [ ] Add monitoring/alert
- [ ] Update budget
- [ ] Implement guardrail
- [ ] Update runbook
- [ ] Training needed

## Impact

| Metric | Value |
|--------|-------|
| Total overspend | |
| Duration | |
| Lessons learned | |
```

---

## 9. FinOps Team Charter Template

```markdown
# FinOps Team Charter

## Mission

Maximize business value from cloud investments by enabling data-driven spending decisions, fostering a cost-aware culture, and continuously optimizing cloud efficiency.

## Scope

### In Scope
- Cloud cost visibility and reporting
- Cost allocation and chargeback
- Optimization recommendations
- Commitment management (RIs, Savings Plans)
- Budget management and forecasting
- Anomaly detection and investigation
- FinOps tooling selection and management

### Out of Scope
- Infrastructure provisioning (owned by Platform team)
- Application architecture decisions (owned by Engineering)
- Vendor contract negotiation (owned by Procurement)

## Team Structure

| Role | Responsibilities | Allocation |
|------|------------------|------------|
| FinOps Lead | Strategy, stakeholder management | 100% |
| FinOps Engineer | Reporting, optimization, tooling | 100% |
| Cloud Finance | Forecasting, budgets, chargebacks | 50% |
| Engineering Rep | Technical feasibility, implementation | 25% |

## RACI Matrix

| Activity | FinOps | Engineering | Finance | Leadership |
|----------|--------|-------------|---------|------------|
| Cost reporting | A/R | C | I | I |
| Optimization | A | R | I | I |
| Budget setting | C | C | A/R | I |
| Commitment purchases | R | C | A | I |
| Anomaly investigation | R | A | I | I |

## Key Metrics

| Metric | Target | Current |
|--------|--------|---------|
| Cost allocation accuracy | >95% | |
| Tag compliance | >90% | |
| RI/SP coverage | 70-80% | |
| RI/SP utilization | >95% | |
| Waste percentage | <10% | |
| Cost per unit of service | Decreasing | |

## Review Cadence

| Meeting | Frequency | Attendees |
|---------|-----------|-----------|
| Daily standup | Daily | FinOps team |
| Engineering sync | Weekly | FinOps + Eng leads |
| Cost review | Monthly | All stakeholders |
| Commitment review | Quarterly | FinOps + Finance |
| Strategy review | Annually | Leadership |
```

---

## Sources

- [FinOps Foundation Templates](https://www.finops.org/resources/)
- [AWS Tagging Best Practices](https://docs.aws.amazon.com/whitepapers/latest/tagging-best-practices/tagging-best-practices.html)
- [Azure Policy Documentation](https://learn.microsoft.com/en-us/azure/governance/policy/)
- [GCP Resource Labels](https://cloud.google.com/resource-manager/docs/creating-managing-labels)
- [Terraform AWS Provider](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)
