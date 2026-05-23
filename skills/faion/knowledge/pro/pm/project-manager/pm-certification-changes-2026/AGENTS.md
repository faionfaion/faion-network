---
slug: pm-certification-changes-2026
tier: pro
group: pm
domain: pm
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Decoded 2026-07-01 PMP Examination Content Outline changes: domain weight shifts (People 42→33%, Process 50→41%, Business Environment 8→26%), new question types, prep impact.
content_id: "1a2b3c4d5e6f7a8b"
complexity: light
produces: report
est_tokens: 3500
tags: [pmp, certification, exam-weights, business-environment, study-planning]
---
# PM Certification Changes 2026

## Summary

**One-sentence:** Decoded 2026-07-01 PMP Examination Content Outline changes: domain weight shifts (People 42→33%, Process 50→41%, Business Environment 8→26%), new question types, prep impact.

**One-paragraph:** Decoded 2026-07-01 PMP Examination Content Outline changes: domain weight shifts (People 42→33%, Process 50→41%, Business Environment 8→26%), new question types, prep impact.

**Ефективно для:**

- PM-ів, що мали готувати ECO 2021 і shifted на 2026.
- Exam-prep providers, що оновлюють course content.
- L&D teams, що inform candidates про upcoming changes.
- Hiring managers, що оцінюють certification recency.

## Applies If (ALL must hold)

- Candidate sitting PMP after 2026-07-01.
- Prep material from prior ECO needs re-alignment.
- Org tracks PMP recency for staffing.
- Decision needed on book/course refresh.

## Skip If (ANY kills it)

- Already PMP-certified and not renewing.
- Sitting before 2026-07-01.
- Pursuing PRINCE2 or IPMA instead.
- No certification interest at all.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Scope brief | Markdown | engagement intake |
| Stakeholder roster | table | PM |
| Historical reference data | csv / log | PMO data warehouse |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[pm-certification-alignment-2026]] | Alignment artefact this report informs. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules + `skip-this-methodology` | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid/forbidden | 850 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom/root-cause/fix | 750 |
| `content/05-examples.xml` | essential | one worked example end-to-end | 700 |
| `content/06-decision-tree.xml` | essential | Apply/skip routing on observable signals | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `change-summariser` | haiku | Render the change table. |
| `impact-analyst` | sonnet | Estimate prep-time delta per candidate profile. |

## Templates

| File | Purpose |
|------|---------|
| `templates/change-report.md` | Side-by-side ECO 2021 vs ECO 2026 with delta column. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-pm-certification-changes-2026.py` | Validate the output artefact against the schema | Pre-commit on every artefact change |

## Related

- [[pm-certification-alignment-2026]]
- [[pm-framework-focus-areas]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observables (exam_date, prep_material_age, candidate_profile) to apply / fall-back / skip. Each leaf references a rule from `01-core-rules.xml`.
