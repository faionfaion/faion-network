---
slug: pm-certification-alignment-2026
tier: pro
group: pm
domain: pm
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Curriculum + content alignment to the 2026 PMP Exam Content Outline (ECO) covering People (33%), Process (41%), Business Environment (26%).
content_id: "6e3f4425f482a208"
complexity: medium
produces: spec
est_tokens: 4900
tags: [pmp, certification, curriculum, 2026-eco, business-environment]
---
# PM Certification Alignment 2026

## Summary

**One-sentence:** Curriculum + content alignment to the 2026 PMP Exam Content Outline (ECO) covering People (33%), Process (41%), Business Environment (26%).

**One-paragraph:** Curriculum + content alignment to the 2026 PMP Exam Content Outline (ECO) covering People (33%), Process (41%), Business Environment (26%). The methodology applies in pm-traditional contexts where the preconditions in `Applies If` hold and none of the `Skip If` triggers fire. Decision routing lives in `content/06-decision-tree.xml`; testable rules with rationale live in `content/01-core-rules.xml`; the validator at `scripts/validate-pm-certification-alignment-2026.py` enforces the output contract.

**Ефективно для:**

- Training providers rebuilding curriculum to 2026 ECO weights.
- PMOs aligning internal upskilling to new exam emphasis.
- Candidates planning study time allocation per domain.
- Practice-exam authors recalibrating item bank to 2026 weights.

## Applies If (ALL must hold)

- Target audience sits PMP after July 1, 2026.
- Curriculum can be re-weighted per domain.
- Item bank or content units can be tagged by ECO task.

## Skip If (ANY kills it)

- Audience sits exam before 2026-07-01 — use legacy ECO.
- Non-PMP certification (PRINCE2, Scrum) — different alignment needed.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| 2026 ECO document | PDF/Markdown | PMI source |
| Current curriculum map | spreadsheet | training provider |
| Item bank with tags | CSV/DB | training provider |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[pm-certification-changes-2026]] | this methodology consumes the changes diff |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules (incl. skip rule) with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid/forbidden examples | 900 |
| `content/03-failure-modes.xml` | essential | Antipatterns with symptom/root-cause/fix triplets | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with input/action/output/decision-gate | 800 |
| `content/05-examples.xml` | optional | End-to-end worked example | 700 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `map-curriculum` | sonnet | Judgement: which content unit maps to which ECO task. |
| `score-coverage` | haiku | Mechanical coverage %. |
| `draft-gap-plan` | sonnet | Plan to close uncovered ECO tasks. |

## Templates

| File | Purpose |
|------|---------|
| `templates/alignment-map.md` | Curriculum × ECO task alignment template with coverage gap markers |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-pm-certification-alignment-2026.py` | Validate the spec artefact against the schema in `02-output-contract.xml` | CI on each artefact change; pre-commit |

## Related

- [[pm-certification-changes-2026]]
- [[lessons-learned]]
- [[communications-management]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (preconditions, baseline presence, threshold pass/fail) to a concrete action; each leaf references a rule from `01-core-rules.xml`. Use it when in doubt about whether or how to apply this methodology to the case at hand.

