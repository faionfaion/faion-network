---
slug: strategy-analysis-gap-analysis
tier: pro
group: business-analyst
domain: ba
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Identifies the delta between current and future state — capability gaps, process gaps, system gaps — with severity and remediation owner, feeding the change strategy.
content_id: "a7e12576ab3b1f84"
complexity: medium
produces: report
est_tokens: 2500
tags: [strategy-analysis, gap-analysis, capability-gap, delta, remediation]
---
# Strategy Analysis — Gap Analysis

## Summary

**One-sentence:** A documented delta between current and future state with capability + process + system gaps, severity, and named remediation owner per gap.

**One-paragraph:** With current + future specs in hand, gap analysis names exactly what is missing or different. Each gap is typed (capability / process / system / data / skill / regulatory), severity-scored (blocker / major / minor), and owned. The output feeds `strategy-analysis-change-strategy` for option comparison and the requirements backlog for build sequencing.

**Ефективно для:**

- Post-vision phase before kicking off requirements work.
- M&A integration where two organisations' as-is collides with one target.
- Vendor selection where fit-gap scoring drives the decision.
- Compliance gap audits.

## Applies If (ALL must hold)

- current-state spec exists
- future-state spec exists
- remediation owners can be named per gap type
- named decision-maker exists for prioritisation

## Skip If (ANY kills it)

- current or future state spec missing — produce them first
- the future-state target is so close to current that gaps are trivial
- the organisation has no capacity to remediate (gap analysis without action = decoration)

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| current-state spec | MD / wiki | strategy-analysis-current-state |
| future-state spec | MD / wiki | strategy-analysis-future-state |
| severity rubric | MD | BA team |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[strategy-analysis-current-state]] | Source of as-is rows. |
| [[strategy-analysis-future-state]] | Source of to-be rows. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: typed gaps, severity-rubric-bound, owner per gap, no overlap with adjacent gaps, traceability to current + future rows | 1000 |
| `content/02-output-contract.xml` | essential | JSON Schema for gap-analysis report: gaps[] with type, severity, owner, rationale, source | 800 |
| `content/03-failure-modes.xml` | essential | 5 failure modes: untyped gaps, severity drift, anonymous owners, overlap with adjacent gaps, no remediation owner | 800 |
| `content/04-procedure.xml` | essential | 4-step procedure: align rows → identify deltas → score severity → assign owners | 600 |
| `content/05-examples.xml` | essential | Worked example: 6-gap excerpt from a CRM consolidation gap analysis | 500 |
| `content/06-decision-tree.xml` | essential | Tree on spec freshness + remediation capacity + decision-maker availability | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `row_alignment` | haiku | Mechanical match of current-state rows to future-state rows. |
| `delta_identification` | sonnet | Identify deltas between aligned rows. |
| `severity_scoring` | sonnet | Apply severity rubric per gap. |
| `owner_assignment` | sonnet | Assign named remediation owner per gap. |

## Templates

| File | Purpose |
|------|---------|
| `templates/gap-analysis-report.md` | Markdown skeleton with gaps[] section. |
| `templates/gap-row.csv` | Header for gap rows (type, severity, owner, source). |
| `templates/_smoke-test.md` | Minimum viable gap-analysis report. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-strategy-analysis-gap-analysis.py` | Validates gap-analysis report against the JSON Schema. | After gap-scoring round; pre-commit. |

## Related

- [[strategy-analysis-current-state]]
- [[strategy-analysis-future-state]]
- [[strategy-analysis-change-strategy]]
- [[strategy-analysis-business-need]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input completeness, ownership clarity, regulatory context, scope size) to a rule from `01-core-rules.xml`. Use it when in doubt about whether to run, skip, or split this methodology.
