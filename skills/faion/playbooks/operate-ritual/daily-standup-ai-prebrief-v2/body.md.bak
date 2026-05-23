# Daily standup with AI pre-brief

## Context

Distributed team walks into the 15-min sync with the AI pre-brief already posted in the channel: yesterday's merges per person, blocked PRs, failing CI jobs, Sentry/Datadog regressions, today's intended focus. Standup runs on exceptions, not status theater.

## Outcome

By the end of this playbook, the operator has run the 3 stages below and produced the written decision artefact in the final stage.

Success criteria:

- All 3 stages have written outputs in the project record
- Each stage's decision gate was answered before advancing (yes / no in writing)
- Final stage produced the required written decision artifact
- Every methodology reference loaded cleanly via `faion get-content`

## Steps

### 1. Set the Pre-Brief

AI does the boring summary before humans meet.

Tasks:
- Pick the AI tool and connect it to issues / chat / git history
- Define the pre-brief template (yesterday, blockers, risks)
- Time-box the human standup to 10 minutes max

Outputs:
- AI integration live
- pre-brief template
- 10-minute time-box rule

Decision gate: Advance only when pre-brief is delivered to channel before the meeting.

### 2. Run It Daily

Use the pre-brief; don't re-read it aloud.

Tasks:
- Team reads pre-brief 5 minutes before standup
- Standup discusses only blockers and decisions, not status
- Update pre-brief prompts when accuracy drifts

Outputs:
- daily pre-brief logs
- standup decision log
- prompt-update log

Decision gate: Advance when standup time has dropped vs baseline.

### 3. Tune & Retro

Improve the loop weekly.

Tasks:
- Once a week, score pre-brief accuracy and usefulness
- Iterate prompts and inputs
- Decide: keep / change / drop the AI pre-brief

Outputs:
- weekly accuracy score
- prompt diff log
- keep/change/drop memo

Decision gate: Required output: a written weekly tune note.

## Decision points

- Stage 1 (Set the Pre-Brief): Advance only when pre-brief is delivered to channel before the meeting.
- Stage 2 (Run It Daily): Advance when standup time has dropped vs baseline.
- Stage 3 (Tune & Retro): Required output: a written weekly tune note.

## References

- `tracker-ai-triage-classify-route`
- `tracker-linear-agent-as-assignee`
- `api-monitoring-alerting`
- `kanban-scaled-agile-ceremonies`
- `raci-matrix`
- `scrum-ceremonies`
- `mistake-memory`
- `pattern-memory`

Gaps (status: draft until empty):
- `daily-standup-ai-prebrief-template` (see `gaps[]` in `playbook.yaml`)
- `exception-driven-standup-protocol` (see `gaps[]` in `playbook.yaml`)
