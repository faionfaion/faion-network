<!-- purpose: legacy template for ads-ab-testing-ads — test-brief -->
<!-- consumes: per AGENTS.md Prerequisites -->
<!-- produces: artefact per content/02-output-contract.xml -->
<!-- depends-on: content/01-core-rules.xml, content/06-decision-tree.xml -->
<!-- token-budget-impact: ~400-1200 tokens when loaded as context -->

# A/B Test Brief: [Test Name]

## Hypothesis

We believe [variant description] will outperform [control description] because [specific reasoning based on data or theory].

## Variables

| Element | Control | Variant |
|---------|---------|---------|
| Changed element | [Current] | [New] |
| Held constant | [List everything identical] | [Same] |

## Test Parameters

- Platform: [Meta Experiments / Google Ads Experiments / Manual]
- Audience: [Name — identical for both]
- Budget: $[X] per variant per day
- Duration: [X] days (minimum)
- Primary metric: [CTR / Conversions / CPA]
- Secondary metric (guardrail): [Must not regress by more than X%]
- Required sample: [X] impressions per variant / [X] conversions per variant
- Significance method: [Bayesian P>0.95 / Frequentist 95% CI]
- Stop date: [Date — do not stop early]

## Baseline

- Current [primary metric]: [X%/$X]
- Minimum detectable effect: [Y%]
- Expected outcome: [Variant wins / Unsure / Directional only]
