# Jobs To Be Done (Researcher)

## Summary

**One-sentence:** Map customer progress via switching interviews and tag Push / Pull / Habit / Fear forces — produces a job-map + force-aggregation report.

**One-paragraph:** Roadmap decisions based on stated wants drift; decisions based on observed switching survive. This methodology runs JTBD switching interviews (≥10 recent switchers), tags each transcript with the four forces (Push of the situation, Pull of the new, Habit of the present, Fear of the new), and aggregates forces into a job map + force-strength rubric. Output: a JTBD report with job statement, force aggregation, and the resulting hire/fire criteria for the product.

**Ефективно для:**

- PM choosing between two product directions both 'wanted' by users.
- Indie operator whose retention drops mysteriously despite high NPS.
- Researcher establishing a JTBD baseline for a niche.
- Founder whose 'customer wants X' inputs keep producing flat roadmaps.

## Applies If (ALL must hold)

- ≥10 recent switchers (within last 90 days) are reachable.
- Operator can spend ≥45 minutes per interview.
- Switching event was observable (signed up / cancelled / changed tools).
- Downstream consumer reads JTBD output (roadmap / positioning).

## Skip If (ANY kills it)

- <10 reachable switchers — defer or borrow from upstream cohort.
- Switching event isn't observable (no event log, no churn signal).
- Team uses an opportunity-tree methodology that already encodes JTBD.
- Operator dismisses force aggregation as 'too academic' — change methodology.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Switcher cohort list | csv (handle + switch event + date) | billing + research |
| JTBD interview guide | md | this methodology |
| Force-aggregation rubric | csv / md | this methodology |
| Job-statement template | When [situation] I want to [job] so I can [outcome] | this methodology |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/research/researcher/problem-validation` | validation discipline upstream of switching interview |
| `solo/research/interview-insight-tagging-schema` | force tags consume controlled vocabulary |

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
| `draft-jobs-to-be-done` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/jobs-to-be-done.md` | Markdown skeleton for the report artefact, matching content/02-output-contract.xml |
| `templates/jobs-to-be-done.schema.json` | JSON Schema seed + filled fixture for the report artefact |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-jobs-to-be-done.py` | Validate output against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- `[[problem-validation]]`
- `[[affinity-diagramming]]`
- `[[pain-point-research]]`

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal (applies_if + skip_if check, then the next observable input), routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
