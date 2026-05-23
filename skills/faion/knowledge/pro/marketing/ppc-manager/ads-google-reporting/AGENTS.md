---
slug: ads-google-reporting
tier: pro
group: marketing
domain: marketing
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Generates a Google Ads weekly/monthly performance report + ranked action queue tied to conversion metrics, segmented by device / network / location / audience / time.
content_id: "066b118e7d71cf03"
complexity: medium
produces: report
est_tokens: 4400
tags: [google-ads, reporting, optimization, analytics, metrics]
---
# Google Ads Reporting and Optimization

## Summary

**One-sentence:** Generates a Google Ads weekly/monthly performance report + ranked action queue tied to conversion metrics, segmented by device / network / location / audience / time.

**One-paragraph:** Structured analyze-decide-act cycle for Google Ads: pull Overview / Campaigns / Keywords / Search Terms / Auction Insights, segment by device, network, location, audience and time, diagnose each KPI deviation via a fixed symptom→cause map (low CTR → copy; low QS → ad-group split; high CPA → bids / quality / targeting; low IS → budget / bid), and emit a ranked action queue. Vanity metrics (clicks, impressions, CTR) are diagnostic only — never targets.

**Ефективно для:**

- Тижневий / місячний цикл оптимізації Google Ads з ≥30 днями історії та ≥100 конверсій на варіант.
- Діагностика падіння CPA / IS / CR через карту симптом→корінь→дія.
- Сегментний аналіз (device, network, location, audience, time) для прицільних bid-adjustments.
- Пріоритезація дій по spend × deviation × confidence.

## Applies If (ALL must hold)

- Continuous paid search campaigns with ≥30 days of data and ≥100 conversions per variant.
- Diagnosing CPA spikes, falling impression share, or declining conversion rate.
- Multi-campaign portfolio where optimization effort must be prioritized.
- Scaling spend and need to attribute movement to a specific lever (bids, budgets, targeting, creative).

## Skip If (ANY kills it)

- Accounts under 30 days old — algorithmic variance dominates treatment effect.
- Campaigns under 100 conversions per variant — insufficient data; ship better variant and wait.
- Holiday peaks (Black Friday, Q4) — exogenous demand masks creative/targeting changes.
- Daily micro-optimization — day-to-day noise resets learning; weekly cadence only.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Google Ads account access | OAuth / login | ad-platform owner |
| Conversion tracking baseline | GA4 / GTAG events | ads-conversion-tracking methodology |
| KPI target table | JSON / Markdown | stakeholder + finance |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/marketing/ppc-manager/ads-conversion-tracking` | Conversion events must be defined before reporting on CPA / ROAS. |
| `pro/marketing/ppc-manager/ads-attribution-models` | Attribution choice determines which conversions count per channel. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules for ads-google-reporting | 1200 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid examples | 900 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns with symptom/root-cause/fix | 900 |
| `content/04-procedure.xml` | essential | 5-step procedure | 950 |
| `content/05-examples.xml` | medium | One worked end-to-end example | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule ref | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `pull-and-segment` | haiku | Mechanical data fetch + table assembly. |
| `diagnose-deviation` | sonnet | Per-metric symptom→cause judgment. |
| `prioritize-actions` | sonnet | Rank by spend × deviation × confidence. |

## Templates

| File | Purpose |
|------|---------|
| `templates/performance-report.md` | Monthly performance report Markdown skeleton. |
| `templates/weekly-checklist.md` | 30-minute weekly optimization checklist. |
| `templates/report-artefact.json` | Schema-conformant sample artefact used by validator self-test. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ads-google-reporting.py` | Validate output artefact against the JSON Schema in `content/02-output-contract.xml` | Pre-commit hook + CI on every methodology PR |

## Related

- [[ads-google-keywords]]
- [[ads-google-creative]]
- [[ads-conversion-tracking]]
- [[ads-attribution-models]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from one observable (do preconditions hold?) and maps each branch to a concrete `<conclusion ref="rule-id">` from `01-core-rules.xml`. Use it whenever the operator must choose between applying this methodology, deferring, or routing to a sibling.
