---
slug: gcp-networking-vpc
tier: pro
group: infra
domain: infra
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: GCP networking: custom VPC with three-tier subnets, firewall rules (least privilege), Cloud NAT, global HTTPS load balancer, Cloud Armor WAF, VPC Service Controls perimeter, and networking checklists.
content_id: "ac517b5688da5887"
complexity: medium
produces: config
est_tokens: 4100
tags: [gcp, vpc, networking, firewall, cloud-armor]
---
# Gcp Networking Vpc

## Summary

**One-sentence:** GCP networking: custom VPC with three-tier subnets, firewall rules (least privilege), Cloud NAT, global HTTPS load balancer, Cloud Armor WAF, VPC Service Controls perimeter, and networking checklists.

**One-paragraph:** GCP networking best practices: custom VPC with four subnet tiers (public, private, GKE, database), least-privilege firewall rules with IAP-only SSH, Cloud NAT for private outbound, global HTTPS load balancer with managed SSL, Cloud Armor WAF with OWASP rules and rate limiting, and VPC network checklist.

**Ефективно для:**

- Custom VPC з регіональними subnet-ами замість auto-mode.
- Firewall rules per-service-account замість per-tag (де можливо).
- Hierarchical firewall policies на org/folder level.
- VPC flow logs + Packet Mirroring для security observability.

## Applies If (ALL must hold)

- Creating a new GCP project that will host workloads (VM, GKE, Cloud Run, Cloud SQL).
- Replacing the default VPC with a production-ready custom network.
- Setting up a global HTTPS load balancer with managed SSL certificates.
- Adding WAF protection (XSS, SQLi, rate limiting) via Cloud Armor.
- Auditing firewall rules for public exposure or missing IAP restrictions.

## Skip If (ANY kills it)

- Multi-VPC / inter-org topologies — use `gcp-networking`.
- K8s service-mesh decisions.
- Cloud Run egress — use `cloud-run-vpc-access`.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| VPC mode | auto / custom | network owner |
| Subnet plan | regions + CIDR blocks | network owner |
| Firewall basis | service-account vs tag | security |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[gcp-security-iam]] | Sibling methodology that supplies context required here. |
| [[gcp-compute-gke]] | Sibling methodology that supplies context required here. |

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
| `validate-output` | haiku | Mechanical schema validation via `scripts/validate-gcp-networking-vpc.py`. |

## Templates

| File | Purpose |
|------|---------|
| `templates/gcp-networking-vpc.yaml` | Skeleton for the config artefact this methodology produces. |
| `templates/_smoke-test.yaml` | Minimum viable filled-in example. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-gcp-networking-vpc.py` | Validate the config artefact against the JSON Schema in `02-output-contract.xml`. | CI on each artefact change; pre-commit; manual on draft. |

## Related

- [[gcp-security-iam]]
- [[gcp-compute-gke]]
- [[gcp-cloud-run-serverless]]

## Decision tree

See `content/06-decision-tree.xml`. The tree branches on observable workload / configuration signals and routes to a specific rule id from `01-core-rules.xml`. Use it whenever the input shape is ambiguous between two adjacent methodologies in this sub-skill (e.g. gcp-networking-vpc vs an adjacent sibling).
