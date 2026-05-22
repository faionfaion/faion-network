---
slug: devops-aws-monitoring-dr
tier: pro
group: infra
domain: infra
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Production AWS workloads require CloudWatch dashboards per tier, metric alarms with SNS notifications, X-Ray distributed tracing across Lambda and API Gateway, and a tested DR strategy matched to business RTO/RPO.
content_id: "cf6ed11ac9e0221a"
tags: [aws, cloudwatch, monitoring, disaster-recovery, observability]
---
# AWS Monitoring, Alerting, and Disaster Recovery

## Summary

**One-sentence:** Production AWS workloads require CloudWatch dashboards per tier, metric alarms with SNS notifications, X-Ray distributed tracing across Lambda and API Gateway, and a tested DR strategy matched to business RTO/RPO.

**One-paragraph:** Production AWS workloads require CloudWatch dashboards per tier, metric alarms with SNS notifications, X-Ray distributed tracing across Lambda and API Gateway, and a tested DR strategy matched to business RTO/RPO. Alerting must be tiered: critical (immediate page), warning (business hours), informational (digest). DR must be tested on a schedule — untested DR is no DR.

## Applies If (ALL must hold)

- Setting up monitoring for a new production AWS workload.
- Adding observability to an existing architecture that lacks dashboards or alarms.
- Designing or testing a disaster recovery runbook for a business-critical service.
- Preparing for an architecture review that includes the Reliability and Operational Excellence pillars.

## Skip If (ANY kills it)

- Dev and staging environments with no production traffic — basic alarms only, no DR needed.
- Third-party monitoring stacks (Datadog, New Relic) already deployed — integrate CloudWatch metrics as a source there instead of duplicating dashboards.

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
