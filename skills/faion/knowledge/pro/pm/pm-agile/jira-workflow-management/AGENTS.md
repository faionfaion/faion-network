---
slug: jira-workflow-management
tier: pro
group: pm
domain: pm
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: "Jira project setup config: issue-type scheme, workflow state machine, transition rules, automation policies, JQL conventions for Scrum and Kanban teams."
content_id: "aafe6ea5b22c1a8a"
complexity: medium
produces: config
est_tokens: 4500
tags: [jira, workflow, issue-types, automation, jql]
---
# Jira Workflow Management

## Summary

**One-sentence:** Jira project setup config: issue-type scheme, workflow state machine, transition rules, automation policies, JQL conventions for Scrum and Kanban teams.

**One-paragraph:** Jira Workflow Management defines the testable methodology that turns the recurring work named in this skill into a repeatable, auditable artefact. The methodology is grounded in 6 core rules (see `content/01-core-rules.xml`), a JSON-Schema output contract, 4 catalogued failure modes, a 5-step procedure, and a decision tree whose leaves all reference a rule id.

**Ефективно для:**

- Atlassian-stack shops using Jira Cloud or Server as the primary tracker.
- Multi-team programs where workflow consistency matters across boards.
- Teams whose automation needs go beyond default Jira behaviour (cross-issue links, SLA timers).
- Engineers building dashboards on JQL queries that must remain stable.

## Applies If (ALL must hold)

- Jira admin role available for workflow + scheme changes.
- Team has agreed on a single workflow per issue-type (Story, Bug, Task, Epic).
- Naming convention for projects + components has been decided up-front.
- Automation rules budget (Jira Cloud free tier limits) is acceptable.

## Skip If (ANY kills it)

- Team is migrating to Linear / GitHub Projects — defer Jira config to the migration ADR.
- Single-team, <10 issues/week — default Jira workflows are good enough.
- Workflow change would require migrating thousands of existing issues — defer to a migration plan.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Source-of-truth data | tool export / sheet / API | upstream system named in this methodology |
| Prior cycle's artefact (if any) | json / md | repo / wiki where artefacts persist |
| Named consumer | person / agent | engagement charter |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/pm/AGENTS.md` | Parent group context (vocabulary, neighbouring methodologies). |
| `pro/sdd/AGENTS.md` if present | SDD discipline for the artefact lifecycle (status flow, owners, review). |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules with rationale + source | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft 2020-12) + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom/root-cause/fix | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure with input/action/output | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule id | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `jira-workflow-management_template_fill` | haiku | Bounded template fill, no judgement. |
| `jira-workflow-management_evidence_check` | sonnet | Bounded comparison + judgement on anchored evidence. |
| `jira-workflow-management_synthesis` | opus | Cross-input synthesis + final write-up. |

## Templates

| File | Purpose |
|------|---------|
| `templates/output-schema.json` | JSON Schema (draft 2020-12) for the Jira workflow configuration artefact. |
| `templates/workflow-states.yaml` | Canonical Scrum + Kanban workflow states + transitions in YAML. |
| `templates/bulk-transition.py` | Reference script for safe bulk transitions via Jira REST API. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-jira-workflow-management.py` | Validate the artefact against the schema in `content/02-output-contract.xml`. | CI on each artefact change; pre-commit. |

## Related

- parent skill: `pro/pm/` (see neighbouring methodologies).
- [[launch-raci-template]]
- [[reporting-basics]]
- external: industry references cited inline in `content/01-core-rules.xml`.

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input
preconditions, source-of-truth access, named-consumer presence) onto a concrete
verdict — apply the methodology, downgrade to draft, or skip — with each leaf
referencing a rule id from `content/01-core-rules.xml`.
