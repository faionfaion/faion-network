---
slug: competitive-positioning
tier: pro
group: product
domain: pm
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Defines how the product is uniquely valuable vs alternatives via positioning canvas (April-Dunford style) with category, target, differentiators, value, anti-positioning; output is a positioning spec.
content_id: "ac9908306140e513"
complexity: medium
produces: spec
est_tokens: 5400
tags: [pm, pro, spec, positioning, marketing, category]
---
# Competitive Positioning (PM)

## Summary

**One-sentence:** Defines how the product is uniquely valuable vs alternatives via positioning canvas (April-Dunford style) with category, target, differentiators, value, anti-positioning; output is a positioning spec.

**One-paragraph:** Defines how the product is uniquely valuable vs alternatives via positioning canvas (April-Dunford style) with category, target, differentiators, value, anti-positioning; output is a positioning spec. The methodology pins the artefact shape, anchors every non-trivial field to evidence, and routes the operator via a decision tree that always terminates either on an applicable rule or on `skip-this-methodology`. Apply when preconditions hold; skip via the tree otherwise.

**Ефективно для:**

- Pre-launch positioning: pin category + differentiators before marketing site copy.
- Pivot positioning refresh: April-Dunford recheck when entering a new category.
- Sales enablement: shared positioning doc trains AE + SDR on category framing.
- Investor pitch: positioning canvas is the spine of the deck's market slide.

## Applies If (ALL must hold)

- Product is post-MVP with paying users or LOIs.
- ≥3 real alternatives (including 'do nothing') are identifiable.
- Founder + marketing have authority to commit to one category framing.
- Customer interviews can confirm whether positioning resonates.

## Skip If (ANY kills it)

- Pre-product — positioning is hypothesis, use customer-discovery first.
- Market category is decided externally (regulated industry) — no choice to make.
- Founder will not commit to one category — drafted positioning will be stale by ship.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Alternatives list | ≥3 alternatives + 'do nothing' | research |
| Customer wins list | ≥5 won customers + 'why us' note | sales |
| Customer losses list | ≥3 lost deals + 'why them' note | sales |
| Category candidates | ≥2 candidate categories | PM + marketing |

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
| `content/05-examples.xml` | reference | Full worked example end-to-end | ~900 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion(ref=rule-id) | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-skip-vs-apply` | sonnet | Decision-tree application requires judgement. |
| `draft-competitive-positioning-(pm)` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/artefact-skeleton.md` | Markdown skeleton conforming to the output contract |
| `templates/artefact-instance.json` | JSON instance of a filled artefact |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-competitive-positioning.py` | Validate produced artefact against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- Parent: `pro/product/AGENTS.md`
- [[blurred-roles-team-evolution]]
- [[annual-roadmap-vs-quarterly-okr-stitch]]
- [[ai-feature-spec-contract]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
