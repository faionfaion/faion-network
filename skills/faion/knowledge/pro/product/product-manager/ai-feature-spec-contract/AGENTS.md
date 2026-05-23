---
slug: ai-feature-spec-contract
tier: pro
group: product
domain: pm
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Locks the brief + gate + rollout artefacts an AI-powered feature must satisfy before it moves from idea to production safely; output is a structured spec contract.
content_id: "a4ebd9f166f0f943"
complexity: deep
produces: spec
est_tokens: 5800
tags: [pm, pro, spec, ai-feature, contract]
---
# AI Feature Spec Contract

## Summary

**One-sentence:** Locks the brief + gate + rollout artefacts an AI-powered feature must satisfy before it moves from idea to production safely; output is a structured spec contract.

**One-paragraph:** Locks the brief + gate + rollout artefacts an AI-powered feature must satisfy before it moves from idea to production safely; output is a structured spec contract. The methodology pins the artefact shape, anchors every non-trivial field to evidence, and routes the operator via a decision tree that always terminates either on an applicable rule or on `skip-this-methodology`. Apply when preconditions hold; skip via the tree otherwise.

**Ефективно для:**

- AI feature kickoff: pin contract before a model touches user traffic.
- Pre-gate review: what every AI feature spec must include to pass.
- Audit existing AI features: contract reveals which features skipped a gate.
- Cross-functional AI ramp: eng + research + safety + product align on one spec.

## Applies If (ALL must hold)

- Feature uses LLM or generative-AI on user inputs.
- Eval harness exists or can be built within the gate window.
- Named PM + eng + safety owners exist.
- Pre-launch eval threshold can be defined ('feature must hit metric X >= Y').

## Skip If (ANY kills it)

- Feature is deterministic (no model in the loop) — apply prd-via-ai-without-losing-why instead.
- No eval harness possible (purely subjective output, no rubric) — needs new eval discipline.
- No safety owner — block AI feature until safety review staffed.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Feature brief | structured one-pager: customer + outcome + risk | PM |
| Eval rubric | scoring function with thresholds | research |
| Risk register | named risks with mitigations | safety |
| Rollout plan | ramp schedule with kill switch | eng |

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
| `draft-ai-feature-spec-contract` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/artefact-skeleton.md` | Markdown skeleton conforming to the output contract |
| `templates/artefact-instance.json` | JSON instance of a filled artefact |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ai-feature-spec-contract.py` | Validate produced artefact against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- Parent: `pro/product/AGENTS.md`
- [[prd-via-ai-without-losing-why]]
- [[annual-roadmap-vs-quarterly-okr-stitch]]
- [[post-launch-72h-watch-runbook]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
