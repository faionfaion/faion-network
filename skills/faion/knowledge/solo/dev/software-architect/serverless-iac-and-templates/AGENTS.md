---
slug: serverless-iac-and-templates
tier: solo
group: dev
domain: architecture
version: 1.0.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: IaC blueprint for a serverless stack: SAM / CDK / Serverless Framework / Pulumi / Terraform choice, parameterised template with env-aware stages, deployment pipeline, drift detection.
content_id: "78c0522112227665"
complexity: medium
produces: config
est_tokens: 4300
tags: [serverless, iac, sam, cdk, terraform]
---
# Serverless IaC and Templates

## Summary

**One-sentence:** IaC blueprint for a serverless stack: SAM / CDK / Serverless Framework / Pulumi / Terraform choice, parameterised template with env-aware stages, deployment pipeline, drift detection.

**One-paragraph:** IaC blueprint for a serverless stack: SAM / CDK / Serverless Framework / Pulumi / Terraform choice, parameterised template with env-aware stages, deployment pipeline, drift detection. Decision tree, output contract, failure modes, and a procedure (when complexity ≥ medium) live under `content/`. Templates in `templates/` start with a 5-line `__faion_header__` block; the validator script in `scripts/` is stdlib-only with `--help` and `--self-test`.

**Ефективно для:**

- New serverless project moving from prototype to production-ready IaC.
- Existing serverless stack with console drift or missing parameterisation.
- Multi-environment (dev / staging / prod) deployment about to be set up.
- Output produces `config` matching the schema in `content/02-output-contract.xml`.

## Applies If (ALL must hold)

- New serverless project moving from prototype to production-ready IaC.
- Existing serverless stack with console drift or missing parameterisation.
- Multi-environment (dev / staging / prod) deployment about to be set up.

## Skip If (ANY kills it)

- Throwaway experiment with no operational expectations.
- Single-function service already managed by an existing IaC pattern; no change in scope.
- Migration to containers / VMs already approved; IaC effort would be wasted.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Resource inventory (functions, queues, tables, IAM) | list | team |
| Cloud provider account + region(s) | field | ops |
| Environment list (dev / staging / prod) + stage naming | doc | ops |
| Existing IaC tool standard (if any) | doc | platform |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[solo/dev/software-architect/serverless-foundations]] | Foundations checklist precedes IaC investment. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 7 testable rules (incl. skip-this-methodology) with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid example + invalid example + forbidden traits | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom + root-cause + fix | 800 |
| `content/04-procedure.xml` | essential | 6-step end-to-end procedure with input/action/output per step | 900 |
| `content/06-decision-tree.xml` | essential | Root question + observable branches → conclusion(ref=rule-id); skip leaf always reachable | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `pick-tool` | sonnet | Bounded choice: SAM / CDK / Serverless Framework / Pulumi / Terraform. |
| `scaffold-template` | sonnet | Generate parameterised template with stage / env support. |
| `wire-pipeline` | sonnet | Author CI deployment pipeline + drift detection job. |

## Templates

| File | Purpose |
|------|---------|
| `templates/samconfig.toml` | SAM CLI configuration with multi-stage parameter overrides. |
| `templates/template.yaml` | SAM template skeleton parameterised by Environment. |
| `templates/deploy.yaml` | GitHub Actions deploy pipeline with drift detection. |
| `templates/_smoke-test.toml` | Minimum viable filled-in artefact for sanity-checking the schema. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-serverless-iac-and-templates.py` | Validate the produced artefact against the schema in `content/02-output-contract.xml`. | Pre-commit; CI on each artefact change; `--self-test` in dev. |

## Related

- [[solo/dev/software-architect/serverless-foundations]]
- [[solo/dev/software-architect/serverless-architecture-patterns]]
- [[solo/dev/software-architect/serverless-cost-optimization]]

## Decision tree

See `content/06-decision-tree.xml`. Root question: *Are all four prerequisites populated (inventory, account, environments, tool standard)?* The tree's purpose is to route an input through observable signals to a conclusion that references a rule from `content/01-core-rules.xml`; the skip-this-methodology branch is always reachable so an inappropriate caller exits cleanly.
