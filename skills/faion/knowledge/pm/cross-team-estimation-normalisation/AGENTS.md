# Cross-Team Estimation Normalisation

## Summary

**One-sentence:** Report converting cross-team story points into normalised throughput (cycle-time × items-per-week), with calibration session notes and an honest non-comparability caveat for the steering committee.

**One-paragraph:** Story points are not comparable across teams, yet program rollups pretend they are. This methodology specifies calibration sessions, throughput-based forecasting at program tier (cycle-time × items-per-week, not summed points), and an honest non-comparability caveat communicated to the steering committee. Output: a program report grounded in throughput, with per-team confidence bands and a 'why we do not sum points' explainer.

**Ефективно для:** program managers reconciling multi-team velocity; PMOs preparing executive briefings; agencies running multi-pod delivery.

## Applies If (ALL must hold)

- Program coordinates ≥3 teams with their own velocity systems
- Steering committee asks for cross-team rollups
- ≥4 sprints of per-team throughput data exists
- PM has authority to introduce normalisation methodology

## Skip If (ANY kills it)

- Single-team program — normalisation unnecessary
- Teams use same estimation system AND have shared calibration history — normalisation already done
- Steering committee accepts per-team independence — political win, no normalisation needed

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Per-team throughput (items/week) for last 8 weeks | CSV | PM tool |
| Per-team cycle-time distribution | CSV | PM tool |
| Calibration session notes (last 30 days) | Markdown | program wiki |
| Steering committee escalation history | Markdown | PMO log |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/pm/project-manager` | parent role skill |
| [[ai-sprint-planning-agent]] | per-team capacity inputs |

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
| `collect_per_team_throughput` | haiku | Mechanical extraction |
| `compute_program_throughput` | sonnet | Bounded math + confidence bands |
| `draft_caveat_explainer` | sonnet | Bounded narrative on why not sum points |
| `executive_brief` | opus | Cross-team synthesis for steering |

## Templates

| File | Purpose |
|------|---------|
| `templates/cross-team-estimation-normalisation.json` | JSON schema for the program report |
| `templates/cross-team-estimation-normalisation.md` | Markdown program report skeleton |
| `templates/non-comparability-caveat.md` | Reusable explainer for the steering committee |
| `templates/_smoke-test.json` | Minimum-viable filled report |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-cross-team-estimation-normalisation.py` | Validate output against the 02-output-contract schema | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `geek/pm/`
- [[ai-sprint-planning-agent]]
- [[ai-status-digest-pipeline]]

## Decision tree

The decision tree at `content/06-decision-tree.xml` filters whether cross-team-estimation-normalisation applies: root question — "Does the program span ≥3 teams AND steering committee asks for rollups?". Branches lead to a specific core rule from `01-core-rules.xml` when the methodology fits, or to a `skip-methodology` conclusion when it does not. Rules referenced: r1-throughput-not-points, r2-typed-input, r3-confidence-bands, r4-named-caveat, r5-calibration-session-required, r6-versioned-record.
