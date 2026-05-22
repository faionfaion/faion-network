---
slug: gcp-compute-gke
tier: pro
group: infra
domain: infra
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Compute Engine and GKE best practices: Shielded VMs with OS Login (no SSH keys), regional managed instance groups with autoscaling and health checks, GKE Autopilot (default) vs hardened Standard clusters with Workload Identity, private endpoints, Dataplane V2 (Cilium), and security hardening checklists.
content_id: "8b89b3403da94fda"
tags: [gcp, compute-engine, gke, kubernetes, autoscaling]
---
# GCP Compute Engine and GKE

## Summary

**One-sentence:** Compute Engine and GKE best practices: Shielded VMs with OS Login (no SSH keys), regional managed instance groups with autoscaling and health checks, GKE Autopilot (default) vs hardened Standard clusters with Workload Identity, private endpoints, Dataplane V2 (Cilium), and security hardening checklists.

**One-paragraph:** Compute Engine and GKE best practices: Shielded VMs with OS Login (no SSH keys), regional managed instance groups with autoscaling and health checks, GKE Autopilot (default) vs hardened Standard clusters with Workload Identity, private endpoints, Dataplane V2 (Cilium), and security hardening checklists.

## Applies If (ALL must hold)

- Provisioning Compute Engine VMs for stateful workloads or legacy applications.
- Setting up regional managed instance groups with autoscaling for web tiers.
- Creating a new GKE cluster (Autopilot recommended for most use cases).
- Hardening an existing GKE Standard cluster (Workload Identity, private nodes, network policy).
- Reviewing compute or GKE security posture against checklists.

## Skip If (ANY kills it)

- Containerized stateless applications — prefer Cloud Run (use gcp-cloud-run-serverless).
- VPC and firewall configuration — use gcp-networking-vpc for that layer.
- IAM service accounts and Workload Identity pool setup — covered in gcp-security-iam.

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
