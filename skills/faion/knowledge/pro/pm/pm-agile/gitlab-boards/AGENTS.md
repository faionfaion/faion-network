---
slug: gitlab-boards
tier: pro
group: pm
domain: pm
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: "GitLab Issue Boards configuration with scoped labels (workflow::*, priority::*, type::*), board column policies, WIP limits, and seed-script for label hygiene."
content_id: "0497567bfaceef45"
complexity: medium
produces: config
est_tokens: 4400
tags: [gitlab, kanban, scoped-labels, issue-boards, devops]
---
# GitLab Issue Boards

## Summary

**One-sentence:** GitLab Issue Boards configuration with scoped labels (workflow::*, priority::*, type::*), board column policies, WIP limits, and seed-script for label hygiene.

**One-paragraph:** GitLab Issue Boards defines the testable methodology that turns the recurring work named in this skill into a repeatable, auditable artefact. The methodology is grounded in 6 core rules (see `content/01-core-rules.xml`), a JSON-Schema output contract, 4 catalogued failure modes, a 5-step procedure, and a decision tree whose leaves all reference a rule id.

**Ефективно для:**

- Team already running GitLab CI/CD and wanting boards co-located with issues.
- Kanban-style flow (no fixed sprints) with WIP-limit discipline.
- Multi-project group where label naming must be stable across repos.
- Need an audit trail of state changes via issue events.

## Applies If (ALL must hold)

- GitLab project (CE or EE) with Maintainer role available for label setup.
- Issues are the primary unit of work tracking (not external Jira/Linear).
- Team agrees on scoped-label scheme (workflow:: / priority:: / type::) before seeding.
- Group-level labels are accessible if labels need to be shared across projects.

## Skip If (ANY kills it)

- Team uses GitHub Projects or Jira as the issue tracker; GitLab Boards is the wrong tool.
- Single-developer repo — label scaffolding overhead exceeds value.
- GitLab Free with >5 board columns required — Free caps multiple boards; upgrade or simplify.

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
| `gitlab-boards_template_fill` | haiku | Bounded template fill, no judgement. |
| `gitlab-boards_evidence_check` | sonnet | Bounded comparison + judgement on anchored evidence. |
| `gitlab-boards_synthesis` | opus | Cross-input synthesis + final write-up. |

## Templates

| File | Purpose |
|------|---------|
| `templates/output-schema.json` | JSON Schema (draft 2020-12) for the GitLab Boards configuration artefact. |
| `templates/issue-template-bug.md` | Bug report issue template (steps, expected, actual, environment). |
| `templates/issue-template-feature.md` | Feature request issue template (user need, acceptance criteria). |
| `templates/scoped-labels.py` | Reference script listing the canonical scoped-label scheme. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-gitlab-boards.py` | Validate the artefact against the schema in `content/02-output-contract.xml`. | CI on each artefact change; pre-commit. |

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
