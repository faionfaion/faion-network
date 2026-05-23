# AI Sprint Planning Agent

## Summary

**One-sentence:** Spec for an agent that ingests team velocity, calendar (OOO, holidays, on-call), and carryover, and proposes a realistic capacity plan for the next sprint with named confidence bounds.

**One-paragraph:** Existing agile-ceremonies-setup gives a meeting template; nothing runs an agent that ingests velocity, calendar, and carryover and proposes a sprint capacity plan with confidence bounds. This methodology specifies the agent: typed input (last 4 sprints' velocity, OOO calendar, on-call rotation, sprint carryover), bounded transformation (per-engineer capacity × confidence band), and a sprint plan output the PM and team review before commit.

**Ефективно для:** scrum masters running planning; PMs setting sprint commitments; engineering managers running ad-hoc capacity reviews.

## Applies If (ALL must hold)

- Team has ≥4 sprints of velocity data
- Calendar (OOO, holidays, on-call) is machine-readable
- Carryover from previous sprint is documented
- Team is willing to use AI-augmented planning

## Skip If (ANY kills it)

- Team <4 sprints old — no velocity baseline
- Calendar inaccessible (no shared system) — agent input not feasible
- Team rejects AI-augmented planning — political constraint
- Single-engineer team — overkill

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Last 4 sprints' velocity (story points or hours) | CSV / API | Jira / Linear |
| OOO + on-call calendar for next sprint | ICS or YAML | team calendar |
| Carryover work list | YAML / CSV | sprint backlog |
| Per-engineer focus-time budget | YAML | team config |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/pm/project-manager` | parent role skill |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules with rationale + source | ~900 |
| `content/02-output-contract.xml` | essential | JSON schema, valid + invalid examples | ~700 |
| `content/03-failure-modes.xml` | essential | Antipatterns with symptom + root cause + fix | ~800 |
| `content/06-decision-tree.xml` | essential | Decision tree gating whether this methodology applies | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `ingest_velocity_calendar` | haiku | Mechanical extraction |
| `compute_capacity_bands` | sonnet | Bounded math + confidence band per engineer |
| `propose_sprint_plan` | sonnet | Bounded recommendation |
| `review_with_team` | opus | Cross-engineer narrative for the planning meeting |

## Templates

| File | Purpose |
|------|---------|
| `templates/ai-sprint-planning-agent.json` | JSON schema for the sprint plan |
| `templates/ai-sprint-planning-agent.md` | Markdown skeleton for the plan review |
| `templates/_smoke-test.json` | Minimum-viable filled plan |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ai-sprint-planning-agent.py` | Validate output against the 02-output-contract schema | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `geek/pm/`
- [[ai-status-digest-pipeline]]
- [[ai-risk-aging-agent]]
- [[cross-team-estimation-normalisation]]

## Decision tree

The decision tree at `content/06-decision-tree.xml` filters whether ai-sprint-planning-agent applies: root question — "Does the team have ≥4 sprints of velocity AND machine-readable calendar AND a willingness to use the agent?". Branches lead to a specific core rule from `01-core-rules.xml` when the methodology fits, or to a `skip-methodology` conclusion when it does not. Rules referenced: r1-bound-scope, r2-typed-input, r3-confidence-bands, r4-carryover-accounted, r5-llm-grounding, r6-versioned-record.
