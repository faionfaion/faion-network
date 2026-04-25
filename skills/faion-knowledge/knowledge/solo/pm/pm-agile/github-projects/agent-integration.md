# Agent Integration — GitHub Projects

## When to use
- Teams already on GitHub for code — zero-tool-switch for issues, PRs, and project tracking in one platform.
- Open source projects where community contributors need a public board to see what is planned and in progress.
- When you want GitHub Actions to drive project automation without a separate Zapier/Make subscription.
- Solopreneur with a monorepo or multi-repo setup — GitHub Projects v2 supports cross-repo items natively.
- When using `gh` CLI in CI/CD pipelines to update project item fields automatically on deploy or test events.

## When NOT to use
- Non-engineering stakeholders who have no GitHub account and cannot be granted access — GitHub Projects are GitHub-account-gated.
- Teams needing rich time tracking, capacity planning, or burndown charts — GitHub Projects analytics are minimal.
- Projects with complex approval workflows, custom issue types, or multi-tier hierarchies — GitHub issues are flat.
- Enterprises with security policies that prohibit external SaaS for issue tracking — GitHub.com is not on-premise.

## Where it fails / limitations
- GitHub Projects v2 GraphQL API uses a separate "node ID" system — IDs in the REST issues API (number) do not map directly to ProjectV2Item IDs without a lookup step.
- No native SLA tracking, priority escalation, or triage queue — must be emulated with labels and GitHub Actions.
- Iteration (sprint) field auto-advances by date, but the API does not expose a simple "current iteration" query; agents must filter by date range to find the active iteration.
- GraphQL mutations for project fields require the `project:write` OAuth scope; classic `repo` scope is not sufficient.
- Workflow automation (built-in) is limited to 8 built-in triggers; complex logic (e.g., "if label X and assignee is null, alert") requires GitHub Actions.
- GitHub Actions automation tokens expire and must be refreshed; long-running agents using GITHUB_TOKEN have a 24-hour TTL.

## Agentic workflow
A Claude subagent can operate as a GitHub Project PM: using the GraphQL API it reads current iteration items, identifies unestimated or unassigned issues, posts comments requesting updates, and updates custom field values (Priority, Team) based on label inference. For release management, the agent can query milestone progress, generate a release checklist issue, and post a status comment when all milestone issues are closed. GitHub Actions workflows can call the agent as a step on PR events, updating the project board automatically when code moves through review stages.

### Recommended subagents
- `github-project-triage` — reads new issues added to project, checks for missing required fields (Priority, Estimate, Assignee), posts a comment listing what is needed.
- `github-release-reporter` — queries milestone + project items for a release, generates a release checklist issue, posts milestone completion percentage as a comment.
- `github-sprint-planner` — queries backlog items by Priority field, proposes a sprint plan (iteration assignment) based on estimate totals vs. capacity, outputs a draft plan for human review.

### Prompt pattern
```
Using the GitHub GraphQL API, query project <PROJECT_NUMBER> for all items
where the Status field is "Backlog" and the Estimate field is null.
For each item return: {number, title, repository, labels}.
Do not modify any items.
```

```
Given this GitHub project item JSON: <item_json>
Determine Priority (P0/P1/P2/P3) based on labels and title keywords:
- label "critical" or "urgent" → P0
- label "bug" with no workaround mentioned → P1
- default → P2
Update the Priority field via updateProjectV2ItemFieldValue mutation.
Return: {item_id, old_priority, new_priority, reason}.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `gh` (GitHub CLI) | Full project management: create/list/update items, fields, views | `brew install gh` / https://cli.github.com/manual/gh_project |
| `gh api` | Raw GraphQL and REST queries from terminal | Built into `gh` |
| `actions/add-to-project` | GitHub Action: auto-add issues/PRs to project on trigger | https://github.com/actions/add-to-project |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| GitHub GraphQL API | SaaS | Yes | Full project v2 CRUD. Requires `project:write` scope for mutations. |
| GitHub REST API | SaaS | Yes | Issues, milestones, labels. Does not expose ProjectV2 fields. |
| GitHub Actions | SaaS | Yes | Native automation; GITHUB_TOKEN available in every workflow. |
| Linear (import) | SaaS | Partial | One-way GitHub → Linear sync via native integration. |
| ZenHub | SaaS | Partial | Extends GitHub with epics, velocity; separate API layer. |
| Jira (GitHub app) | SaaS | Partial | Links issues to Jira tickets via smart commits; not two-way project field sync. |

## Templates & scripts
See `templates.md` for issue YAML templates and release checklist issue format.

`gh` CLI snippet to list unestimated items in a project:
```bash
#!/usr/bin/env bash
# Requires: gh auth login with project:read scope
PROJECT_NUM=1
ORG=myorg

gh api graphql -f query='
query($org: String!, $num: Int!) {
  organization(login: $org) {
    projectV2(number: $num) {
      items(first: 100) {
        nodes {
          id
          content { ... on Issue { number title } }
          fieldValues(first: 10) {
            nodes {
              ... on ProjectV2ItemFieldNumberValue {
                number
                field { ... on ProjectV2Field { name } }
              }
            }
          }
        }
      }
    }
  }
}' -f org="$ORG" -F num="$PROJECT_NUM" \
| jq '[.data.organization.projectV2.items.nodes[]
  | select(.fieldValues.nodes | map(select(.field.name == "Estimate")) | length == 0)
  | {id, number: .content.number, title: .content.title}]'
```

## Best practices
- Use organization-level projects (not repo-level) for multi-repo work — organization projects can pull in issues from any repo in the org.
- Define custom fields at project creation time and document their allowed values in the project README — agents need a stable schema to query and update fields reliably.
- Use `"Fixes #123"` in PR descriptions to auto-close issues on merge; this triggers the built-in "Item closed" → "Done" workflow without agent intervention.
- Store the project node ID (`PVT_*`) in a config file or environment variable — it does not change, unlike the human-readable project number.
- For GitHub Actions automation, use a dedicated service account (GitHub App) rather than personal access tokens so token rotation does not break pipelines.
- Tag iteration fields with consistent naming (`2024-W01`, `Sprint-24`) so agents can pattern-match the current iteration without a complex date-range query.

## AI-agent gotchas
- The ProjectV2Item node ID is different from the Issue number — agents must resolve `content { ... on Issue { number } }` to map between the two; passing the wrong ID to a mutation silently fails.
- GraphQL pagination: items default to returning 100 max; use `pageInfo { hasNextPage endCursor }` and re-query with `after: cursor` to get full results.
- `GITHUB_TOKEN` in Actions has `project` scope only when the workflow explicitly requests it — add `permissions: { projects: write }` to the workflow YAML or the mutation returns 403.
- Built-in workflows ("Item added to project" → set Status to Backlog) run asynchronously after the API call; an agent that creates an item and immediately reads it back may see no Status field set yet.
- The `gh project item-edit` CLI command requires the item node ID, not the issue number — always resolve the node ID first via `gh project item-list`.
- Human checkpoint required before bulk field updates (e.g., setting Priority on 200 backlog items) — no undo exists for bulk project field mutations.

## References
- https://docs.github.com/en/issues/planning-and-tracking-with-projects — GitHub Projects documentation
- https://cli.github.com/manual/gh_project — `gh project` CLI reference
- https://docs.github.com/en/graphql/reference/objects#projectv2 — GraphQL ProjectV2 schema
- https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows — Actions trigger events
- https://github.com/actions/add-to-project — Official Action for auto-adding issues to projects
