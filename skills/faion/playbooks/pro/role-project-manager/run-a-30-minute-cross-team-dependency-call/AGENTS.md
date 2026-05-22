---
slug: run-a-30-minute-cross-team-dependency-call
tier: pro
group: role-project-manager
persona: role-project-manager
goal: operate-ritual
complexity: medium
version: 1.0.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion-network
summary: "A weekly call across teams (P4 across vendors / client side; P6 across squads): align on handoffs, surface late commitments, and lock the next-week handoff schedule."
content_id: d004d7e95c0ac21f
methodology_refs:
  - value-stream-management
  - communications-management
  - risk-register
  - schedule-development
  - stakeholder-engagement-advanced
  - raci-matrix
---

# Run a 30-minute cross-team dependency call

## Context

A weekly call across teams (P4 across vendors / client side; P6 across squads): align on handoffs, surface late commitments, and lock the next-week handoff schedule.

Tier: **pro**. Complexity: **medium**. Group: **role-project-manager**. Persona: **role-project-manager**.

## Outcome

This playbook is done when:

- Pre-pulled commitments + aging view on screen.
- Every late item has recovery owner + date.
- Every next-week handoff double-confirmed.
- Every above-threshold dependency has an escalation decision.
- Handoff schedule broadcast within 60 minutes.

## Steps

### 1. Pre-pull commitments

Walk in with the data, not the discussion.

Tasks:
- Pull every team's commitments from last week and next week.
- Flag late or shifted commitments.
- Build a dependency-aging view.

Outputs:
- Pre-pulled commitments + aging view.

Decision gate: Advance when the data is on screen before the call starts.

### 2. Open with the late list

Tackle the worst dependencies first.

Tasks:
- Show the late list with team + item + days late.
- Ask each team owner for a recovery plan.
- Cap the time per item to keep the call moving.

Outputs:
- Late-list recovery plans.

Decision gate: Advance when every late item has a recovery owner and date.

### 3. Lock next-week handoffs

Schedule the handoffs concretely.

Tasks:
- Walk next week's planned handoffs by date.
- Confirm each handoff with both sides.
- Resolve any double-booked dependencies.

Outputs:
- Next-week handoff schedule.

Decision gate: Advance when every next-week handoff is double-confirmed.

### 4. Risk + escalation

Surface dependencies headed for trouble.

Tasks:
- Flag dependencies above the slack threshold.
- Decide which need escalation outside the call.
- Update the risk register.

Outputs:
- Escalation list.

Decision gate: Advance when every above-threshold dependency has an escalation decision.

### 5. Broadcast

Send the schedule + recoveries to all involved.

Tasks:
- Post the next-week handoff schedule to the program channel.
- Notify each recovery owner with their commitment.
- Log the escalations into the program risk register.

Outputs:
- Broadcast + risk register entries.

Decision gate: Required: handoff schedule broadcast within 60 minutes of call end.

## Decision points

- Cap-time vs deep-dive — cap-time inside the call; deep-dives are separate meetings.
- Escalate vs absorb — escalate when the dependency would breach a milestone; absorb when slack is still sufficient.

## References

Methodologies cited by this playbook (all under `skills/faion/knowledge/`):

- `pro/pm/pm-agile/value-stream-management`
- `pro/pm/pm-traditional/communications-management`
- `pro/pm/pm-traditional/risk-register`
- `pro/pm/pm-traditional/schedule-development`
- `pro/pm/pm-traditional/stakeholder-engagement-advanced`
- `pro/pm/project-manager/raci-matrix`
