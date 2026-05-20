---
slug: gcp-overview-cli
tier: pro
group: infra
domain: infrastructure-engineer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Google Cloud Platform infrastructure best practices (2025-2026): service catalogue, gcloud CLI setup, authentication, named configurations, CI/CD deployment patterns, disaster recovery, and cost optimization using Recommender and BigQuery billing exports.
content_id: "854681efa98aa54b"
tags: [gcp, gcloud, cli, deployment, cost-optimization]
---
# GCP Infrastructure Overview and CLI

## Summary

**One-sentence:** Google Cloud Platform infrastructure best practices (2025-2026): service catalogue, gcloud CLI setup, authentication, named configurations, CI/CD deployment patterns, disaster recovery, and cost optimization using Recommender and BigQuery billing exports.

**One-paragraph:** Google Cloud Platform infrastructure best practices (2025-2026): service catalogue, gcloud CLI setup, authentication, named configurations, CI/CD deployment patterns, disaster recovery, and cost optimization using Recommender and BigQuery billing exports.

## Applies If (ALL must hold)

- Setting up a new GCP project or onboarding a developer to an existing project.
- Establishing CI/CD pipelines that build, push, and deploy container images.
- Selecting the right GCP service for a given workload type (VM vs serverless vs GKE).
- Running cost audits or finding idle resources via Recommender.
- Configuring disaster recovery across regions for Compute Engine or Cloud SQL.

## Skip If (ANY kills it)

- Deep IAM / network hardening — use gcp-security-iam and gcp-networking-vpc instead.
- Terraform IaC templates — use gcp-terraform-templates instead.
- LLM prompt generation for GCP tasks — use gcp-llm-prompts instead.

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
