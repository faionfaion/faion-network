---
slug: aarrr-pirate-metrics
tier: pro
group: marketing
domain: marketing
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Five-stage growth funnel — Acquisition, Activation, Retention, Revenue, Referral — with per-stage numeric metric + baseline + bottleneck-identification rule before any tactic ships.
content_id: "aarrr-pirate-1"
complexity: medium
produces: report
est_tokens: 3200
tags: [growth, aarrr, metrics, funnel, plg]
---
# AARRR Pirate Metrics

## Summary

**One-sentence:** Five-stage growth funnel — Acquisition, Activation, Retention, Revenue, Referral — with per-stage numeric metric + baseline + bottleneck-identification rule before any tactic ships.

**One-paragraph:** AARRR is the canonical five-stage funnel for product-led growth. This methodology pins discipline around its use: every stage MUST have ≥1 numeric metric with a 30-day baseline; the funnel is read top-down (a leaky upstream stage invalidates downstream optimization); bottleneck is identified before tactics chosen; tactics tagged with the stage they move; weekly dashboard publishes all 5 stages even when only 1 is changing.

**Ефективно для:**

- Growth-marketer onboarding to a new product — first dashboard.
- Quarterly growth review — bottleneck identification.
- Pre-PMF founder — confirm correct stage to invest.
- Agency client kickoff — shared vocabulary.

## Applies If (ALL must hold)

- Product with ≥1 acquisition channel + measurable conversion event.
- Analytics layer (PostHog / Mixpanel / Amplitude / GA4 / SQL).
- 30-day history available.
- Owner with authority to direct tactics across stages.

## Skip If (ANY kills it)

- Pre-launch — no acquisition signal yet.
- Pure brand product (no direct-response metric).
- Service business without product funnel — different framework.
- Single one-shot transaction (no retention surface).

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Acquisition source data | dashboard / API | analytics |
| Activation event definition | spec | product |
| Retention cohort query | SQL / dashboard | analytics |
| Revenue / billing events | dashboard | billing |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[ab-testing-basics]] | Downstream tactics use A/B framework. |
| [[experiment-hypothesis-scoring]] | Tactic backlog feeds AARRR stages. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: metric-per-stage-with-baseline, top-down-read, bottleneck-named-before-tactic, weekly-all-five-published, tactic-stage-tagged | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema for report + valid/invalid | 800 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns with symptom/root-cause/fix | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure | 600 |
| `content/05-examples.xml` | essential | Worked example end-to-end | 500 |
| `content/06-decision-tree.xml` | essential | Routing tree → rule from 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `compute-snapshot` | haiku | Numeric extraction. |
| `identify-bottleneck` | sonnet | Top-down judgment. |

## Templates

| File | Purpose |
|------|---------|
| `templates/weekly-report.json` | JSON example of weekly AARRR report |
| `templates/weekly-dashboard.md` | Markdown dashboard skeleton |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-aarrr-pirate-metrics.py` | Validate one report JSON against the schema | After draft, before publish |

## Related

- [[ab-testing-basics]]
- [[experiment-hypothesis-scoring]]
- [[plg-optimization-tactics]]

## Decision tree

See `content/06-decision-tree.xml`. The tree routes observable signals to one of the rules in `01-core-rules.xml`. Use it before producing the output — picking the wrong branch is the most common failure.
