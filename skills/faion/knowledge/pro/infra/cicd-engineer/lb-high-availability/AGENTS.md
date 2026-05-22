---
slug: lb-high-availability
tier: pro
group: infra
domain: infra
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: High availability for load-balanced systems requires redundancy at both the load balancer tier and the backend tier, distributed across availability zones or regions.
content_id: "a3c619a5f17c9539"
tags: [load-balancing, high-availability, multi-region, gslb, infrastructure]
---
# Load Balancer High Availability Patterns

## Summary

**One-sentence:** High availability for load-balanced systems requires redundancy at both the load balancer tier and the backend tier, distributed across availability zones or regions.

**One-paragraph:** High availability for load-balanced systems requires redundancy at both the load balancer tier and the backend tier, distributed across availability zones or regions. Single-region HA uses active-active or active-passive LB pairs with zone-spread backends. Multi-region HA adds Global Server Load Balancing (GSLB) via anycast or DNS-based routing. Connection draining and readiness-probe coordination enable zero-downtime deployments.

## Applies If (ALL must hold)

- Designing a new load-balanced service with an availability SLA ≥99.9%.
- Reviewing an architecture proposal for hidden SPOFs at the load balancer tier.
- Planning a zero-downtime deployment or maintenance procedure.
- Adding multi-region failover to an existing single-region deployment.
- Post-incident review after a load balancer failure caused an outage.

## Skip If (ANY kills it)

- Development or staging environments where downtime is acceptable — HA adds cost without value there.
- Internal tools with no SLA — single instance is fine.
- Load balancing algorithm selection — see lb-algorithms.
- Health check configuration depth — see lb-health-checks.

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

- parent skill: `pro/infra/cicd-engineer/`
