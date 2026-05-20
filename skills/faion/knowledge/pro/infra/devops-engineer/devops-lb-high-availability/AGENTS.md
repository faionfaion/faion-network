---
slug: devops-lb-high-availability
tier: pro
group: infra
domain: devops-engineer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A load balancer is itself a single point of failure unless deployed in an HA topology.
content_id: "7308941a3d7042ae"
tags: [load-balancing, high-availability, cloud, aws, disaster-recovery]
---
# Load Balancer High Availability and Cloud Patterns

## Summary

**One-sentence:** A load balancer is itself a single point of failure unless deployed in an HA topology.

**One-paragraph:** A load balancer is itself a single point of failure unless deployed in an HA topology. Active-active with floating VIP is the standard on-premise pattern; cloud managed LBs (AWS ALB, GCP HTTPS LB, Azure Front Door) handle HA internally across availability zones. Select the cloud LB product based on OSI layer and routing requirements.

## Applies If (ALL must hold)

- Any production service with an SLA above 99% — a single LB instance cannot achieve this.
- Multi-AZ deployments where backend servers span availability zones.
- Global applications requiring cross-region failover or latency-based routing.
- Deployments where the load balancer tier must survive a full AZ failure.

## Skip If (ANY kills it)

- Development or staging environments where downtime during maintenance is acceptable — HA adds cost and complexity.
- Do not implement active-active LB without cross-session state synchronisation or sticky sessions — inconsistent routing will break stateful applications.

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
