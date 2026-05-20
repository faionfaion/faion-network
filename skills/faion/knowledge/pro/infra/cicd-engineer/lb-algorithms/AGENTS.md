---
slug: lb-algorithms
tier: pro
group: infra
domain: cicd-engineer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Load balancing algorithms distribute traffic across backend servers.
content_id: "84840439728be4cb"
tags: [load-balancing, algorithms, round-robin, least-connections, infrastructure]
---
# Load Balancing Algorithm Selection

## Summary

**One-sentence:** Load balancing algorithms distribute traffic across backend servers.

**One-paragraph:** Load balancing algorithms distribute traffic across backend servers. Static algorithms (round-robin, weighted round-robin, IP hash, random) ignore real-time server load; dynamic algorithms (least connections, weighted least connections, least response time, resource-based) adapt to server state. Algorithm choice is driven by request duration homogeneity, server capacity uniformity, and autoscaling behavior.

## Applies If (ALL must hold)

- Selecting an algorithm before writing any load balancer config.
- Reviewing an existing config that exhibits uneven backend utilization or high p99 latency.
- Autoscaling events are causing distribution problems (ip-hash + frequent scale events).
- Traffic has variable request cost (some endpoints are fast, others are slow, long-running).

## Skip If (ANY kills it)

- Session persistence is the primary concern — see lb-session-persistence for ip-hash and cookie-based approaches.
- Tool-specific algorithm configuration (HAProxy balance directive, Nginx upstream) — see load-balancing-implementation.
- Service mesh internal load balancing (Envoy/Istio) — those use distinct xDS-configured algorithms.

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
