# Daily standup with AI pre-brief

**Playbook slug:** `daily-standup-ai-prebrief`
**Tier:** geek
**Complexity:** light
**Persona:** P6 — Product-Dev Team

## Intent

Status-theater standup → 15-min exception-driven sync sitting on top of an AI-generated pre-brief.

## Scope

A distributed product-dev team walks into the 15-minute sync with the AI pre-brief already posted in the channel: yesterday's merges per person, blocked PRs, failing CI jobs, Sentry/Datadog regressions, today's intended focus. Standup runs on exceptions only — what surprises the team, what's blocked, what changed since the brief was generated. No round-robin "yesterday/today/blockers" reading.

### What this playbook covers

Three light stages: generate the pre-brief, hold a 15-minute exception sync, feed memory. The chain treats standup as a *coordination ceremony*, not status reporting. Information flows happen in the channel via the brief; the meeting is reserved for the deltas a human needs to decide on now. The discipline is in the 15-minute hard stop — if it slides, the brief is failing and the team should fix that, not lengthen the meeting.

### Non-goals

- Replacing 1:1s — standup is sync coordination, not management
- Sprint planning — see `sprint-planning-sdd-task-expansion`
- Retros — see `biweekly-retro-mistake-memory`

### Prerequisites

- Tracker (Linear/Jira) wired with AI triage
- AI bot with channel-post permission
- Documented exception-driven standup protocol agreed by team

## Success criteria

The playbook is done when:
- Pre-brief posted before standup time, daily
- Standup ≤15 min
- Exceptions surfaced + assigned in the meeting
- Mistake-memory + pattern-memory updated when standup teaches the team something new

## Stages

### Stage 1: Generate the pre-brief

**Intent:** AI agent aggregates yesterday's signal into a single channel post before standup.

**Methodologies in chain:**
- `tracker-linear-agent-as-assignee` → `geek/sdlc-ai/tracker-linear-agent-as-assignee`
- `tracker-ai-triage-classify-route` → `geek/sdlc-ai/tracker-ai-triage-classify-route`
- `api-monitoring-alerting` → `pro/dev/software-developer/api-monitoring-alerting`

**Decision gate:**
> Advance to the sync only when the pre-brief is posted. No brief = standup happens but is logged as a process miss.

### Stage 2: Run the 15-min exception sync

**Intent:** Cover exceptions, blockers, and changes since the brief. Skip everything that's already in the brief.

**Methodologies in chain:**
- `scrum-ceremonies` → `pro/pm/pm-agile/scrum-ceremonies`
- `kanban-scaled-agile-ceremonies` → `pro/pm/pm-agile/kanban-scaled-agile-ceremonies`
- `raci-matrix` → `pro/pm/pm-agile/raci-matrix`

**Decision gate:**
> End the meeting at 15 minutes regardless. Spill = sign that standup turned into status theater.

### Stage 3: Feed the memory + close the loop

**Intent:** Patterns and mistakes from today land in memory; not just in heads.

**Methodologies in chain:**
- `mistake-memory` → `solo/sdd/sdd/mistake-memory`
- `pattern-memory` → `solo/sdd/sdd/pattern-memory`

**Decision gate:**
> If a real pattern showed up but didn't make it to memory, schedule a 5-min follow-up — don't lose it.

## Common pitfalls

- Pre-brief skipped "just today" — within a week the brief stops being trusted
- Standup expands to 30 min — kills exception-driven discipline
- Decisions stay verbal — the next person on-call has no trail
- Memory updates skipped — the team stops learning

## Quality checklist (self-review)

- Could a new joiner read yesterday's brief + decisions thread and be caught up?
- Did standup end at 15 minutes?
- Did at least one mistake or pattern land in memory this week?

## Related playbooks

- `sentry-datadog-alert-triage`
- `backlog-grooming-pm-tech-lead`
- `biweekly-retro-mistake-memory`

## Known gaps

The following methodologies are referenced or implied by this playbook but do not yet exist in the knowledge base. They are tracked in the manifest `gaps[]` array and block publication until resolved (BLOCK policy).
- **daily-standup-ai-prebrief-template** (tier `geek`, blocks stage 1) — Pre-brief stage references AI-generated standup brief but no concrete template exists
- **exception-driven-standup-protocol** (tier `geek`, blocks stage 2) — Sync stage needs a written exception-driven protocol so team behaviour is repeatable

## CLI usage

```
faion get-content daily-standup-ai-prebrief --format md       # human-readable rendering
faion get-content daily-standup-ai-prebrief --format context  # agent-optimised context bundle
faion get-content daily-standup-ai-prebrief --format json     # raw structured form
```
