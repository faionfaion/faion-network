# Agent Integration — Azure DevOps Boards

## When to use
- Microsoft-stack shops already on Azure (AD/Entra, Azure Pipelines, Repos, Test Plans).
- Regulated industries (CMMI process template) needing audit trails on every state transition.
- Teams wanting tight work-item ↔ commit ↔ build ↔ release traceability without third-party glue.
- Enterprise portfolios where Epics → Features → Stories → Tasks hierarchy maps to OKRs / quarterly planning.
- Organizations standardizing on a single tool for code, CI/CD, and PM to consolidate vendor sprawl.

## When NOT to use
- Pure SaaS / non-Microsoft ecosystem; ADO is heavyweight outside the Azure stack.
- Small / fast-moving startup — Linear, Shortcut, GitHub Projects feel 10× lighter.
- Open-source projects with external contributors — onboarding to ADO is friction.
- Teams that need a great mobile UX or modern UI — ADO Boards UX trails Linear/Jira/Shortcut.
- Process customization beyond inheritance — XML "Hosted XML" is deprecated in cloud; you'll regret heavy custom processes.

## Where it fails / limitations
- WIQL has SQL syntax but is not SQL — joins, subqueries are limited; complex reports need Analytics views or Power BI.
- Custom inherited processes can't fully un-do system fields; some "remove" requests fail silently.
- Area Path security model is flat per node; granular per-state permissions require workarounds.
- REST API rate limits aren't published per endpoint — heavy migrations hit throttling without warning.
- Test Plans is a separate license tier; agents that touch test cases need elevated PAT scopes.
- "Resolved" vs. "Closed" semantics differ across Agile/Scrum/CMMI — cross-process queries fail subtly.

## Agentic workflow
A creator agent ingests a SDD spec.md and produces a hierarchy of Epic → Feature → User Story → Task work items via REST API, populating description, AC, story points, area path, iteration. A maintainer agent runs nightly: reads Analytics, finds stale active items, posts comments asking for updates. A reporter agent generates the sprint report (burndown, velocity, scope-change) and posts to Teams. Use a single PAT with minimum scopes; rotate via Key Vault.

### Recommended subagents
- `ado-work-item-creator` — converts spec.md / design.md into hierarchical work items with parent-child links.
- `ado-query-runner` — executes WIQL queries, returns results as Markdown table for review.
- `ado-board-auditor` — checks WIP limit breaches, missing definition-of-done items, orphan tasks.
- `ado-pipeline-bridge` — links commits / PRs / builds back to work items via the `AB#123` magic-string convention.
- `faion-feature-executor` — already in repo; can drive ADO tasks once they exist.

### Prompt pattern
```
You are ado-work-item-creator. Inputs: spec.md (markdown), area_path (string),
iteration_path (string), parent_epic_id (int|null). Output: JSON array of work-item
objects with type, title, description (HTML), acceptance_criteria, story_points,
parent_id. Use process Agile (Story not PBI). Do not invent fields outside the schema.
```

