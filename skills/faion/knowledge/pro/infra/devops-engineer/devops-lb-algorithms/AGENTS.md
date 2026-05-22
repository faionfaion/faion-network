---
slug: devops-lb-algorithms
tier: pro
group: infra
domain: infra
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Choosing the correct load balancer type and algorithm is the first architectural decision.
content_id: "ef48992dbc97d8a8"
tags: [load-balancing, algorithms, l4, l7, networking]
---
# Load Balancer Types and Algorithm Selection

## Summary

**One-sentence:** Choosing the correct load balancer type and algorithm is the first architectural decision.

**One-paragraph:** Choosing the correct load balancer type and algorithm is the first architectural decision. Layer 4 (TCP/UDP) optimises for throughput; Layer 7 (HTTP) enables content-based routing. Algorithms range from stateless round robin to stateful consistent hashing — each with distinct trade-offs.

## Applies If (ALL must hold)

- Scaling applications horizontally across multiple backend instances.
- Ensuring high availability where single-server failure must not interrupt service.
- Improving application performance by distributing requests evenly.
- Implementing zero-downtime deployments with traffic draining.
- Managing traffic spikes or geographic distribution of traffic.

## Skip If (ANY kills it)

- Single-instance deployments where a single server is sufficient — adds complexity without benefit.
- Applications with shared mutable state that cannot be distributed (use sticky sessions or a shared store instead).

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
