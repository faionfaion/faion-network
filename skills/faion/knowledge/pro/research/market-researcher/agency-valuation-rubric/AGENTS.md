---
slug: agency-valuation-rubric
tier: pro
group: research
domain: research
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Numeric scoring rubric for agency valuation rubric that converts qualitative judgment into a comparable 0-100 (or 1-5 weighted) signal usable across cohorts.
content_id: "858cc0c8296cf041"
tags: [agency, research, scorecard]
---
# Agency Valuation Rubric

## Summary

**One-sentence:** Numeric scoring rubric for agency valuation rubric that converts qualitative judgment into a comparable 0-100 (or 1-5 weighted) signal usable across cohorts.

**One-paragraph:** Numeric scoring rubric for agency valuation rubric that converts qualitative judgment into a comparable 0-100 (or 1-5 weighted) signal usable across cohorts. Micro-agency multiples are public and patterned (typically 2–4x EBITDA, with multipliers for productized revenue %, retainer %, owner-dependency, niche stickiness). Founders need a self-service rubric to plug in their numbers before talking to any broker. market-researcher does not cover deal comps.

## Applies If (ALL must hold)

- You evaluate >1 instance against the same criteria addressed by agency valuation rubric (calls, vendors, candidates).
- Scores will be used for a binary decision (advance, reject, prioritize).
- Each criterion has a defined 1-5 anchor; raters trained on the rubric before scoring.
- ≥2 raters per instance for any score that gates a >$10k or strategic decision.

## Skip If (ANY kills it)

- n < 3 instances — gut feel is faster and accuracy is similar.
- Decisions are single-criterion (price-only, deadline-only) — full rubric is overhead.
- Strategic, single-shot decisions where qualitative narrative beats numeric blend.

## Prerequisites

- Rubric file or sheet with anchors written for each criterion 1-5.
- Rater(s) trained on at least 3 calibration examples before scoring real instances.
- Storage for scores reachable from downstream decision step (CRM, spreadsheet).

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/research/market-researcher/AGENTS.md` | Parent skill context (vocabulary, neighbouring methodologies) |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | The 4 testable rules every application enforces | ~900 |
| `content/02-output-contract.xml` | essential | Required output schema, forbidden patterns, allowed transformations | ~700 |
| `content/03-failure-modes.xml` | essential | 5 detector + repair clauses for known agent failures | ~900 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `per_criterion_score` | sonnet | Anchored 1-5 judgment per dimension |
| `multi_rater_reconciliation` | opus | Resolve divergent scores with rationale |

## Templates

| File | Purpose |
|------|---------|
| `templates/output-schema.json` | JSON Schema for the methodology's required output |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-output.py` | Enforce the output-contract before main agent accepts | After subagent returns, before commit/publish |

## Related

- parent skill: `pro/research/market-researcher/`
- peer methodologies: see siblings under `pro/research/market-researcher/`
- external: industry references cited inline in `content/01-core-rules.xml`
