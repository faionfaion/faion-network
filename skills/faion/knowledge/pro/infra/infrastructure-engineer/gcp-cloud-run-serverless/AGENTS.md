---
slug: gcp-cloud-run-serverless
tier: pro
group: infra
domain: infrastructure-engineer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Cloud Run and Cloud Functions Gen2 best practices: deploy with a dedicated service account, Secret Manager secrets, VPC connector for private resource access, min-instances for production cold-start elimination, blue-green traffic splitting for safe rollouts, and Binary Authorization for image trust.
content_id: "4a540f131864a5ec"
tags: [gcp, cloud-run, serverless, cloud-functions, blue-green]
---
# GCP Cloud Run and Serverless

## Summary

**One-sentence:** Cloud Run and Cloud Functions Gen2 best practices: deploy with a dedicated service account, Secret Manager secrets, VPC connector for private resource access, min-instances for production cold-start elimination, blue-green traffic splitting for safe rollouts, and Binary Authorization for image trust.

**One-paragraph:** Cloud Run and Cloud Functions Gen2 best practices: deploy with a dedicated service account, Secret Manager secrets, VPC connector for private resource access, min-instances for production cold-start elimination, blue-green traffic splitting for safe rollouts, and Binary Authorization for image trust.

## Applies If (ALL must hold)

- Deploying a containerized stateless API or web application on Cloud Run.
- Setting up Cloud Functions Gen2 for HTTP triggers or Pub/Sub event processing.
- Configuring blue-green or canary releases for a Cloud Run service.
- Adding VPC connector to reach private Cloud SQL or internal services.
- Auditing Cloud Run service security configuration.

## Skip If (ANY kills it)

- Stateful workloads or long-running background jobs — use Compute Engine or GKE.
- Workloads requiring DaemonSets, host network access, or custom node config — use GKE Standard.
- VPC and firewall configuration — use gcp-networking-vpc.

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
