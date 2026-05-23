---
slug: pivot-vs-quit-decision-template
tier: pro
group: product
domain: product
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Pins a decision record comparing pivot-to-v2 versus full shutdown using product signals, runway, founder energy, and customer pull; output is a signed decision-record artefact.
content_id: "0ccd5dfe83c2e9af"
complexity: medium
produces: decision-record
est_tokens: 5400
tags: [product, pro, decision-record, pivot, shutdown]
---
# Pivot vs Quit Decision Template

## Summary

**One-sentence:** Pins a decision record comparing pivot-to-v2 versus full shutdown using product signals, runway, founder energy, and customer pull; output is a signed decision-record artefact.

**One-paragraph:** Pins a decision record comparing pivot-to-v2 versus full shutdown using product signals, runway, founder energy, and customer pull; output is a signed decision-record artefact. The methodology pins the artefact shape, anchors every non-trivial field to evidence, and routes the operator via a decision tree that always terminates either on an applicable rule or on `skip-this-methodology`. Apply when preconditions hold; skip via the tree otherwise.

**Ефективно для:**

- Solo founder facing failed v1 launch with measurable customer signal disagreement.
- Co-founder pair where one wants pivot and one wants quit — needs single source of truth.
- Pre-shutdown audit before refunding customers or pivoting positioning.
- Investor / board comm: explain pivot OR shutdown with explicit evidence trail.

## Applies If (ALL must hold)

- Product launched ≥3 months ago with measurable usage data.
- Founder energy + runway constraints have been honestly assessed in writing.
- ≥3 customer interviews completed in the last 30 days.
- Pivot hypothesis (v2 candidate) is specific and testable, not vague.

## Skip If (ANY kills it)

- Pre-launch — no signal to evaluate, use pmf-rubric-for-solos instead.
- Founder cannot commit to honest assessment of energy / runway — decision will be theatre.
- Quit option already politically decided — write a closure plan, not a comparison.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Usage data snapshot | 3 months of activity events | warehouse |
| Customer interview notes | ≥3 transcripts last 30 days | user research |
| Financial runway | months of expenses covered | accounting |
| Energy + commitment self-rating | scale 1-5 with notes | founder |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/product/AGENTS.md` | Parent group context (vocabulary, neighbouring methodologies) |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥6 testable rules with rationale + source incl. `skip-this-methodology` | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid + invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns with symptom / root-cause / fix | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end with decision gates | ~900 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion(ref=rule-id) | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-skip-vs-apply` | sonnet | Decision-tree application requires judgement. |
| `draft-pivot-vs-quit-decision-template` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/artefact-skeleton.md` | Markdown skeleton conforming to the output contract |
| `templates/artefact-instance.json` | JSON instance of a filled artefact |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-pivot-vs-quit-decision-template.py` | Validate produced artefact against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- Parent: `pro/product/AGENTS.md`
- [[pmf-rubric-for-solos]]
- [[portfolio-sunset-decision-frame]]
- [[freelancer-to-saas-time-box]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
