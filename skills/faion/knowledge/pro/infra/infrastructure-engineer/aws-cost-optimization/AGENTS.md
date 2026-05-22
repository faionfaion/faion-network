---
slug: aws-cost-optimization
tier: pro
group: infra
domain: infra
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: AWS cost optimization covers four levers: compute (Reserved Instances, Savings Plans, Spot), storage (S3 tiering, lifecycle policies, EBS cleanup), networking (VPC endpoints, CloudFront, NAT consolidation), and right-sizing (matching instance type to actual utilization).
content_id: "d94ad534b1f62fe3"
tags: [aws, cost-optimization, reserved-instances, savings-plans, finops]
---
# AWS Cost Optimization

## Summary

**One-sentence:** AWS cost optimization covers four levers: compute (Reserved Instances, Savings Plans, Spot), storage (S3 tiering, lifecycle policies, EBS cleanup), networking (VPC endpoints, CloudFront, NAT consolidation), and right-sizing (matching instance type to actual utilization).

**One-paragraph:** AWS cost optimization covers four levers: compute (Reserved Instances, Savings Plans, Spot), storage (S3 tiering, lifecycle policies, EBS cleanup), networking (VPC endpoints, CloudFront, NAT consolidation), and right-sizing (matching instance type to actual utilization). Use Cost Explorer anchored to 30-day rolling windows, not same-day data which is delayed up to 24h.

## Applies If (ALL must hold)

- Monthly cost review — identify top spend services and apply the right optimization lever per service.
- Pre-commitment analysis before purchasing Reserved Instances or Savings Plans.
- New workload design — choose the right instance type and commitment model from the start.
- Cost spike investigation — quickly narrow down which service or resource type drove the increase.

## Skip If (ANY kills it)

- Prototype or short-lived environments (under 30 days) — on-demand is correct; no commitment makes sense.
- Security-first reviews — optimization and security are separate concerns; do not trade security controls (GuardDuty, Security Hub) for cost savings.

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
