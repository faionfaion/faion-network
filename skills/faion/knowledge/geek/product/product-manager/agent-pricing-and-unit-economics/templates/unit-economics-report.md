<!--
purpose: Unit-economics report skeleton for an LLM-agent product.
consumes: measured tokens + provider prices + retrieval + tool costs + target margin.
produces: A defended per-product COGS / margin / pricing recommendation.
depends-on: ../scripts/validate-agent-pricing-and-unit-economics.py.
token-budget-impact: ~600 tokens when filled.
-->

---
product: "<product-slug>"
owner: "ai-pm:<person>"
version: "1.0.0"
last_reviewed: "2026-05-22"
---

# Unit economics — <product>

## Per-task COGS (measured, ≥100 tasks)

- Input tokens (median): <n> @ $<input_price>/1k → $<x>
- Output tokens (median): <n> @ $<output_price>/1k → $<x>
- Retrieval cost: $<x>/task
- Tool-call cost: $<x>/task
- Infra share: $<x>/task
- **Total COGS / task: $<sum>**

## Variance

- p50 COGS: $<x>
- p95 COGS: $<x>
- Variance class: low | mid | high (p95/p50 ratio)

## Gross margin at proposed price

- Proposed price / task: $<y>
- Gross margin: <margin_pct>%
- Floor: 60% (90% target)

## Recommended pricing model

- <per-seat | metered | outcome> with rationale tied to variance class.

## Fair-use cap

- Threshold: <n tasks/MAU/month>
- Overage policy: <text>

## Repricing trigger

- Re-evaluate if model_provider_price changes >= 10% OR usage distribution p95 shifts >= 50%.

## Decisions / Actions / Next review

- <decision 1>
- Next review: <ISO date, ≤90 days>
