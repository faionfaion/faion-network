---
slug: devops-aws-service-selection
tier: pro
group: infra
domain: devops-engineer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Choosing the right AWS service avoids rework.
content_id: "d76c6c8deaa9f293"
tags: [aws, service-selection, well-architected, compute, decision]
---
# AWS Service Selection: Compute, Database, and Architecture Decisions

## Summary

**One-sentence:** Choosing the right AWS service avoids rework.

**One-paragraph:** Choosing the right AWS service avoids rework. Compute selection follows: short tasks under 15 minutes use Lambda; container workloads prefer Fargate unless EKS control is needed; sustained CPU workloads use Graviton EC2 Reserved Instances. Database selection follows workload access patterns. The Well-Architected Framework 6 pillars provide the decision checklist across all categories.

## Applies If (ALL must hold)

- Starting a new AWS project and selecting core services.
- Reviewing an existing architecture for cost or operational efficiency gaps.
- Migrating on-premises workloads and mapping legacy components to AWS equivalents.
- Conducting a Well-Architected Review against the 6 pillars.

## Skip If (ANY kills it)

- When the architecture is already locked and services are in production — use cost optimization and monitoring methodologies instead.
- For service-specific configuration details — see devops-aws-three-tier and devops-aws-serverless-api.

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

- parent skill: `pro/infra/devops-engineer/`
