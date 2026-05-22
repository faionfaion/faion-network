---
slug: multi-team-coordination-program-continuous-weekly-checkpoints
tier: geek
group: role-project-manager
persona: role-project-manager
goal: operate-ritual
complexity: deep
version: 1.0.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion-network
summary: Run a 3-8 team delivery program (typical Outsource enterprise account or P6 multi-squad product) with stable cross-team dependency flow, predictable inter-team handoffs, and one coherent client/pro...
content_id: c5de88c76dcd991e
methodology_refs:
  - agile-hybrid-approaches
  - kanban-scaled-agile-ceremonies
  - predictive-analytics-pm
  - reporting-basics
  - scrum-ceremonies
  - team-development
  - value-stream-management
  - benefits-realization
  - communications-management
  - lessons-learned
  - project-integration
  - risk-management
  - scope-management
  - azure-devops-boards
  - jira-workflow-management
  - raci-matrix
---

# Multi-team coordination program (continuous, weekly checkpoints)

## Context

Run a 3-8 team delivery program (typical Outsource enterprise account or P6 multi-squad product) with stable cross-team dependency flow, predictable inter-team handoffs, and one coherent client/product view.

Tier: **geek**. Complexity: **deep**. Group: **role-project-manager**. Persona: **role-project-manager**.

## Outcome

This playbook is done when:

- Program operating model doc with team missions.
- Dependency map with named chokepoint owners.
- Weekly program checkpoint running for 3+ weeks.
- 2-sprint forecast convergence within tolerance.
- Quarterly program retro held.

## Steps

### 1. Program structure

Lock the operating model before the first checkpoint.

Tasks:
- Define the team-of-teams structure + each team's mission.
- Build the program RACI for cross-team decisions.
- Lock the cadence (daily team, weekly program, monthly client).

Outputs:
- Program operating model doc.

Decision gate: Advance when every team knows its mission and decision rights.

### 2. Dependency map

Visualise inter-team dependencies up front.

Tasks:
- Pull each team's planned work for the next 4 sprints.
- Map cross-team dependencies as a network.
- Identify chokepoints.

Outputs:
- Dependency map + chokepoint list.

Decision gate: Advance when chokepoints have a named owner.

### 3. Weekly program checkpoint

Stand up the cross-team alignment ritual.

Tasks:
- Run a 30-min cross-team checkpoint weekly.
- Track dependency aging in the program board.
- Escalate dependencies older than threshold.

Outputs:
- Weekly checkpoint cadence.
- Dependency aging report.

Decision gate: Advance after 3 weeks of clean checkpoint runs.

### 4. Predictive read

Use leading indicators, not lagging.

Tasks:
- Track velocity + dependency aging + risk-cost trend.
- Forecast 2-sprint outlook weekly.
- Flag deviations early.

Outputs:
- 2-sprint forecast.

Decision gate: Advance when forecasts converge with actuals within tolerance.

### 5. Cross-team team-development

Build the meta-team chemistry.

Tasks:
- Run a monthly all-program ritual (demo + retro).
- Rotate team leads through the program checkpoint.
- Capture cross-team lessons quarterly.

Outputs:
- Program-level retro notes.

Decision gate: Advance after one full all-program cycle.

### 6. Client / leadership view

Stitch the team-of-teams into one coherent view.

Tasks:
- Build a single program dashboard.
- Send weekly program note to client + leadership.
- Hold a monthly steerco.

Outputs:
- Program dashboard.
- Weekly program note.

Decision gate: Required: weekly program note continues uninterrupted.

### 7. Continuous improvement

Avoid drift across quarters.

Tasks:
- Quarterly program-level retro.
- Rotate cross-team handoff scripts based on lessons.
- Sunset rituals that no longer earn their cost.

Outputs:
- Quarterly retro + ritual sunset log.

Decision gate: Required: a quarterly retro is held; no skipping.

## Decision points

- Single program board vs federated team boards — federated for team autonomy; single board only for cross-team work.
- Sync vs async program checkpoint — async note + 30-min sync; never one without the other.

## References

Methodologies cited by this playbook (all under `skills/faion/knowledge/`):

- `pro/pm/pm-agile/agile-hybrid-approaches`
- `pro/pm/pm-agile/kanban-scaled-agile-ceremonies`
- `pro/pm/pm-agile/predictive-analytics-pm`
- `pro/pm/pm-agile/reporting-basics`
- `pro/pm/pm-agile/scrum-ceremonies`
- `pro/pm/pm-agile/team-development`
- `pro/pm/pm-agile/value-stream-management`
- `pro/pm/pm-traditional/benefits-realization`
- `pro/pm/pm-traditional/communications-management`
- `pro/pm/pm-traditional/lessons-learned`
- `pro/pm/pm-traditional/project-integration`
- `pro/pm/pm-traditional/risk-management`
- `pro/pm/pm-traditional/scope-management`
- `pro/pm/project-manager/azure-devops-boards`
- `pro/pm/project-manager/jira-workflow-management`
- `pro/pm/project-manager/raci-matrix`
