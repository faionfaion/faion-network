# LLM-Agent Product Pricing & Unit Economics

## Summary

**One-sentence:** Measure per-task COGS (tokens + retrieval + tool calls + infra), set a gross-margin floor, pick a pricing model that fits cost variance, and cap fair-use exposure — for LLM-agent products in the $5-100K MRR band where token-cost variance can outpace a flat seat fee.

**One-paragraph:** SaaS pricing guides assume near-zero marginal cost; agent products have material per-request cost (tokens, retrieval, tool calls) that scales with usage. This methodology pins five rules: measure per-task COGS (don't estimate), target ≥60% gross margin (70%+ for healthy SaaS), pick a pricing model whose shape matches COGS variance (per-seat at fixed MAU cap for low-variance, metered for mid, outcome-based for high), cap heavy-user exposure with a fair-use threshold, and re-price whenever underlying model prices move ≥10%. Output: a defended unit-economics report + pricing tier table + cap policy + repricing runbook.

**Ефективно для:** founder LLM-агент-стартапу в $5-100K MRR, який не хоче, щоб один heavy-user з'їв увесь місячний gross profit.

## Applies If (ALL must hold)

- Building or running an LLM-agent product (vertical agent, AI feature, AI-core SaaS).
- In or expecting to be in the $5-100K MRR range (post-experiment, pre-scale).
- Agent COGS are material (≥10% of intended price).
- You control pricing-model selection (not a marketplace forced into a fixed scheme).
- You have ≥100 real tasks logged or can measure them.

## Skip If (ANY kills it)

- Pre-revenue / not yet selling — do value-prop work first, pricing later.
- Enterprise sales with custom contracts — pricing is negotiated, not self-serve.
- Per-task cost < 1% of price (e.g. embeddings-only feature in a larger SaaS) — generic SaaS pricing suffices.
- Compute is free / sponsored / on customer's own credentials — different math applies.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| 100+ real tasks token sample | CSV / log query | telemetry store |
| Current model pricing | YAML | provider pricing pages |
| Retrieval cost per query | $ figure | vector DB / search bill |
| Tool-call cost per task | $ figure | external API logs |
| Target gross margin | % | finance |
| Customer willingness-to-pay data | doc / sales notes | sales / market research |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/ai-core/ai-agents` | Agent architecture decisions feed COGS computation. |
| `geek/product/product-manager/ai-native-product-development` | Product positioning context. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: measure-COGS-not-estimate, gross-margin-floor, pricing-model-fits-variance, cap-protect-heavy-users, reprice-on-model-changes | ~950 |
| `content/02-output-contract.xml` | essential | Unit-economics report schema + pricing-tier schema + forbidden patterns | ~750 |
| `content/03-failure-modes.xml` | essential | 5+ failure modes (token-blind pricing, unmetered flat, ignored retrieval cost, no cap, model-change blindness) | ~1000 |
| `content/06-decision-tree.xml` | essential | Variance-based pricing-model branch + cap-required gate | ~320 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `cogs_per_task_compute` | haiku | Deterministic arithmetic on measured token counts. |
| `pricing_model_recommendation` | opus | Cross-input judgment: variance, customer behaviour, competitive context. |
| `cap_threshold_synthesis` | sonnet | Calibrate fair-use cap from MAU + heavy-user distribution. |

## Templates

| File | Purpose |
|------|---------|
| `templates/unit-economics-report.md` | Per-product COGS + margin + pricing recommendation. |
| `templates/pricing-tier-table.md` | Public pricing page tier definitions. |
| `templates/cap-policy.md` | Fair-use cap definition + customer-facing language. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-agent-pricing-and-unit-economics.py` | Validate a unit-economics report against rules (margin floor, measured COGS, pricing-model fit, cap present, repricing trigger). | Pre-publish for any pricing change. |

## Related

- [[ai-native-product-development]] — sibling methodology providing positioning context.
- [[agentic-ai-product-development]] — peer methodology consuming the cost-per-task metric.

## Decision tree

The mandatory tree at `content/06-decision-tree.xml` first checks whether COGS are measured (not estimated) and the gross-margin floor is hit. If not → block. Then branches on COGS variance: low → per-seat + cap, mid → metered, high → outcome-based. Always requires a fair-use cap and a repricing trigger.
