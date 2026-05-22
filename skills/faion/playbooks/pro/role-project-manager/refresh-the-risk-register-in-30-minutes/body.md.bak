# Refresh the risk register in 30 minutes

## Context

A weekly pass over the risk register: re-score top 10 by probability×impact, retire stale risks, add new ones from the week's incidents, set next-step owners.

Tier: **pro**. Complexity: **medium**. Group: **role-project-manager**. Persona: **role-project-manager**.

## Outcome

This playbook is done when:

- Every incident mapped to a new or existing risk.
- Every top-10 risk has refreshed score.
- Every active risk has owner + next step + date.
- Top-5 risk broadcast sent within 30 minutes.

## Steps

### 1. Pre-pull incidents

Bring in fresh signal before scoring.

Tasks:
- Pull last week's incidents and near-misses.
- Tag each as 'represents a new risk' or 'instance of existing risk'.
- List candidate new risks for the register.

Outputs:
- New-risk candidate list.

Decision gate: Advance when each incident is mapped to a risk (new or existing).

### 2. Re-score top 10

Refresh probability and impact.

Tasks:
- Walk through the top 10 risks in order.
- Re-score probability × impact on the same scale.
- Flag any risk whose score changed by ≥1 level.

Outputs:
- Re-scored top-10 risks.

Decision gate: Advance when every top-10 risk has a refreshed score and a delta note.

### 3. Retire + add

Keep the register healthy.

Tasks:
- Retire risks that are clearly resolved.
- Add the new-risk candidates above the noise floor.
- Cap the register at a working size (e.g., 30 items).

Outputs:
- Refreshed risk register.

Decision gate: Advance when retired + added items have written rationale.

### 4. Owners + next steps

Every active risk gets a step this week.

Tasks:
- Assign or refresh an owner per active risk.
- Define one concrete next step per risk.
- Set a follow-up date.

Outputs:
- Owners + next-step columns refreshed.

Decision gate: Advance when every active risk has owner + next step + date.

### 5. Surface the top 5

Make the top 5 unignorable.

Tasks:
- Pull the top 5 by re-scored severity.
- Send a 5-bullet risk update to the project team.
- Escalate any 'red' risk to leadership / client.

Outputs:
- Top-5 risk broadcast.

Decision gate: Required: top-5 update sent within 30 minutes of the refresh.

## Decision points

- Retire vs accept-and-monitor — retire only when risk is structurally resolved; otherwise demote to monitor.
- Escalate vs absorb — escalate when a single risk would breach a schedule or cost baseline; absorb otherwise.

## References

Methodologies cited by this playbook (all under `skills/faion/knowledge/`):

- `pro/pm/pm-traditional/communications-management`
- `pro/pm/pm-traditional/quality-management`
- `pro/pm/pm-traditional/risk-management`
- `pro/pm/pm-traditional/risk-register`
- `pro/pm/pm-traditional/stakeholder-engagement`
