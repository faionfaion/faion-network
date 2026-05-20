---
slug: gcp-networking
tier: pro
group: infra
domain: infrastructure-engineer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Comprehensive reference for Google Cloud Platform networking: VPC design, subnets, firewall rules, Cloud NAT, load balancing, and security best practices.
content_id: "65c6821c417faf8d"
tags: [gcp, vpc, networking, firewall, load-balancing]
---
# GCP Networking

## Summary

**One-sentence:** Comprehensive reference for Google Cloud Platform networking: VPC design, subnets, firewall rules, Cloud NAT, load balancing, and security best practices.

**One-paragraph:** Comprehensive reference for Google Cloud Platform networking: VPC design, subnets, firewall rules, Cloud NAT, load balancing, and security best practices. Focus Areas: VPC, subnets, firewall rules, Cloud NAT, load balancing.

## Applies If (ALL must hold)

- Designing or deploying VPC networks for GCP workloads (GKE, Cloud Run, Compute Engine, Cloud SQL).
- Configuring firewall rules with service-account-based filtering for production security.
- Setting up Cloud NAT for private instances to reach the internet without public IPs.
- Implementing global HTTPS load balancers with Cloud Armor, SSL certificates, and CDN.
- Planning Shared VPC architecture for multi-project organizations.
- Troubleshooting GCP connectivity issues (firewall denies, NAT port exhaustion, routing).

## Skip If (ANY kills it)

- Single-VM prototypes where the default VPC is sufficient and network isolation is not required.
- Workloads fully on Cloud Run with no VPC ingress/egress requirements — Cloud Run handles networking at the service level.
- AWS or Azure environments — networking concepts and commands are specific to GCP.

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
