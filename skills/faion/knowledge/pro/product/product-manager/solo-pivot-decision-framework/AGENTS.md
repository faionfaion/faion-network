---
slug: solo-pivot-decision-framework
tier: pro
group: product
domain: pm
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "94baf20aa478bc69"
summary: Opinionated pivot taxonomy (segment / feature / business-model / tech / channel) with triggers, sunk-cost guardrails, and a hard rule for distinguishing a pivot from quitting.
tags: [pivot, product-market-fit, decision-framework, solo-saas, sunk-cost]
---

# Solo Pivot Decision Framework

## Summary

**One-sentence:** Opinionated pivot taxonomy (segment / feature / business-model / tech / channel) with triggers, sunk-cost guardrails, and a hard rule for distinguishing a pivot from quitting.

**One-paragraph:** Eric Ries listed 10 pivot types in The Lean Startup (2011); subsequent founder writing (Steve Blank, Dan Olsen, Mihail Eric) compressed them into 5 actionable categories for one-person teams. This methodology classifies a failing v1 against those 5 axes, surfaces the empirical triggers that justify a pivot vs continuing to optimise vs sunsetting, and forces a written falsifiable hypothesis ("the new bet works if X by date Y") before any rebuild work begins. Output: pivot-type classification + hypothesis + go/no-go threshold + sunk-cost statement.

## Applies If (ALL must hold)

- v1 has been live ≥ 90 days with paying or free users
- ≥ 1 of the failure signals is true: trailing-30-day MRR flat or down, activation &lt; 5%, churn &gt; 8%/mo, NPS &lt; 0
- operator has ≥ 8 weeks of personal runway to execute the pivot
- previous quarter included &gt; 4 hours of customer development conversation

## Skip If (ANY kills it)

- v1 launched &lt; 90 days ago — too early to call; iterate, don't pivot
- failure signals could be fixed by a single pricing, copy, or onboarding change — that's an optimisation, not a pivot
- operator has &lt; 8 weeks runway — pivoting on empty fuel is gambling; sunset and find income
- operator has not done any customer interviews — no signal to pivot from

## Prerequisites

- list of v1 metrics with trailing 90-day delta (MRR, activation, churn, NPS, signups)
- 5+ customer interview notes from the trailing 30 days
- a list of features built (with effort) and their adoption rate
- written sunk-cost statement: "$X spent, Y months spent, what we LEARNED that survives a pivot"

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/product/product-manager/product-market-fit-hunt` | Provides the leading indicators of PMF; pivot framework consumes those signals |
| `solo/research/researcher/problem-validation` | Pivot hypotheses must be validated upstream before commit |
| `pro/marketing/gtm-strategist/positioning-canvas` | A segment pivot triggers a positioning rewrite |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: taxonomy, falsifiable hypothesis, sunk-cost separation, runway-gate, quit-vs-pivot | ~1000 |
| `content/02-output-contract.xml` | essential | `PivotDecision` schema with hypothesis, threshold, kill-criterion | ~700 |
| `content/03-failure-modes.xml` | essential | 6 modes: shiny-object, founder-rationalisation, false-signal, etc. | ~900 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `metric_extraction_from_dashboards` | haiku | Mechanical |
| `pivot_type_classification` | sonnet | Bounded judgment vs taxonomy |
| `hypothesis_falsification_design` | opus | Needs deep synthesis |
| `sunk_cost_separation` | sonnet | Pattern-matching cost vs learning |

## Templates

| File | Purpose |
|------|---------|
| `templates/pivot-decision.json` | Output schema |
| `templates/pivot-hypothesis-canvas.md` | Pre-pivot canvas operator fills |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/pivot-readiness-check.py` | Validates prerequisites + runway gate | Before kicking off pivot synthesis |

## Related

- parent skill: `pro/product/product-manager/`
- peer methodologies: `product-market-fit-hunt`, `feature-prioritisation`
- external: [Eric Ries — The Lean Startup (2011)](http://theleanstartup.com/) · [Steve Blank — Pivot or Persevere](https://steveblank.com/2013/03/04/should-the-startup-pivot-tools-for-the-trade/) · [Dan Olsen — The Lean Product Playbook](https://dan-olsen.com/lpp/)
