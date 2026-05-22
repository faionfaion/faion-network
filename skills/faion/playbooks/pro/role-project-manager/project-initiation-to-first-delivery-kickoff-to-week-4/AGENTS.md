---
slug: project-initiation-to-first-delivery-kickoff-to-week-4
tier: pro
group: role-project-manager
persona: role-project-manager
goal: TBD
complexity: deep
version: 1.0.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion-network
summary: From signed SOW to first demo-able increment landed in client UAT, with charter, baselined plan, risk register, RACI, comms cadence, and burn-up trend all live.
content_id: 046dced38755faff
methodology_refs:
  - agile-hybrid-approaches
  - reporting-basics
  - scrum-ceremonies
  - change-control
  - communications-management
  - cost-estimation
  - earned-value-management
  - project-integration
  - risk-management
  - risk-register
  - schedule-development
  - scope-management
  - stakeholder-engagement
  - stakeholder-register
  - wbs-creation
  - work-breakdown-structure
  - agile-ceremonies-setup
  - jira-workflow-management
  - raci-matrix
---

# Project initiation to first delivery (kickoff → week 4)

## Context

From signed SOW to first demo-able increment landed in client UAT, with charter, baselined plan, risk register, RACI, comms cadence, and burn-up trend all live.

Tier: **pro**. Complexity: **deep**. Group: **role-project-manager**. Persona: **role-project-manager**.

## Outcome

This playbook is done when:

- Signed charter + RACI.
- Baselined schedule + cost plan.
- Risk register with owners.
- Live Jira board + ceremony cadence.
- Demo-able increment in client UAT by week 4.

## Steps

### 1. Charter + kickoff

Bring the SOW alive in a kickoff that locks scope, roles, and cadence.

Tasks:
- Draft the project charter from the SOW.
- Run a client kickoff meeting with both sides.
- Capture sign-off on scope + roles + cadence.

Outputs:
- Signed project charter.
- Kickoff minutes.

Decision gate: Advance when both sides have signed the charter.

### 2. RACI + stakeholder register

Lock who decides, does, consults, informs.

Tasks:
- Build a stakeholder register.
- Build a RACI matrix tied to the WBS.
- Send to client for sign-off.

Outputs:
- Stakeholder register.
- Signed RACI.

Decision gate: Advance when every WBS deliverable has a single accountable owner.

### 3. WBS + baselined plan

Decompose to a baselined schedule + cost plan.

Tasks:
- Build the WBS.
- Build a baselined schedule with milestones.
- Build a baselined cost plan.

Outputs:
- WBS.
- Baselined schedule.
- Baselined cost plan.

Decision gate: Advance when schedule + cost baselines are signed and stored.

### 4. Risk register

Stand up the live risk register on day one.

Tasks:
- Identify top 10 risks from SOW + kickoff.
- Score by probability × impact.
- Assign owners + next-step actions.

Outputs:
- Top-10 risk register.

Decision gate: Advance when every top-10 risk has an owner and a next step.

### 5. Comms cadence

Lock the meeting + reporting drumbeat.

Tasks:
- Schedule weekly client status, internal standup, monthly steerco.
- Lock report templates.
- Distribute the calendar.

Outputs:
- Comms calendar.
- Reporting template set.

Decision gate: Advance when the calendar is sent and accepted by the client.

### 6. Agile ceremonies

Stand up the delivery cadence on the team side.

Tasks:
- Stand up daily standups, sprint planning, review, retro.
- Configure Jira (or equivalent) board.
- Run the first ceremony cycle.

Outputs:
- Live Jira board.
- First-cycle ceremony notes.

Decision gate: Advance when first sprint completes its cycle.

### 7. First demo + UAT

Land a demo-able increment in client UAT by week 4.

Tasks:
- Identify the smallest end-to-end slice.
- Build, deploy to UAT, demo to client.
- Capture feedback into a change-control queue.

Outputs:
- First demo-able increment in UAT.
- Client feedback log.

Decision gate: Required: a working increment in client UAT by week 4.

## Decision points

- Pure agile vs hybrid — hybrid when the client expects fixed-bid milestones; pure agile only when SOW is T&M.
- Single PM vs PM + scrum-master split — split only above 6 engineers; below that the PM wears both hats.

## References

Methodologies cited by this playbook (all under `skills/faion/knowledge/`):

- `pro/pm/pm-agile/agile-hybrid-approaches`
- `pro/pm/pm-agile/reporting-basics`
- `pro/pm/pm-agile/scrum-ceremonies`
- `pro/pm/pm-traditional/change-control`
- `pro/pm/pm-traditional/communications-management`
- `pro/pm/pm-traditional/cost-estimation`
- `pro/pm/pm-traditional/earned-value-management`
- `pro/pm/pm-traditional/project-integration`
- `pro/pm/pm-traditional/risk-management`
- `pro/pm/pm-traditional/risk-register`
- `pro/pm/pm-traditional/schedule-development`
- `pro/pm/pm-traditional/scope-management`
- `pro/pm/pm-traditional/stakeholder-engagement`
- `pro/pm/pm-traditional/stakeholder-register`
- `pro/pm/pm-traditional/wbs-creation`
- `pro/pm/pm-traditional/work-breakdown-structure`
- `pro/pm/project-manager/agile-ceremonies-setup`
- `pro/pm/project-manager/jira-workflow-management`
- `pro/pm/project-manager/raci-matrix`
