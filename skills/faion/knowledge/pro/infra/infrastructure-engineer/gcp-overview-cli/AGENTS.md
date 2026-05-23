---
slug: gcp-overview-cli
tier: pro
group: infra
domain: infra
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: GCP service overview, gcloud CLI setup, authentication, configuration management, CI/CD deployment patterns, disaster recovery, and cost optimization commands.
content_id: "b0745e97fc3b4d85"
complexity: light
produces: checklist
est_tokens: 3200
tags: [gcp, gcloud, cli, deployment, cost-optimization]
---
# Gcp Overview Cli

## Summary

**One-sentence:** GCP service overview, gcloud CLI setup, authentication, configuration management, CI/CD deployment patterns, disaster recovery, and cost optimization commands.

**One-paragraph:** Google Cloud Platform infrastructure best practices (2025-2026): service catalogue, gcloud CLI setup, authentication, named configurations, CI/CD deployment patterns, disaster recovery, and cost optimization using Recommender and BigQuery billing exports.

**Ефективно для:**

- Швидкий старт з gcloud CLI: projects, auth, config-configurations.
- Service-account impersonation у локальній dev-сесії.
- Application Default Credentials для SDK / Terraform / клієнтських бібліотек.
- Per-environment configurations (gcloud config configurations).

## Applies If (ALL must hold)

- Setting up a new GCP project or onboarding a developer to an existing project.
- Establishing CI/CD pipelines that build, push, and deploy container images.
- Selecting the right GCP service for a given workload type (VM vs serverless vs GKE).
- Running cost audits or finding idle resources via Recommender.
- Configuring disaster recovery across regions for Compute Engine or Cloud SQL.

## Skip If (ANY kills it)

- Programmatic SDK usage — use the language client library directly.
- Terraform / Pulumi workflows — use IaC methodologies.
- GUI-only Cloud Console workflows.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| gcloud install | gcloud binary on PATH | developer machine |
| Target environment(s) | list of project ids | team |
| Service-account impersonation target (if any) | SA email | IAM owner |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[gcp-security-iam]] | Sibling methodology that supplies context required here. |
| [[gcp-networking-vpc]] | Sibling methodology that supplies context required here. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules with statement + rationale + source | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid/forbidden | ~800 |
| `content/03-failure-modes.xml` | essential | Antipatterns with symptom/root-cause/fix | ~800 |
| `content/06-decision-tree.xml` | essential | Routing tree → rule id from 01-core-rules | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-applicability` | sonnet | Decision tree application — needs nuance + context awareness. |
| `draft-checklist` | sonnet | Light judgement on field selection + naming conventions. |
| `validate-output` | haiku | Mechanical schema validation via `scripts/validate-gcp-overview-cli.py`. |

## Templates

| File | Purpose |
|------|---------|
| `templates/gcp-overview-cli.md` | Skeleton for the checklist artefact this methodology produces. |
| `templates/_smoke-test.md` | Minimum viable filled-in example. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-gcp-overview-cli.py` | Validate the checklist artefact against the JSON Schema in `02-output-contract.xml`. | CI on each artefact change; pre-commit; manual on draft. |

## Related

- [[gcp-security-iam]]
- [[gcp-networking-vpc]]
- [[gcp-compute-gke]]
- [[gcp-cloud-run-serverless]]
- [[gcp-terraform-templates]]

## Decision tree

See `content/06-decision-tree.xml`. The tree branches on observable workload / configuration signals and routes to a specific rule id from `01-core-rules.xml`. Use it whenever the input shape is ambiguous between two adjacent methodologies in this sub-skill (e.g. gcp-overview-cli vs an adjacent sibling).
