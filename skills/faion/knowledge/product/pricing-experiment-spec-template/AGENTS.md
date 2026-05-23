# Pricing Experiment Spec Template

## Summary

**One-sentence:** Pinned spec template (hypothesis -> result) for pricing experiments with owner, evidence anchors, and ship/abort gates; output is a per-experiment spec instance.

**One-paragraph:** Pinned spec template (hypothesis -> result) for pricing experiments with owner, evidence anchors, and ship/abort gates; output is a per-experiment spec instance. The methodology pins the artefact shape, anchors every non-trivial field to evidence, and routes the operator via a decision tree that always terminates either on an applicable rule or on `skip-this-methodology`. Apply when preconditions hold; skip via the tree otherwise.

**Ефективно для:**

- Standardise pricing experiment write-ups so results are comparable quarter to quarter.
- Pre-launch gate: every pricing experiment must produce this spec before traffic split.
- Post-mortem: per-experiment spec is the source of truth for what was tested vs concluded.
- Investor / board memo: pin pricing test discipline with structured spec history.

## Applies If (ALL must hold)

- Pricing experiment design (see pricing-experiment-design) already validated.
- Stripe / billing instrumented to attribute revenue to variant cohort.
- Named pricing owner exists and signs off pre-launch.
- Post-experiment review meeting scheduled within 7 days of test end.

## Skip If (ANY kills it)

- Pricing experiment design not yet validated — apply design methodology first.
- Billing cannot attribute revenue to variant — instrumentation gap.
- No named pricing owner — assign before drafting spec.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Pricing experiment design | approved design spec id | PM + pricing |
| Billing attribution layer | variant_id -> customer_id mapping live | eng |
| Power analysis | expected effect + MDE + target n | data |
| Review meeting calendar | post-test review with attendees | calendar |

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
| `draft-pricing-experiment-spec-template` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/artefact-skeleton.md` | Markdown skeleton conforming to the output contract |
| `templates/artefact-instance.json` | JSON instance of a filled artefact |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-pricing-experiment-spec-template.py` | Validate produced artefact against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- Parent: `pro/product/AGENTS.md`
- [[pricing-experiment-design]]
- [[post-launch-72h-watch-runbook]]
- [[north-star-metric-design]]

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal and routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
