---
slug: gce-instance-templates
tier: pro
group: infra
domain: infra
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Design, version, and manage GCE instance templates as the single source of truth for VM configuration in Managed Instance Groups and standalone deployments.
content_id: "4485d67d57eb8351"
complexity: medium
produces: config
est_tokens: 4100
tags: [gcp, compute-engine, instance-templates, infrastructure-as-code]
---
# Gce Instance Templates

## Summary

**One-sentence:** Design, version, and manage GCE instance templates as the single source of truth for VM configuration in Managed Instance Groups and standalone deployments.

**One-paragraph:** Instance templates are immutable, reusable VM configurations that define machine type, boot disk image, network settings, service account, labels, and startup/shutdown scripts. Every Managed Instance Group (MIG) requires an instance template; standalone VMs benefit from templates for consistency. Always version templates by name and use image families, not specific image versions, to get automatic security patches.

**Ефективно для:**

- Версіоновані instance templates (immutable) як основа MIG.
- Startup script + образ із pre-installed agent для бутстрапу VM.
- Service account з мінімальним scope + metadata-driven config.
- OS Login + IAP замість SSH-ключів у metadata.

## Applies If (ALL must hold)

- Creating a Managed Instance Group — MIGs require an instance template, no exceptions.
- Deploying multiple VMs with identical configuration in different zones or for autoscaling.
- Rolling out application version updates across a fleet without downtime (create new template, update MIG).
- Canary deployments — MIGs support two template versions simultaneously at configurable percentages.
- Building a custom machine image baked with pre-installed software to reduce startup time from minutes to seconds.

## Skip If (ANY kills it)

- One-off VM that won't be replicated — create instance directly.
- GKE node-pool template — managed by GKE, not GCE template.
- Cloud Run / Cloud Functions deployment.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Image | GCE image / family | platform team |
| Service account | least-privilege SA | IAM owner |
| Startup script | shell or cloud-init | team |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[gce-managed-instance-groups]] | Sibling methodology that supplies context required here. |
| [[gce-spot-vms]] | Sibling methodology that supplies context required here. |

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
| `validate-output` | haiku | Mechanical schema validation via `scripts/validate-gce-instance-templates.py`. |

## Templates

| File | Purpose |
|------|---------|
| `templates/gce-instance-templates.yaml` | Skeleton for the config artefact this methodology produces. |
| `templates/_smoke-test.yaml` | Minimum viable filled-in example. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-gce-instance-templates.py` | Validate the config artefact against the JSON Schema in `02-output-contract.xml`. | CI on each artefact change; pre-commit; manual on draft. |

## Related

- [[gce-managed-instance-groups]]
- [[gce-spot-vms]]
- [[gcp-terraform-templates]]

## Decision tree

See `content/06-decision-tree.xml`. The tree branches on observable workload / configuration signals and routes to a specific rule id from `01-core-rules.xml`. Use it whenever the input shape is ambiguous between two adjacent methodologies in this sub-skill (e.g. gce-instance-templates vs an adjacent sibling).
