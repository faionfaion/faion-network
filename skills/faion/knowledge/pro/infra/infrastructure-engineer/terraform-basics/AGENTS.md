---
slug: terraform-basics
tier: pro
group: infra
domain: infra
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Core Terraform spec: HCL 8-block structure, providers with version pins + default tags, meta-arguments (for_each vs count), lifecycle, remote state with locking, standard file layout.
content_id: "af7f93c96e90050b"
complexity: medium
produces: spec
est_tokens: 4300
tags: [terraform, hcl, iac, basics, providers]
---
# Terraform Basics

## Summary

**One-sentence:** Core Terraform spec: HCL 8-block structure, providers with version pins + default tags, meta-arguments (for_each vs count), lifecycle, remote state with locking, standard file layout.

**One-paragraph:** Core Terraform spec: HCL 8-block structure, providers with version pins + default tags, meta-arguments (for_each vs count), lifecycle, remote state with locking, standard file layout. Output is a versioned artefact a downstream agent or human reviewer can consume without re-deriving the rationale. Hard rules are pinned in `content/01-core-rules.xml`; the JSON Schema contract in `content/02-output-contract.xml` gates downstream consumption; failure modes in `content/03-failure-modes.xml` block the common antipatterns observed in real deployments.

**Ефективно для:**

- Перший Terraform проєкт або зміна підходу: треба перейти на 8-block структуру з версією >=1.5.
- Resources створюються через count, а треба stable keys і unique identifiers — переїзд на for_each.
- Команда комітить .tfstate або .terraform.lock.hcl у git — треба негайно це випрямити.
- Provider без version constraints або без default_tags — кожен resource потрібно теггувати вручну.

## Applies If (ALL must hold)

- Starting a new Terraform project and scaffolding the file structure
- Configuring providers (AWS, GCP, Azure) with version constraints and default tags
- Writing resources with proper meta-arguments (count, for_each, lifecycle, depends_on)
- Looking up built-in function syntax (string, collection, encoding, date functions)
- Setting up remote state backends (S3+DynamoDB, GCS, Azure Blob, Terraform Cloud)

## Skip If (ANY kills it)

- Advanced state operations (import, mv, rm, moved blocks) — use terraform-state
- Production CI/CD pipeline patterns — use terraform (advanced)
- Module design and versioning — use terraform-modules-* methodologies

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Trigger context | Markdown / ticket / transcript | upstream task |
| Named owner | string (handle, email, role) | team roster |
| Storage location | URL / repo path | artefact store |
| Prior cycle artefact (if any) | this methodology's output | last run |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/infra/AGENTS.md` | parent group context (vocabulary, neighbouring methodologies) |
| `solo/sdd/sdd` | SDD discipline for artefact lifecycle (status flow, owners, review) |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules + run-the-checklist + skip-this-methodology conclusions | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid + invalid + forbidden examples | ~800 |
| `content/03-failure-modes.xml` | essential | >=3 antipatterns with symptom / root-cause / fix | ~700 |
| `content/04-procedure.xml` | essential | step-by-step procedure (input/action/output/decision-gate) | ~700 |
| `content/05-examples.xml` | essential | one worked end-to-end example with inputs and final artefact | ~700 |
| `content/06-decision-tree.xml` | essential | root-question + branches + conclusion refs to 01-core-rules | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft_inputs_summary` | haiku | template fill, bounded transformation |
| `synthesize_decision` | sonnet | per-instance judgment over bounded inputs |
| `review_for_compliance` | opus | cross-input synthesis when stakes are high or evidence chain is required |

## Templates

| File | Purpose |
|------|---------|
| `templates/spec.md` | working skeleton matching the `produces=spec` shape |
| `templates/_smoke-test.md` | minimum-viable filled-in smoke-test fixture |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-terraform-basics.py` | enforce `02-output-contract.xml` JSON Schema | after subagent returns, before downstream consumer reads |

## Related

- parent skill: `pro/infra/`
- peer methodology: see other entries in `skills/faion/knowledge/pro/infra/`
- external: industry references cited inline in `content/01-core-rules.xml`

## Decision tree

See `content/06-decision-tree.xml`. The tree starts at `Does the project need core Terraform spec (HCL + providers + state) without advanced CI/module patterns?` and routes to one of the 5 conclusions referencing rules in `01-core-rules.xml` (run-the-checklist, skip-this-methodology, defer-to-upstream, escalate-to-owner, schedule-recompute). Use it when in doubt about applicability or scope.
