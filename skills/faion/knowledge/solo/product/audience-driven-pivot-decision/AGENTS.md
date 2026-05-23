---
slug: audience-driven-pivot-decision
tier: solo
group: product
domain: product
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: "Decision-record framework for pivoting the product while keeping the audience \u2014 distinct from zero-to-one repivots; gated by audience-asset checks and a single-product kill criterion."
content_id: "41912af86f2c2f99"
complexity: deep
produces: decision-record
est_tokens: 4000
tags: [audience-driven-pivot-decision, product, solo, pivot, decision-record]
---
# Audience Driven Pivot Decision

## Summary

**One-sentence:** Decision-record framework for pivoting the product while keeping the audience — distinct from zero-to-one repivots; gated by audience-asset checks and a single-product kill criterion.

**One-paragraph:** When MRR stalls and the product fails, the operator has two paths: kill the product (zero-to-one repivot) or pivot the product while keeping the audience. This methodology pins the second path. Inputs: audience size + LTV history + their stated unsolved jobs. Output: a versioned decision-record naming the surviving audience cohort, the new product hypothesis, the kill criterion for the old product, the migration plan, and the validation gate before any new build starts. Avoids the 'I'll just rebrand' trap and the 'I'll abandon my list' trap.

**Ефективно для:**

- Indie operator with ≥1k engaged audience members but stagnant product MRR.
- Newsletter operator whose product attach rate plateaus.
- Course creator whose audience grew past the original course's scope.
- Niche tool builder whose users want an adjacent product.

## Applies If (ALL must hold)

- Operator has an engaged audience asset ≥500 (newsletter / Discord / mailing list / customer base).
- Current product MRR has been flat or declining for ≥3 months.
- Audience has surfaced ≥3 distinct unsolved jobs in the last 90 days.
- Operator can dedicate ≥4 weeks to validation before any new product build.

## Skip If (ANY kills it)

- Audience is <500 active — audience asset isn't strong enough to anchor a pivot.
- Current product is growing — premature optimisation.
- Operator wants to leave the audience behind (this is a zero-to-one repivot, different methodology).
- Operator cannot articulate the audience's core unsolved job in one sentence.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Audience asset metrics | csv / dashboard | audience platform |
| Last-12-month MRR trend | csv / dashboard | billing system |
| Last-90-day customer-interview notes | md / Notion | research repo |
| Kill-criterion draft for current product | 1 sentence | operator notes |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/product/product-manager` | parent operating context |
| `solo/product/kill-criteria-template` | format for current-product kill |
| `solo/product/discovery-research-handoff-template` | research evidence shape |

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
| `draft-audience-driven-pivot-decision` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/audience-driven-pivot-decision.md` | Markdown skeleton for the decision-record artefact, matching content/02-output-contract.xml |
| `templates/audience-driven-pivot-decision.schema.json` | JSON Schema seed + filled fixture for the decision-record artefact |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-audience-driven-pivot-decision.py` | Validate output against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- `[[kill-criteria-template]]`
- `[[distribution-first-ideation]]`
- `[[demo-hypothesis-template]]`

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal (applies_if + skip_if check, then the next observable input), routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
