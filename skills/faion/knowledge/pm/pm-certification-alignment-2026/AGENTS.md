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

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[pm-certification-changes-2026]] | Companion that documents the changes themselves. |
| [[pm-framework-focus-areas]] | PMBoK 8 framework backbone. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 13 testable rules + `skip-this-methodology`: ECO tagging, coverage vs weights, five themes, gap actions, evidence-based study plan, weight-times-gap allocation, anchor citation, sustainability standards, scenario practice, BE priority areas, CSV matrix in git, re-run on ECO refresh; background: 2026 domain weight deltas and the five exam themes | 2000 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid/forbidden | 950 |
| `content/03-failure-modes.xml` | essential | 7 antipatterns with symptom/root-cause/fix, including agent failure modes (weight-proportional plan, verbatim exam content, hard-coded dates) | 1000 |
| `content/04-procedure.xml` | essential | 6-step procedure end-to-end; step 6 re-runs the mapping on ECO refresh via coverage_gaps.py | 600 |
| `content/06-decision-tree.xml` | essential | Apply/skip routing on observable signals, plus anchor and Business Environment gap branches | 450 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `methodology-classifier` | sonnet | Tag each methodology with primary domain + theme. |
| `gap-analyzer` | opus | Spot domains under-covered relative to ECO weights. |
| `study-plan-author` | sonnet | Author candidate-specific study plan. |

## Templates

| File | Purpose |
|------|---------|
| `templates/alignment-rubric.md.j2` | Methodology × ECO-domain matrix with coverage score. |
| `templates/alignment-rubric.md` | Methodology × ECO-domain matrix with coverage score. Generated from `templates/alignment-rubric.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/study-plan.md.j2` | Candidate study plan with weekly time-budget. |
| `templates/study-plan.md` | Candidate study plan with weekly time-budget. Generated from `templates/study-plan.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-pm-certification-alignment-2026.py` | Validate the output artefact against the schema | Pre-commit on every artefact change |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[pm-certification-changes-2026]]
- [[pm-framework-focus-areas]]
- [[performance-domains-overview]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observables (exam_date, methodology_count, certification_body) to apply / fall-back / skip. Each leaf references a rule from `01-core-rules.xml`.
