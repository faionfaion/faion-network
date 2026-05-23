---
slug: terraform-iac
tier: pro
group: infra
domain: infra
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: "Terraform IaC architecture spec: module composition pattern, state-isolation per environment, monorepo vs polyrepo decision, blast-radius limits per workspace, refactor playbook for legacy resources."
content_id: "c4df8d324b529589"
complexity: medium
produces: spec
est_tokens: 3800
tags: [terraform, infrastructure-as-code, iac, modules, state-management]
---

# Terraform IaC

## Summary

**One-sentence:** Terraform IaC architecture spec: module composition pattern, state-isolation per environment, monorepo vs polyrepo decision, blast-radius limits per workspace, refactor playbook for legacy resources.

**One-paragraph:** terraform-iac sits above 'terraform' (the tool) and covers the architecture: how to lay out state across envs, where modules live, how to isolate blast radius, how to refactor legacy resources without state surgery causing outage. The standard pattern: one workspace per (env, layer), modules in a registry, state isolated so a prod apply cannot touch dev. Refactor uses moved blocks (TF >=1.1) instead of state rm/import gymnastics. This methodology codifies the layout + the boundary rules + the refactor playbook.

**Ефективно для:**

- Workspace per (env, layer) — prod apply не може зачепити dev.
- Module registry замість copy-paste між проєктами.
- Refactor через moved blocks замість state rm + import dance.
- Blast radius per workspace: 'один apply, один scope'.

## Applies If (ALL must hold)

- Multiple envs (dev / staging / prod) sharing a Terraform codebase
- Multiple infra layers (network / data / compute / app) with different change cadences
- Legacy resources need refactoring (moved blocks, import)
- Compliance requires explicit blast-radius limits

## Skip If (ANY kills it)

- Single-env single-layer infra — 'terraform' methodology alone is enough
- Hand-off-only project where the consumer will rewrite the layout

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Existing Terraform setup | repo + state backend | platform team |
| Module registry (Terraform Registry / Artifactory) | registry credentials | platform team |
| Terraform >=1.5 | binary version | DevOps lead |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[terraform]] | Tool fundamentals — pinning, remote state, CI apply |
| [[drift-classification-taxonomy]] | How drift gets surfaced + classified |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules with rationale + source | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid/forbidden examples | ~800 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom/root-cause/fix | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure with input/action/output | ~700 |
| `content/05-examples.xml` | medium | Worked example end-to-end | ~500 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `workspace_split_plan` | opus | Cross-resource impact judgment |
| `module_extraction` | sonnet | HCL refactor |
| `blast_radius_writeup` | sonnet | Concise structured writing |

## Templates

| File | Purpose |
|------|---------|
| `templates/backend-s3.tf` | Backend s3 template |
| `templates/github-actions.yml` | Github actions template |
| `templates/modules-vpc.tf` | Modules vpc template |
| `templates/variables.tf` | Variables template |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-terraform-iac.py` | Validate the artefact against the output-contract schema | Pre-commit; on artefact write |

## Related

- [[terraform]]
- [[drift-classification-taxonomy]]
- [[greenfield-infra-decision-matrix]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, scope, scale) to a concrete action, each leaf referencing a rule id from `01-core-rules.xml`. Use it before applying any other section of the methodology to confirm scope and pick the right variant.
