---
slug: terraform-state
tier: pro
group: infra
domain: infra
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Remote state architecture spec: backend choice (S3+DynamoDB, GCS, Terraform Cloud), locking, encryption, import/mv/rm operations, moved blocks, state file recovery.
content_id: "d59f1a0ccc72a95b"
complexity: deep
produces: spec
est_tokens: 4300
tags: [terraform, state, backend, locking, iac]
---
# Terraform State

## Summary

**One-sentence:** Remote state architecture spec: backend choice (S3+DynamoDB, GCS, Terraform Cloud), locking, encryption, import/mv/rm operations, moved blocks, state file recovery.

**One-paragraph:** Remote state architecture spec: backend choice (S3+DynamoDB, GCS, Terraform Cloud), locking, encryption, import/mv/rm operations, moved blocks, state file recovery. Output is a versioned artefact a downstream agent or human reviewer can consume without re-deriving the rationale. Hard rules are pinned in `content/01-core-rules.xml`; the JSON Schema contract in `content/02-output-contract.xml` gates downstream consumption; failure modes in `content/03-failure-modes.xml` block the common antipatterns observed in real deployments.

**Ефективно для:**

- Команда переходить з local state на remote — треба обрати backend і ввімкнути locking.
- Існуючий ресурс створено вручну у консолі — треба terraform import без destroy/create.
- Рефакторинг modules ламає state — треба moved {} блоки замість state mv-команд.
- Стан зламано після concurrent apply без locking — потрібен план recovery + backfill.

## Applies If (ALL must hold)

- Choosing or migrating remote state backend (S3+DynamoDB vs GCS vs Terraform Cloud)
- Setting up state locking + encryption + versioning
- Running terraform import / mv / rm to fix or restructure state
- Using moved {} blocks to refactor module structure without resource recreation
- Recovering from a corrupted or out-of-sync state file

## Skip If (ANY kills it)

- HCL syntax basics — use terraform-basics
- Pipeline plan/apply controls — use terraform (advanced)
- Module development — use terraform-modules-* methodologies

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
| `scripts/validate-terraform-state.py` | enforce `02-output-contract.xml` JSON Schema | after subagent returns, before downstream consumer reads |

## Related

- parent skill: `pro/infra/`
- peer methodology: see other entries in `skills/faion/knowledge/pro/infra/`
- external: industry references cited inline in `content/01-core-rules.xml`

## Decision tree

See `content/06-decision-tree.xml`. The tree starts at `Does the task involve a Terraform backend, locking, encryption, or state surgery?` and routes to one of the 5 conclusions referencing rules in `01-core-rules.xml` (run-the-checklist, skip-this-methodology, defer-to-upstream, escalate-to-owner, schedule-recompute). Use it when in doubt about applicability or scope.
