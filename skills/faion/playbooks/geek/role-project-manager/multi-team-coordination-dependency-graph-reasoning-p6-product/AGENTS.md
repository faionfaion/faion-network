---
slug: multi-team-coordination-dependency-graph-reasoning-p6-product
tier: geek
group: role-project-manager
persona: PM coordinating 3+ feature teams in a P6 product context
goal: operate-ritual
complexity: deep
version: 1.0.0
status: draft
last_reviewed: 2026-05-22
maintainers:
  - faion-network
summary: PM coordinating 3+ feature teams ships cross-team work without weekly fire drills, surfaces blockers within 24h, no surprise integration breaks.
content_id: b3c2b00840e8f9a0
methodology_refs:
  - kanban-scaled-agile-ceremonies
  - value-stream-management
  - communications-management
  - project-integration
  - quality-management
  - predictive-analytics-pm
---

# Multi-team coordination & dependency-graph reasoning (P6 product)

## Context

PM owns coordination across 3+ feature teams shipping into a shared product. This playbook sets up a maintained dependency graph, a scrum-of-scrums async cadence, integration-readiness gates, and release-readiness reviews. Done when two consecutive releases ship with zero surprise integration breaks and blockers surface within 24h of forming.

## Outcome

Cross-team coordination chaos -> live dependency graph + 24h blocker-surface SLA + no surprise releases. PM coordinating 3+ feature teams ships cross-team work without weekly fire drills, surfaces blockers within 24h, no surprise integration breaks.

## Steps

1. Make all cross-team dependencies visible. Interview each team lead about upstream + downstream needs; Construct a directed dependency graph (issues + epics + services); Publish to a shared, queryable surface
2. Weekly cross-team sync without a meeting. Stand up a weekly async thread for cross-team blockers; Standard prompts: blockers raised / blockers resolved / risks; Require team-lead participation within 24h
3. 24h surface time, no exceptions. Define cross-team blocker status taxonomy; Auto-escalate blockers >24h to PM; Track blocker time-to-surface as a KPI
4. Nothing ships across teams without an integration check. Define gate criteria: contract tests, schema check, feature flag; Require gate sign-off in PR template; Block merges on red gate state
5. Pre-release review catches what the gate missed. Async release-readiness checklist 48h pre-release; Each team lead signs their slice; PM signs the aggregate
6. Keep the graph live, not stale. Weekly graph diff vs reality; Pull dependencies out as new epics arrive; Archive resolved nodes

## Decision points

- **Build dependency graph** -> Advance when each team confirms their slice is accurate.
- **Scrum-of-scrums async** -> Advance after 2 consecutive weeks of full participation.
- **Blocker SLA** -> Advance when median time-to-surface is <24h for 2 weeks.
- **Integration-readiness gate** -> Advance after one full release cycle uses the gate.
- **Release-readiness review** -> Advance after 2 consecutive clean releases.
- **Refine the graph** -> Done when graph age never exceeds 1 day post-change.

## References

- `faion/knowledge/pro/pm/pm-agile/kanban-scaled-agile-ceremonies`
- `faion/knowledge/pro/pm/pm-agile/value-stream-management`
- `faion/knowledge/pro/pm/pm-traditional/communications-management`
- `faion/knowledge/pro/pm/pm-traditional/project-integration`
- `faion/knowledge/pro/pm/pm-traditional/quality-management`
- `faion/knowledge/pro/pm/project-manager/predictive-analytics-pm`
- Related: `ai-assisted-sprint-planning-with-capacity-reality-check`, `distressed-project-rescue-90-day-turnaround`
