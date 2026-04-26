# GitHub Projects

## Summary

GitHub Projects v2 is a native project management layer on top of GitHub issues and pull requests, offering table, board, and roadmap views with custom fields, iterations, and built-in automation. It is the right tool when the team already uses GitHub for code — zero tool-switch for issue tracking, PR linking, and project boards.

## Why

Co-locating code and project management eliminates sync overhead: closing a PR with "Fixes #123" auto-advances the issue to Done. GitHub Actions can drive project field updates on any event (label added, PR merged, deploy triggered) without a third-party automation subscription. Cross-repository projects at org level give a unified view of multi-repo work without duplicating issues.

## When To Use

- Teams already on GitHub for source control — no additional tool accounts needed
- Open-source projects requiring a public project board visible to community contributors
- Solopreneur or small team with a monorepo or multi-repo setup
- CI/CD pipelines that need to update project field values on deploy or test events via `gh` CLI
- Organizations that want tight code-to-project traceability without a separate PM tool

## When NOT To Use

- Non-engineering stakeholders who have no GitHub account — boards are GitHub-account-gated
- Teams needing rich time tracking, capacity planning, or burndown charts — GitHub analytics are minimal
- Projects requiring complex approval workflows, custom issue types, or multi-tier hierarchies
- Enterprises with security policies that prohibit external SaaS for issue tracking

## Content

| File | What's inside |
|------|---------------|
| `content/01-project-structure.xml` | Project types, custom fields, views (table/board/roadmap), milestone integration |
| `content/02-automation.xml` | Built-in workflows, GitHub Actions automation, issue templates, GraphQL API patterns |
| `content/03-agent-usage.xml` | Agentic workflow, recommended subagents, GraphQL gotchas, best practices |

## Templates

| File | Purpose |
|------|---------|
| `templates/project-config.yaml` | Project custom fields and views configuration reference |
| `templates/issue-feature.yaml` | GitHub issue YAML template for feature requests |
| `templates/workflow-project-automation.yaml` | GitHub Actions workflow for auto-adding issues to project |
| `templates/graphql-query-items.graphql` | GraphQL query to fetch project items with field values |
| `templates/prompt-triage.txt` | Prompt for agent to triage unestimated project items |
