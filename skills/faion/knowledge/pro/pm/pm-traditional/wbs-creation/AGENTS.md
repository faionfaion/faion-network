---
slug: wbs-creation
tier: pro
group: pm
domain: pm
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Decompose project scope into deliverable-oriented, hierarchically numbered work packages, 100% rule applied at every level, leaves 8-80h with full dictionary entries.
content_id: "76479139d380fd9c"
complexity: medium
produces: spec
est_tokens: 4200
tags: [wbs, scope-management, pmi, decomposition, work-packages]
---
# WBS Creation

## Summary

**One-sentence:** Decompose project scope into deliverable-oriented, hierarchically numbered work packages, 100% rule applied at every level, leaves 8-80h with full dictionary entries.

**One-paragraph:** WBS Creation is the act of producing the hierarchical breakdown: walking the signed scope baseline, decomposing into noun-led deliverables, stopping at 8-80h leaves, authoring the dictionary, and validating 100%-rule coverage and absence of gold-plating. Output is a WBS outline plus dictionary committed alongside the scope baseline.

**Ефективно для:**

- Programmes needing earned-value (EVM) — leaves are the EVM atomic unit.
- Fixed-bid contracts where scope baseline drives the price.
- Multi-team programmes needing owner-per-leaf accountability.
- Audited delivery requiring deliverable-to-baseline traceability.

## Applies If (ALL must hold)

- Signed scope baseline exists (scope-management complete).
- Project will be tracked via earned-value or milestone reporting.
- Multiple work packages need owner assignment + acceptance criteria.
- Programme reporting requires hierarchical roll-up.

## Skip If (ANY kills it)

- Pure Scrum team — backlog replaces WBS.
- Solo project — checklist is sufficient.
- Pre-PMF discovery where scope is hypothesis-driven.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Signed scope baseline | scope-statement.md | scope-management |
| Charter | signed PDF | sponsor |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `scope-management` | Locked scope is the parent of the WBS root. |
| `schedule-development` | Consumes WBS leaves as schedule activities. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules — 100% rule, deliverable-oriented, 8-80h leaves, dictionary, no gold-plating | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for WBS tree + valid/invalid examples | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns | 800 |
| `content/04-procedure.xml` | essential | 5-step decomposition procedure | 800 |
| `content/05-examples.xml` | optional | Worked WBS snippet at 3 levels | 600 |
| `content/06-decision-tree.xml` | essential | Decision tree mapping WBS state to a rule | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decompose-deliverables` | sonnet | Domain judgment on noun-led decomposition. |
| `dictionary-fill` | haiku | Template fill per leaf. |
| `coverage-audit` | opus | Cross-tree 100%-rule and gold-plating synthesis. |

## Templates

| File | Purpose |
|------|---------|
| `templates/wbs-outline.md` | Hierarchical WBS outline. |
| `templates/wbs-dictionary-entry.md` | Per-leaf dictionary template. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-wbs-creation.py` | Schema-validate WBS JSON artefact. | Pre-commit + pre-EVM baseline. |
| `scripts/wbs_lint.py` | Lint WBS outline: numbering, owners, 8-80h leaves. | Pre-commit + before steering review. |

## Related

- [[scope-management]]
- [[schedule-development]]
- [[cost-estimation]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals from the wbs-creation input (precondition checks, scale thresholds, evidence presence) to a concrete action, with each leaf referencing a rule id from `01-core-rules.xml`. Consult it whenever the methodology could branch based on context.
