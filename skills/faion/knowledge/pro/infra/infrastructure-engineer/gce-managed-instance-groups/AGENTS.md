---
slug: gce-managed-instance-groups
tier: pro
group: infra
domain: infrastructure-engineer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A Managed Instance Group (MIG) maintains a set of identical VMs created from a single instance template, provides autohealing by replacing failed instances, supports rolling updates and canary deployments, and integrates with Google Cloud Load Balancing.
content_id: "1ecd4aa804ea4969"
tags: [gcp, compute-engine, managed-instance-groups, high-availability]
---
# GCE Managed Instance Groups (MIGs)

## Summary

**One-sentence:** A Managed Instance Group (MIG) maintains a set of identical VMs created from a single instance template, provides autohealing by replacing failed instances, supports rolling updates and canary deployments, and integrates with Google Cloud Load Balancing.

**One-paragraph:** A Managed Instance Group (MIG) maintains a set of identical VMs created from a single instance template, provides autohealing by replacing failed instances, supports rolling updates and canary deployments, and integrates with Google Cloud Load Balancing. Use regional MIGs (multi-zone) for all production workloads; zonal MIGs are acceptable only for dev/test or cost-sensitive batch jobs.

## Applies If (ALL must hold)

- Any stateless production service that needs more than one VM — regional MIG with minimum 3 instances (one per zone).
- Autoscaling web applications or APIs — MIG is required for the autoscaler to add/remove instances.
- Batch processing fleets where failed workers must be automatically replaced without operator intervention.
- GKE node pools (GKE manages MIGs internally, but understanding the pattern is useful when using custom node pools).
- Blue-green or canary deploys — MIGs support two template versions at configurable percentages via rolling-action start-update with --canary-version.

## Skip If (ANY kills it)

- Stateful workloads that require per-instance persistent identity (databases, Kafka brokers) — use Stateful MIGs or GKE StatefulSets instead; a standard MIG replaces instances without preserving disk data or network identity.
- Single-VM development machines — MIG overhead is not justified; create the VM directly.
- Workloads with long initialization that cannot tolerate instance replacement — use suspend/resume or ensure the health check initial_delay_sec accounts for full startup time.

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
