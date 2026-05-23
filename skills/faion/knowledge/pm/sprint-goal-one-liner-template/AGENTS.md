# Sprint Goal One Liner Template

## Summary

**One-sentence:** Fill-in-the-blank template producing a one-line, recitable sprint goal anchored to outcome + measurable benefit + surface + out-of-scope — drafted at planning, recited at every standup, graded at review.

**One-paragraph:** Pairs with `sprint-goal-formula`. While the formula explains what makes a goal usable, this template gives the literal sentence shape the team fills in: 'In sprint NN, we will <verb> <user/system> so that <measurable benefit>, focusing on <surface>, deferring <out-of-scope>'. The five slots are mandatory; any missing slot triggers a re-author. The output is one sentence each team member should be able to recite at standup, and that the review can pass/fail without narrative.

**Ефективно для:**

- PM running planning for a team that struggles to remember the goal by Wednesday.
- Tech lead introducing sprint goals where none existed before.
- Coach onboarding a team to Scrum or Shape Up.
- Solo founder enforcing one-outcome-per-sprint discipline.

## Applies If (ALL must hold)

- Team is adopting or fixing sprint goals.
- PM facilitates planning and can require slot-filled output before close.
- Sprint length is fixed (1-3 weeks).
- Team agrees the goal will be recited at standups.

## Skip If (ANY kills it)

- Team has a goal pattern that already passes the recitability test.
- Continuous-flow / Kanban context — no sprint envelope to scope.
- Sprint outputs are entirely externally fixed (compliance, audit).
- Goals are communicated only in docs, never spoken aloud — change the meeting cadence first.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Refined backlog | list | backlog tracker |
| Sprint number + length | int + days | release calendar |
| Out-of-scope candidates | list | carried-over backlog |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/pm/sprint-goal-formula` | rules that grade the filled sentence |
| `solo/pm/project-manager` | ceremony context |

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
| `draft-sprint-goal-one-liner-template` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/sprint-goal-one-liner-template.md` | Markdown skeleton for the spec artefact, matching content/02-output-contract.xml |
| `templates/sprint-goal-one-liner-template.schema.json` | JSON Schema seed + filled fixture for the spec artefact |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-sprint-goal-one-liner-template.py` | Validate output against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- `[[sprint-goal-formula]]`
- `[[retro-facilitation-multistyle]]`
- `[[async-standup-methodology]]`

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal (applies_if + skip_if check, then the next observable input), routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
