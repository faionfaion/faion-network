# Problem Validation

## Summary

**One-sentence:** Confirm a problem is real, painful, and worth solving via Mom-Test-style interviews — produces a validation report with GO / PASS / PIVOT verdict before code is written.

**One-paragraph:** Most products fail because the problem wasn't worth solving. This methodology pins the validation step: ≥7 Mom-Test interviews with target segment (questions about past behaviour, not future intent), tagged for evidence of pain (frequency, cost, workaround quality), with a scoring rubric and a single verdict. Output: a validation report ending in GO (build) / PASS (don't build) / PIVOT (adjust the problem) with named evidence per criterion.

**Ефективно для:**

- Solo founder considering committing engineering effort to a new product.
- PM with a stakeholder asking 'is this worth building'.
- Indie operator who keeps building before validating.
- Researcher producing the validation report for a board-level go/no-go.

## Applies If (ALL must hold)

- Candidate problem stated as a sentence.
- Target segment reachable for ≥7 interviews.
- Operator can run Mom-Test-style interviews (past-behaviour probes).
- Decision to build or not is genuinely open.

## Skip If (ANY kills it)

- Problem is already validated by paying customers.
- <7 reachable interviewees — defer or borrow upstream cohort.
- Operator cannot tolerate a PASS verdict — methodology produces no value.
- Decision is already made and the report is theatre — skip.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Problem statement | 1 sentence (segment + job + trigger) | ideation output |
| Target segment list | ≥7 named interviewees | recruiting |
| Mom-Test interview guide | md | this methodology |
| Scoring rubric | frequency / cost / workaround quality / urgency / segment-fit | this methodology |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/research/researcher/jobs-to-be-done` | JTBD interview canon underpins Mom-Test discipline |
| `solo/research/researcher/pain-point-research` | pain corpus upstream of problem-statement validation |

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
| `draft-problem-validation` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/problem-validation.md` | Markdown skeleton for the report artefact, matching content/02-output-contract.xml |
| `templates/problem-validation.schema.json` | JSON Schema seed + filled fixture for the report artefact |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-problem-validation.py` | Validate output against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- `[[jobs-to-be-done]]`
- `[[pain-point-research]]`
- `[[niche-evaluation]]`

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal (applies_if + skip_if check, then the next observable input), routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
