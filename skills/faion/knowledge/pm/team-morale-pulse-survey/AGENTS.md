# Team Morale Pulse Survey

## Summary

**One-sentence:** A 4-question anonymous pulse survey (eNPS + workload + autonomy + clarity) run mid-sprint to catch morale slides before they become attrition or distressed-project signals.

**One-paragraph:** Annual engagement surveys (Gallup Q12, Officevibe) are too lagged for distressed-project rescue or multi-team coordination. This methodology packages a 60-second 4-question pulse with anonymous submission, weekly cadence, and a deterministic alert rule (eNPS drop > 20 OR any axis median < 6 OR response_rate < 50% → manager 1:1 within 48 business hours). Output: typed `MoralePulse` aggregate + per-team alert events. PM-runnable inside a sprint window. Hard rules: 4 questions only, ≥ 3 respondents + ≥ 60% response before showing per-axis medians, eNPS is `%Promoters − %Detractors` (never arithmetic mean).

**Ефективно для:**

- Mid-sprint morale catch — distressed-project rescue trigger.
- Multi-team program-level engagement signal with consistent cadence.
- Weekly cadence with deterministic 48h-action SLA on alerts.
- Replacement for laggy annual engagement surveys without HR rollout.

## Applies If (ALL must hold)

- Team size 3–15 (single-team) OR multi-team program with consistent cadence.
- PM has authority to schedule 1:1s and act on signals within 48 business hours.
- Team has a private chat channel where the survey link can be posted.
- Engagement spans ≥ 4 sprints so trend analysis is meaningful.

## Skip If (ANY kills it)

- Team size < 3 — anonymity impossible; do real 1:1s.
- HR already runs a competing weekly pulse — duplicate cadence dilutes response rates.
- Team is in active crunch / launch < 7 days out — survey workload is hostile.
- PM cannot or will not act on prior signals — running this destroys trust.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Survey tool | Polly / Officevibe Pulse / Google Forms / Tally with anonymity | tool admin |
| Weekly calendar slot | recurring event | PM calendar |
| Private channel | Slack / Teams | team lead |
| Baseline responses | first 2 weeks of data (calibration, not signal) | survey tool |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[team-development]] | Tuckman staging consumes pulse alerts as a stage-transition signal. |
| [[value-stream-management]] | Cycle-time anomaly + response-rate drop correlate for project rescue. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: 4-question cap, anonymity floor, alert thresholds, action SLA, no-retaliation | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 for `MoralePulse` + alert event + forbidden patterns | ~800 |
| `content/03-failure-modes.xml` | essential | 6 modes: N-of-1 identifying, scope-creep questions, suppressed alert, comment leak, fatigue, eNPS arithmetic | ~900 |
| `content/04-procedure.xml` | medium | 5-step weekly cycle: launch → collect → aggregate → alert → action | ~700 |
| `content/05-examples.xml` | medium | One worked weekly cycle: response set → MoralePulse → triggered alert | ~500 |
| `content/06-decision-tree.xml` | essential | Tree: team_size + response_count + thresholds → suppress / report / alert / pause | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `survey-template-compose` | haiku | Fixed text fill. |
| `response-aggregation` | haiku | Numeric mean + median + NPS formula. |
| `alert-decision` | sonnet | Threshold + multi-axis check. |
| `trend-summary-for-pm` | sonnet | Cross-sprint comparison + narrative. |

## Templates

| File | Purpose |
|------|---------|
| `templates/pulse-survey.md` | The 4-question form (verbatim text) |
| `templates/morale-pulse.json` | `MoralePulse` schema skeleton |
| `templates/alert-event.json` | Alert event schema skeleton |
| `templates/_smoke-test.json` | Minimum viable filled `MoralePulse` for validator |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-team-morale-pulse-survey.py` | Validate a `MoralePulse` against the JSON Schema | Pre-commit on every published pulse |

## Related

- [[team-development]]
- [[value-stream-management]]
- [[retro-action-success-criteria-template]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (team size, responses received, response rate, axis medians, prior-alert state) to `suppress`, `report-only`, `alert`, or `pause-survey`. Every leaf references a rule from `01-core-rules.xml` so the action is always grounded in a checkable invariant.
