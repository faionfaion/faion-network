---
slug: strategy-methods
tier: pro
group: ba
domain: ba
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Toolkit for weighted multi-criteria scoring of solution options, limitation/defect assessment, and BABOK 50-technique lookup.
content_id: "907e05d8c540b473"
tags: [strategy, options-scoring, decision-analysis, babok-techniques, limitation-assessment]
---
# Strategy Methods: Solution Options and Limitation Assessment

## Summary

**One-sentence:** Toolkit for weighted multi-criteria scoring of solution options, limitation/defect assessment, and BABOK 50-technique lookup.

**One-paragraph:** Toolkit for weighted multi-criteria scoring of solution options, limitation/defect assessment, and BABOK 50-technique lookup. Without a structured scoring method, solution recommendations are driven by advocacy rather than evidence. Weighted criteria scoring forces explicit trade-offs; sensitivity analysis reveals whether the recommendation is robust or brittle. Limitation registers with 5-whys root causes prevent remediation from landing on symptoms.

## Applies If (ALL must hold)

- Two or more solution options exist (build/buy/partner/SaaS/status-quo) and a sponsor needs a defensible recommendation with a numeric weighted score
- Vendor/RFP shortlists where 3-5 finalists must be reduced to a single recommendation
- Architecture decisions where competing patterns need comparison beyond gut feel
- Post-deployment when users surface defects and someone must decide fix/workaround/accept/defer
- Steering-committee decision packs requiring alternatives, criteria, weights, and sensitivity analysis
- Quick BA technique lookup: matching a sub-task to the right BABOK technique from the 50-technique reference

## Skip If (ANY kills it)

- One option with an obvious winner — do not invent strawman alternatives to fill a matrix
- Reversible/two-way-door decisions (feature flag, copy change, small refactor) — use a one-line ADR
- Decisions dominated by a single hard constraint (regulatory deadline, cost ceiling) — filter on that constraint alone
- Pure quantitative cash-flow comparisons — use NPV/IRR/payback instead
- Limitation assessment for incidents with a known cause and an in-flight patch — use post-mortem/5-whys

## Prerequisites

- TBD — list concrete input artifacts and where they come from

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `TBD/path` | TBD — what upstream output this consumes |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules migrated from v1 methodology | ~800 |
| `content/02-output-contract.xml` | essential | Output schema (stub — fill from v1 patterns) | ~800 |
| `content/03-failure-modes.xml` | essential | Antipatterns migrated from v1 methodology | ~800 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| TBD | sonnet | TBD |

## Templates

| File | Purpose |
|------|---------|
| TBD | TBD |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| TBD | TBD | TBD |

## Related

- parent skill: `pro/ba/ba-core/`
