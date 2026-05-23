---
slug: gcp-storage
tier: pro
group: infra
domain: infra
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: "Cloud Storage bucket spec (config artefact): storage class, lifecycle rules, CMEK, IAM bindings, retention, Cloud CDN attach — produced as Terraform-ready JSON."
content_id: "8632766c3e142e78"
complexity: medium
produces: config
est_tokens: 4000
tags: [gcp, cloud-storage, storage-classes, lifecycle, cmek]
---
# GCP Cloud Storage

## Summary

**One-sentence:** Cloud Storage bucket spec (config artefact): storage class, lifecycle rules, CMEK, IAM bindings, retention, Cloud CDN attach — produced as Terraform-ready JSON.

**One-paragraph:** Cloud Storage bucket spec (config artefact): storage class, lifecycle rules, CMEK, IAM bindings, retention, Cloud CDN attach — produced as Terraform-ready JSON. The methodology pins the discipline that turns folklore into a reviewable, owned, version-controlled operating artefact: rule-bound output contract, evidence anchors, named owner, published review cadence. Outputs of the wrong shape are rejected at review; outputs without evidence are demoted to hypotheses; outputs without owners are tagged stale.

## Applies If (ALL must hold)

- Designing a new Cloud Storage bucket for production data.
- Adding lifecycle rules to migrate cold data Nearline → Coldline → Archive.
- Attaching Cloud CDN in front of a bucket for global static-asset delivery.
- Switching a bucket to CMEK + uniform bucket-level access.

## Skip If (ANY kills it)

- Multi-region active-active writes — use Firestore / Spanner instead.
- Streaming ordered ingest — use Pub/Sub + Dataflow, not GCS.

**Ефективно для:**

- Об'єкти > 100MB що read-heavy і потребують CDN.
- Backups з clear hot→cold lifecycle (≤ Std 30d → Nearline 90d → Coldline 365d → Archive).
- BigQuery / Vertex AI data lakes з регіональним co-location.
- Compliance-driven workloads з CMEK + retention policy.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Bucket-naming spec | string | platform team |
| Storage-class decision matrix | table | FinOps + data team |
| KMS keyring (for CMEK) | GCP resource | security team |
| IAM principal list | list | team RACI |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/infra/infrastructure-engineer/gcp-security-iam` | CMEK + IAM perimeter conventions reused. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid/forbidden examples | 900 |
| `content/03-failure-modes.xml` | essential | Antipatterns with symptom / root-cause / fix | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure to apply the methodology end-to-end | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals -> rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scaffold-config` | haiku | Mechanical template fill from prerequisites table. |
| `populate-policy` | sonnet | Per-clause translation into config fields with judgment. |
| `review-breach-cases` | opus | Cross-engagement risk + failure-mode synthesis. |

## Templates

| File | Purpose |
|------|---------|
| `templates/config.json` | Config skeleton matching the output schema. |
| `templates/_smoke-test.json` | Minimum viable filled artefact. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-gcp-storage.py` | Validate artefact against the JSON Schema in `content/02-output-contract.xml`. Stdlib-only. | CI on artefact change; pre-commit. |

## Related

- [[gcp-security-iam]]
- [[gcp-terraform-templates]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, scope, evidence presence, owner presence, cadence status) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
