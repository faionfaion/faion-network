# Agent Integration — Azure DevOps Boards

## When to use
- Microsoft-stack organisations (Entra ID, M365, Azure cloud) requiring single sign-on and tenant-level governance.
- Regulated/audit-heavy projects: CMMI process template gives Risk, Change Request, Review work item types out of the box.
- Teams already using Azure Pipelines/Repos/Test Plans — Boards integrates work items with builds, pull requests, releases.
- Portfolio reporting via Azure DevOps Analytics + Power BI for executive dashboards.
- Hybrid on-prem (Azure DevOps Server) requirements where Jira Cloud isn't acceptable.

## When NOT to use
- Engineering-only teams who prefer Linear/GitHub Projects' speed and minimalism — ADO Boards UI is heavier.
- Teams using GitHub primarily — sticking with GitHub Projects (now v2) avoids identity/permission duplication.
- Open-source/community projects — ADO licensing assumes commercial accounts.
- Lightweight one-team Kanban — Trello/ClickUp/Linear ship faster.

## Where it fails / limitations
- Process customisation is powerful but irreversible at the inherited-process level if mismatches accumulate.
- WIQL is SQL-like but limited (no joins beyond parent/child); complex reports require Analytics + Power BI.
- Two ways to define areas/iterations (project vs team) confuse teams; ownership clashes are common.
- PAT-based REST API has scope sprawl; agents need carefully scoped tokens or service principals.
- Migration in/out of ADO is painful (work item links, attachments, history); plan before adopting at scale.
- Automation Rules (in Boards settings) are limited; complex workflows need Azure DevOps Pipelines or Power Automate.

## Agentic workflow
A subagent operates against the ADO REST API (PAT or Microsoft Entra service principal), creating/updating work items, running WIQL queries, and updating board state. Use the `azure-devops-cli` (`az devops`, `az boards`) for shell-friendly automation; use REST for batch operations and dashboards. Treat the process template as code: store custom fields/states/rules in YAML, apply via API, version in repo. Human-in-loop required for state-template changes, sprint commitments, and release approvals — agents may set "Active" but not "Closed" without verification.

### Recommended subagents
- `faion-pm-agent` — sprint planning, backlog refinement, capacity calc.
- `faion-sdd-executor-agent` — converts SDD `TASK_*.md` → User Story/Task work items with `wbs_id` field.
- `faion-business-analyst` — generates User Stories with Gherkin acceptance criteria.
- `faion-software-developer` — links commits/PRs to work items via `AB#<id>` syntax.

### Prompt pattern
```
Given task.md and target_iteration:
1. Convert to Azure Boards User Story JSON Patch payload (System.Title,
   System.Description, AcceptanceCriteria, IterationPath, AreaPath,
   Microsoft.VSTS.Scheduling.StoryPoints).
2. Add Tags from task front-matter.
3. Output curl command using PAT $env(ADO_PAT). Do NOT execute.
```

```
Run WIQL: SELECT [System.Id], [System.Title], [System.State]
FROM WorkItems WHERE [System.IterationPath] = @CurrentIteration
AND [System.WorkItemType] IN ('User Story','Bug') AND [System.AssignedTo] = @Me
Sort by [Microsoft.VSTS.Common.Priority]. Output: ranked list of next actions.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `az` (Azure CLI) + `az devops` | Auth, projects, repos | https://learn.microsoft.com/cli/azure/devops |
| `az boards` | Work item CRUD, queries | https://learn.microsoft.com/cli/azure/boards |
| `az pipelines` | Trigger builds linked to work items | https://learn.microsoft.com/cli/azure/pipelines |
| `tfx-cli` | Process template export/import, extension publish | https://github.com/microsoft/tfs-cli |
| `python-tfs` / `azure-devops` Python SDK | Programmatic access | `pip install azure-devops` |
| `httpie` | Quick REST API exploration with PAT | https://httpie.io |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Azure DevOps Services | SaaS | Yes — REST 7.x, GraphQL via Analytics | Cloud, default |
| Azure DevOps Server | On-prem | Yes — same APIs | Self-hosted, regulated/airgapped orgs |
| Azure DevOps Analytics | SaaS | Yes — OData v4 | Source for Power BI dashboards |
| Power BI | SaaS | Yes — REST + Analytics | Burndown, velocity, CFD |
| GitHub | SaaS | Yes — sync via "Boards-GitHub Integration" | Mirror commits/PRs as work item links |
| Marketplace extensions | SaaS | Mixed | Vet for active maintenance |
| Microsoft Teams | SaaS | Yes — connector + Graph API | Notifications on board events |
| Power Automate | SaaS | Yes — connector | Cross-system automation if Boards rules aren't enough |

## Templates & scripts
See `templates.md` for User Story, Sprint Planning, dashboard widgets, REST examples. Inline minimal create-and-link script (≤50 lines):

```python
# ado_create_story.py — create User Story and link to a Feature parent.
import os, requests, json, sys
ORG, PROJECT = "myorg", "MyProject"
PAT = os.environ["ADO_PAT"]
AUTH = ("", PAT)
HDR = {"Content-Type": "application/json-patch+json"}

