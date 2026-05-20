---
slug: gce-instance-templates
tier: pro
group: infra
domain: infrastructure-engineer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Instance templates are immutable, reusable VM configurations that define machine type, boot disk image, network settings, service account, labels, and startup/shutdown scripts.
content_id: "b9230d345b11e1b8"
tags: [gcp, compute-engine, instance-templates, infrastructure-as-code]
---
# GCE Instance Templates

## Summary

**One-sentence:** Instance templates are immutable, reusable VM configurations that define machine type, boot disk image, network settings, service account, labels, and startup/shutdown scripts.

**One-paragraph:** Instance templates are immutable, reusable VM configurations that define machine type, boot disk image, network settings, service account, labels, and startup/shutdown scripts. Every Managed Instance Group (MIG) requires an instance template; standalone VMs benefit from templates for consistency. Always version templates by name and use image families, not specific image versions, to get automatic security patches.

## Applies If (ALL must hold)

- Creating a Managed Instance Group — MIGs require an instance template, no exceptions.
- Deploying multiple VMs with identical configuration in different zones or for autoscaling.
- Rolling out application version updates across a fleet without downtime (create new template, update MIG).
- Canary deployments — MIGs support two template versions simultaneously at configurable percentages.
- Building a custom machine image baked with pre-installed software to reduce startup time from minutes to seconds.

## Skip If (ANY kills it)

- One-off diagnostic or short-lived VMs — the overhead of template creation exceeds the value; use gcloud directly.
- VMs with highly individualized configurations that differ per instance — templates require all VMs to start from the same base; per-instance divergence belongs in startup scripts reading instance metadata.

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
