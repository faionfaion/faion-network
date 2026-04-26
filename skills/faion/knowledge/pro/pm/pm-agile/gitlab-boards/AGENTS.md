# GitLab Boards

## Summary

GitLab Issue Boards provide kanban-style project management integrated directly with GitLab's DevOps platform. Boards visualize issues through customizable lists based on scoped labels, assignees, or milestones, enabling workflow management alongside CI/CD pipelines. The key mechanism is scoped labels (`::`-syntax) that enforce mutual exclusivity, preventing issues from occupying two workflow states simultaneously.

## Why

Unifying source control, CI/CD, and project tracking in one platform eliminates context-switching overhead and enables automation that is impossible across separate tools — for example, auto-transitioning an issue to `workflow::review` when a linked MR is opened. Scoped labels give the board real state-machine semantics rather than tag soup.

## When To Use

- Teams using GitLab for source control and CI/CD wanting a single-platform PM workflow.
- Multi-project / multi-group programs where group-level boards aggregate cross-repo issues.
- Compliance-conscious organizations that need self-hosted (Omnibus) over SaaS.
- Workflows tied to MR lifecycle (issue → branch → MR → review → merge → close).
- Teams running Iterations (sprints) with cadence automation built into GitLab.

## When NOT To Use

- Source not in GitLab — adopting boards-only via API is awkward; use a source-aligned tool (Jira, Linear, GitHub Projects).
- Heavy portfolio + EVM needs — GitLab roadmaps are basic compared to Jira Plans or MS Project.
- Non-technical stakeholders who refuse Markdown / quick-action syntax — adoption tax exceeds value.
- Tiny teams that don't need WIP limits or scoped labels — Trello is faster with less ceremony.
- Budget constrained to free tier but requiring WIP limits, multiple boards, or iterations (all Premium+).

## Content

| File | What's inside |
|------|---------------|
| `content/01-board-setup.xml` | Board types, scoped label scheme, WIP limits, board configuration rules. |
| `content/02-automation.xml` | CI/CD automation patterns, issue transitions via API, webhook routing, quick-action rules. |
| `content/03-agent-usage.xml` | Agentic workflows: board-author, triage-agent, mr-issue-linker, cycle-time-watcher. Gotchas. |

## Templates

| File | Purpose |
|------|---------|
| `templates/scoped-labels.py` | Script to seed standard scoped labels (`workflow::*`, `priority::*`, `type::*`) via REST API. |
| `templates/issue-template-bug.md` | GitLab issue template for bug reports with quick-action footer. |
| `templates/issue-template-feature.md` | GitLab issue template for feature requests with AC checklist. |

## Scripts

| File | Purpose |
|------|---------|
| `scripts/seed_labels.py` | Create the standard scoped-label set on a GitLab project. |
