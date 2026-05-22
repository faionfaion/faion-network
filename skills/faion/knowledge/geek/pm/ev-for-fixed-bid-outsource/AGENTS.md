---
slug: ev-for-fixed-bid-outsource
tier: geek
group: pm
domain: pm
version: 1.1.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: "Runs two parallel EVM ledgers (client scope vs vendor margin) for fixed-bid outsource engagements so margin burn is caught weeks before close-out."
content_id: "764de2ce69832a93"
complexity: deep
produces: report
est_tokens: 4000
tags: [evm, fixed-bid, outsourcing, margin-tracking, two-ledger]
---
# Ev For Fixed Bid Outsource

## Summary

**One-sentence:** Runs two parallel EVM ledgers (client scope vs vendor margin) for fixed-bid outsource engagements so margin burn is caught weeks before close-out.

**One-paragraph:** Runs two parallel EVM ledgers (client scope vs vendor margin) for fixed-bid outsource engagements so margin burn is caught weeks before close-out. The methodology is anchored to a single named consumer (a PM, EM, portfolio owner, or downstream agent) and a fixed-shape artefact that downstream review can sign off without re-deriving reasoning. Inputs are explicit, evidence is anchored, and the artefact carries `version`, `owner`, and `last_reviewed` so it remains a living operating tool rather than folklore. Outputs that fail the contract are rejected at validation time, not at executive review.

**Ефективно для:** Vendor PM-у на fixed-bid контракті — щоб маржа не зникла мовчки до close-out review.

## Applies If (ALL must hold)

- Engagement is fixed-bid or fixed-bid+T&M-overlay (not pure T&M).
- Vendor PM owns internal labour cost tracking with at least week-grain resolution.
- Work breakdown into ≥5 work packages is feasible and stable.
- A change-request mechanism exists in the contract.

## Skip If (ANY kills it)

- Pure T&M engagements — generic EVM suffices because revenue tracks effort.
- Engagement < 6 weeks or < $50k — EVM overhead exceeds signal value.
- WBS cannot be sized into 1-5% work packages — ledger granularity will be wrong.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Contract terms | PDF/Markdown | client-facing contract repo |
| Internal labour cost feed | CSV/API | HR/finance time-tracking tool |
| Work-package list (1-5% of total value each) | CSV/Markdown | vendor PM |
| Change-request log | tracker | contracts system |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/pm/portfolio-evm-rollup-method` | Portfolio rollup the two ledgers feed into. |
| `geek/pm/project-manager/ai-earned-value-management` | Sensor-driven AC feed the cost ledger can plug into. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules every application enforces | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid/invalid examples + self-check | ~800 |
| `content/03-failure-modes.xml` | essential | Antipatterns with symptom / root-cause / fix | ~900 |
| `content/06-decision-tree.xml` | essential | Root question → branches → conclusions (rule refs) | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `ledger-baseline-fill` | haiku | Template fill from contract + WBS. |
| `weekly-ev-compute` | sonnet | Bounded judgement: classify package status against earning rules. |
| `variance-attribution` | opus | Cross-cause synthesis at close — feeds next-bid model. |

## Templates

| File | Purpose |
|------|---------|
| `templates/skeleton.json` | JSON Schema for the dual-ledger weekly artefact: ledger-A (PV-S, EV-S, SPI-S) + ledger-B (PV-C, EV-C, AC-C, CPI-C) + thresholds + change-requests. |
| `templates/header.yaml` | Frontmatter contract: owner, version, last_reviewed for the produced artefact. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ev-for-fixed-bid-outsource.py` | Validate produced artefact against the JSON Schema in `02-output-contract.xml`. | Pre-merge and on every artefact refresh. |

## Related

- [[portfolio-evm-rollup-method]]
- [[ai-earned-value-management]]
- [[program-dependency-aging-chart-recipe]]

## Decision tree

The mandatory decision tree at `content/06-decision-tree.xml` Decides whether to run dual-ledger EVM (fixed-bid + ≥6 weeks + 1-5% WBS + weekly cost grain), block until WBS is fixed, or skip for T&M / small engagements. Run before week-1 baselining.
