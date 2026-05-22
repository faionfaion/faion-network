---
slug: solo-niche-narrative-framework
tier: pro
group: marketing
domain: marketing
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "e42795211f36f227"
summary: Personal-brand positioning sharpener that refines the "I am the <X> for <Y> who needs <Z>" statement quarterly using paying-customer evidence rather than aspirational positioning.
tags: [positioning, personal-brand, gtm, freelance, niche]
---

# Solo Niche Narrative Framework

## Summary

**One-sentence:** Personal-brand positioning sharpener that refines the "I am the &lt;X&gt; for &lt;Y&gt; who needs &lt;Z&gt;" statement quarterly using paying-customer evidence rather than aspirational positioning.

**One-paragraph:** April Dunford's "Obviously Awesome" positioning framework was built for venture-backed B2B products with a marketing team. Solo operators need a stripped-down, quarterly-cadence personal version: list paying customers from the prior quarter, group by who-actually-pays-vs-who-asks-for-discounts, extract the unique value the cohort verbalises (verbatim — not your own product copy), and emit a fresh positioning statement. Output: one positioning statement + 3 alternatives + ranked evidence. Replaces "I help businesses grow" generic statements with something a paying buyer recognises in 3 seconds.

## Applies If (ALL must hold)

- operator has ≥ 5 paid engagements in the trailing 90-day window
- engagements span ≥ 2 customer types (so cohort comparison is possible)
- positioning is being reviewed (quarterly rate adjustment, LinkedIn rewrite, site refresh)
- operator is willing to fire / refuse a customer cohort if data demands it

## Skip If (ANY kills it)

- operator has &lt; 5 paid engagements — sample size too small; use problem-validation instead
- positioning is being set BEFORE first paid engagement — this is research, not refinement
- operator wants validation of an aspirational niche — framework rejects aspirations without evidence

## Prerequisites

- list of trailing-quarter paying customers with revenue, hours-spent, NPS / referral count
- the operator's prior positioning statement (so drift can be measured)
- 3-5 prospect rejections / lost deals with stated reason (negative evidence)

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/marketing/gtm-strategist/positioning-canvas` | Provides the canonical April Dunford 10-input layout this methodology compresses |
| `solo/marketing/conversion-optimizer/solo-lead-qualification-rubric` | Lead qualification thresholds feed customer cohort definition (who-actually-pays) |
| `solo/research/researcher/customer-interview` | Source of verbatim quotes feeding the &lt;Z&gt; field |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: cohort-from-payers, verbatim Z, negative evidence, drift gate, anti-aspiration | ~900 |
| `content/02-output-contract.xml` | essential | Positioning statement schema, ranking rules, forbidden patterns | ~700 |
| `content/03-failure-modes.xml` | essential | 6 failure modes: aspirational drift, cohort-of-one, jargon &lt;X&gt;, etc. | ~900 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `cohort_extraction_from_invoices` | haiku | Group by revenue/recurrence; mechanical |
| `verbatim_value_extraction` | sonnet | Per-customer quote-mining; bounded |
| `positioning_synthesis` | opus | Cross-cohort coherence; needs deep judgment |
| `drift_diff_vs_last_quarter` | sonnet | Structural diff |

## Templates

| File | Purpose |
|------|---------|
| `templates/positioning-statement.json` | Output schema |
| `templates/cohort-table.md` | Customer cohort comparison grid |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/quarterly-positioning-refresh.py` | Pulls invoices + interview notes → positioning candidates | Quarter-end review |

## Related

- parent skill: `pro/marketing/gtm-strategist/`
- peer methodologies: `positioning-canvas`, `pricing-strategy`
- external: [April Dunford — Obviously Awesome (2019)](https://www.aprildunford.com/obviously-awesome) · [Tyler Tringas — Earnest Capital positioning notes](https://earnestcapital.com/) · [Patrick McKenzie — Stop Calling Yourself A Freelancer](https://www.kalzumeus.com/2011/10/28/dont-call-yourself-a-programmer/)
