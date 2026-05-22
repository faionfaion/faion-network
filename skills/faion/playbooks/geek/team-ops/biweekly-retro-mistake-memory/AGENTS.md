---
slug: biweekly-retro-mistake-memory
tier: geek
group: team-ops
persona: P6
goal: TBD
complexity: light
version: 0.1.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion
summary: Opinion-only retro → data-driven 45-min retro that exits with 2-3 owned experiments.
content_id: 94e8554bd8acc9bb
methodology_refs:
  - mistake-memory
  - dora-metrics
  - value-stream-management
  - scrum-ceremonies
  - team-development
  - quality-gates-confidence
  - reflexion-learning
  - pattern-memory
---

# Bi-weekly retro with mistake-memory feedback

**Playbook slug:** `biweekly-retro-mistake-memory`
**Tier:** geek
**Complexity:** light
**Persona:** P6 — Product-Dev Team

## Intent

Opinion-only retro → data-driven 45-min retro that exits with 2-3 owned experiments.

## Scope

Team runs a 45-minute retro at sprint close. Inputs are not opinions only — also: AI-aggregated mistake-memory entries since last retro, DORA + alert-volume + on-call load + PR-cycle-time signals, value-stream-management lens. Outputs are 2-3 concrete experiments for the next sprint, each with an owner and a success criterion.

### What this playbook covers

Three stages: pre-read, 45-minute run, wire experiments into sprint. The pre-read is what differentiates this from generic retros: instead of "I feel like X is broken," the room starts from data and adds lived experience. Experiments cap at 3 by design — anything more is a sign the team is venting, not planning.

The facilitator's job is to defend the cap and refuse vague experiments. "We should communicate better" is not an experiment; "Tech lead writes a 3-line summary of every async decision and posts it in #eng-decisions for two weeks, success = team can answer 'what did we decide last week' unaided" is. Without that bar, retros decay into theatre — visible-but-empty.

Owners ack out loud. Silent assignment is unowned by Friday. Each experiment ticket has a measurable success criterion; without one, there's no way to know in two weeks whether the change worked. Failed experiments are interesting and feed pattern-memory; vague experiments leave no signal at all.

### Non-goals

- Daily standups — see `daily-standup-ai-prebrief`
- Quarter retros — see `quarter-planning-okr-reset`
- Performance reviews — out of scope

### Prerequisites

- mistake-memory + pattern-memory updated through the sprint
- DORA metrics available
- Scrum/Kanban cadence in place

## Success criteria

The playbook is done when:
- Data inputs reviewed (mistake-memory + DORA + on-call)
- 2-3 experiments defined with owners
- Each experiment has a written success criterion
- Retro doc appended to history

## Stages

### Stage 1: Pre-read

**Intent:** AI summarises mistakes + DORA + value-stream signals before the room sits.

**Methodologies in chain:**
- `mistake-memory` → `solo/sdd/sdd/mistake-memory`
- `dora-metrics` → `pro/infra/devops-engineer/dora-metrics`
- `value-stream-management` → `pro/pm/pm-agile/value-stream-management`

**Decision gate:**
> Advance when the pre-read is published. Retros that start without pre-read default to opinion-only.

### Stage 2: Run the 45-min retro

**Intent:** Look at signals + opinions; converge on 2-3 experiments.

**Methodologies in chain:**
- `scrum-ceremonies` → `pro/pm/pm-agile/scrum-ceremonies`
- `team-development` → `pro/pm/pm-agile/team-development`
- `quality-gates-confidence` → `solo/sdd/sdd/quality-gates-confidence`
- `reflexion-learning` → `solo/sdd/sdd/reflexion-learning`

**Decision gate:**
> End at 45 min. Spill is a sign of unfocused facilitation — schedule a follow-up if needed.

### Stage 3: Wire experiments into sprint

**Intent:** Experiments become real tickets in the next sprint with success criteria.

**Methodologies in chain:**
- `pattern-memory` → `solo/sdd/sdd/pattern-memory`

**Decision gate:**
> Required: tickets filed. Verbal experiments are next retro's complaints.

## Common pitfalls

- No pre-read — retro becomes opinions-only
- More than 3 experiments — none ship
- Experiments without success criteria — can't tell if they worked
- Retro turns into theater for management — kills honesty

## Quality checklist (self-review)

- Did each experiment have a written success criterion?
- Did we use the data, or just talk over it?
- Will I know in 2 weeks whether this experiment succeeded?

## Related playbooks

- `quarter-planning-okr-reset`
- `incident-postmortem-preventive-backlog`
- `daily-standup-ai-prebrief`

## Known gaps

The following methodologies are referenced or implied by this playbook but do not yet exist in the knowledge base. They are tracked in the manifest `gaps[]` array and block publication until resolved (BLOCK policy).
- **retro-action-success-criteria-template** (tier `geek`, blocks stage 2) — Retro stage needs a template that forces success criteria per experiment
- **anti-theater-retro-guardrails** (tier `geek`, blocks stage 2) — Run-the-retro stage needs explicit anti-theater facilitation guardrails

## CLI usage

```
faion get-content biweekly-retro-mistake-memory --format md       # human-readable rendering
faion get-content biweekly-retro-mistake-memory --format context  # agent-optimised context bundle
faion get-content biweekly-retro-mistake-memory --format json     # raw structured form
```
