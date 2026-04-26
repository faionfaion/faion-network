# Product Development Trends

## Summary

A research lens for current product-development practice trends: AI-augmented ideation, continuous customer feedback loops, rapid-pivot cadence, and cross-functional team structures. Produces a trend brief with URL-cited primary sources. This is the general (non-year-pinned) version; for 2026-specific signal collection and scoring, use `product-development-trends-2026/` instead.

## Why

Development teams misalign on methodology when they use 2019-era playbooks in a 2025+ market. This methodology surfaces the four axes where practice has shifted most, applies a three-stage pipeline (signal collection → triage → human checkpoint), and enforces a recency gate so the brief reflects the current landscape rather than training-data residue.

## When To Use

- Quarterly methodology alignment before opening the SDD roadmap or spec.
- Briefing a new PM, researcher, or engineer on current team-shape and discovery cadence norms.
- Pre-PRD discovery: surfacing AI-augmented ideation candidates before locking feature specs.
- Competitive briefs where a methodology upgrade is the differentiator (e.g. agile → continuous discovery).

## When NOT To Use

- Sprint planning or story splitting — use `pm-agile` or `sdd-planning` instead.
- Single-feature validation — use `user-researcher/problem-validation`.
- Pricing or TAM/SAM/SOM analysis — use `market-researcher/pricing-research` and `tam-sam-som`.
- Less than 6 weeks since last trend pass with no triggering event (funding round, major competitor move, regulatory shift).
- Regulated domains (medical devices, fintech, avionics) where waterfall + audit trail is a contractual requirement.

## Content

| File | What's inside |
|------|---------------|
| `content/01-trends.xml` | Four trend axes with impact table, AI-Human ideation flow, and key research output types |
| `content/02-methodology.xml` | Three-stage pipeline: signal collection, scored triage, human checkpoint; scoring rules |

## Templates

| File | Purpose |
|------|---------|
| `templates/score-signals.py` | Signal scoring: recency/evidence/applicability scoring, threshold filtering, markdown table output |
