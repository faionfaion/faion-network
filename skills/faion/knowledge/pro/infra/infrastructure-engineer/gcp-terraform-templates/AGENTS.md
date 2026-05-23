---
slug: gcp-terraform-templates
tier: pro
group: infra
domain: infra
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: "Production Terraform module set spec for GCP (VPC, firewall, SA, Cloud Run v2, GKE Autopilot, Cloud SQL, WIF) — produced as a module-manifest config plus root composition."
content_id: "95197cbafa96e038"
complexity: deep
produces: config
est_tokens: 4400
tags: [gcp, terraform, iac, modules, hcl]
---
# GCP Terraform Templates

## Summary

**One-sentence:** Production Terraform module set spec for GCP (VPC, firewall, SA, Cloud Run v2, GKE Autopilot, Cloud SQL, WIF) — produced as a module-manifest config plus root composition.

**One-paragraph:** Production Terraform module set spec for GCP (VPC, firewall, SA, Cloud Run v2, GKE Autopilot, Cloud SQL, WIF) — produced as a module-manifest config plus root composition. The methodology pins the discipline that turns folklore into a reviewable, owned, version-controlled operating artefact: rule-bound output contract, evidence anchors, named owner, published review cadence. Outputs of the wrong shape are rejected at review; outputs without evidence are demoted to hypotheses; outputs without owners are tagged stale.

## Applies If (ALL must hold)

- Bootstrapping a new GCP project with production-grade IaC.
- Adding a Cloud Run / GKE / Cloud SQL component to an existing Terraform root.
- Standardising SA + IAM patterns across teams via shared modules.
- Migrating ad-hoc `gcloud` scripts to versioned Terraform.

## Skip If (ANY kills it)

- Click-ops experiments — use a sandbox project, not Terraform.
- One-shot debug resources — `terraform import` later if they survive.

**Ефективно для:**

- Багатопроектні GCP орги з ≥ 3 env (dev/staging/prod).
- Команди де `gcloud` бан у production.
- Workload-Identity-Federation для CI/CD.
- Cost-controlled bootstraps з Cloud Run + Cloud SQL + GKE Autopilot.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Terraform ≥ 1.7 | binary | platform team |
| Google provider ≥ 5.0 pinned | module config | platform team |
| Remote state bucket (GCS) with object versioning | GCP bucket | platform team |
| Org policies / folder IDs | GCP resource | security team |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/infra/infrastructure-engineer/gcp-security-iam` | IAM + WIF design reused inside modules. |
| `pro/infra/infrastructure-engineer/iac-basics` | Module-design conventions. |

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
| `scripts/validate-gcp-terraform-templates.py` | Validate artefact against the JSON Schema in `content/02-output-contract.xml`. Stdlib-only. | CI on artefact change; pre-commit. |

## Related

- [[gcp-security-iam]]
- [[iac-basics]]
- [[iac-patterns-module-design]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, scope, evidence presence, owner presence, cadence status) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
