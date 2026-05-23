---
slug: gcp-networking
tier: pro
group: infra
domain: infra
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Comprehensive GCP networking reference: VPC design, subnets, firewall rules, Cloud NAT, load balancing, and security best practices for production workloads.
content_id: "f3d63917ff1e001a"
complexity: deep
produces: config
est_tokens: 4100
tags: [gcp, vpc, networking, firewall, load-balancing]
---
# Gcp Networking

## Summary

**One-sentence:** Comprehensive GCP networking reference: VPC design, subnets, firewall rules, Cloud NAT, load balancing, and security best practices for production workloads.

**One-paragraph:** Comprehensive reference for Google Cloud Platform networking: VPC design, subnets, firewall rules, Cloud NAT, load balancing, and security best practices. Focus Areas: VPC, subnets, firewall rules, Cloud NAT, load balancing.

**Ефективно для:**

- Shared VPC між project-ами у одній організації.
- VPC peering / Network Connectivity Center для multi-VPC топологій.
- Cloud NAT для приватних instance-ів з egress до інтернету.
- Global HTTPS Load Balancer з Cloud Armor + CDN.
- Private Service Connect для GCP managed services.

## Applies If (ALL must hold)

- Designing or deploying VPC networks for GCP workloads (GKE, Cloud Run, Compute Engine, Cloud SQL).
- Configuring firewall rules with service-account-based filtering for production security.
- Setting up Cloud NAT for private instances to reach the internet without public IPs.
- Implementing global HTTPS load balancers with Cloud Armor, SSL certificates, and CDN.
- Planning Shared VPC architecture for multi-project organizations.
- Troubleshooting GCP connectivity issues (firewall denies, NAT port exhaustion, routing).

## Skip If (ANY kills it)

- Single-VPC, single-project basics — use `gcp-networking-vpc`.
- K8s-internal networking — use GKE Network Policies.
- Non-GCP networking decisions.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| VPC topology decision | shared VPC / multi-VPC / peering | network owner |
| Egress requirements | Cloud NAT / internet / private | team |
| L7 ingress requirements | regions / SSL / Cloud Armor | security |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[cloud-run-jobs]] | Sibling methodology that supplies context required here. |
| [[cloud-run-monitoring]] | Sibling methodology that supplies context required here. |

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
| `validate-output` | haiku | Mechanical schema validation via `scripts/validate-gcp-networking.py`. |

## Templates

| File | Purpose |
|------|---------|
| `templates/gcp-networking.yaml` | Skeleton for the config artefact this methodology produces. |
| `templates/_smoke-test.yaml` | Minimum viable filled-in example. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-gcp-networking.py` | Validate the config artefact against the JSON Schema in `02-output-contract.xml`. | CI on each artefact change; pre-commit; manual on draft. |

## Related

- [[cloud-run-jobs]]
- [[cloud-run-monitoring]]

## Decision tree

See `content/06-decision-tree.xml`. The tree branches on observable workload / configuration signals and routes to a specific rule id from `01-core-rules.xml`. Use it whenever the input shape is ambiguous between two adjacent methodologies in this sub-skill (e.g. gcp-networking vs an adjacent sibling).
