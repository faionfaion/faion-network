# Business Model Research

## Summary

**One-sentence:** Builds a Business Model Canvas (9 blocks, Hard/Soft tagged) with P10/P50/P90 unit economics and 5 stress tests, ending in a viable / viable-with-fixes / not-viable verdict.

**One-paragraph:** Systematic analysis of how a business will create, deliver, and capture value, structured as a Business Model Canvas (9 blocks) plus P10/P50/P90 unit economics (CAC, LTV, LTV:CAC, payback period) and 5 stress tests. Every Canvas cell is tagged Hard (sourced) or Soft (founder estimate); LTV is capped at a 60-month lifetime; the verdict reports on the P10 scenario, never the median.

**Ефективно для:**

- Pre-spec фаза: засновник має ідею, але не має захищеної monetization story.
- Pricing-рішення в умовах невизначеності: ARPU/margin/churn треба змоделювати до price page.
- Pivot review: продукт існує, але LTV:CAC < 3:1 і модель може бути зламана.
- Investor memo / seed deck з секцією 'How we make money' + stress tests.
- Multi-revenue-stream дизайн: subscription + usage + marketplace fee blend.

## Applies If (ALL must hold)

- Founder has a product idea but no defended monetization story.
- Pricing decision under uncertainty: ARPU, margin, and churn assumptions must be modeled before a price page ships.
- Pivot review: existing product is missing LTV:CAC >= 3:1 and the model itself may be broken.
- Investor memo / seed deck requires a 'How we make money' section with stress tests.
- Multi-revenue-stream design: subscription + usage + marketplace fee blends in one product.

## Skip If (ANY kills it)

- Internal tools, OSS side-projects, or hobby apps with no intent to monetize.
- Already-shipping product with 12+ months of real ARR data — use aarrr-pirate-metrics instead.
- Pure infrastructure libraries where revenue is a downstream consequence.
- Government or grant-funded work where the customer is a budget line, not a buyer.
- Two-sided marketplace pre-launch with zero supply — run network-effects discovery first.
- Hardware or regulated products where margin is dictated by BOM + compliance, not chosen.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Value-chain map | markdown / diagram | founder interview |
| Public competitor list | list with pricing URLs | competitor-analysis output |
| ARPU and churn assumptions | CSV with Hard/Soft tags | founder + comparables harvest |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[competitor-analysis]] | supplies comparable companies that ground ARPU and churn cells |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules + skip gate | ~1200 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid/invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns (symptom/root-cause/fix) | ~900 |
| `content/04-procedure.xml` | essential | 6-step procedure end-to-end | ~900 |
| `content/05-examples.xml` | essential | Worked example trace | ~900 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule id | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `value-chain-map` | sonnet | Structured diagramming with light judgment. |
| `comparable-harvesting` | haiku | Mechanical WebSearch + URL fetch. |
| `canvas-fill` | sonnet | Synthesis across 9 blocks with Hard/Soft tagging. |
| `unit-economics-compute` | sonnet | Formula application with P10/P50/P90 ranges. |
| `stress-test-verdict` | opus | Strategic interpretation of 5 stress tests + verdict. |

## Templates

| File | Purpose |
|------|---------|
| `templates/business-model-canvas.md` | 9-block Canvas skeleton with Hard/Soft tagging |
| `templates/unit-econ-scenarios.sh` | P10/P50/P90 LTV:CAC + payback calculator from CLI arguments |
| `templates/business-model-report.md` | Final report skeleton: Canvas + unit economics + stress tests + verdict |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-business-model-research.py` | Validate the artefact against `content/02-output-contract.xml` schema | CI on each artefact change; pre-commit |

## Related

- [[competitor-analysis]]
- [[market-research-tam-sam-som]]
- [[distribution-channel-research]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals onto a rule id from `content/01-core-rules.xml`, so the agent can decide in one read whether to run the methodology, halt, or route elsewhere. Use it whenever the inputs feel ambiguous.
