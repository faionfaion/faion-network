---
slug: pricing-research
tier: solo
group: research
domain: research
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: "Six-step pricing report: value math, competitor matrix, Van Westendorp 4-question survey, billing model choice, tier design, and validation via real sales."
content_id: "14c4c61409575768"
complexity: medium
produces: report
est_tokens: 4700
tags: [pricing, research, saas, van-westendorp, tiers]
---
# Pricing Research (Market Researcher)

## Summary

**One-sentence:** Six-step pricing report: value math, competitor matrix, Van Westendorp 4-question survey, billing model choice, tier design, and validation via real sales.

**One-paragraph:** Pricing intuition under-prices. This methodology pins a six-step report: (1) value-capture math (annual value delivered / saved), (2) competitor pricing matrix, (3) Van Westendorp price-sensitivity survey (4 questions, ≥30 responses), (4) billing-model choice (one-time / subscription / usage), (5) tier design with feature distribution, (6) validation via real sales (≥5 paying customers at the proposed price). Output: a pricing report with the recommended price, the proposed tiers, and the validation plan.

**Ефективно для:**

- Solo founder choosing the first paid tier.
- Operator re-pricing after a pivot.
- Indie builder underpricing because of impostor syndrome.
- PM deciding subscription vs usage-based billing.

## Applies If (ALL must hold)

- ≥30 prospects reachable for the Van Westendorp survey.
- ≥3 competitors are publicly priced.
- Operator can deliver value math anchored to a customer's saved hours or dollars.
- Operator can run a controlled paid-validation step (lifetime deal, beta tier).

## Skip If (ANY kills it)

- <30 prospects reachable — survey is unreliable; defer or borrow upstream data.
- All competitors are stealth-priced — use value math + sales experiments only.
- Operator wants pure intuition pricing — methodology cannot help.
- Pricing must follow a regulator (insurance, healthcare) — different methodology.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Customer-value math | spreadsheet (hours saved or revenue added) | operator interviews |
| Competitor price matrix | csv | competitor scan |
| Van Westendorp survey instrument | Tally / Typeform | this methodology |
| Survey distribution channel | audience / list | operator outreach |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/research/market-researcher/niche-evaluation` | niche sizing context for tier design |
| `solo/research/researcher/pricing-research` | sibling researcher-tier methodology with overlapping discipline |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules with rationale + source + skip-this-methodology fallback | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | ~800 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns with symptom / root-cause / fix | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | ~800 |
| `content/05-examples.xml` | essential | One end-to-end worked example | ~700 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion(ref=rule-id) | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-skip-vs-apply` | sonnet | Decision-tree application requires judgement. |
| `draft-pricing-research` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/pricing-research.md` | Markdown skeleton for the report artefact, matching content/02-output-contract.xml |
| `templates/pricing-research.schema.json` | JSON Schema seed + filled fixture for the report artefact |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-pricing-research.py` | Validate output against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- `[[niche-evaluation]]`
- `[[idea-generation]]`
- `[[naming-and-domains]]`

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal (applies_if + skip_if check, then the next observable input), routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
