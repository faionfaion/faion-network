# Interview Hot-Take Template

## Summary

**One-sentence:** 5-bullet hot-take capture within 30 minutes of an interview — pins the freshness signal before formal synthesis flattens it.

**One-paragraph:** By the time formal synthesis runs (a week later), the interviewer has lost the freshness signal: which moment surprised them, which answer cracked, which quote should not be paraphrased. This methodology pins a 5-bullet hot-take per interview, captured within 30 minutes of session end: the surprise, the contradiction, the strongest quote, the open question that emerged, the next-step the interviewer commits to. Lives in the research repo next to the transcript and feeds the insight-card layer downstream.

**Ефективно для:**

- Solo researcher running back-to-back interviews.
- PM doing their first round of discovery interviews.
- Founder logging customer conversations on the move.
- Researcher whose synthesis arrives a week late and loses the 'aha' moments.

## Applies If (ALL must hold)

- Interviewer can capture within 30 minutes of session end.
- Interview was at least 20 minutes long.
- Transcript or notes exist for the session.
- Hot-takes will feed downstream synthesis (insight cards, opportunity tree).

## Skip If (ANY kills it)

- Interview was under 10 minutes — capture only the next-step.
- Capture window passed by >24 hours — write a delayed-capture flagged note.
- Session is internal (not user research) — use meeting notes template.
- Researcher already has an established freshness-capture habit that works.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Interview transcript or audio | md / mp3 | research repo |
| Session metadata | interviewee handle + timestamp + duration | research log |
| Hot-take capture path | md | research repo |
| 30-minute capture timer | timer / alarm | operator setup |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/research/insight-evidence-card-template` | downstream insight card shape |
| `solo/research/researcher/affinity-diagramming` | downstream synthesis grouping |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules with rationale + source + skip-this-methodology fallback | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | ~800 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns with symptom / root-cause / fix | ~800 |
| `content/05-examples.xml` | essential | One end-to-end worked example | ~700 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion(ref=rule-id) | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-skip-vs-apply` | sonnet | Decision-tree application requires judgement. |
| `draft-interview-hot-take-template` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/interview-hot-take-template.md` | Markdown skeleton for the spec artefact, matching content/02-output-contract.xml |
| `templates/interview-hot-take-template.schema.json` | JSON Schema seed + filled fixture for the spec artefact |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-interview-hot-take-template.py` | Validate output against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- `[[insight-evidence-card-template]]`
- `[[interview-insight-tagging-schema]]`
- `[[affinity-diagramming]]`

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal (applies_if + skip_if check, then the next observable input), routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
