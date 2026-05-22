---
slug: gcp-gke-architecture
tier: pro
group: infra
domain: infra
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: GKE provides two cluster modes (Autopilot and Standard), multiple topology options (zonal/regional/multi-cluster), and several node pool strategies (general, spot, GPU, high-memory).
content_id: "455912253758728e"
tags: [gcp, gke, kubernetes, terraform, autopilot]
---
# GKE Architecture Patterns

## Summary

**One-sentence:** GKE provides two cluster modes (Autopilot and Standard), multiple topology options (zonal/regional/multi-cluster), and several node pool strategies (general, spot, GPU, high-memory).

**One-paragraph:** GKE provides two cluster modes (Autopilot and Standard), multiple topology options (zonal/regional/multi-cluster), and several node pool strategies (general, spot, GPU, high-memory). Choose Autopilot for most workloads; use Standard only for GPU, privileged containers, or deep custom node configs.

## Applies If (ALL must hold)

- Deploying containerized workloads on GCP requiring Kubernetes orchestration.
- Production services requiring 99.9%+ availability — use regional topology.
- Batch or fault-tolerant workloads — use spot node pools for 70-90% cost reduction.
- ML inference or video processing — use GPU-attached node pools in Standard mode.
- Multi-region failover or global routing — use multi-cluster topology.

## Skip If (ANY kills it)

- Fully serverless stateless workloads — Cloud Run is simpler and cheaper than GKE for event-driven HTTP.
- Small single-binary services with predictable load — over-engineering adds cluster management cost.

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
