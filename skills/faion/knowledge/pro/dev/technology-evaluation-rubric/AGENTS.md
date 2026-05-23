---
slug: technology-evaluation-rubric
tier: pro
group: dev
domain: dev
version: 1.0.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Weighted-rubric methodology for evaluating ≥2 technologies before design freeze: cost, latency, ecosystem, ops burden, exit cost — with named owner and last_reviewed date.
content_id: "6a02008d6fe9c4fb"
complexity: medium
produces: rubric
est_tokens: 4100
tags: [evaluation, tech-selection, rubric, architect]
---
# Technology Evaluation Rubric

## Summary

**One-sentence:** Weighted-rubric methodology for evaluating ≥2 technologies before design freeze: cost, latency, ecosystem, ops burden, exit cost — with named owner and last_reviewed date.

**One-paragraph:** Weighted-rubric methodology for evaluating ≥2 technologies before design freeze: cost, latency, ecosystem, ops burden, exit cost — with named owner and last_reviewed date. The methodology pins the artefact shape via a JSON Schema (see `content/02-output-contract.xml`), ties every conclusion in the decision tree to a rule id in `content/01-core-rules.xml`, and gates output via `scripts/validate-technology-evaluation-rubric.py` (stdlib-only, `--self-test` available). Apply when preconditions in Applies-If hold; route to `skip-this-methodology` otherwise. The output artefact is versioned (semver), owner-signed (named human, never 'team' / 'we'), and consumable by a downstream agent or human reviewer without re-deriving the rationale.

**Ефективно для:**

- Architect вибирає між ≥2 candidate technologies (e.g. Kafka vs Pulsar) до design freeze.
- Cost + latency budget вже sketched — потрібна consistent compare-and-rank methodology.
- Procurement gate потребує rubric-scored output замість one-paragraph email.
- Future-self / sibling-team буде revisit рішення через 6 місяців — потрібен audit trail.

## Applies If (ALL must hold)

- ≥2 candidate technologies in scope (rubric of 1 is just a writeup)
- Cost + latency budget exists or can be sketched within the eval window
- Decision-maker reads rubric output (not just engineer ranking)
- Exit-cost dimension applicable (vendor lock-in, migration cost)

## Skip If (ANY kills it)

- Only one candidate — rubric of 1 is not a comparison; just write it up
- Decision already made politically — rubric becomes post-hoc justification
- Pre-budget phase — rubric needs cost / latency numbers as input
- Trivial pick (well-known default, no real alternative) — overhead unjustified

## Prerequisites

| Trigger artefact | format | author / source |
|---|---|---|
| Task brief | Markdown | requester |
| Named owner | string | requester / RACI |
| Prior artefact (if updating) | repo path | artefact store |
| Constraint inputs (budget, SLA, compliance) | structured | requester / policy |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/dev/INDEX.xml` | Parent domain context (vocabulary, neighbouring methodologies) |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules + skip-this-methodology, each with rationale + source | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns (symptom / root-cause / fix) | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end with decision gates | ~900 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion(ref=rule-id) | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-skip-vs-apply` | sonnet | Decision-tree application — light judgement on preconditions vs skip-if. |
| `draft-technology-evaluation-rubric` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/rubric.json` | JSON instance with axis scores |
| `templates/rubric.md` | Rubric skeleton with weighted axes |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-technology-evaluation-rubric.py` | Validate produced artefact against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- Parent: `pro/dev/INDEX.xml`
- [[vendor-eval-pilot-template]]
- [[vendor-exit-cost-estimator]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
