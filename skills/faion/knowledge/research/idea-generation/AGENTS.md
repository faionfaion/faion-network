# Idea Generation (Researcher)

## Summary

**One-sentence:** Researcher-tier ideation: 7 frameworks (skills, pain mining, job substitution, productized service, unbundling, market stacking, own problems) producing 20–50 scored candidates.

**One-paragraph:** Mirror of the market-researcher tier but biased to research-driven inputs (interview corpora, observed pain points) rather than personal skills first. This methodology runs the same 7 frameworks with research-source priors: pain-point corpus first, observed switching behaviour second, personal skills last. Output: a candidate list scored on the canonical 5-criterion matrix, with the top 5 carrying evidence links into the research repo.

**Ефективно для:**

- Researcher running structured ideation off an interview corpus.
- PM doing discovery research that needs to surface candidate features / products.
- Solo operator whose pain-point log accumulated over a quarter.
- Indie builder wanting research-anchored ideation rather than gut-driven.

## Applies If (ALL must hold)

- Pain-point corpus exists (≥10 sourced entries).
- Operator can run a 2-hour focused ideation session.
- Downstream scoring step is committed (niche-evaluation).
- Candidates will be validated, not shipped directly.

## Skip If (ANY kills it)

- No pain-point corpus — run pain-point-research first.
- Operator has a validated idea with paying users — skip ideation.
- Single-method run wanted — use market-researcher/idea-generation instead.
- Refresh cadence still fresh (<14 days).

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Pain-point corpus | csv / md | pain-point-research |
| Interview switching-behaviour log | md | JTBD interviews |
| Skills + constraints brief | md | operator self-assessment |
| Scoring matrix template | csv | this methodology |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/research/researcher/pain-point-research` | the pain corpus this ideation consumes |
| `solo/research/market-researcher/idea-generation` | shared seven-framework engine |
| `solo/research/researcher/niche-evaluation` | downstream scoring rubric |

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
| `draft-idea-generation` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/idea-generation.md` | Markdown skeleton for the report artefact, matching content/02-output-contract.xml |
| `templates/idea-generation.schema.json` | JSON Schema seed + filled fixture for the report artefact |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-idea-generation.py` | Validate output against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- `[[pain-point-research]]`
- `[[niche-evaluation]]`
- `[[jobs-to-be-done]]`

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal (applies_if + skip_if check, then the next observable input), routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
