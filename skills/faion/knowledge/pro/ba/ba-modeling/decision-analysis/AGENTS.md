---
slug: decision-analysis
tier: pro
group: ba
domain: ba
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Structured 6-step process for evaluating options against weighted criteria: define decision → identify options → define and lock criteria with weights → score options with evidence URLs per cell → sensitivity analysis (±20% weight Monte Carlo) → document rationale.
content_id: "540833b2f15e6888"
tags: [decision-making, option-evaluation, sensitivity-analysis, monte-carlo, decision-matrix]
---
# Decision Analysis

## Summary

**One-sentence:** Structured 6-step process for evaluating options against weighted criteria: define decision → identify options → define and lock criteria with weights → score options with evidence URLs per cell → sensitivity analysis (±20% weight Monte Carlo) → document rationale.

**One-paragraph:** Structured 6-step process for evaluating options against weighted criteria: define decision → identify options → define and lock criteria with weights → score options with evidence URLs per cell → sensitivity analysis (±20% weight Monte Carlo) → document rationale. Weights are locked before scoring; sensitivity analysis determines whether the recommendation is robust or fragile (top option wins less than 70% of Monte Carlo trials → escalate to human).

## Applies If (ALL must hold)

- Reversible-but-expensive choice with three or more candidate options where the team is sliding toward gut feel (CRM selection, build-vs-buy, LLM provider choice).
- Stakeholders disagree because they secretly weight criteria differently — making weights explicit collapses the argument.
- Decision will be re-litigated later (board review, audit, post-mortem) and a written rationale is needed.
- Comparing N options against a current baseline (Pugh matrix mode).
- A decision has long-tail risk that only surfaces when tabulated (vendor lock-in, regulatory exposure).
- Sequential / conditional decisions with probabilities — switch to decision tree with expected value.

## Skip If (ANY kills it)

- Two-option, low-cost, easily reversible decisions — use a 5-minute pros/cons list.
- Decision is actually about strategy, not selection — run a brainstorm session first.
- Analysis is retrofitted to justify a decision already made (the #1 failure mode).
- Pure financial trade-offs with quantifiable cash flows — use NPV / discounted cash flow directly.
- Decisions under deep uncertainty where numbers have more than one order-of-magnitude error.

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

- parent skill: `pro/ba/ba-modeling/`
