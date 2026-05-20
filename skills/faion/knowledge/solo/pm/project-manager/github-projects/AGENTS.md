---
slug: github-projects
tier: solo
group: pm
domain: project-manager
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: For teams already on GitHub, GitHub Projects provides native code-task traceability: "Fixes #123" in a PR automatically transitions the linked issue to Done when merged.
content_id: "ac938ee61721c021"
tags: [github, projects, issue-tracking, automation, graphql]
---
# GitHub Projects v2 for Code-Task Traceability

## Summary

**One-sentence:** For teams already on GitHub, GitHub Projects provides native code-task traceability: "Fixes #123" in a PR automatically transitions the linked issue to Done when merged.

**One-paragraph:** For teams already on GitHub, GitHub Projects provides native code-task traceability: "Fixes #123" in a PR automatically transitions the linked issue to Done when merged. Organization-level projects span multiple repositories. Custom fields (Status, Priority, Sprint iteration, Team) are configured in the GitHub UI before agent automation begins. The GitHub CLI (gh project) is the simplest agent interface — no GraphQL boilerplate needed for most operations.

## Applies If (ALL must hold)

- Codebase is on GitHub and code-task traceability ("Fixes #123") is a priority.
- Team already manages Issues and PRs on GitHub.
- Open-source project needs a public-facing project board for community contributors.
- Cross-repository work under one GitHub organization.
- GitHub Actions already in use — extending to project automation is a natural fit.

## Skip If (ANY kills it)

- Team is not on GitHub (GitLab, Bitbucket) — tool is GitHub-native only.
- Complex portfolio management across many products — GitHub Projects lacks portfolio hierarchy.
- OKR or goal tracking required — GitHub has no goals layer; use Linear or ClickUp.
- Non-technical stakeholders need to update tasks — GitHub UI has a learning curve.
- Built-in velocity charts, burndown, or capacity planning required — needs custom Actions.

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

- parent skill: `solo/pm/project-manager/`
