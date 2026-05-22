---
slug: aws-monitoring-observability
tier: pro
group: infra
domain: infra
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Production AWS observability uses CloudWatch for metrics, logs, and alarms; X-Ray for distributed tracing; an org-level CloudTrail with KMS encryption and log file validation for API auditing; and AWS Config for resource configuration tracking and compliance.
content_id: "da8240099b49fec4"
tags: [aws, cloudwatch, observability, monitoring, alarms]
---
# AWS Monitoring and Observability Stack

## Summary

**One-sentence:** Production AWS observability uses CloudWatch for metrics, logs, and alarms; X-Ray for distributed tracing; an org-level CloudTrail with KMS encryption and log file validation for API auditing; and AWS Config for resource configuration tracking and compliance.

**One-paragraph:** Production AWS observability uses CloudWatch for metrics, logs, and alarms; X-Ray for distributed tracing; an org-level CloudTrail with KMS encryption and log file validation for API auditing; and AWS Config for resource configuration tracking and compliance. Alarms feed SNS topics that route to PagerDuty, OpsGenie, or Slack. All resources are Terraform-managed.

## Applies If (ALL must hold)

- Setting up a new environment or account and defining the baseline monitoring stack.
- Adding workloads (EKS cluster, RDS cluster, ALB) that require metric coverage and alerting.
- Compliance audits that require evidence of CloudTrail coverage and Config rule compliance.
- Incidents where the post-mortem reveals a monitoring gap that allowed the failure to go undetected.

## Skip If (ANY kills it)

- Day-2 incident triage — this methodology is for setup; use runbooks for active incidents.
- Non-AWS clouds — use GCP Cloud Monitoring / Datadog equivalents.

## Prerequisites

- TBD — list concrete input artifacts and where they come from

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `TBD/path` | TBD — what upstream output this consumes |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules migrated from v1 methodology | ~800 |
| `content/02-output-contract.xml` | essential | Output schema (stub — fill from v1 patterns) | ~800 |
| `content/03-failure-modes.xml` | essential | Antipatterns migrated from v1 methodology | ~800 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| TBD | sonnet | TBD |

## Templates

| File | Purpose |
|------|---------|
| TBD | TBD |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| TBD | TBD | TBD |

## Related

- parent skill: `pro/infra/infrastructure-engineer/`
