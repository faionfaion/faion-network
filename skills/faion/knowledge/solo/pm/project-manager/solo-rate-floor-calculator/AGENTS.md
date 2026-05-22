---
slug: solo-rate-floor-calculator
tier: solo
group: pm
domain: pm
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "1e8053236d44e4ef"
summary: Solo-specific effective-hourly calculator that loads target income with taxes, downtime, marketing time, benefits, and tooling cost to produce a defensible rate floor below which engagements are mathematically unprofitable.
tags: [pricing, rate-floor, freelance, financial-modeling, hourly]
---

# Solo Rate Floor Calculator

## Summary

**One-sentence:** Solo-specific effective-hourly calculator that loads target income with taxes, downtime, marketing time, benefits, and tooling cost to produce a defensible rate floor below which engagements are mathematically unprofitable.

**One-paragraph:** Generic "billable hours" calculators (Kalzumeus, freelance-rate-calculator.com) assume an idealised solo operator with linear hours and zero non-billable overhead. In practice, ~40% of a solo's calendar is sales, admin, learning, and recovery time. This methodology asks for 7 inputs (target income, working weeks, billable %, tax rate, benefit cost, tooling cost, profit margin), runs a load formula derived from the Patrick McKenzie "consultant compensation" essay, and emits a floor rate with sensitivity bands. Output: `RateFloor` object with floor_usd_per_hour, project_minimum, defensible breakdown.

## Applies If (ALL must hold)

- operator is solo (no W-2 income, no co-founder splitting revenue)
- engagement type ∈ {hourly, fixed-price, retainer-with-hour-cap}
- operator has 6+ months of historical billable-vs-total time data OR willingness to estimate honestly
- operator is in a tax jurisdiction with known effective rate (US, EU, UK, CA, AU)

## Skip If (ANY kills it)

- operator has a stable W-2 and freelancing is side income — rate floor logic doesn't apply
- operator is in an exotic tax regime without a stable effective rate
- the engagement is value-based or equity-based — different methodology
- engagement is &lt; 10 hours total — fixed micro-price, floor irrelevant

## Prerequisites

- target annual gross income (USD) — the number that pays operator's life
- known tax bracket / effective rate including self-employment loading
- expected billable hours per year (be honest — most solos overestimate by 50%)
- tooling subscriptions running annually (Figma, Notion, hosting, AI subs)
- desired profit margin above operator's salary (typically 15-30%)

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/pm/project-manager/financial-basics` | Tax-rate and benefit-cost source-of-truth |
| `solo/marketing/conversion-optimizer/solo-lead-qualification-rubric` | Floor result is consumed by qualification rubric (r4) |
| `solo/comms/communicator/proposal-anatomy` | Floor pricing flows into proposal pricing |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: honest billable %, all-in tax, downtime, profit-margin, sensitivity | ~900 |
| `content/02-output-contract.xml` | essential | `RateFloor` schema with bands and breakdown | ~700 |
| `content/03-failure-modes.xml` | essential | 6 modes: optimistic billable %, ignored taxes, etc. | ~900 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `input_validation` | haiku | Range checks |
| `floor_calculation` | sonnet | Deterministic math + cross-checks |
| `sensitivity_analysis` | sonnet | Tabular scenarios |
| `defense_narrative` | sonnet | Short explanation for prospect-facing use |

## Templates

| File | Purpose |
|------|---------|
| `templates/rate-floor.json` | Output schema |
| `templates/load-spreadsheet.csv` | Editable input grid |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/compute-floor.py` | Inputs → floor + bands | Quarterly review or per major engagement |

## Related

- parent skill: `solo/pm/project-manager/`
- peer methodologies: `solo-lead-qualification-rubric`, `solo-time-tracking-discipline`
- external: [Patrick McKenzie — Don't Call Yourself A Programmer](https://www.kalzumeus.com/2011/10/28/dont-call-yourself-a-programmer/) · [Jonathan Stark — Hourly Billing Is Nuts](https://jonathanstark.com/hbinz) · [Brennan Dunn — Double Your Freelancing Rate](https://doubleyourfreelancing.com/)
