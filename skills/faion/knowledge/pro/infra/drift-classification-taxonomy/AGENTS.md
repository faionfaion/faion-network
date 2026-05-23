---
slug: drift-classification-taxonomy
tier: pro
group: infra
domain: infra
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: "Closed taxonomy for infrastructure drift causes (hand-edit, external automation, vendor change, legitimate-emergency, unknown) so terraform plan diffs route to the right fix path instead of being silently re-applied."
content_id: "0b9e40ee6dce73c7"
complexity: medium
produces: rubric
est_tokens: 3700
tags: [infra, pro, drift, terraform, taxonomy]
---

# Drift Classification Taxonomy

## Summary

**One-sentence:** Closed taxonomy for infrastructure drift causes (hand-edit, external automation, vendor change, legitimate-emergency, unknown) so terraform plan diffs route to the right fix path instead of being silently re-applied.

**One-paragraph:** Drift detection tools surface 'something differs' but stop there. Teams default to 'terraform apply and call it done', which loses the emergency fix the on-call applied to production at 3 AM. A taxonomy classifies each drift by cause: hand-edit (someone clicked in the console), external-automation (a different tool wrote to the same resource), vendor-change (cloud provider changed defaults), legitimate-emergency (on-call hotfix that needs to be backported), unknown. Each class routes to a different fix path: hand-edit → revert + train; emergency → backport to HCL; external-automation → boundary review; vendor → bump provider; unknown → triage. Output: drift-classification.yaml per environment + a weekly drift triage cadence.

**Ефективно для:**

- Drift diff не 'apply and forget'; classify → route → fix.
- Legitimate emergency drift backported в HCL замість 're-applied away'.
- Hand-edit drift тренує команду на CI-only apply discipline.
- Vendor-default drift тригерить provider bump замість silent override.

## Applies If (ALL must hold)

- Terraform / Pulumi codebase managing infra in production
- Drift detection runs (weekly plan job or continuous via TF Cloud)
- Multiple humans + tools touch the same resources (otherwise drift is rare)
- Compliance asks for evidence of drift triage

## Skip If (ANY kills it)

- Single-engineer single-tool setup with no drift over 30 days — overhead not justified
- Greenfield without yet-deployed resources — drift will surface later, not now

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Terraform plan + diff history | CI artifacts | platform team |
| Audit log access (cloud activity / change history) | credentials | platform team |
| Triage ritual slot (weekly) | team calendar | platform team |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[terraform]] | Drift detection presupposes Terraform with remote state |
| [[greenfield-infra-decision-matrix]] | Tool choice context |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules with rationale + source | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid/forbidden examples | ~800 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns with symptom/root-cause/fix | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure with input/action/output | ~700 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `evidence_search` | sonnet | Audit-log scan + correlation |
| `class_routing` | haiku | Mechanical lookup once evidence known |
| `backport_pr_draft` | sonnet | HCL synthesis from console state |

## Templates

| File | Purpose |
|------|---------|
| `templates/skeleton.json` | Skeleton template |
| `templates/skeleton.md` | Skeleton template |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-drift-classification-taxonomy.py` | Validate the artefact against the output-contract schema | Pre-commit; on artefact write |

## Related

- [[terraform]]
- [[terraform-iac]]
- [[greenfield-infra-decision-matrix]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, scope, scale) to a concrete action, each leaf referencing a rule id from `01-core-rules.xml`. Use it before applying any other section of the methodology to confirm scope and pick the right variant.
