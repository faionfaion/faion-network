---
slug: lb-haproxy-production
tier: pro
group: infra
domain: cicd-engineer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Production HAProxy setup covers: global performance tuning (maxconn, nbthread, cpu-map), TLS 1.
content_id: "c59926cc9f7fedb5"
tags: [haproxy, load-balancing, tls, high-availability, infrastructure]
---
# HAProxy Production Configuration

## Summary

**One-sentence:** Production HAProxy setup covers: global performance tuning (maxconn, nbthread, cpu-map), TLS 1.

**One-paragraph:** Production HAProxy setup covers: global performance tuning (maxconn, nbthread, cpu-map), TLS 1.2+/1.3 with strong cipher suites, rate limiting via stick-tables (100 req/10s per IP), path-based ACL routing to separate backends, HTTP health checks with expect directives, and active-passive HA using keepalived for VIP failover.

## Applies If (ALL must hold)

- Standing up HAProxy in front of a service fleet on bare metal, VMs, or as a Kubernetes Ingress controller.
- Implementing rate limiting without an external Redis/Memcached state store (stick-tables are in-process).
- Routing TCP (database, Redis) alongside HTTP workloads from a single LB process.
- Setting up active-passive HA with keepalived for a VIP that survives node failure.

## Skip If (ANY kills it)

- Simple web server + LB combo — Nginx handles this with less configuration overhead.
- Static content caching — Nginx has a built-in cache layer; HAProxy does not.
- Managed cloud environments where ALB/NLB is available — operational overhead outweighs control.

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