def create_story(title, desc, ac, points, iteration, parent_id):
    url = (f"https://dev.azure.com/{ORG}/{PROJECT}/_apis/wit/workitems/"
           f"$User%20Story?api-version=7.0")
    body = [
        {"op": "add", "path": "/fields/System.Title", "value": title},
        {"op": "add", "path": "/fields/System.Description", "value": desc},
        {"op": "add", "path": "/fields/Microsoft.VSTS.Common.AcceptanceCriteria",
         "value": ac},
        {"op": "add", "path": "/fields/Microsoft.VSTS.Scheduling.StoryPoints",
         "value": points},
        {"op": "add", "path": "/fields/System.IterationPath",
         "value": iteration},
        {"op": "add", "path": "/relations/-", "value": {
            "rel": "System.LinkTypes.Hierarchy-Reverse",
            "url": (f"https://dev.azure.com/{ORG}/{PROJECT}/"
                    f"_apis/wit/workItems/{parent_id}")
        }},
    ]
    r = requests.post(url, headers=HDR, auth=AUTH, data=json.dumps(body))
    r.raise_for_status()
    return r.json()["id"]

if __name__ == "__main__":
    sid = create_story(*sys.argv[1:])
    print(f"created story id={sid}")
```

## Best practices
- Pick one process template per org and inherit (don't fork): mass-edit migrations across forks are painful.
- Set WIP limits per board column and surface them in card-style rules; without limits Boards become "Active" landfills.
- Use Area Path for ownership, Iteration Path for time. Don't overload either.
- Link commits/PRs with `AB#<id>` so traceability is automatic; don't rely on manual association.
- Capacity planning: enter team member days off; velocity forecasts are only useful with capacity adjustment.
- Save WIQL as Shared Queries with stable URLs; agents reference URL, not query body, so query updates don't break consumers.
- For audit: enable Process History export; CMMI states (Proposed/Active/Resolved/Closed) plus the audit trail satisfy SOX/SOC2.
- PAT scoping: read-only by default; write-scope tokens per agent role; rotate every 90 days.

## AI-agent gotchas
- Iteration paths must be created before assignment; agent that "fixes" a missing iteration by creating one in production breaks sprint history.
- WIQL `@CurrentIteration` is team-scoped; agent across teams sees stale data unless team is specified.
- `System.Tags` is a semicolon-separated string, not an array; agents naively setting it overwrite existing tags.
- JSON Patch ops are order-sensitive; setting State before required fields fails silently with 200 + ValidationError in body.
- Throttling: ADO returns 429 + Retry-After under load; agents must implement backoff (Microsoft documents an 18,750 TSTU/5min limit).
- Linking by full URL is required for relations; bare IDs are silently dropped.
- Process customisation via REST has eventual consistency: read-after-write may show stale schema for ~30s.
- "Closed" state from agents requires verifying acceptance evidence is attached; otherwise audit gap.
- Personally-Identifying-Information: Description fields are not encrypted at rest beyond ADO defaults; never store secrets there.

## References
- Azure Boards docs: https://learn.microsoft.com/en-us/azure/devops/boards/
- REST API reference: https://learn.microsoft.com/en-us/rest/api/azure/devops/wit/
- Process customisation: https://learn.microsoft.com/en-us/azure/devops/organizations/settings/work/customize-process
- WIQL syntax: https://learn.microsoft.com/en-us/azure/devops/boards/queries/wiql-syntax
- Analytics OData: https://learn.microsoft.com/en-us/azure/devops/report/extend-analytics/data-model-analytics-service
- Rate limits: https://learn.microsoft.com/en-us/azure/devops/integrate/concepts/rate-limits
- `az devops` CLI: https://learn.microsoft.com/en-us/cli/azure/devops
- Python SDK: https://github.com/microsoft/azure-devops-python-api
