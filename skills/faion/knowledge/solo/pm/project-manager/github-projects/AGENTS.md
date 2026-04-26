# GitHub Projects

## Summary

GitHub Projects (v2) native project management: custom fields (Status, Priority, Sprint iteration, Team), table/board/roadmap views, built-in workflows for automatic status transitions, and GitHub Actions for complex automation. Primary agent interface is `gh project` CLI and GraphQL mutations. All field writes require node_ids — store project_id and field_ids in constitution.md after first fetch.

## Why

For teams already on GitHub, adding a separate PM tool creates context-switching overhead. GitHub Projects provides native code-task traceability: "Fixes #123" in a PR automatically transitions the linked issue to Done when merged. Organization-level projects span multiple repositories. The GitHub CLI (`gh project`) is the simplest agent interface — no GraphQL boilerplate needed for most operations.

## When To Use

- Codebase is on GitHub and code-task traceability ("Fixes #123") is a priority
- Team already manages Issues and PRs on GitHub
- Open-source project needs a public-facing project board for community contributors
- Cross-repository work under one GitHub organization
- GitHub Actions already in use — extending to project automation is a natural fit

## When NOT To Use

- Team is not on GitHub (GitLab, Bitbucket) — tool is GitHub-native only
- Complex portfolio management across many products — GitHub Projects lacks portfolio hierarchy
- OKR or goal tracking required — GitHub has no goals layer; use Linear or ClickUp
- Non-technical stakeholders need to update tasks — GitHub UI has a learning curve
- Built-in velocity charts, burndown, or capacity planning required — needs custom Actions

## Content

| File | What's inside |
|------|---------------|
| `content/01-project-setup.xml` | Project configuration rules, custom fields setup, views configuration, workflow automation rules |
| `content/02-api-agent.xml` | GraphQL API rules, gh CLI patterns, agent gotchas, GitHub Actions integration |

## Templates

| File | Purpose |
|------|---------|
| `templates/issue-feature.yml` | GitHub issue template for feature requests (YAML form) |
| `templates/workflow-project-automation.yml` | GitHub Actions workflow for adding issues to project and setting fields |