```
WIQL skeleton for stale-item check:
SELECT [System.Id], [System.Title], [System.ChangedDate]
FROM WorkItems
WHERE [System.State] = 'Active'
  AND [System.ChangedDate] < @Today - 5
  AND [System.IterationPath] = @CurrentIteration
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `az devops` | Official CLI: work items, queries, pipelines | `az extension add --name azure-devops` |
| `az boards work-item create` | Scriptable WI creation, parent linking, fields | https://learn.microsoft.com/cli/azure/boards/work-item |
| `az boards query` | Run saved WIQL or inline query | https://learn.microsoft.com/cli/azure/boards/query |
| `vsts-cli` (legacy) | Older alternative; use `az devops` for new work | (deprecated) |
| Power BI CLI / API | Build dashboards on the OData Analytics feed | https://learn.microsoft.com/azure/devops/report/powerbi/ |
| `requests` + PAT | Direct REST when CLI lacks a verb | https://learn.microsoft.com/rest/api/azure/devops/wit/ |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Azure DevOps Services (cloud) | SaaS | Yes — REST + GraphQL-ish OData | Primary target; auth via PAT or Entra OAuth. |
| Azure DevOps Server (on-prem) | Self-hosted | Yes — same REST API | Watch API version differences vs. cloud. |
| GitHub Issues | SaaS | Yes — GraphQL | Cheaper, lighter alternative for repo-bound projects. |
| Jira | SaaS | Yes — REST | Cross-tool sync via Microsoft Power Automate or Unito. |
| Power BI | SaaS | Yes — REST | Native Analytics views integration; good for portfolio dashboards. |
| Microsoft Teams | SaaS | Yes — Graph API | Workflow notifications, adaptive cards from agents. |
| Wiki (built-in) | SaaS | Yes — REST | Store ADRs / runbooks in same project as work items. |

## Templates & scripts
See `templates.md` for the User Story / Sprint Planning Markdown blocks. Inline ADO REST creation example (`scripts/create_story.sh`):

```bash
#!/usr/bin/env bash
set -euo pipefail
ORG="${ADO_ORG:?}"; PROJ="${ADO_PROJ:?}"; PAT="${ADO_PAT:?}"
TITLE="${1:?title}"; ITERATION="${2:?iteration_path}"; AREA="${3:?area_path}"
B64=$(printf ':%s' "$PAT" | base64 -w0)
curl -fsS -X POST \
  -H "Content-Type: application/json-patch+json" \
  -H "Authorization: Basic $B64" \
  -d "[
    {\"op\":\"add\",\"path\":\"/fields/System.Title\",\"value\":\"$TITLE\"},
    {\"op\":\"add\",\"path\":\"/fields/System.IterationPath\",\"value\":\"$ITERATION\"},
    {\"op\":\"add\",\"path\":\"/fields/System.AreaPath\",\"value\":\"$AREA\"}
  ]" \
  "https://dev.azure.com/${ORG}/${PROJ}/_apis/wit/workitems/\$User%20Story?api-version=7.0"
```

## Best practices
- Use Inherited processes only; never customize system fields. You'll need them on upgrade.
- Pin one process per organization; mixing Agile and Scrum across projects breaks cross-project queries.
- Set up a "definition of ready" rule on the board to block stories without AC entering the sprint.
- Tie commits to work items via `AB#1234` in commit message; ADO auto-links and gives traceability.
- Use Analytics views (OData) for any report touching >2 sprints — WIQL is fine for live queries, terrible for trends.
- Rotate PATs via Azure Key Vault; never paste PATs into agent system prompts (use env vars / secret refs).

## AI-agent gotchas
- WIQL is whitespace-sensitive in some clauses; agents drop trailing brackets and produce silent empty results.
- "Description" field accepts HTML, not Markdown — convert agent-generated MD with a sanitizer (e.g., `pandoc -t html`).
- ADO returns 200 OK on partial work-item creation when a custom field is invalid — always re-fetch and validate.
- Iteration path strings are case-sensitive and use backslash separators; `Project/Sprint 1` ≠ `Project\Sprint 1`.
- Bulk create with > 200 items in parallel triggers throttling; agents should batch in chunks of 50 with backoff.
- @mentions in comments require user identity SID, not display name; resolve via Identities API first.
- Test Plans, Pipelines, Repos each have independent PAT scopes — agent fails late if scope is missing.

## References
- https://learn.microsoft.com/en-us/azure/devops/boards/
- https://learn.microsoft.com/en-us/rest/api/azure/devops/wit/
- https://learn.microsoft.com/en-us/azure/devops/boards/queries/wiql-syntax
- https://learn.microsoft.com/en-us/azure/devops/report/powerbi/
- https://learn.microsoft.com/en-us/azure/devops/organizations/settings/work/customize-process
