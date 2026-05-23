# Scrum Ceremonies

## Summary

**One-sentence:** Defines the five Scrum events (Sprint Planning, Daily Standup, Sprint Review, Sprint Retrospective, Backlog Refinement) with time-boxes, facilitation patterns, and quality gates per sprint length.

**One-paragraph:** Defines the five Scrum events (Sprint Planning, Daily Standup, Sprint Review, Sprint Retrospective, Backlog Refinement) with time-boxes, facilitation patterns, and quality gates per sprint length. The methodology applies in pm-agile contexts where the preconditions in `Applies If` hold and none of the `Skip If` triggers fire. Decision routing lives in `content/06-decision-tree.xml`; testable rules with rationale live in `content/01-core-rules.xml`; the validator at `scripts/validate-scrum-ceremonies.py` enforces the output contract.

**Ефективно для:**

- Bootstrapping Scrum for a new team and wiring ceremonies into a PM tool (Jira, Linear, GitHub Projects).
- Replacing free-form standups with structured cadence after onboarding or merging teams.
- Remote/distributed Scrum optimisation — async standups, retro tools, recorded reviews.
- Evidence collection for transformations (sprint-goal achievement, retro-action follow-through, velocity stability).

## Applies If (ALL must hold)

- Cross-functional team of 3-9 delivering in 1-4 week iterations.
- Sprint goal must be falsifiable in one sentence.
- Retro actions must have an owner and a linked issue or they do not exist.

## Skip If (ANY kills it)

- Solo developer or pair — Scrum overhead exceeds value; use Kanban with lightweight reviews.
- Pure research or discovery teams with no incremental delivery.
- Crisis or incident periods — break-glass first.
- Hardware-heavy programs where 2-week sprints do not match material lead times.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Product backlog (refined ≥1.5x capacity) | Markdown/Jira | Product Owner |
| Sprint length | int weeks | team agreement |
| Definition of Done | Markdown | team |
| PM tool credentials | API token | team admin |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[team-development]] | team must reach Norming before retros yield signal |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules (incl. skip rule) with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid/forbidden examples | 900 |
| `content/03-failure-modes.xml` | essential | Antipatterns with symptom/root-cause/fix triplets | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with input/action/output/decision-gate | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `plan-sprint` | sonnet | Light judgement: backlog ready check + capacity arithmetic. |
| `score-retro` | haiku | Mechanical: count owned + linked actions vs un-owned. |
| `review-readiness` | haiku | Boolean checks on completion ratio, environment, invitees. |

## Templates

| File | Purpose |
|------|---------|
| `templates/retrospective.md` | Retro structure with metrics, formats (Start-Stop-Continue, 4Ls, Mad-Sad-Glad, Sailboat) and action table |
| `templates/sprint-planning.md` | Sprint Planning notes template with sprint goal box, top items, capacity, and Part-1/Part-2 split |
| `templates/sprint-review-readiness.py` | Pre-review gate script: completion ratio, demoable items, environment, invited stakeholders |
| `templates/standup-bot.yaml` | Geekbot async standup configuration with 3-question template and blocker SLA |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-scrum-ceremonies.py` | Validate the playbook-step artefact against the schema in `02-output-contract.xml` | CI on each artefact change; pre-commit |

## Related

- [[team-development]]
- [[tool-migration-basics]]
- [[value-stream-management]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (preconditions, baseline presence, threshold pass/fail) to a concrete action; each leaf references a rule from `01-core-rules.xml`. Use it when in doubt about whether or how to apply this methodology to the case at hand.

