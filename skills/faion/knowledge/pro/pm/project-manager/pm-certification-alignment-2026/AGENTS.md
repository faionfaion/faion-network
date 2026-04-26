# PM Certification Alignment 2026

## Summary

Maps existing project-manager methodology content to the 2026 PMBOK 8 / PMP Examination Content Outline (ECO) domain weights and five exam themes. The primary 2026 change is a +18% shift in Business Environment domain weight (People 33%, Process 41%, Business Environment 26%). Every coverage claim must cite a verbatim ECO or PMBOK section anchor — no anchor means no coverage. Study time allocation is gap-weighted, not domain-weight-weighted.

## Why

PM certification exam content has materially shifted from PMBOK 7: Business Environment (value delivery, sustainability, AI, organizational change) grew from 8% to 26% while People and Process shrank. Internal PM curricula and onboarding docs built on PMBOK 6/7 have structural gaps in the new high-weight areas. A coverage matrix against the live ECO prevents study plans from optimizing for the old exam.

## When To Use

- Preparing for PMP, CAPM, or PMI Disciplined Agile certifications under the 2026 ECO.
- Updating internal PM curricula, onboarding docs, or playbooks to reflect new domain weights.
- Mapping existing methodology library to 2026 themes and identifying coverage gaps.
- Designing study plans for PMs migrating from PMBOK 6/7 to PMBOK 8.

## When NOT To Use

- Practitioners not pursuing a certification — apply PMBOK 7/8 principles directly; no exam-prep overhead.
- Pre-2026 study plans that need to ship before the ECO cut-over date.
- Highly specialized domains (Agile-only, regulated construction, defense) — supplement with role-specific guides; this methodology is breadth, not depth.
- One-off content gap fixes — read the official ECO directly.

## Content

| File | What's inside |
|------|---------------|
| `content/01-domain-weights.xml` | 2026 domain weight deltas, five exam themes, study-allocation rule, anchor-citation requirement. |
| `content/02-coverage-gaps.xml` | Priority areas for the +18% Business Environment shift, alignment-matrix rules, common agent failures. |

## Templates

none

## Scripts

| File | Purpose |
|------|---------|
| `scripts/coverage_gaps.py` | Reads alignment-matrix.csv; lists ECO tasks with no methodology coverage by domain. |
