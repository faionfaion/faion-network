---
slug: cloud-run-vpc-access
tier: pro
group: infra
domain: infrastructure-engineer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Cloud Run services connect to private VPC resources via Direct VPC egress (preferred) or Serverless VPC Access connectors.
content_id: "8c4eaf26ce55f16d"
tags: [gcp, cloud-run, vpc, networking, sidecars]
---
# Cloud Run VPC Access and Multi-Container

## Summary

**One-sentence:** Cloud Run services connect to private VPC resources via Direct VPC egress (preferred) or Serverless VPC Access connectors.

**One-paragraph:** Cloud Run services connect to private VPC resources via Direct VPC egress (preferred) or Serverless VPC Access connectors. Direct VPC egress provides 2x throughput, lower cost, and lower latency compared to connectors. Multi-container support (up to 10 containers per instance) enables sidecar patterns for database proxies, observability agents, and security middleware.

## Applies If (ALL must hold)

- Connecting a Cloud Run service to private Cloud SQL, AlloyDB, or Memorystore (Redis).
- Reaching internal GCP services or on-premises resources via VPN/Interconnect.
- Adding Cloud SQL Proxy sidecar to avoid IAP or public Cloud SQL IP exposure.
- Adding OpenTelemetry collector sidecar for metrics and tracing.
- Migrating from Serverless VPC Access connectors to Direct VPC egress.
- Restricting Cloud Run ingress to internal load balancer only.

## Skip If (ANY kills it)

- Services that only access public internet APIs — no VPC egress needed.
- VPC architecture and subnet design — see gcp-networking-vpc.
- General Cloud Run service deployment — see cloud-run-deployment.

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
