---
slug: wbs-creation
tier: pro
group: pm
domain: pm
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Hierarchical decomposition of project scope into deliverable-oriented work packages using the 100% rule + 8-80 hour sizing + WBS Dictionary; emits a typed `WBS` spec with append-only IDs and per-leaf acceptance criteria.
content_id: "76479139d380fd9c"
complexity: deep
produces: spec
est_tokens: 4400
tags: [wbs, scope, decomposition, 100-rule, dictionary]
---
# WBS Creation

## Summary

**One-sentence:** Hierarchical decomposition of project scope into deliverable-oriented work packages using the 100% rule (nouns not verbs), 8-80 hour leaf sizing, and a per-leaf WBS Dictionary with explicit acceptance criteria.

**One-paragraph:** Without a WBS, scope is ambiguous: estimates are guesses, dependencies are invisible, and forgotten work surfaces too late to recover. The 100% rule forces completeness — if all children are done, the parent is done. Deliverable orientation (nouns not verbs) keeps the tree stable when implementation decisions change. This methodology codifies the discipline: noun-only nodes, mandatory overhead branches (PM/QA/Deployment/Documentation/Training/Transition — typically 15-25% of effort), 8-80 hour leaves, append-only IDs (CR/risk/task references survive renumbering), and a Dictionary entry per leaf carrying scope-included/excluded, deliverable, acceptance criteria, owner, hours, and dependencies. Two-pass agentic workflow: ideate Level-1 → decompose each branch → Dictionary entries; human review mandatory between passes.

**Ефективно для:**

- Predictive / waterfall projects with fixed scope (agency contracts, ERP rollouts, hardware launches).
- Hybrid: WBS at program level, sprints underneath each work package.
- Cost-loaded schedules and EVM tracking — WBS is the spine for cost accounts.
- Compliance projects (SOC2, HIPAA, ISO 27001) where the 100% rule maps to control coverage.

## Applies If (ALL must hold)

- Project has a signed scope statement or SOW.
- Deliverables are known well enough that ≥ 70% of scope can be enumerated.
- A change-control process exists so WBS edits route through CR, not chat.
- Team uses version control where the WBS YAML and Dictionary cards live.

## Skip If (ANY kills it)

- Pure-agile teams driven by a product backlog — WBS calcifies what should flex.
- Discovery / R&D where deliverables are emergent — use hypothesis backlog instead.
- Fast-moving startup product work where scope changes weekly — overhead exceeds value.
- Solo work on a feature under 2 weeks — a checklist beats a WBS.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Approved scope statement | Markdown / signed PDF | sponsor |
| Glossary of deliverable terms | YAML | BA or PM |
| Anchor estimates (≥ 3 known-good) | YAML | history / SME |
| Architecture sketch (optional) | Markdown | architect |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[work-breakdown-structure]] | Sibling methodology; this one is the "build" focus, the sibling is the broader frame. |
| [[raci-ai-assisted]] | Each leaf needs exactly one accountable (A) role — RACI maps onto WBS leaves. |
| [[team-development]] | Skills-matrix feeds the owner-role field per leaf. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 rules: deliverable-orientation (nouns), 100% rule, 8-80 sizing, overhead branches, append-only IDs, WBS Dictionary mandatory | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 for `WBS` + Dictionary entry + forbidden patterns | ~1000 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns: verb-default, uneven depth, hallucinated owners/dates, consolidation to fit count, ID reuse after delete | ~800 |
| `content/04-procedure.xml` | essential | 6-step procedure: ideate L1 → decompose → 100%-check → size → Dictionary → validate | ~800 |
| `content/05-examples.xml` | medium | One worked WBS: e-commerce MVP, 5 branches, 12 leaves, balanced depth, full Dictionary entry for one leaf | ~600 |
| `content/06-decision-tree.xml` | essential | Tree: scope known? size? overhead present? depth balanced? → action + rule | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `wbs-decomposer` | sonnet | Light judgment on deliverable taxonomy. |
| `wbs-dictionary-writer` | sonnet | Per-leaf card with judgment on AC + exclusions. |
| `validate-100-rule` | haiku | Mechanical sum-of-children check. |
| `validate-8-80-sizing` | haiku | Mechanical bound check on leaves. |

## Templates

| File | Purpose |
|------|---------|
| `templates/wbs-outline.md` | Hierarchical WBS outline skeleton with numbered levels |
| `templates/wbs-dictionary-entry.md` | Single work-package Dictionary card with all required fields |
| `templates/wbs-validate.py` | Helper used by Step 6 to validate weight + 8-80 against wbs.yaml |
| `templates/_smoke-test.yaml` | Minimum-viable filled `WBS` for validator self-test |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-wbs-creation.py` | Validate a `WBS` against the JSON Schema + 100% rule + 8-80 leaves | Pre-commit on WBS edits |

## Related

- [[work-breakdown-structure]]
- [[raci-ai-assisted]]
- [[team-development]]

## Decision tree

See `content/06-decision-tree.xml`. The tree decides when to: (a) split a leaf for 8-80, (b) merge a too-small leaf, (c) reject a verb-named node, (d) add a missing overhead branch, or (e) refuse to renumber. Every leaf references a rule from `01-core-rules.xml`.
