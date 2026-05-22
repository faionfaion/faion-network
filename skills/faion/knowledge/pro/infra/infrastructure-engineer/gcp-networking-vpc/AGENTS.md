---
slug: gcp-networking-vpc
tier: pro
group: infra
domain: infra
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: GCP networking best practices: custom VPC with four subnet tiers (public, private, GKE, database), least-privilege firewall rules with IAP-only SSH, Cloud NAT for private outbound, global HTTPS load balancer with managed SSL, Cloud Armor WAF with OWASP rules and rate limiting, and VPC network checklist.
content_id: "3e704e2da42a60b0"
tags: [gcp, vpc, networking, firewall, cloud-armor]
---
# GCP Networking and VPC

## Summary

**One-sentence:** GCP networking best practices: custom VPC with four subnet tiers (public, private, GKE, database), least-privilege firewall rules with IAP-only SSH, Cloud NAT for private outbound, global HTTPS load balancer with managed SSL, Cloud Armor WAF with OWASP rules and rate limiting, and VPC network checklist.

**One-paragraph:** GCP networking best practices: custom VPC with four subnet tiers (public, private, GKE, database), least-privilege firewall rules with IAP-only SSH, Cloud NAT for private outbound, global HTTPS load balancer with managed SSL, Cloud Armor WAF with OWASP rules and rate limiting, and VPC network checklist.

## Applies If (ALL must hold)

- Creating a new GCP project that will host workloads (VM, GKE, Cloud Run, Cloud SQL).
- Replacing the default VPC with a production-ready custom network.
- Setting up a global HTTPS load balancer with managed SSL certificates.
- Adding WAF protection (XSS, SQLi, rate limiting) via Cloud Armor.
- Auditing firewall rules for public exposure or missing IAP restrictions.

## Skip If (ANY kills it)

- IAM and service account design — use gcp-security-iam instead.
- Compute Engine or GKE cluster creation — use gcp-compute-gke for those specifics.

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
