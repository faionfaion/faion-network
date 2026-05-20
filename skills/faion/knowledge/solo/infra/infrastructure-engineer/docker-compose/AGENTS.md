---
slug: docker-compose
tier: solo
group: infra
domain: infrastructure-engineer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Production-grade Docker Compose patterns for multi-container infrastructure stacks: no version: field, named volumes, custom networks with internal: true for database tiers, health checks on every service with depends_on: condition: service_healthy, resource limits via deploy.
content_id: "c73dda5c7f775d91"
tags: [docker, compose, infrastructure, networking, security]
---
# Docker Compose (Infrastructure)

## Summary

**One-sentence:** Production-grade Docker Compose patterns for multi-container infrastructure stacks: no version: field, named volumes, custom networks with internal: true for database tiers, health checks on every service with depends_on: condition: service_healthy, resource limits via deploy.

**One-paragraph:** Production-grade Docker Compose patterns for multi-container infrastructure stacks: no version: field, named volumes, custom networks with internal: true for database tiers, health checks on every service with depends_on: condition: service_healthy, resource limits via deploy.resources, and restart: unless-stopped. The compose.yaml file (not docker-compose.yml) is the modern canonical name.

## Applies If (ALL must hold)

- Defining multi-container application stacks (app + DB + cache + worker)
- Provisioning shared infrastructure services on a VPS (PostgreSQL, Redis, RabbitMQ)
- Setting up isolated per-project stacks with own networks, volumes, and resource limits
- Rolling out infrastructure updates requiring orchestrated service restarts with health-check ordering

## Skip If (ANY kills it)

- Single-container deployments — docker run + systemd unit is simpler and more observable
- Production at scale requiring multi-host orchestration — use Kubernetes or Docker Swarm
- Zero-downtime blue-green deploys — Compose lacks traffic shifting; use Kubernetes or a load balancer pair
- Stateless functions or serverless workloads

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

- parent skill: `solo/infra/infrastructure-engineer/`
