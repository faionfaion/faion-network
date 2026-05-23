---
slug: terraform-modules-structure
tier: pro
group: infra
domain: infra
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Per-module file structure spec: main.tf, variables.tf with validation, outputs.tf, versions.tf, README.md, examples/. Defines single-responsibility boundary.
content_id: "845fd8615b0f3b9b"
complexity: medium
produces: spec
est_tokens: 4300
tags: [terraform, modules, structure, iac]
---
# Terraform Modules — Structure

## Summary

**One-sentence:** Per-module file structure spec: main.tf, variables.tf with validation, outputs.tf, versions.tf, README.md, examples/. Defines single-responsibility boundary.

**One-paragraph:** Per-module file structure spec: main.tf, variables.tf with validation, outputs.tf, versions.tf, README.md, examples/. Defines single-responsibility boundary. Output is a versioned artefact a downstream agent or human reviewer can consume without re-deriving the rationale. Hard rules are pinned in `content/01-core-rules.xml`; the JSON Schema contract in `content/02-output-contract.xml` gates downstream consumption; failure modes in `content/03-failure-modes.xml` block the common antipatterns observed in real deployments.

**Ефективно для:**

- Модуль має >1 'responsibility' (наприклад, vpc + ecs + rds в одному) — потрібно розбити по single-responsibility.
- У модулі немає README.md з прикладом використання — споживачі не знають як його викликати.
- Команди різних teams роблять модулі з різним layout — треба зафіксувати стандарт.
- variables.tf не має validation блоків — користувачі ловлять обмеження тільки на cloud API.

## Applies If (ALL must hold)

- Creating a new Terraform module from scratch
- Refactoring a module that has grown beyond a single responsibility
- Standardising file layout across modules owned by different teams
- Adding examples/ subdir to prove a module works end-to-end

## Skip If (ANY kills it)

- Module composition / wiring — use terraform-modules-composition
- Module semantic versioning — use terraform-modules-versioning
- Module security review — use terraform-modules-security

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
| `scripts/validate-terraform-modules-structure.py` | enforce `02-output-contract.xml` JSON Schema | after subagent returns, before downstream consumer reads |

## Related

- parent skill: `pro/infra/`
- peer methodology: see other entries in `skills/faion/knowledge/pro/infra/`
- external: industry references cited inline in `content/01-core-rules.xml`

## Decision tree

See `content/06-decision-tree.xml`. The tree starts at `Is the goal to scaffold or normalise a single Terraform module's file structure?` and routes to one of the 5 conclusions referencing rules in `01-core-rules.xml` (run-the-checklist, skip-this-methodology, defer-to-upstream, escalate-to-owner, schedule-recompute). Use it when in doubt about applicability or scope.
