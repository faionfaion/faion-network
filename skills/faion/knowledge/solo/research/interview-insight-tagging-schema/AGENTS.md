---
slug: interview-insight-tagging-schema
tier: solo
group: research
domain: research
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: "Pins a controlled tag vocabulary for atomic-insight tagging so interview synthesis feeds an opportunity tree, not a tag-soup."
content_id: "35953fbf025a1414"
complexity: medium
produces: spec
est_tokens: 4700
tags: [tagging, schema, research, synthesis, controlled-vocabulary]
---
# Interview Insight Tagging Schema

## Summary

**One-sentence:** Pins a controlled tag vocabulary for atomic-insight tagging so interview synthesis feeds an opportunity tree, not a tag-soup.

**One-paragraph:** Existing user-interview methodologies cover running interviews; none pin a shared taxonomy for tagging atomic insights so they aggregate into an opportunity tree. This methodology defines the schema: tag categories (Job, Pain, Workaround, Outcome, Segment, Channel), allowed values per category, naming convention, and the rule that every insight card carries ≥1 tag per category. Output: a versioned tag manifest the team commits to, consumed by the insight-card layer, the affinity board, and the opportunity tree.

**Ефективно для:**

- Research team where two analysts tag the same interview differently.
- Solo researcher accumulating tag drift across 3 quarters of interviews.
- PM trying to aggregate insights into a tree and finding tag chaos.
- Operator switching research tools and needing tag portability.

## Applies If (ALL must hold)

- Team runs recurring user research (≥1 interview / week).
- Insights are tagged at the atomic-card level, not the interview level.
- Downstream aggregation needs cross-interview joins by tag.
- Team has ≥3 months of interview history to taxonomise.

## Skip If (ANY kills it)

- Single one-shot research sprint — inline tags suffice.
- Team uses an enforced research-tool taxonomy already (Dovetail with strict schema).
- Insights never aggregate (one-shot decisions only).
- Team disagrees on segment definitions — resolve segments first.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Interview corpus | md / Dovetail / Notion | research repo |
| Segment map | list of named segments | research plan |
| Existing ad-hoc tags | csv / list | research tool |
| Aggregation downstream consumer | opportunity tree / dashboard | research deliverable |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/research/insight-evidence-card-template` | the card layer that consumes these tags |
| `solo/research/researcher/affinity-diagramming` | downstream grouping uses these tags |

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
| `draft-interview-insight-tagging-schema` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/interview-insight-tagging-schema.md` | Markdown skeleton for the spec artefact, matching content/02-output-contract.xml |
| `templates/interview-insight-tagging-schema.schema.json` | JSON Schema seed + filled fixture for the spec artefact |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-interview-insight-tagging-schema.py` | Validate output against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- `[[insight-evidence-card-template]]`
- `[[interview-hot-take-template]]`
- `[[affinity-diagramming]]`

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal (applies_if + skip_if check, then the next observable input), routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
