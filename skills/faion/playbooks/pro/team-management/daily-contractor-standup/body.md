# Daily contractor standup (async Slack)

**Playbook slug:** `daily-contractor-standup`
**Tier:** pro
**Complexity:** light
**Persona:** P5 -- Micro-agency founder

## Intent

10-min async ritual to blockers surfaced, day's deliverables confirmed, founder unblocked from being the bottleneck.

## Scope

Founder runs a 10-minute async standup with 1-3 contractors. Output: blockers surfaced, day's deliverables confirmed, founder unblocked from being the bottleneck. Exit artifact: standup thread with each contractor's update + founder responses by mid-morning.

### What this playbook covers

This is a structured chain of existing faion methodologies adapted for a 2-3 person agency founder who is also the senior delivery operator. It assumes 1-3 contractors handle the rest. Every stage ends with an explicit decision gate so the operator can tell whether to advance, iterate, or kill -- agency founders drift fastest when client comfort overrides honest staging. Each chained methodology lives in the knowledge base and can be read via `faion get-content <methodology-slug>`. The chain order is intentional: skipping a stage typically surfaces as a billing, retention, or contractor problem two months later.

### Non-goals

- Long synchronous status meetings - async only
- Sprint planning rituals - separate cadence

### Prerequisites

- Shared Slack / Discord channel with contractors
- Standup template pinned

## Success criteria

The playbook is done when:
- Each contractor posts update by 10am
- Every blocker has founder response within 4h
- Day's deliverables are written and confirmed
- No more than 10 min of founder time spent

## Stages

### Stage 1: Each contractor posts update

**Intent:** Standard 3-line format: yesterday / today / blocker.

**Tasks:**
- Post yesterday's delta
- Post today's deliverable
- Flag blockers explicitly

**Methodologies in chain:**
- `scrum-ceremonies` -> `pro/pm/pm-agile/scrum-ceremonies`
- `active-listening` -> `solo/comms/communicator/active-listening`

**Outputs:**
- Updates posted by deadline

**Decision gate:**
> Advance when every contractor has posted.

### Stage 2: Founder reads + unblocks

**Intent:** Resolve every blocker in writing, fast.

**Tasks:**
- Scan all updates within 15 min
- Respond to each blocker with decision / action
- Reassign work if scope shifted

**Methodologies in chain:**
- `communications-management` -> `pro/pm/project-manager/communications-management`
- `risk-management` -> `pro/pm/project-manager/risk-management`
- `feedback` -> `solo/comms/communicator/feedback`
- `stakeholder-communication` -> `solo/comms/communicator/stakeholder-communication`

**Outputs:**
- Blocker resolutions threaded

**Decision gate:**
> No blocker exits unanswered for more than 4h.

### Stage 3: Close the standup

**Intent:** Reaffirm the day's deliverables; tag anything that slips.

**Tasks:**
- Confirm deliverables for today
- Tag slipping items for tomorrow

**Methodologies in chain:**
- (no resolved methodologies -- see gaps below)

**Outputs:**
- Day's deliverables confirmed
- Slip log row

**Decision gate:**
> Required: every contractor's day ends with explicit deliverables OR slip note.

## Common pitfalls

- Letting standup become a discussion - back to sync meetings
- Skipping the blocker response - kills async culture
- Posting your own updates as if you are the doer instead of the unblocker

## Quality checklist (self-review)

- Did I unblock every blocker, or just acknowledge them?
- Are deliverables specific enough to verify tonight?
- Did this take 10 min or less of my time?

## Related playbooks

- `subcontractor-task-brief-generation`
- `run-2-3-person-team-comms-without-a-pm`

## Known gaps

The following methodologies are referenced or implied by this playbook but do not yet exist in the knowledge base. They are tracked in the manifest `gaps[]` array and block publication until resolved (BLOCK policy).

- **async-standup-template-micro-agency** (tier `pro`, blocks stage 1) -- Standup post stage needs a tested template for micro-agency context

## CLI usage

```
faion get-content daily-contractor-standup --format md       # human-readable rendering
faion get-content daily-contractor-standup --format context  # agent-optimised context bundle
faion get-content daily-contractor-standup --format json     # raw structured form
```
