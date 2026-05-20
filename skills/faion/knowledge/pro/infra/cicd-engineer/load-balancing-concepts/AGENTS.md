---
slug: load-balancing-concepts
tier: pro
group: infra
domain: cicd-engineer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Load balancing distributes network traffic across multiple servers to ensure high availability, reliability, and performance.
content_id: "fb77c1b8661b73c9"
tags: [load-balancing, high-availability, networking, infrastructure, health-checks]
---
# Load Balancing Concepts

## Summary

**One-sentence:** Load balancing distributes network traffic across multiple servers to ensure high availability, reliability, and performance.

**One-paragraph:** Load balancing distributes network traffic across multiple servers to ensure high availability, reliability, and performance. This methodology covers load balancing strategies, algorithms, health checks, session persistence, and L4 vs L7 architecture patterns.

## Applies If (ALL must hold)

- Scaling applications horizontally
- Ensuring high availability (HA)
- Improving application performance
- Implementing zero-downtime deployments
- Managing traffic spikes
- Distributing workloads across regions

## Skip If (ANY kills it)

- Single-server development environments where overhead is not justified
- Internal tools with minimal traffic and no HA requirements
- Stateful applications that cannot be refactored to share state externally — sticky sessions are a workaround, not a solution

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
