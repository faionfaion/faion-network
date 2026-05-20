---
slug: devops-lb-haproxy
tier: pro
group: infra
domain: devops-engineer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: HAProxy provides battle-tested L4/L7 load balancing with precise control over timeouts, health checks, ACL routing, and sticky sessions.
content_id: "4c61d64b5594a80c"
tags: [haproxy, load-balancing, nginx, proxy, rate-limiting]
---
# HAProxy and Nginx Load Balancer Configuration

## Summary

**One-sentence:** HAProxy provides battle-tested L4/L7 load balancing with precise control over timeouts, health checks, ACL routing, and sticky sessions.

**One-paragraph:** HAProxy provides battle-tested L4/L7 load balancing with precise control over timeouts, health checks, ACL routing, and sticky sessions. The production web pattern uses frontend/backend separation: HTTP frontend → HTTPS frontend → ACL routing → multiple backends with independent algorithms. Rate limiting uses stick tables. L4 mode handles databases with protocol-aware health checks.

## Applies If (ALL must hold)

- Self-hosted infrastructure where managed cloud LBs are not available or too expensive.
- Environments requiring advanced ACL-based routing, custom stick tables, or protocol-specific health checks (MySQL, PostgreSQL, Redis).
- Docker Compose or bare-metal setups needing a lightweight LB without Kubernetes.
- Migrating from a cloud LB to on-premise, or needing consistent config across cloud and on-prem.

## Skip If (ANY kills it)

- New cloud-native workloads — prefer managed cloud LBs (AWS ALB, GCP HTTPS LB) unless specific features are needed.
- Do not run HAProxy as the only LB instance in production — it becomes a SPOF; always deploy active-passive or active-active pairs.

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
