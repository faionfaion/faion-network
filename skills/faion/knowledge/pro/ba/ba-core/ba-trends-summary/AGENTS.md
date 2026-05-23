---
slug: ba-trends-summary
tier: pro
group: ba
domain: ba
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Produces a quarterly checklist mapping current BA-discipline trends (AI-enabled, product-ops, value-stream) to concrete adoption decisions for the engagement.
content_id: "4224aa4c9147dbc6"
complexity: light
produces: checklist
est_tokens: 2900
tags: [ba, trends, industry, adoption, review]
---
# BA Trends Summary

## Summary

**One-sentence:** Produces a quarterly checklist mapping current BA-discipline trends (AI-enabled, product-ops, value-stream) to concrete adoption decisions for the engagement.

**One-paragraph:** Produces a quarterly checklist mapping current BA-discipline trends (AI-enabled, product-ops, value-stream) to concrete adoption decisions for the engagement. This methodology codifies the rules, output contract, antipatterns, and decision tree so the artefact is reproducible across teams and audits.

**Ефективно для:**

- Quarterly retro BA-команди — потрібен зведений огляд що змінилось у дисципліні.
- Engagement renewal, де sponsor запитує 'що нового ви приносите?'.
- Внутрішній CoP — щоквартальна публікація для BA-чат-групи.
- Toolchain audit: треба зіставити власний tooling із зовнішніми benchmark'ами.

## Applies If (ALL must hold)

- Quarterly BA practice review where industry trends must be considered for adoption.
- BA team is auditing its toolchain and methods against external benchmarks.
- Engagement renewal where 'why pay for BA?' demands a current-state justification.
- Internal community-of-practice deliverable summarising recent BA shifts.

## Skip If (ANY kills it)

- Mid-cycle execution sprint — trend reviews disrupt focus.
- BA practice is mature and the trend report would change nothing.
- No trend has emerged worth tracking this cycle.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Industry source list (IIBA, BA Times, Lean Enterprise) | URL list | BA |
| Engagement context (industry vertical, scale) | Markdown | BA |
| Previous trends summary (last quarter) | Markdown | BA archive |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[modern-ba-framework]] | trend items reference framework choices |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules with rationale + skip-this-methodology guard | 800 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid/forbidden examples | 800 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns: symptom / root-cause / fix | 700 |
| `content/06-decision-tree.xml` | essential | Decision tree on observable signals → conclusion refs to rule ids | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scan-sources` | haiku | Mechanical extraction of headlines + dates from source list. |
| `classify-trend` | sonnet | Map each headline to an adoption decision (adopt / trial / hold / drop). |
| `write-summary` | sonnet | Synthesise into a one-page checklist. |

## Templates

| File | Purpose |
|------|---------|
| `templates/trends-checklist.md` | One-page quarterly trends checklist with adoption decisions. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ba-trends-summary.py` | Validate the artefact JSON against the output contract schema | CI on each artefact change; pre-commit |

## Related

- [[modern-ba-framework]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input fields, scores, thresholds) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
