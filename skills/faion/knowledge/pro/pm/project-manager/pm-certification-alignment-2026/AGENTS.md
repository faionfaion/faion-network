---
slug: pm-certification-alignment-2026
tier: pro
group: pm
domain: pm
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Maps existing project-manager methodology content to 2026 PMBOK 8 / PMP Examination Content Outline domain weights and five exam themes (People 33%, Process 41%, Business Environment 26%).
content_id: "b6a5c4d3e2f1a0b9"
complexity: medium
produces: rubric
est_tokens: 4000
tags: [pmp, pmbok-8, certification, exam, 2026-eco]
---
# PM Certification Alignment 2026

## Summary

**One-sentence:** Maps existing project-manager methodology content to 2026 PMBOK 8 / PMP Examination Content Outline domain weights and five exam themes (People 33%, Process 41%, Business Environment 26%).

**One-paragraph:** Maps existing project-manager methodology content to 2026 PMBOK 8 / PMP Examination Content Outline domain weights and five exam themes (People 33%, Process 41%, Business Environment 26%).

**Ефективно для:**

- PM-ів, що готуються до PMP-2026 exam і хочуть знати where to study.
- L&D teams, що адаптують внутрішній PM-curriculum до new ECO.
- Agency-ів, що пропонують exam-prep як supplementary service.
- PMO, де certification renewal залежить від actively maintained content.

## Applies If (ALL must hold)

- Candidate planning to sit PMP after 2026-07-01.
- Existing PM methodology library to be re-classified.
- L&D team can dedicate review time per quarter.
- Exam-content outline (ECO) accessible.

## Skip If (ANY kills it)

- Candidate sitting before 2026-07-01 — old ECO applies.
- No PM-certification ambition.
- Methodology library &lt;30 entries — alignment overhead too high.
- Org uses non-PMI certification (PRINCE2, IPMA) — different mapping.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Scope brief | Markdown | engagement intake |
| Stakeholder roster | table | PM |
| Historical reference data | csv / log | PMO data warehouse |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[pm-certification-changes-2026]] | Companion that documents the changes themselves. |
| [[pm-framework-focus-areas]] | PMBoK 8 framework backbone. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules + `skip-this-methodology` | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid/forbidden | 850 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom/root-cause/fix | 750 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | 800 |
| `content/06-decision-tree.xml` | essential | Apply/skip routing on observable signals | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `methodology-classifier` | sonnet | Tag each methodology with primary domain + theme. |
| `gap-analyzer` | opus | Spot domains under-covered relative to ECO weights. |
| `study-plan-author` | sonnet | Author candidate-specific study plan. |

## Templates

| File | Purpose |
|------|---------|
| `templates/alignment-rubric.md` | Methodology × ECO-domain matrix with coverage score. |
| `templates/study-plan.md` | Candidate study plan with weekly time-budget. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-pm-certification-alignment-2026.py` | Validate the output artefact against the schema | Pre-commit on every artefact change |

## Related

- [[pm-certification-changes-2026]]
- [[pm-framework-focus-areas]]
- [[performance-domains-overview]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observables (exam_date, methodology_count, certification_body) to apply / fall-back / skip. Each leaf references a rule from `01-core-rules.xml`.
