---
slug: update-the-burndown-burnup-and-decide-one-corrective-action
tier: solo
group: role-project-manager
persona: role-project-manager
goal: operate-ritual
complexity: light
version: 1.0.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion-network
summary: "A daily ~15-minute ritual: refresh the chart, read the slope, choose exactly one corrective lever (re-scope, re-assign, raise risk, or do nothing on purpose)."
content_id: 89ecf3ec997f09c2
methodology_refs:
  - predictive-analytics-pm
  - reporting-basics
  - change-control
  - communications-management
  - risk-register
  - jira-workflow-management
  - dashboard-setup
---

# Update the burndown / burnup and decide one corrective action

## Context

A daily ~15-minute ritual: refresh the chart, read the slope, choose exactly one corrective lever (re-scope, re-assign, raise risk, or do nothing on purpose).

Tier: **solo**. Complexity: **light**. Group: **role-project-manager**. Persona: **role-project-manager**.

## Outcome

This playbook is done when:

- Chart refreshed daily and current.
- Slope direction named with evidence.
- Exactly one corrective lever chosen.
- Lever communicated within 1 hour.

## Steps

### 1. Refresh the chart

Ensure the chart reflects today, not yesterday.

Tasks:
- Pull current status from Jira / tracker.
- Verify scope baseline has not drifted.
- Refresh the chart.

Outputs:
- Refreshed burndown/burnup chart.

Decision gate: Advance when the chart is current.

### 2. Read the slope

Read the line, not the headline.

Tasks:
- Compare actual slope vs ideal line.
- Identify whether the gap is widening, stable, or closing.
- Note any inflection in the last 3 data points.

Outputs:
- Slope read (widening / stable / closing).

Decision gate: Advance when slope direction is named with evidence.

### 3. Pick one lever

Choose exactly one corrective action.

Tasks:
- List candidate levers: re-scope, re-assign, raise risk, do-nothing.
- Pick exactly one based on the slope read.
- Document the rationale.

Outputs:
- One-lever decision note.

Decision gate: Advance when exactly one lever is chosen (not zero, not two).

### 4. Communicate the lever

Surface the call where it matters.

Tasks:
- Tell the team what is changing.
- Tell the client / leadership if scope or schedule moved.
- Update the risk register if 'raise risk' was the lever.

Outputs:
- Lever-broadcast record.

Decision gate: Required: the chosen lever is communicated within 1 hour.

## Decision points

- Do-nothing-on-purpose vs panic-act — do-nothing is a legitimate lever when noise dominates signal.
- Re-scope vs re-assign — re-scope first; re-assigning rarely fixes a planning miss.

## References

Methodologies cited by this playbook (all under `skills/faion/knowledge/`):

- `pro/pm/project-manager/predictive-analytics-pm`
- `pro/pm/pm-agile/reporting-basics`
- `pro/pm/pm-traditional/change-control`
- `pro/pm/pm-traditional/communications-management`
- `pro/pm/pm-traditional/risk-register`
- `pro/pm/project-manager/jira-workflow-management`
- `solo/pm/pm-agile/dashboard-setup`
