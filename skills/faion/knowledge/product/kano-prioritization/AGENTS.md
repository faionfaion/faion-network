# Kano Prioritization

## Summary

**One-sentence:** Kano-based classifier separating must-haves, performance features, delighters, indifferent, reverse features — produces a categorised feature list with survey-grounded categories.

**One-paragraph:** Faion has MoSCoW and RICE prioritisation; Kano is the missing classifier for distinguishing must-have basics from delighters and for spotting reverse features that actively annoy. This methodology pins the survey shape (two questions per feature: functional + dysfunctional reactions), the category-assignment rule (based on response pairs), the minimum sample (≥30 per segment), and the output (categorised list with confidence + revisit date). PMs in product roles need this when leadership asks for 'wow' features that data shows are indifferent.

**Ефективно для:**

- Solo PM with leadership pushing for 'wow' features.
- Indie operator deciding whether a new feature is must-have or vanity.
- Tech-lead facing prioritisation pressure across must / wow / nice.
- Course creator deciding curriculum modules by audience reaction.

## Applies If (ALL must hold)

- There is a candidate feature list of ≥5 items needing classification.
- Operator can survey ≥30 users per primary segment.
- Audience consents to a 5-minute survey.
- Survey results will drive a roadmap decision, not just inform.

## Skip If (ANY kills it)

- Feature list <5 items — overhead exceeds benefit.
- Audience pool <30 — survey is statistically uninformative.
- Operator already used Kano <90 days ago — rerun in 90 days.
- Roadmap is contractually fixed — Kano output cannot route a decision.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Candidate feature list | md / csv | backlog tracker |
| Audience segmentation | csv | CRM / newsletter platform |
| Survey tool | Typeform / Tally / Google Forms | vendor |
| Segment sample size estimates | table | operator analytics |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/product/product-manager` | parent operating context |
| `solo/product/friction-to-backlog` | candidate-feature source |
| `solo/product/design-debt-vs-design-bet` | post-classification routing |

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
| `draft-kano-prioritization` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/kano-prioritization.md` | Markdown skeleton for the rubric artefact, matching content/02-output-contract.xml |
| `templates/kano-prioritization.schema.json` | JSON Schema seed + filled fixture for the rubric artefact |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-kano-prioritization.py` | Validate output against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- `[[friction-to-backlog]]`
- `[[design-debt-vs-design-bet]]`
- `[[indie-portfolio-scorecard]]`

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal (applies_if + skip_if check, then the next observable input), routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
