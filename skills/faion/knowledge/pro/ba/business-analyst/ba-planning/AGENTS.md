# Business Analysis Planning

## Summary

A six-step framework that defines how BA work will be performed before requirements gathering begins: selecting plan-driven, change-driven, or hybrid approach based on context; building the stakeholder list; scheduling elicitation activities; specifying deliverables; and establishing governance (approver, change process, escalation path). The BA Approach Document is stored as a versioned Markdown+YAML file in git, refreshed on a 14-day cadence.

## Why

Ad-hoc analysis produces inconsistent coverage, missed stakeholders, and unclear sign-off authority. BABOK v3 ch. 3 treats planning as a Knowledge Area, not a preliminary step — without a named approver and a deliverable list agreed upfront, the BA effort has no contract and audit trails collapse. The 14-day staleness trigger catches plan-reality drift before it becomes a project risk.

## When To Use

- Kicking off a multi-stakeholder initiative (>3 stakeholder groups) where elicitation, deliverables, and approval flow must be agreed before requirements work starts.
- Regulated programs (medical, fintech, gov, ISO 9001/SOX) where auditors expect a documented BA approach with named approvers.
- Hybrid plan-driven + change-driven engagements where artifacts must be explicitly declared as baselined vs. living.
- Spinning up a new BA capability inside a delivery team that had none previously.
- Seeding inputs for stakeholder-analysis, elicitation-techniques, and requirements-lifecycle.

## When NOT To Use

- Solo founder building an MVP — planning ceremony is overhead; use a one-page lean canvas.
- Pure XP/Scrum teams running on a refined backlog with a Definition of Ready that already encodes the BA approach.
- Initiatives shorter than ~2 weeks of effort with one stakeholder — the plan costs more than the work it organizes.
- When the sponsor refuses to commit a governance model in writing — without an approver the plan is shelfware.
- Throwaway prototypes, spikes, or research probes.

## Content

| File | What's inside |
|------|---------------|
| `content/01-planning-steps.xml` | Six planning steps, approach-selection matrix (plan-driven/change-driven/hybrid), elicitation technique table, deliverable types. |
| `content/02-agent-workflow.xml` | Git-native plan management, replan triggers, recommended subagents, prompt patterns, AI gotchas. |

## Templates

| File | Purpose |
|------|---------|
| `templates/ba-approach-document.md` | BA Approach Document with YAML frontmatter (engagement_id, approach, approver, last_reviewed) and all eight sections. |
| `templates/ba-activity-plan.md` | Weekly activity plan template with day-by-day activity, stakeholders, and deliverable columns. |
| `templates/ba-plan-check.py` | Script: validate BA Approach Document frontmatter, check review cadence, emit JSON status. |
