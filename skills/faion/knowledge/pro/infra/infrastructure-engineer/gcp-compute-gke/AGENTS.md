---
slug: gcp-compute-gke
tier: pro
group: infra
domain: infra
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: GCP Compute Engine and GKE: Shielded VMs, OS Login, regional MIG autoscaling, GKE Autopilot vs Standard hardened clusters, Workload Identity, Dataplane V2, and compute/GKE security checklists.
content_id: "9ff8a9c2514d0220"
complexity: medium
produces: config
est_tokens: 4100
tags: [gcp, compute-engine, gke, kubernetes, autoscaling]
---
# Gcp Compute Gke

## Summary

**One-sentence:** GCP Compute Engine and GKE: Shielded VMs, OS Login, regional MIG autoscaling, GKE Autopilot vs Standard hardened clusters, Workload Identity, Dataplane V2, and compute/GKE security checklists.

**One-paragraph:** Compute Engine and GKE best practices: Shielded VMs with OS Login (no SSH keys), regional managed instance groups with autoscaling and health checks, GKE Autopilot (default) vs hardened Standard clusters with Workload Identity, private endpoints, Dataplane V2 (Cilium), and security hardening checklists.

**Ефективно для:**

- Standard mode GKE з node-pools для prod / batch / spot.
- Autopilot для команд без k8s ops capacity.
- Workload Identity замість node-level SA-keys.
- Managed Prometheus + GKE-native logging.

## Applies If (ALL must hold)

- Provisioning Compute Engine VMs for stateful workloads or legacy applications.
- Setting up regional managed instance groups with autoscaling for web tiers.
- Creating a new GKE cluster (Autopilot recommended for most use cases).
- Hardening an existing GKE Standard cluster (Workload Identity, private nodes, network policy).
- Reviewing compute or GKE security posture against checklists.

## Skip If (ANY kills it)

- Single-service deployment that fits Cloud Run.
- Tiny workload without k8s operational capacity.
- Non-containerised legacy app — use GCE instead.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Workload size | node count / pod count estimate | capacity planner |
| Ops capacity | team SRE coverage level | engineering manager |
| Networking design | VPC + subnets + Private Services | network owner |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[gcp-networking-vpc]] | Sibling methodology that supplies context required here. |
| [[gcp-security-iam]] | Sibling methodology that supplies context required here. |

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
| `validate-output` | haiku | Mechanical schema validation via `scripts/validate-gcp-compute-gke.py`. |

## Templates

| File | Purpose |
|------|---------|
| `templates/gcp-compute-gke.yaml` | Skeleton for the config artefact this methodology produces. |
| `templates/_smoke-test.yaml` | Minimum viable filled-in example. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-gcp-compute-gke.py` | Validate the config artefact against the JSON Schema in `02-output-contract.xml`. | CI on each artefact change; pre-commit; manual on draft. |

## Related

- [[gcp-networking-vpc]]
- [[gcp-security-iam]]
- [[gcp-cloud-run-serverless]]

## Decision tree

See `content/06-decision-tree.xml`. The tree branches on observable workload / configuration signals and routes to a specific rule id from `01-core-rules.xml`. Use it whenever the input shape is ambiguous between two adjacent methodologies in this sub-skill (e.g. gcp-compute-gke vs an adjacent sibling).
