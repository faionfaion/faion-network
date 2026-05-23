---
slug: agency-pricing-tiers
tier: pro
group: marketing
domain: marketing
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Playbook step: constructs good/better/best agency service tiers so the 'best' is the actual margin tier and the middle anchors the buyer.
content_id: "06c0152c49a053e1"
complexity: medium
produces: playbook-step
est_tokens: 4200
tags: [agency, pricing, tiers, anchoring, playbook]
---
# Agency Pricing Tiers

## Summary

**One-sentence:** Playbook step: constructs good/better/best agency service tiers so the 'best' is the actual margin tier and the middle anchors the buyer.

**One-paragraph:** Playbook step: constructs good/better/best agency service tiers so the 'best' is the actual margin tier and the middle anchors the buyer. Use it when agency продає 1-tier engagement і втрачає upsell + price-anchor. The methodology pins the artefact shape via JSON Schema in `content/02-output-contract.xml`, so a downstream agent can validate the output mechanically rather than by prose review.

**Ефективно для:**

- Agency продає 1-tier engagement і втрачає upsell + price-anchor.
- Good/better/best tier construction — best має найвищу margin.
- Mid-tier anchoring через price gap distribution (3 / 5 / 8 множник).
- Scope-up procedure mid-engagement задокументована.

## Applies If (ALL must hold)

- The producing agent has read access to the inputs named in Prerequisites.
- The downstream consumer expects an artefact whose shape matches `produces=playbook-step`.
- A named human reviewer is available for signoff before any binding action.
- The task has more than a one-shot scope — output will be re-read or extended later.

## Skip If (ANY kills it)

- Pre-discovery: inputs unstable, problem not named — pick a discovery methodology instead.
- One-shot prompt task that nobody else will reuse — write a plain prompt, not a methodology call.
- Output consumer wants a different shape than `produces=playbook-step` — pick a methodology whose contract matches.
- Hard real-time path where the output-contract validator can't run in budget.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Brief / inputs | Markdown or JSON | requester / upstream methodology |
| Domain context | text | parent skill `pro/marketing/growth-marketer/` |
| Output destination | path or system | downstream owner |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/marketing/growth-marketer/AGENTS.md` | Parent skill vocabulary + neighbouring methodologies |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5+ testable rules with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | 3+ antipatterns with symptom/root-cause/fix | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with input/action/output/decision-gate | 800 |
| `content/06-decision-tree.xml` | essential | Decision tree: observable signals -> rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `gather-inputs` | haiku | Mechanical extraction from upstream artefacts |
| `apply-rules` | sonnet | Apply `01-core-rules.xml` + decision tree against state |
| `synthesise-output` | sonnet | Final artefact authoring matching `02-output-contract.xml` |
| `validate-output` | haiku | Run `scripts/validate-agency-pricing-tiers.py` against the artefact |

## Templates

| File | Purpose |
|------|---------|
| `templates/agency-pricing-tiers.playbook-step.md` | Markdown playbook-step skeleton with 5-line header |
| `templates/agency-pricing-tiers.example.json` | Example output JSON conforming to 02-output-contract.xml |
| `templates/_smoke-test.json` | Minimum viable filled-in artefact for the validator self-test |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-agency-pricing-tiers.py` | Validate produced artefact against `02-output-contract.xml` schema | After `synthesise-output`, before commit/publish |

## Related

- parent skill: `pro/marketing/growth-marketer/`
- [[ab-testing-setup]]
- [[north-star-metric]]
- [[activation-framework]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals (artefact shape, freshness, scope) to either a `run-the-methodology` conclusion or a `skip-this-methodology` conclusion, with every leaf referencing a rule id from `01-core-rules.xml`. Use it when the operator is unsure whether this methodology applies to the current task.
