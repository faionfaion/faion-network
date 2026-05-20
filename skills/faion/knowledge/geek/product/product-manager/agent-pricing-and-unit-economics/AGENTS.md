---
slug: agent-pricing-and-unit-economics
tier: geek
group: product
domain: product-manager
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "293399a144a3bebf"
summary: Per-task cost modelling, gross margin computation, and pricing-model selection (seat / task / outcome) for LLM-agent products targeting $5-100K MRR.
tags: [llm, agent, pricing, unit-economics, gross-margin, cost-of-goods-sold, outcome-pricing]
---
# LLM-Agent Product Pricing & Unit Economics

## Summary

**One-sentence:** Per-task cost modelling, gross margin computation, and pricing-model selection (seat / task / outcome) for LLM-agent products targeting $5-100K MRR.

**One-paragraph:** SaaS pricing guides assume near-zero marginal cost; agent products have material per-request cost (tokens, retrieval, tool calls) that scales with usage. Mechanism: compute per-task COGS (input_tokens × input_price + output_tokens × output_price + retrieval_cost + tool_call_cost + infra_cost), set a target gross margin (70%+ for healthy SaaS, 50-60% acceptable for early), pick pricing model — (A) per-seat at fixed MAU cap, (B) per-task / metered, (C) outcome-based — based on task COGS variance and customer willingness. The wrong model leaves money on the table OR bankrupts on a heavy user. Output: per-product unit economics report + a defended pricing tier set.

## Applies If (ALL must hold)

- you are building or have launched an LLM-agent product (vertical agent, AI feature, SaaS with AI core)
- you are or expect to be in the $5-100K MRR range (post-experiment, pre-scale)
- agent costs are material (≥ 10% of price you intend to charge)
- you control pricing model selection (not a marketplace forced into a fixed scheme)

## Skip If (ANY kills it)

- pre-revenue / not yet selling — use value-prop work first, pricing later
- enterprise sales with custom contracts — pricing is negotiated, this methodology is for self-serve
- per-task cost &lt; 1% of price (e.g., embeddings-only feature in a larger SaaS) — SaaS pricing methodology suffices
- compute is free / sponsored / running on customer's own credentials — different math applies

## Prerequisites (must be true before starting)

- baseline of average input + output tokens per task (measure 100+ real tasks, not estimate)
- current model pricing from providers (Anthropic, OpenAI, etc.)
- retrieval system cost per query (vector DB / embeddings / search)
- tool-call costs per task (function calls, external API fees)
- target gross margin (e.g., 70%) and operating margin
- customer willingness-to-pay data (from sales conversations OR competitor pricing)

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/ai/ai-agents/<vertical-agent-design>` | Agent architecture decisions feed COGS computation |
| `solo/marketing/gtm-strategist/ops-pricing-strategy` | General pricing tactics; this methodology specializes for token-cost products |
| `geek/product/product-manager/ai-native-product-development` | Product positioning context |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: measure cogs not estimate, target gross margin floor, pricing model fits cost variance, cap-protect heavy users, repricing on model changes | ~950 |
| `content/02-output-contract.xml` | essential | Unit economics report schema, pricing tier schema, forbidden patterns | ~750 |
| `content/03-failure-modes.xml` | essential | 7 failure modes (token-blind pricing, unmetered flat, ignored retrieval cost, no cap, model-change blindness, outcome-pricing fantasy, free-tier bleed) | ~1000 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `cogs_per_task_compute` | haiku | Deterministic arithmetic on measured token counts |
| `pricing_model_recommendation` | opus | Cross-input judgment: variance, customer behavior, competitive context |
| `cap_threshold_synthesis` | sonnet | Calibrate fair-use cap from MAU + heavy-user distribution |
| `repricing_trigger_alert` | sonnet | Detect model-price change or usage-distribution shift |

## Templates

| File | Purpose |
|------|---------|
| `templates/unit-economics-report.md` | Per-product COGS + margin + pricing recommendation |
| `templates/pricing-tier-table.md` | Public pricing page tier definitions |
| `templates/cap-policy.md` | Fair-use cap definition + customer-facing language |
| `templates/repricing-runbook.md` | When/how to reprice when model costs change |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/measure-task-tokens.py` | Sample real tasks → input/output token distributions | Pre-pricing analysis |
| `scripts/cogs-calculator.py` | Compute per-task COGS from token + retrieval + tool costs | Pricing design |
| `scripts/usage-distribution-check.py` | Detect heavy-user tail that violates cap economics | Monthly post-launch |

## Related

- parent skill: `geek/product/product-manager/`
- peer methodologies: `ai-native-product-development`, `ops-pricing-strategy`
- external: [a16z - LLM cost-economics analysis](https://a16z.com/) · [Anthropic pricing](https://www.anthropic.com/pricing) · [Tomasz Tunguz - AI pricing models](https://tomtunguz.com/)
