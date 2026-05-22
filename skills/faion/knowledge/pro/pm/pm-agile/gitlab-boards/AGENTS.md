---
slug: gitlab-boards
tier: pro
group: pm
domain: pm
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: GitLab Issue Boards provide kanban-style project management integrated directly with GitLab's DevOps platform.
content_id: "935f0b7572a29575"
tags: [gitlab, kanban, project-management, devops, issue-boards]
---
# GitLab Boards

## Summary

**One-sentence:** GitLab Issue Boards provide kanban-style project management integrated directly with GitLab's DevOps platform.

**One-paragraph:** GitLab Issue Boards provide kanban-style project management integrated directly with GitLab's DevOps platform. Boards visualize issues through customizable lists based on scoped labels, assignees, or milestones, enabling workflow management alongside CI/CD pipelines. Unifying source control, CI/CD, and project tracking in one platform eliminates context-switching overhead and enables automation that is impossible across separate tools — for example, auto-transitioning an issue to `workflow::review` when a linked MR is opened. Scoped labels give the board real state-machine semantics rather than tag soup.

## Applies If (ALL must hold)

- Teams using GitLab for source control and CI/CD wanting a single-platform PM workflow.
- Multi-project / multi-group programs where group-level boards aggregate cross-repo issues.
- Compliance-conscious organizations that need self-hosted (Omnibus) over SaaS.
- Workflows tied to MR lifecycle (issue → branch → MR → review → merge → close).
- Teams running Iterations (sprints) with cadence automation built into GitLab.

## Skip If (ANY kills it)

- Source not in GitLab — adopting boards-only via API is awkward; use a source-aligned tool (Jira, Linear, GitHub Projects).
- Heavy portfolio + EVM needs — GitLab roadmaps are basic compared to Jira Plans or MS Project.
- Non-technical stakeholders who refuse Markdown / quick-action syntax — adoption tax exceeds value.
- Tiny teams that don't need WIP limits or scoped labels — Trello is faster with less ceremony.
- Budget constrained to free tier but requiring WIP limits, multiple boards, or iterations (all Premium+).

## Prerequisites

- TBD — list concrete input artifacts and where they come from

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `TBD/path` | TBD — what upstream output this consumes |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules migrated from v1 methodology | ~800 |
| `content/02-output-contract.xml` | essential | Output schema (stub — fill from v1 patterns) | ~800 |
| `content/03-failure-modes.xml` | essential | Antipatterns migrated from v1 methodology | ~800 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| TBD | sonnet | TBD |

## Templates

| File | Purpose |
|------|---------|
| TBD | TBD |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| TBD | TBD | TBD |

## Related

- parent skill: `pro/pm/pm-agile/`
