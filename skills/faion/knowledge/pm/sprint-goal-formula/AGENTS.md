# Sprint Goal Formula

## Summary

**One-sentence:** Three-part sprint-goal formula (outcome + boundary + measure) — one sentence the team can recite, used to filter mid-sprint scope additions and grade the review pass/fail.

**One-paragraph:** Most teams ship sprints with a goal that is either missing ('clear the backlog') or unfalsifiable ('improve checkout'). This methodology pins the goal to a single sentence built from three required parts: an outcome (verb + user/system change), a boundary (scope edge — what is in/out), and a measure (a verifiable signal that determines done). Mid-sprint, any new request is graded against the goal binary-style. At sprint review, the measure is the pass/fail check — no narrative grading.

**Ефективно для:**

- Solo PM facilitating sprint planning for a 1-3 person engineering team.
- Tech lead acting as PM in an early-stage startup.
- Indie contractor running fixed-cadence delivery for one or two clients.
- Founder enforcing weekly focus on a multi-product portfolio.

## Applies If (ALL must hold)

- Team works in fixed-cadence sprints (1-3 weeks).
- PM (or facilitator) leads sprint planning end-to-end.
- A single team works on the sprint backlog (not a multi-team commitment).
- Backlog has >5 candidate items so a goal is needed to choose between them.

## Skip If (ANY kills it)

- Continuous-flow / Kanban — there are no sprint boundaries to set a goal around.
- Single-developer solo project where the dev IS the user — use `tiny-bets-quarterly-cadence` instead.
- Hard contractual sprint scope where every line item is mandatory.
- Sprint is purely operational (incidents, support) with no outcome to commit to.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Refined backlog | list with ≥3 thematic items | backlog tracker |
| One stakeholder available | name + handle | engagement charter |
| Previous sprint review notes | doc | previous sprint folder |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/pm/project-manager` | parent solo-PM operating context |
| `pro/pm/pm-agile` | agile ceremony cadence + vocabulary |

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
| `draft-sprint-goal-formula` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/sprint-goal-formula.md` | Markdown skeleton for the spec artefact, matching content/02-output-contract.xml |
| `templates/sprint-goal-formula.schema.json` | JSON Schema seed + filled fixture for the spec artefact |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-sprint-goal-formula.py` | Validate output against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- `[[sprint-goal-one-liner-template]]`
- `[[retro-facilitation-multistyle]]`
- `[[async-standup-methodology]]`

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal (applies_if + skip_if check, then the next observable input), routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
