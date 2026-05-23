---
slug: gce-managed-instance-groups
tier: pro
group: infra
domain: infra
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Deploy and operate GCE Managed Instance Groups (MIGs) for production: regional vs zonal placement, health checks, autohealing, rolling updates, and canary deployments.
content_id: "d5a4b65f7600774f"
complexity: medium
produces: config
est_tokens: 4100
tags: [gcp, compute-engine, managed-instance-groups, high-availability]
---
# Gce Managed Instance Groups

## Summary

**One-sentence:** Deploy and operate GCE Managed Instance Groups (MIGs) for production: regional vs zonal placement, health checks, autohealing, rolling updates, and canary deployments.

**One-paragraph:** A Managed Instance Group (MIG) maintains a set of identical VMs created from a single instance template, provides autohealing by replacing failed instances, supports rolling updates and canary deployments, and integrates with Google Cloud Load Balancing. Use regional MIGs (multi-zone) for all production workloads; zonal MIGs are acceptable only for dev/test or cost-sensitive batch jobs.

**Ефективно для:**

- Regional MIG із multi-zone розподілом для HA.
- Rolling updates через Updater з maxSurge/maxUnavailable.
- Auto-healing через HTTP health-check + initial-delay для бутстрапу.
- Per-instance configs для канаркового rollout у MIG.

## Applies If (ALL must hold)

- Any stateless production service that needs more than one VM — regional MIG with minimum 3 instances (one per zone).
- Autoscaling web applications or APIs — MIG is required for the autoscaler to add/remove instances.
- Batch processing fleets where failed workers must be automatically replaced without operator intervention.
- GKE node pools (GKE manages MIGs internally, but understanding the pattern is useful when using custom node pools).
- Blue-green or canary deploys — MIGs support two template versions at configurable percentages via rolling-action start-update with --canary-version.

## Skip If (ANY kills it)

- Single-VM workload with no need for HA/auto-heal.
- GKE — use Kubernetes Deployments/StatefulSets.
- Cloud Run / serverless workloads.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Instance template (versioned) | GCE instance template | from `gce-instance-templates` |
| Health check | HTTP/HTTPS/TCP | team |
| Placement strategy | regional vs zonal | team |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[gce-instance-templates]] | Sibling methodology that supplies context required here. |
| [[gce-autoscaling]] | Sibling methodology that supplies context required here. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules with statement + rationale + source | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid/forbidden | ~800 |
| `content/03-failure-modes.xml` | essential | Antipatterns with symptom/root-cause/fix | ~800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with input/action/output | ~900 |
| `content/06-decision-tree.xml` | essential | Routing tree → rule id from 01-core-rules | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-applicability` | sonnet | Decision tree application — needs nuance + context awareness. |
| `draft-config` | sonnet | Light judgement on field selection + naming conventions. |
| `validate-output` | haiku | Mechanical schema validation via `scripts/validate-gce-managed-instance-groups.py`. |

## Templates

| File | Purpose |
|------|---------|
| `templates/gce-managed-instance-groups.yaml` | Skeleton for the config artefact this methodology produces. |
| `templates/_smoke-test.yaml` | Minimum viable filled-in example. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-gce-managed-instance-groups.py` | Validate the config artefact against the JSON Schema in `02-output-contract.xml`. | CI on each artefact change; pre-commit; manual on draft. |

## Related

- [[gce-instance-templates]]
- [[gce-autoscaling]]
- [[gce-spot-vms]]

## Decision tree

See `content/06-decision-tree.xml`. The tree branches on observable workload / configuration signals and routes to a specific rule id from `01-core-rules.xml`. Use it whenever the input shape is ambiguous between two adjacent methodologies in this sub-skill (e.g. gce-managed-instance-groups vs an adjacent sibling).
