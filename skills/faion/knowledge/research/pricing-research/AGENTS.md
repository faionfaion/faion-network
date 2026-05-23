# Pricing Research (Researcher)

## Summary

**One-sentence:** Researcher-tier pricing research combining value-capture math, competitor matrix, Van Westendorp WTP, billing model, and tier design — anchored to research evidence.

**One-paragraph:** Sibling of the market-researcher pricing methodology with research-anchored discipline. Same six steps (value math → competitor matrix → Van Westendorp → billing model → tier design → validation) but every step requires interview / behavioural evidence in addition to public sources. Output: a pricing report with recommended price, tier shape, validation plan, and a confidence band tied to evidence count.

**Ефективно для:**

- Researcher producing a pricing report for stakeholder review.
- PM cross-checking marketer-tier pricing recommendation.
- Solo operator running their own pricing research without a market lead.
- Founder defending a price decision to a board.

## Applies If (ALL must hold)

- ≥30 prospects reachable for Van Westendorp.
- ≥3 competitors are publicly priced.
- Operator has ≥3 customer interviews with value-anchor data.
- Operator can run a paid-validation step.

## Skip If (ANY kills it)

- <30 reachable prospects — survey unreliable.
- No interview evidence on value anchor — gather first.
- Operator wants pure intuition pricing — methodology cannot help.
- Pricing must follow regulator — different methodology.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Customer interview value-anchor data | spreadsheet (hours saved / revenue added) | research interviews |
| Competitor price matrix | csv | competitor scan |
| Van Westendorp survey instrument | Tally / Typeform | this methodology |
| Survey channel | audience / list | operator outreach |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/research/market-researcher/pricing-research` | shared six-step engine; this tier adds research-evidence discipline |
| `solo/research/researcher/jobs-to-be-done` | JTBD output anchors willingness-to-pay segments |

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

- `[[jobs-to-be-done]]`
- `[[niche-evaluation]]`
- `[[problem-validation]]`

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal (applies_if + skip_if check, then the next observable input), routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
