---
slug: vendor-margin-defense-checklist
tier: pro
group: pm
domain: pm
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: 6-pattern weekly detector for fixed-price margin erosion (silent scope creep, free analysis, missing CR, AI rework loops, gold-plating, sympathy discounts); emits MarginBleedReport with diplomatic client-conversation draft when single bleed >5% or cumulative >10%.
content_id: "b6103aaa6e45ad70"
complexity: medium
produces: checklist
est_tokens: 3700
tags: [margin-defense, outsource, fixed-price, scope-creep, vendor]
---
# Vendor Margin Defense Checklist

## Summary

**One-sentence:** A 6-pattern weekly checklist that detects silent margin-eroding behaviours (silent scope creep, free analysis, missing change requests, AI rework loops, gold-plating, sympathy discounting) before they consume 10–20% of fixed-price project margin.

**One-paragraph:** Fixed-price engagements lose margin not to dramatic incidents but to slow leaks: a free 4-hour analysis call that should have been billable, a "small change" that doubled scope, an AI agent looping on rework because no one wrote the change request, the senior dev gold-plating a UI nobody asked for. This methodology codifies 6 detection patterns with a weekly Friday cadence and a deterministic alert rule (any single bleed > 5% of project margin OR cumulative > 10% → diplomatic client conversation within 48h). Output: typed `MarginBleedReport` with detected leaks + dollar/hour quantification + draft client message. Built on Patrick McKenzie consulting essays and Jonathan Stark fixed-price playbook.

**Ефективно для:**

- Fixed-price freelance / micro-agency engagements ≥ 3 weeks long.
- Detecting silent leaks before they hit 10% cumulative bleed.
- Drafting the diplomatic client conversation (not delegating it to vendor instinct).
- Distinguishing real bleed from accounted-for `SALES_INVESTMENT` write-offs.

## Applies If (ALL must hold)

- Engagement is fixed-price OR T&M with a budget cap.
- Project duration ≥ 3 weeks (shorter does not accumulate enough patterns to detect).
- Written statement-of-work with deliverables list exists.
- ≥ 1 weekly client checkpoint scheduled.

## Skip If (ANY kills it)

- Open-ended T&M with no cap — no margin to defend.
- Engagement < 2 weeks — overhead exceeds value.
- Months-old retainer with high trust — pattern detection is noise.
- Engagement value < $5k — overhead exceeds protected margin.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Statement of Work | Markdown | client / signed PDF |
| Time tracking | CSV / Harvest / Toggl export | tracker |
| Comms thread | Slack export / email mbox | client channel |
| Change-request template | Markdown | this methodology |
| Quoted margin baseline | YAML | proposal |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[work-breakdown-structure]] | SOW deliverables map onto WBS leaves; bleed signals reference WBS ids. |
| [[solo-change-order-mini-contract]] | The CR sent when a bleed triggers must use this template. |
| [[solo-late-fee-and-pause-clause-template]] | Cumulative bleed > 10% may trigger pause-clause discussion. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: 6-pattern coverage, weekly cadence, bleed alert threshold, written CR, billable-by-default | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 for `MarginBleedReport` + forbidden patterns | ~800 |
| `content/03-failure-modes.xml` | essential | 6 modes: noise tolerance, polite-tax, false free-analysis, AI-rework false positive, gold-plate-misclassed, sympathy discount sustained | ~900 |
| `content/04-procedure.xml` | medium | 5-step weekly procedure: scan time-log → classify patterns → quantify → alert → draft | ~700 |
| `content/06-decision-tree.xml` | essential | Tree: bleed % per pattern + cumulative + write-off tag → suppress / report / alert / pause-clause | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `time-log-pattern-scan` | haiku | Mechanical detection against rules. |
| `pattern-classification` | sonnet | Bounded judgment (free_analysis vs SALES_INVESTMENT). |
| `bleed-quantification` | sonnet | Cost math with margin context. |
| `client-message-draft` | sonnet | Diplomatic but clear copy. |

## Templates

| File | Purpose |
|------|---------|
| `templates/bleed-report.json` | `MarginBleedReport` skeleton |
| `templates/change-request.md` | CR template the vendor sends when scope shifts |
| `templates/margin-alert-message.md` | Diplomatic client message for bleed > 5% |
| `templates/_smoke-test.json` | Minimum viable filled `MarginBleedReport` |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-vendor-margin-defense-checklist.py` | Validate a `MarginBleedReport` against the JSON Schema | Friday end-of-week pre-send check |

## Related

- [[work-breakdown-structure]]
- [[solo-change-order-mini-contract]]
- [[solo-late-fee-and-pause-clause-template]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (per-pattern severity, cumulative bleed, SALES_INVESTMENT tag, recurrence count) to suppress / report / alert / pause-clause. Every leaf references a rule from `01-core-rules.xml`.
