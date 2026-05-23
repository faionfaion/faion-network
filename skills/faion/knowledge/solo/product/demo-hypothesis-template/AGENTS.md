---
slug: demo-hypothesis-template
tier: solo
group: product
domain: product
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: "One-page demo-hypothesis spec: forces every customer demo to declare what hypothesis it tests, success metric, falsification signal, follow-up gate \u2014 so demos stop being feature parades."
content_id: "4dc9262f8c884ca2"
complexity: medium
produces: spec
est_tokens: 4700
tags: [demo-hypothesis-template, product, solo, demo, discovery]
---
# Demo Hypothesis Template

## Summary

**One-sentence:** One-page demo-hypothesis spec: forces every customer demo to declare what hypothesis it tests, success metric, falsification signal, follow-up gate — so demos stop being feature parades.

**One-paragraph:** Customer demos drift into feature tours when nobody declares the hypothesis being tested. This methodology forces a one-page artefact filled BEFORE every demo: which hypothesis (segment + job + price-sensitivity), how the demo tests it (the specific moment / question / interaction), success metric (the observable behaviour that confirms), kill signal (the response that falsifies), follow-up gate (must complete before booking the next demo). The artefact is the demo agenda.

**Ефективно для:**

- Solo founder running sales demos that turn into feature walkthroughs.
- Product person doing customer discovery interviews labelled 'demos'.
- Indie operator with low close rate and no demo-to-learning loop.
- Tech-lead doing pre-sale demos with no PM partner.

## Applies If (ALL must hold)

- Founder runs ≥2 demos per week.
- Demos currently produce no captured learning artefact.
- Founder owns the demo calendar.
- There is an explicit segment / persona hypothesis open.

## Skip If (ANY kills it)

- Demos are post-sale onboarding sessions — not discovery.
- Founder has a dedicated demo specialist who already follows a playbook.
- All demos are stable enterprise procurement gates — methodology adds friction.
- Demo cadence <1/month — too few for a habit.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Hypothesis register | md / Notion | discovery doc |
| Prospect snippet (name + segment) | string | CRM |
| Demo calendar | url | calendar tool |
| Past demo notes (≥3) | md | research repo |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/product/discovery-research-handoff-template` | research evidence shape |
| `solo/product/product-manager` | parent operating context |

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
| `draft-demo-hypothesis-template` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/demo-hypothesis-template.md` | Markdown skeleton for the spec artefact, matching content/02-output-contract.xml |
| `templates/demo-hypothesis-template.schema.json` | JSON Schema seed + filled fixture for the spec artefact |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-demo-hypothesis-template.py` | Validate output against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- `[[discovery-research-handoff-template]]`
- `[[friction-to-backlog]]`
- `[[audience-driven-pivot-decision]]`

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal (applies_if + skip_if check, then the next observable input), routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
