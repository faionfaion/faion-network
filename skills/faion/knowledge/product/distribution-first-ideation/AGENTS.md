# Distribution First Ideation

## Summary

**One-sentence:** Pre-build ideation discipline: validate the audience + channel BEFORE the product — smoke page, waitlist conversion, channel-fit test produce a go/no-go decision-record.

**One-paragraph:** Most discovery methodologies start with the problem; this one starts with the distribution channel. Solo operators need to validate that they own (or can cheaply earn) a distribution channel BEFORE building. The methodology pins three validation gates: (1) named channel with measurable reach, (2) smoke-page test hitting target traffic in 14 days, (3) waitlist conversion ≥10% of channel traffic. Output: a go/no-go decision-record per idea with channel evidence, smoke-page URL, waitlist counts, kill criterion.

**Ефективно для:**

- Indie operator weighing 3-5 product ideas.
- Newsletter writer evaluating a paid product spinoff.
- Solo founder past one failed product, repivoting around audience.
- Operator burned by 'great idea, no distribution' launches.

## Applies If (ALL must hold)

- Operator has access to ≥1 distribution channel with measurable reach.
- Idea is pre-build (no code written yet) OR fewer than 30 product hours invested.
- Operator can run a 14-day smoke-page validation.
- Operator is willing to kill the idea on negative signal.

## Skip If (ANY kills it)

- Build already past MVP — switch to demand-validation methodology.
- Operator has no channel and won't earn one in 30 days.
- Idea is contractually committed (paid pre-order).
- Channel is contested (e.g., employer-owned audience).

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Channel inventory | md / dashboard | operator notes |
| Idea brief | 1 paragraph | operator notes |
| Smoke-page hosting account | Carrd / Webflow / GitHub Pages | vendor |
| Analytics setup | Plausible / Fathom / GA | analytics vendor |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/marketing/content-marketer` | channel + smoke-page copy |
| `solo/product/audience-driven-pivot-decision` | audience-as-anchor logic |
| `solo/product/demo-hypothesis-template` | hypothesis evidence shape |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules with rationale + source + skip-this-methodology fallback | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | ~800 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns with symptom / root-cause / fix | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | ~800 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion(ref=rule-id) | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-skip-vs-apply` | sonnet | Decision-tree application requires judgement. |
| `draft-distribution-first-ideation` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/distribution-first-ideation.md` | Markdown skeleton for the decision-record artefact, matching content/02-output-contract.xml |
| `templates/distribution-first-ideation.schema.json` | JSON Schema seed + filled fixture for the decision-record artefact |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-distribution-first-ideation.py` | Validate output against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- `[[audience-driven-pivot-decision]]`
- `[[demo-hypothesis-template]]`
- `[[cohort-based-mini-course-launch]]`

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal (applies_if + skip_if check, then the next observable input), routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
