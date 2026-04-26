# Agent Integration — GitHub Projects

## When to use
- Codebase is on GitHub and code–task traceability is important ("Fixes #123" linking)
- Team already manages Issues and PRs on GitHub — adding a separate PM tool creates context-switching overhead
- Open-source project needs a public-facing project board for community contributors
- Cross-repository work needs to be tracked under one organization-level project
- GitHub Actions automation is already in use — extending to project automation is natural

## When NOT to use
- Team is not on GitHub (GitLab, Bitbucket) — native project management is only GitHub-native
- Complex portfolio management needed across many products — GitHub Projects lacks portfolio hierarchy
- OKR/goal tracking required — GitHub has no goals layer; use Linear or ClickUp
- Non-technical stakeholders need to update tasks — GitHub UI has a learning curve
- Velocity charts, burndown, or capacity planning required out-of-the-box — needs extra Actions/scripts

## Where it fails / limitations
- GraphQL API is the primary interface; REST is limited for Projects v2 — agents must use GraphQL mutations
- Custom field writes require the project item's node_id, which must be fetched first (two-step operations)
- Iteration fields (sprints) cannot be created via API — must be pre-configured in the GitHub UI
- ProjectV2 item node_ids are not stable across project transfers
- GitHub Actions automation is coarse-grained; status field transitions based on complex conditions need custom workflows
- No built-in WIP limit enforcement — requires GitHub Actions or external tooling

## Agentic workflow
An agent uses the GitHub GraphQL API (via `gh` CLI or direct HTTP) to read project items, update custom fields (Status, Priority, Sprint), and add draft issues or link existing issues to the project. GitHub Actions automation handles mechanical transitions (issue closed → Status=Done). Agents focus on higher-level operations: sprint planning (assigning issues to iteration), triage (setting Priority from issue labels), and reporting (querying project state for a summary). The `gh project` subcommands provide the simplest agent-accessible interface.

### Recommended subagents
- General task subagent (claude-haiku) — field updates, issue assignment to sprint, label sync
- Planning subagent (claude-sonnet-4-6) — sprint planning, triage, board state summary generation

### Prompt pattern
```
Use `gh` CLI. Project URL: {project_url}. Repo: {owner}/{repo}.

1. gh project item-list {project_number} --owner {owner} --format json
2. Filter items where Status = "Backlog" AND Priority = "P0"
3. For each: gh project item-edit --id {item_id} --project-id {project_id}
   --field-id {status_field_id} --single-select-option-id {in_progress_option_id}
Report: list of moved items and new status.
```

```
Run: gh issue list --repo {owner}/{repo} --label "triage" --json number,title,labels,assignees
For each issue, determine Priority based on label (P0-Critical → P0, bug → P1, enhancement → P2).
Set the Priority custom field via GraphQL mutation updateProjectV2ItemFieldValue.
Output: issue number | title | assigned priority.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `gh` (GitHub CLI) | Primary interface: `gh project`, `gh issue`, `gh pr` | `brew install gh` / https://cli.github.com/manual/gh_project |
| `gh-dash` | Terminal dashboard for PRs and Issues | `gh extension install dlvhdr/gh-dash` / https://github.com/dlvhdr/gh-dash |
| `github-project-manager` | Python SDK for GitHub Projects v2 | `pip install PyGithub` / https://pygithub.readthedocs.io |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| GitHub Projects v2 | SaaS | Yes — GraphQL API + gh CLI | Best native option; requires GraphQL for field writes |
| GitHub Actions | SaaS | Yes — YAML workflows | Trigger agent workflows on issue/PR events; see workflow examples in README |
| Linear | SaaS | Yes — REST + GraphQL | Alternative if GitHub Projects proves too limited; two-way sync via Unito |
| Unito | SaaS | Partial | Syncs GitHub Issues ↔ Jira/Asana/ClickUp; no direct agent API |
| Zapier | SaaS | Partial | No-code GitHub → other tool automation; not agent-native |

## Templates & scripts
Issue templates (Feature, Bug, Sprint Planning, Release Checklist) are in `templates.md`. GitHub Actions workflow example is in the README.

Inline — add all open P0-labeled issues to a GitHub Project:
```bash
#!/usr/bin/env bash
# add-p0-to-project.sh
OWNER="${1:?Usage: $0 owner repo project_number}"
REPO="${2:?}"
PROJECT="${3:?}"
gh issue list --repo "$OWNER/$REPO" --label "P0-Critical" --json number \
  | jq -r '.[].number' \
  | while read -r num; do
      gh project item-add "$PROJECT" --owner "$OWNER" --url \
        "https://github.com/$OWNER/$REPO/issues/$num"
      echo "Added issue #$num to project $PROJECT"
    done
```

## Best practices
- Store project_number, field_ids (Status, Priority, Sprint), and option_ids in `.aidocs/memory/` or constitution.md — GraphQL mutations need them every time
- Use organization-level projects for cross-repo work; repo-level projects are limited to one repository
- Enable "Auto-add items" workflow in project settings for the main repo — reduces manual issue-to-project linking
- Use issue templates (`.github/ISSUE_TEMPLATE/`) to enforce consistent structure that agents can reliably parse
- Link PRs to issues with "Fixes #NNN" — GitHub automatically transitions Status to Done on merge when "Item closed" workflow is active
- Set iteration (sprint) field duration at project creation; cannot be changed via API later
- Use milestones for release targets in addition to project boards — `gh milestone` is fully CLI-accessible

## AI-agent gotchas
- GraphQL mutations require node_ids (e.g., `PVT_kwDO...`), not human-readable names — agents must run a query first to fetch these; store them to avoid repeated lookups
- `gh project item-edit` requires both `--project-id` and the field's `--field-id` — two separate IDs that differ from the project number shown in the URL
- Built-in "Item closed" automation only transitions Status; Priority and Sprint must be set explicitly by agents
- Creating iteration options via API is not supported as of 2025 — pre-create sprint iterations in the GitHub UI before agent sprint planning
- GitHub Actions `PROJECT_TOKEN` must have `project` scope (not default `GITHUB_TOKEN`) — a common cause of silent API failures
- Rate limits: GraphQL 5000 points/hour per token; complex project queries consume 50-100 points each; monitor for large boards

## References
- https://docs.github.com/en/issues/planning-and-tracking-with-projects — GitHub Projects documentation
- https://cli.github.com/manual/gh_project — gh project CLI reference
- https://docs.github.com/en/graphql — GitHub GraphQL API
- https://docs.github.com/en/actions — GitHub Actions
- https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests — Issue templates
