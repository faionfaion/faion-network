---
slug: gcp-arch-patterns
tier: pro
group: infra
domain: infrastructure-engineer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Production-ready GCP architectural patterns for GKE clusters, Cloud SQL, Cloud Storage with CDN, microservices on Cloud Run, and data pipelines (Dataflow + BigQuery).
content_id: "189f755b238cf652"
tags: [gcp, gke, cloud-sql, cloud-run, architecture]
---
# GCP Architecture Patterns

## Summary

**One-sentence:** Production-ready GCP architectural patterns for GKE clusters, Cloud SQL, Cloud Storage with CDN, microservices on Cloud Run, and data pipelines (Dataflow + BigQuery).

**One-paragraph:** Production-ready GCP architectural patterns for GKE clusters, Cloud SQL, Cloud Storage with CDN, microservices on Cloud Run, and data pipelines (Dataflow + BigQuery). Concrete rules: regional GKE with private nodes, Workload Identity, managed Prometheus; Cloud SQL `availability_type = REGIONAL` with PITR for production; Spot VMs with taints for batch.

## Applies If (ALL must hold)

- Provisioning a new production GKE cluster (regional, private, node-pool strategy).
- Setting up Cloud SQL PostgreSQL with HA, PITR, and read replicas.
- Implementing CDN for static assets via Cloud Storage + Global LB.
- Building microservices with Cloud Run, Pub/Sub, and Secret Manager.
- Designing data pipelines (batch ETL or streaming via Dataflow + BigQuery).
- Migrating from AWS to GCP equivalent services (EKS→GKE, RDS→Cloud SQL, SQS→Pub/Sub).
- Pre-deployment review of an existing GCP environment before a launch or audit.

## Skip If (ANY kills it)

- GCP project hierarchy, IAM, and billing basics — use `gcp-arch-basics`.
- GCP Compute Engine (VMs, instance groups) — use `gcp-compute`.
- GCP networking (VPC, firewall, Cloud NAT) — use `gcp-networking`.
- GCP Cloud Storage lifecycle and CMEK — use `gcp-storage`.
- AWS architecture decisions — use `aws-architecture-services`.

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
