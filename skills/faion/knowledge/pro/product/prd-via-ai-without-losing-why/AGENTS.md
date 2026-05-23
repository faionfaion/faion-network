---
slug: prd-via-ai-without-losing-why
tier: pro
group: product
domain: product
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Pins a PRD authoring procedure that uses AI for drafting but locks the 'why' (customer evidence, business outcome, anti-goals) before any LLM expansion; output is a PRD spec with citation chain.
content_id: "f7fb3c73d90ed0ae"
complexity: medium
produces: spec
est_tokens: 5400
tags: [product, pro, spec, prd, ai-authoring]
---
# PRD via AI Without Losing Why

## Summary

**One-sentence:** Pins a PRD authoring procedure that uses AI for drafting but locks the 'why' (customer evidence, business outcome, anti-goals) before any LLM expansion; output is a PRD spec with citation chain.

**One-paragraph:** Pins a PRD authoring procedure that uses AI for drafting but locks the 'why' (customer evidence, business outcome, anti-goals) before any LLM expansion; output is a PRD spec with citation chain. The methodology pins the artefact shape, anchors every non-trivial field to evidence, and routes the operator via a decision tree that always terminates either on an applicable rule or on `skip-this-methodology`. Apply when preconditions hold; skip via the tree otherwise.

**Ефективно для:**

- PM uses LLM to draft PRDs but downstream eng cannot tell signal from filler.
- Pre-feature kickoff: align 'why' before AI expands 'what' into prose.
- Anti-feature creep: anti-goals locked first so AI suggestions cannot reintroduce cut scope.
- Audit existing AI-drafted PRDs: identify which sections lost the 'why' under prose.

## Applies If (ALL must hold)

- Feature has ≥3 customer interview citations or ≥1 quantitative signal.
- Business outcome is one measurable sentence ('move X by Y in Z weeks').
- Anti-goals (explicit out-of-scope) can be listed.
- PM has authority to reject AI output that drifts from locked 'why'.

## Skip If (ANY kills it)

- No customer evidence — apply customer-discovery methodology first.
- No measurable business outcome — PRD will be aspirational.
- AI tool not approved for use in product specs (compliance gate).

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Customer evidence pack | ≥3 quoted interviews + ≥1 quant signal | research |
| Business outcome | one measurable sentence | PM |
| Anti-goals list | ≥3 explicit out-of-scope items | PM |
| Approved AI tool | name + version + compliance status | ops |

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
| `draft-prd-via-ai-without-losing-why` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/artefact-skeleton.md` | Markdown skeleton conforming to the output contract |
| `templates/artefact-instance.json` | JSON instance of a filled artefact |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-prd-via-ai-without-losing-why.py` | Validate produced artefact against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- Parent: `pro/product/AGENTS.md`
- [[ai-feature-spec-contract]]
- [[north-star-metric-design]]
- [[annual-roadmap-vs-quarterly-okr-stitch]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
