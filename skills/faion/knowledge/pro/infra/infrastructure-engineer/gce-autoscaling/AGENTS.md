---
slug: gce-autoscaling
tier: pro
group: infra
domain: infrastructure-engineer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: The GCE autoscaler adjusts the size of a Managed Instance Group in response to one or more scaling signals: CPU utilization, load balancing capacity, custom Cloud Monitoring metrics, time-based schedules, or ML-based predictive forecasting.
content_id: "1aa0e9959377f1db"
tags: [gcp, compute-engine, autoscaling, performance]
---
# GCE Autoscaling

## Summary

**One-sentence:** The GCE autoscaler adjusts the size of a Managed Instance Group in response to one or more scaling signals: CPU utilization, load balancing capacity, custom Cloud Monitoring metrics, time-based schedules, or ML-based predictive forecasting.

**One-paragraph:** The GCE autoscaler adjusts the size of a Managed Instance Group in response to one or more scaling signals: CPU utilization, load balancing capacity, custom Cloud Monitoring metrics, time-based schedules, or ML-based predictive forecasting. Multiple signals can be combined; the autoscaler scales to whichever signal demands the most capacity. Scale-in controls prevent rapid downscaling that would cause flapping during brief traffic dips.

## Applies If (ALL must hold)

- Any MIG-backed service with variable traffic — CPU-based autoscaling is the correct default.
- HTTP(S) services behind a Google Cloud Load Balancer — load balancing utilization signal tracks requests-per-second more accurately than CPU for frontend services.
- Queue-draining workers — custom Cloud Monitoring metric (queue depth) drives scaling proportional to backlog size.
- Predictable daily or weekly traffic patterns (e.g., business-hours web apps) — schedule-based autoscaling pre-provisions capacity before demand arrives.
- Applications with initialization time longer than 2 minutes — predictive autoscaling prevents latency spikes at ramp-up by starting instances before traffic arrives.

## Skip If (ANY kills it)

- Stateful MIGs where instance replacement destroys per-instance data — autoscaling removes instances without draining persistent state; use manual scaling or stateful MIG policies instead.
- MIGs with min_replicas = 0 for production services — a scale-to-zero event during a traffic dip causes a cold-start latency spike when traffic returns; keep minimum >= 1 (or >= 3 for regional MIGs).
- Workloads with unpredictable, spiky traffic (e.g., viral events) where the 60-second reaction time is too slow — pre-scale via a schedule or use Cloud Run/GKE with faster scale-to-zero.

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

- parent skill: `pro/infra/infrastructure-engineer/`
