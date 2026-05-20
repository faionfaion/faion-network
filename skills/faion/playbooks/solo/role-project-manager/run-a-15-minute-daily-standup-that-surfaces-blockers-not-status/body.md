# Run a 15-minute daily standup that surfaces blockers, not status

## Context

A tight 15-minute ceremony where each contributor names yesterday's done, today's plan, and a real blocker; the PM exits with a refreshed blocker list and at most one parking-lot follow-up scheduled.

Tier: **solo**. Complexity: **light**. Group: **role-project-manager**. Persona: **role-project-manager**.

## Outcome

This playbook is done when:

- Pre-walk note exists before the standup.
- Round finishes inside 12 minutes.
- Zero solutioning happens in the standup itself.
- Refreshed blocker list published within 30 minutes.

## Steps

### 1. Pre-walk the board

Walk the board before the standup so the meeting is fast.

Tasks:
- Skim the board for items not moved in 2 days.
- Note any obvious blockers.
- Pre-draft a parking-lot list.

Outputs:
- Pre-walk note.

Decision gate: Advance when the pre-walk took under 5 minutes.

### 2. Run the round

Each contributor: yesterday, today, blocker.

Tasks:
- Enforce strict 60-90 seconds per person.
- Cut status-only updates with a polite redirect.
- Capture blockers in real time.

Outputs:
- Per-person update log.

Decision gate: Advance when the round finishes inside 12 minutes.

### 3. Park, don't solve

Hold problem-solving out of the standup.

Tasks:
- Drop solution discussions into the parking lot.
- Cap parking lot at the most urgent 1-2 items.
- Schedule parking-lot follow-up immediately after.

Outputs:
- Parking-lot list.

Decision gate: Advance when zero solutioning happened in the standup itself.

### 4. Refresh blocker board

Update the public blocker list.

Tasks:
- Post the refreshed blocker list to the team channel.
- Tag owners and ETAs.
- Surface aging blockers (>2 days) to leadership.

Outputs:
- Updated blocker list.

Decision gate: Required: blocker list is published within 30 minutes of standup end.

## Decision points

- Sync vs async standup — async is the default; sync only when the team is in heavy collaboration mode.
- Cross-timezone rotation — rotate the host so no one timezone always pays the cost.

## References

Methodologies cited by this playbook (all under `skills/faion/knowledge/`):

- `pro/pm/pm-agile/kanban-scaled-agile-ceremonies`
- `pro/pm/pm-agile/scrum-ceremonies`
- `pro/pm/pm-traditional/communications-management`
- `pro/pm/project-manager/agile-ceremonies-setup`
- `solo/pm/pm-agile/dashboard-setup`
- `solo/pm/project-manager/clickup-setup`
