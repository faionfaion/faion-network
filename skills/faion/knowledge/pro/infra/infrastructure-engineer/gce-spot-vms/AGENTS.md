---
slug: gce-spot-vms
tier: pro
group: infra
domain: infrastructure-engineer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Spot VMs offer up to 91% discount over standard on-demand pricing but can be preempted by GCP with a 30-second warning at any time.
content_id: "d8a6388f3b270128"
tags: [gcp, compute-engine, spot-vms, cost-optimization]
---
# GCE Spot VMs

## Summary

**One-sentence:** Spot VMs offer up to 91% discount over standard on-demand pricing but can be preempted by GCP with a 30-second warning at any time.

**One-paragraph:** Spot VMs offer up to 91% discount over standard on-demand pricing but can be preempted by GCP with a 30-second warning at any time. Spot VMs have no 24-hour limit (unlike the legacy Preemptible VMs they replace) and support the same machine types, regions, and features. They are suitable for batch processing, dev/test environments, fault-tolerant stateless services, and GKE burst capacity. Always use MIGs with autohealing to automatically recreate preempted instances.

## Applies If (ALL must hold)

- Batch processing pipelines (data transforms, ML training, rendering) that checkpoint progress — preemption loses at most one checkpoint interval of work.
- Dev and test environments — workloads are not user-facing; interruptions are acceptable and savings are significant.
- GKE burst capacity via spot node pools — non-critical Pods run on spot nodes with tolerations; critical Pods remain on standard nodes.
- Stateless microservices with MIG autohealing and enough instances that losing one zone's Spot capacity does not breach SLO.
- CI/CD build agents — builds are retried on preemption; savings are 60-91%.

## Skip If (ANY kills it)

- Single-instance production databases or stateful services without external state storage — preemption causes data loss and downtime.
- Workloads with strict SLOs that cannot tolerate the 30-second preemption window or the instance replacement time — use standard VMs as the baseline, Spot only for burst.
- Long-running jobs that cannot checkpoint and would lose more than the cost savings if preempted — calculate (preemption_probability * work_lost_cost) vs Spot savings before committing.
- Applications requiring a guaranteed minimum runtime longer than the observed Spot availability in the target zone — monitor preemption rates per zone and switch zones if availability is low.

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
