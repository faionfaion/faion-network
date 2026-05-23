# Work Breakdown Structure

## Summary

**One-sentence:** WBS artefact: hierarchical decomposition of project scope into noun-led work packages, each owned by one person, estimable in 8-80h, with 100% coverage and no overlap.

**One-paragraph:** The Work Breakdown Structure is the canonical PMBoK artefact: a noun-led tree of deliverables produced via decomposition, with every leaf assignable, estimable in 8-80h, and verifiable against the signed scope baseline. The WBS is the spine that schedule, cost, and EVM consume; without it, those downstream artefacts inherit ambiguity.

**Ефективно для:**

- Programmes consuming WBS downstream for schedule, cost, and EVM.
- Multi-team coordination requiring single source of truth for deliverables.
- Audit + governance contexts needing baseline traceability.
- Fixed-bid pricing models where WBS is the contractual artefact.

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
| `scripts/validate-work-breakdown-structure.py` | Schema-validate WBS JSON artefact. | Pre-commit + pre-EVM baseline. |
| `scripts/wbs-check.py` | Lint WBS outline: numbering, owners, 8-80h leaves. | Pre-commit + before steering review. |

## Related

- [[scope-management]]
- [[schedule-development]]
- [[cost-estimation]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals from the work-breakdown-structure input (precondition checks, scale thresholds, evidence presence) to a concrete action, with each leaf referencing a rule id from `01-core-rules.xml`. Consult it whenever the methodology could branch based on context.
