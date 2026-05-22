---
slug: run-2-3-person-team-comms-without-a-pm
tier: pro
group: team-management
persona: P5
goal: TBD
complexity: medium
version: 0.1.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion
summary: "Founder-as-PM rhythm: one weekly sync + structured async + Friday close - replaces standups/retros/1:1s for 2-3 person teams."
content_id: c055c84572e10e4f
methodology_refs:
  - communications-management
  - stakeholder-engagement
  - ops-contractor-management
  - lessons-learned
---

# Run 2-3 person team comms without a full-time PM

**Playbook slug:** `run-2-3-person-team-comms-without-a-pm`
**Tier:** pro
**Complexity:** medium
**Persona:** P5 -- Micro-agency founder

## Intent

Founder-as-PM rhythm: one weekly sync + structured async + Friday close - replaces standups/retros/1:1s for 2-3 person teams.

## Scope

Establish the minimum communication rhythm for a 2-3 person agency where the founder is also the PM. Replaces standups, retros, and 1:1s with one weekly sync + structured async + a Friday close-the-books ritual. Exit artifact: weekly cadence calendar + async templates + Friday close ritual live for 4 weeks.

### What this playbook covers

This is a structured chain of existing faion methodologies adapted for a 2-3 person agency founder who is also the senior delivery operator. It assumes 1-3 contractors handle the rest. Every stage ends with an explicit decision gate so the operator can tell whether to advance, iterate, or kill -- agency founders drift fastest when client comfort overrides honest staging. Each chained methodology lives in the knowledge base and can be read via `faion get-content <methodology-slug>`. The chain order is intentional: skipping a stage typically surfaces as a billing, retention, or contractor problem two months later.

### Non-goals

- Scrum-of-scrums for 20-person teams - out of scope
- Replacing all real-time comms with async - keep one weekly sync

### Prerequisites

- Active 2-3 person team (any mix of contractors + founder)
- Shared workspace (Slack / Notion / Linear / equivalent)

## Success criteria

The playbook is done when:
- Weekly sync scheduled and held
- Daily async standup template pinned + used
- Friday close-the-books ritual live
- Founder spends 3h/week or less on PM overhead
- Each team member confirms cadence in writing

## Stages

### Stage 1: Pick the rhythm

**Intent:** Single weekly sync + async + Friday close.

**Tasks:**
- Set weekly sync slot
- Pin async standup template
- Set Friday close ritual

**Methodologies in chain:**
- `communications-management` -> `pro/pm/project-manager/communications-management`
- `stakeholder-engagement` -> `pro/pm/project-manager/stakeholder-engagement`

**Outputs:**
- Cadence calendar
- Pinned templates

**Decision gate:**
> Advance once cadence accepted in writing by each team member.

### Stage 2: Run async standup

**Intent:** Yesterday / today / blocker, async.

**Tasks:**
- Each member posts daily by 10am
- Founder unblocks within 4h
- Tag scope-creep + risk in same thread

**Methodologies in chain:**
- `ops-contractor-management` -> `pro/marketing/gtm-strategist/ops-contractor-management`

**Outputs:**
- Async standup thread daily

**Decision gate:**
> Advance once 5 consecutive days of async runs cleanly.

### Stage 3: Weekly sync

**Intent:** 45 min, max - sync on plan, blockers, decisions.

**Tasks:**
- Run agenda doc updated by each member
- Decide on top-3 priorities for the week
- Capture decisions in writing

**Methodologies in chain:**
- (no resolved methodologies -- see gaps below)

**Outputs:**
- Decisions doc
- Top-3 priorities

**Decision gate:**
> Advance only when meeting fits 45 min or less with decisions captured.

### Stage 4: Friday close + retro-lite

**Intent:** Close the week + 10-min retro signal.

**Tasks:**
- Each member posts wins, slips, next-week ask
- Tag systemic issues for monthly retro
- Run lessons-learned briefing

**Methodologies in chain:**
- `lessons-learned` -> `pro/pm/project-manager/lessons-learned`

**Outputs:**
- Friday close doc

**Decision gate:**
> Required: Friday close happens every week. Missing it triggers root-cause review.

## Common pitfalls

- Adding daily syncs because async feels 'risky' - founder becomes bottleneck
- Skipping Friday close because the week 'was not busy' - kills signal
- Letting the weekly sync expand past 45 min - kills the budget

## Quality checklist (self-review)

- Did the weekly sync stay under 45 min?
- Did the founder unblock within 4h each day?
- Did Friday close actually happen every Friday?

## Related playbooks

- `daily-contractor-standup`
- `subcontractor-task-brief-generation`

## Known gaps

The following methodologies are referenced or implied by this playbook but do not yet exist in the knowledge base. They are tracked in the manifest `gaps[]` array and block publication until resolved (BLOCK policy).

- **small-team-comms-rhythm** (tier `pro`, blocks stage 1) -- Pick-the-rhythm stage needs a documented small-team cadence reference
- **founder-as-pm-survival-kit** (tier `pro`, blocks stage 3) -- Weekly-sync stage needs a survival-kit reference for founder-as-PM context

## CLI usage

```
faion get-content run-2-3-person-team-comms-without-a-pm --format md       # human-readable rendering
faion get-content run-2-3-person-team-comms-without-a-pm --format context  # agent-optimised context bundle
faion get-content run-2-3-person-team-comms-without-a-pm --format json     # raw structured form
```
