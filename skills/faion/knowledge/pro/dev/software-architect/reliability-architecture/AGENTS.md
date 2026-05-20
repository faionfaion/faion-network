---
slug: reliability-architecture
tier: pro
group: dev
domain: software-architect
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Designing systems that maintain availability targets, recover from failures, and degrade gracefully under stress.
content_id: "51ddb6513c17bd26"
tags: [reliability, slo, fault-tolerance, disaster-recovery, chaos-engineering]
---
# Reliability Architecture

## Summary

**One-sentence:** Designing systems that maintain availability targets, recover from failures, and degrade gracefully under stress.

**One-paragraph:** Designing systems that maintain availability targets, recover from failures, and degrade gracefully under stress. Core outputs: SLO/SLI/error-budget definitions, fault-tolerance pattern selection (circuit breaker, retry with jitter, bulkhead, timeout), graceful degradation tiers, health check endpoints, chaos engineering plan, and DR strategy (RPO/RTO, 3-2-1 backups).

## Applies If (ALL must hold)

- Defining SLOs before a new service goes to production
- Conducting an architecture review where availability targets exceed 99.9%
- Adding fault tolerance after an outage revealed cascading failure modes
- Designing health check endpoints for Kubernetes probes
- Planning a chaos engineering programme or DR drill

## Skip If (ANY kills it)

- MVP or internal tool where 99% availability (3.65 days/year downtime) is acceptable — over-engineering adds cost
- Single-service monolith without external dependencies — most patterns target distributed call paths
- When the bottleneck is a business/product problem, not an infrastructure one

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

- parent skill: `pro/dev/software-architect/`
