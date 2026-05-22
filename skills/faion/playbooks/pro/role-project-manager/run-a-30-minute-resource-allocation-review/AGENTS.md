---
slug: run-a-30-minute-resource-allocation-review
tier: pro
group: role-project-manager
persona: PM running P4 multi-engagement or P6 multi-stream squads
goal: operate-ritual
complexity: medium
version: 1.0.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion-network
summary: "Weekly 30-minute pass: confirm no one is >100% allocated, find idle capacity, rebalance across projects or squads."
content_id: f22750d3cfec52f4
methodology_refs:
  - change-control
  - communications-management
  - resource-management
  - schedule-development
  - stakeholder-engagement
  - jira-workflow-management
  - raci-matrix
  - capacity-planning
---

# Run a 30-minute resource allocation review

## Context

PM holds the resource picture for 3-15 people across multiple engagements (P4) or streams (P6). This playbook runs a single weekly 30-minute review: ingest current load, flag overloads + under-utilization, decide reallocations, and update the system of record. Done when next-week plan reflects the changes and affected people know.

## Outcome

Allocation snapshot -> rebalanced plan with named moves applied before the next week starts. Weekly 30-minute pass: confirm no one is >100% allocated, find idle capacity, rebalance across projects or squads.

## Steps

1. Get the truth before deciding. Pull next-week allocation from tracker (Jira / Float / sheet); Flag anyone >100% or <50%; Note any role conflicts (one person on two crit-path tasks)
2. Convert flags into reallocation moves. For each overload: drop / defer / reassign / accept-overtime; For each idle capacity: pull-forward / pickup billable / training; Update the RACI for anything moved
3. Make the moves stick in the system. Update tracker entries before leaving the meeting; Adjust project plans where dependencies shift; Log allocation deltas vs original plan
4. People affected hear it from the PM, not the calendar. DM each person about their change with the reason; Update steerco/PMO with material reallocations; Note client-facing changes for next sync
5. Build the historical trend so next-quarter forecasts are calibrated. Append this week's metrics to the allocation log; Note recurring overload patterns; Flag structural issues for the next capacity-planning cycle

## Decision points

- **Snapshot** -> Advance once flags are visible and the picture matches reality.
- **Decide** -> Advance when no flag remains unresolved or each remaining flag has a written reason.
- **Apply** -> Advance only when tracker is consistent; do not rely on memory.
- **Communicate** -> Done when each affected person has acknowledged.
- **Log** -> Done when log shows this week's snapshot and any pattern flagged for follow-up.

## References

- `faion/knowledge/pro/pm/pm-traditional/change-control`
- `faion/knowledge/pro/pm/pm-traditional/communications-management`
- `faion/knowledge/pro/pm/pm-traditional/resource-management`
- `faion/knowledge/pro/pm/pm-traditional/schedule-development`
- `faion/knowledge/pro/pm/pm-traditional/stakeholder-engagement`
- `faion/knowledge/pro/pm/project-manager/jira-workflow-management`
- `faion/knowledge/pro/pm/project-manager/raci-matrix`
- `faion/playbooks/pro/delivery-ops/capacity-planning`
- Related: `run-an-escalation-conversation-with-a-stakeholder`, `distressed-project-rescue-90-day-turnaround`
