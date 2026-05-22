---
slug: gcp-network-architecture
tier: pro
group: infra
domain: infra
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: GCP networking centers on VPC design (Single, Shared, Hub-and-Spoke), IP address planning for GKE secondary ranges, Private Service Connect for private Google API access, Cloud NAT for egress, and hierarchical firewall policies for org-wide security.
content_id: "1cba3f48bfbdfaca"
tags: [gcp, vpc, networking, terraform, shared-vpc]
---
# GCP Network Architecture Patterns

## Summary

**One-sentence:** GCP networking centers on VPC design (Single, Shared, Hub-and-Spoke), IP address planning for GKE secondary ranges, Private Service Connect for private Google API access, Cloud NAT for egress, and hierarchical firewall policies for org-wide security.

**One-paragraph:** GCP networking centers on VPC design (Single, Shared, Hub-and-Spoke), IP address planning for GKE secondary ranges, Private Service Connect for private Google API access, Cloud NAT for egress, and hierarchical firewall policies for org-wide security. Shared VPC is the standard pattern for multi-project environments.

## Applies If (ALL must hold)

- Designing a multi-project GCP environment — use Shared VPC to centralize network control.
- Deploying GKE clusters — plan pod and service secondary CIDR ranges before creating subnets.
- Private instances needing Google API access (Cloud SQL, Storage, BigQuery) — use Private Service Connect.
- Private instances needing internet egress without public IPs — use Cloud NAT.
- Enterprise environments with on-premises connectivity — design hub-and-spoke topology with VPN or Interconnect.

## Skip If (ANY kills it)

- Single-project sandbox environments — Shared VPC overhead is not justified; use a simple single VPC.
- Fully public serverless workloads (Cloud Run with default networking) — VPC plumbing adds complexity with no benefit.

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
