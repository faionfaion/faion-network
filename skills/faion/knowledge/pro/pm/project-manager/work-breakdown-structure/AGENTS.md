---
slug: work-breakdown-structure
tier: pro
group: pm
domain: pm
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Frames WBS as scope-baseline artefact (PMI standard): noun-based deliverable tree + 100% rule + 8-80 leaves + WBS Dictionary; emits a typed `WBS` spec consumed by schedule, EVM, RACI, and SDD-task generation downstream.
content_id: "7d179f8e01a9c104"
complexity: deep
produces: spec
est_tokens: 4400
tags: [wbs, scope, project-planning, deliverables, estimation]
---
# Work Breakdown Structure

## Summary

**One-sentence:** Frames WBS as a deliverable-oriented scope baseline (PMI standard): noun-based hierarchical decomposition, 100% rule, 8-80 hour leaves, and a Dictionary entry per leaf — the spine from which schedule, cost, RACI, and SDD tasks derive.

**One-paragraph:** WBS is *the* scope baseline. Schedule and cost are derived from it; they are NOT contained in it. Without a deliverable-oriented WBS, scope statement → estimates → schedule decouple silently and forgotten work surfaces during execution. The 100% rule + 8-80 hour leaf rule + WBS Dictionary (included/excluded scope, acceptance criteria, owner, hours, dependencies) make the artefact actionable instead of decorative. This methodology codifies the PMI standard for project-manager workflow (sibling [[wbs-creation]] is the build-focused playbook; this one is the framing methodology consumed by RACI, schedule, EVM, and SDD task generation). Append-only IDs preserve traceability across change requests, risk entries, and tasks.

**Ефективно для:**

- Translating an approved SOW into an estimable, assignable work-package tree before scheduling.
- Bidding on fixed-scope work requiring bottom-up estimation.
- Diffing a drafted WBS against the scope statement to find gaps / overlaps (100% rule audit).
- Re-baselining after a change request — mutating only the affected branch with append-only IDs.

## Applies If (ALL must hold)

- Approved scope statement / SOW exists.
- ≥ 70% of deliverables are known well enough to enumerate.
- Change-control process exists so WBS edits route through CR.
- Version control hosts the WBS YAML + Dictionary cards.

## Skip If (ANY kills it)

- Pure Scrum / Kanban driven by a product backlog — duplicate sources of truth.
- Discovery / research projects with < 30% of scope known.
- Solo work on a feature under 2 weeks — a checklist is simpler.
- Innovation / platform exploration with emergent deliverables — use rolling-wave planning.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Approved SOW / scope statement | Markdown / signed PDF | sponsor |
| Glossary of deliverable terms | YAML | BA / PM |
| Anchor estimates (≥ 3 known-good) | YAML | history |
| Architecture sketch (optional) | Markdown | architect |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[wbs-creation]] | Sibling — the build-focused playbook; this methodology is the framing standard. |
| [[raci-ai-assisted]] | Each WBS leaf needs exactly one accountable role; RACI consumes WBS leaves. |
| [[value-stream-management]] | Flow / DORA metrics are reported by-branch using WBS IDs as labels. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 rules: deliverable-orientation, 100% rule, 8-80 sizing, overhead branches, append-only IDs, Dictionary required | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 for `WBS` + Dictionary + forbidden patterns | ~1000 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns: verb-default, schedule-bleed (dates in WBS), uneven depth, hallucinated owners, ID reuse after delete | ~800 |
| `content/04-procedure.xml` | essential | 6-step procedure: ideate L1 → decompose → 100% check → size → Dictionary → baseline | ~800 |
| `content/05-examples.xml` | medium | One worked WBS: MVP launch, 5 L1 branches, balanced depth, Dictionary entry shown | ~600 |
| `content/06-decision-tree.xml` | essential | Tree: node shape, overhead present, weight sum, leaf size, id collision → action + rule | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `wbs-decomposer` | sonnet | Light judgment on deliverable taxonomy. |
| `wbs-dictionary-writer` | sonnet | Per-leaf card with included/excluded scope + AC. |
| `100-rule-validator` | haiku | Mechanical sum check. |
| `8-80-validator` | haiku | Mechanical bound check. |

## Templates

| File | Purpose |
|------|---------|
| `templates/wbs-template.md` | Hierarchical WBS outline with PM + all mandatory branches |
| `templates/wbs-dict-entry.md` | Single work-package Dictionary card |
| `templates/wbs-validate.py` | Helper validator (weight + 8-80) consumed by Step 6 |
| `templates/_smoke-test.json` | Minimum-viable filled `WBS` for validator self-test |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-work-breakdown-structure.py` | Validate a `WBS` against the JSON Schema + invariants | Pre-commit on WBS edits |

## Related

- [[wbs-creation]]
- [[raci-ai-assisted]]
- [[value-stream-management]]

## Decision tree

See `content/06-decision-tree.xml`. The tree decides per node whether to: split a too-large leaf, merge a too-small leaf, reject a verb-named node, refuse renumbering on id collision, or add a missing overhead branch. Each leaf references a rule from `01-core-rules.xml`.
