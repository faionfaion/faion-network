# Agent Integration — GitLab Boards

## When to use
- Teams already using GitLab for source control + CI/CD; consolidate PM in the same platform to avoid context switching.
- Multi-project / multi-group programs where group-level boards aggregate cross-repo work.
- Compliance-conscious orgs that need self-hosted (Omnibus, Reference Architecture) over SaaS.
- Workflows tied to MR lifecycle (issue → branch → MR → review → merge → close) where automation hangs off CI events.
- Teams running Iterations (sprints) with cadence automation built in.
- Pair with `gitlab-cicd/`, `jira-workflow-management/` (migration source), `pm-tools-overview/` (selection).

## When NOT to use
- Source not in GitLab — adopting boards-only via API is awkward; use the source-aligned tool (Jira/Linear/GitHub) instead.
- Heavy portfolio + EVM needs — GitLab roadmaps are basic compared to Jira Plans / MS Project.
- Non-technical stakeholders who refuse Markdown / quick-action syntax — adoption tax exceeds value.
- Tiny teams that do not need WIP limits or scoped labels — Trello is faster.
- Free tier needs WIP limits / multiple boards / iterations (Premium+) — budget mismatch.

## Where it fails / limitations
- WIP limits, multiple boards per project, iterations, and scoped labels are Premium+ — free tier loses much of the value.
- Group boards inherit subgroup labels inconsistently; agents that move issues across groups can lose label context.
- Quick actions (`/label`, `/assign`) only work in issue/MR descriptions and comments — REST API edits do not parse them.
- Webhooks are per-project (or system) — agents listening at the right scope must subscribe carefully or miss events.
- Service Desk emails create issues with sparse fields; auto-triage agents must enrich heavily.
- GraphQL coverage gaps remain for some board operations; mix REST + GraphQL or hit dead ends.
- Self-hosted instances drift from SaaS feature releases by months; agents written against SaaS may break on Self-Managed.
- Rate limits per user / IP on Self-Managed are admin-configurable and frequently surprise integrations.

## Agentic workflow
A `board-author` agent generates board-list YAML from a process description (workflow stages, WIP limits, filters), applies via REST, and emits a smoke-test sequence (create issue, transition through every list, verify counts). A `triage-agent` runs nightly: pulls open `workflow::triage` issues, applies labels by content (severity, component, type), assigns reviewers using CODEOWNERS-like rules, and moves to `workflow::ready`. A `mr-issue-linker` ensures every MR has `Closes #N` and matching scoped labels before merge. A `cycle-time-watcher` derives DORA + flow metrics from board activity. Humans approve label-scheme changes, board structure changes, and triage policy.

### Recommended subagents
- `board-author` (sonnet) — synthesize board lists + scoped labels from process YAML.
- `triage-agent` (sonnet) — classify and route incoming issues; never auto-close.
- `mr-issue-linker` (haiku) — enforce link discipline pre-merge.
- `cycle-time-watcher` (haiku, scheduled) — pull lead/cycle time from issue events; alert on drift.
- `quick-action-generator` (haiku) — emit `/label /milestone /weight /estimate` snippets for templates.
- `webhook-router` (haiku) — receive GitLab events, route to the appropriate downstream agent.

### Prompt pattern
```
You are board-author. Inputs: process.yaml (stages with WIP limits, filters,
label scheme). Emit (a) a list of scoped labels to create with `::` syntax,
(b) an array of board lists with order + WIP, (c) a smoke-test plan that
creates a test issue and walks it through every transition. Return STRICT
JSON. Refuse if any stage lacks an exit criterion.
```

```
You are triage-agent. Given an incoming issue (title, body, project context,
existing labels), output: { "type": "bug|feature|tech-debt|docs|question",
"priority": "critical|high|medium|low", "component": "<from project list>",
"workflow": "ready|backlog", "reasons": [...] }. Cite spans from the body
that support each tag. Do not invent components not in the project's list.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `glab` | First-party GitLab CLI: issues, MRs, labels, boards | https://gitlab.com/gitlab-org/cli |
| `glab-cli/glab issue` | Issue CRUD with quick-action support | as above |
| `python-gitlab` | Powerful Python client | `pip install python-gitlab` |
| `node-gitlab` | Node client | `npm i @gitbeaker/node` |
| `git push -o ci.skip` / `merge_request.create` | Push-options drive MR creation w/ labels | https://docs.gitlab.com/ee/user/project/push_options.html |
| `pre-commit` + `gitlab-ci-lint` | Validate `.gitlab-ci.yml` and label discipline locally | https://pre-commit.com |
| `webhook` (adnanh) | Local webhook receiver for development | https://github.com/adnanh/webhook |
| `mermaid-cli` | Render board state as a Mermaid flow | `npm i -g @mermaid-js/mermaid-cli` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| GitLab.com SaaS | SaaS | REST + GraphQL | Easiest to integrate; SaaS rate limits apply. |
| GitLab Self-Managed (Omnibus) | OSS | REST + GraphQL | Same APIs; admin-configured rate limits. |
| GitLab Dedicated | SaaS | REST + GraphQL | Single-tenant Cloud; same APIs. |
| GitLab Service Desk | SaaS/OSS | REST | Email-to-issue; agents triage; pair with `triage-agent`. |
| GitLab Runner (Docker / k8s) | OSS | n/a | Run automation as scheduled CI jobs. |
| Mattermost | OSS | REST | First-class GitLab integration; pair for chatops. |
| Slack / Teams | SaaS | REST | Webhook routing for issue events. |
| Jira/Linear (cross-link) | SaaS | REST | Bridge integrations; mark source-of-truth. |
| Confluence / Notion / Wiki.js | SaaS/OSS | REST | Process and label-scheme docs. |
| LinearB / Swarmia / Sleuth | SaaS | REST | Engineering metrics overlay if native is insufficient. |

## Templates & scripts
README ships extensive issue/MR templates and quick-action examples. Inline below: a script that creates the standard scoped-label set on a project.

```python
#!/usr/bin/env python3
"""seed_labels.py — create scoped labels on a GitLab project."""
from __future__ import annotations
import os, sys
import requests

GL = os.environ["GITLAB_URL"].rstrip("/")
TOKEN = os.environ["GITLAB_TOKEN"]
PROJECT = sys.argv[1]  # numeric id or url-encoded path

LABELS = [
    ("workflow::backlog", "#6699cc"),
    ("workflow::ready", "#3399cc"),
    ("workflow::in-progress", "#ddaa00"),
    ("workflow::review", "#aa66cc"),
    ("workflow::testing", "#cc6600"),
    ("workflow::done", "#33aa55"),
    ("priority::critical", "#cc0000"),
    ("priority::high", "#ee5500"),
    ("priority::medium", "#cc9900"),
    ("priority::low", "#888888"),
    ("type::feature", "#33aa66"),
    ("type::bug", "#cc3333"),
    ("type::tech-debt", "#996699"),
    ("type::docs", "#5577aa"),
]

s = requests.Session()
s.headers["PRIVATE-TOKEN"] = TOKEN
for name, color in LABELS:
    r = s.post(f"{GL}/api/v4/projects/{PROJECT}/labels",
               data={"name": name, "color": color})
    if r.status_code not in (201, 409):  # 409 = already exists
        r.raise_for_status()
    print(f"{r.status_code:3d}  {name}")
```

## Best practices
- Use scoped labels (`workflow::*`, `priority::*`, `type::*`) — mutual exclusivity prevents conflicting states.
- Keep total label count under 25 per project; archive/rename rather than accumulate.
- Configure WIP limits at the team's measured throughput, not aspirational; tighten if cycle-time degrades.
- Issue + MR templates are version-controlled in `.gitlab/`; review changes via MR like code.
- Use Iterations + iteration-cadence for sprints; let the system create cycles automatically.
- Wire `Closes #N` into MR description as a CI lint rule; do not rely on humans to remember.
- Group-level boards for cross-team programs; keep filters narrow to avoid noise.
- Push-options for branch creation (`-o merge_request.create -o merge_request.label="workflow::review"`) — agents consistent across humans.
- Service Desk: triage with labels and only after enrichment; never auto-close.
- Self-Managed: pin runner versions; rebuild integrations after major upgrades.

## AI-agent gotchas
- Quick actions only work in description / comment bodies created via UI/email — REST POSTs with `/label ~"..."` in the description text DO parse them, but PUTs editing the description DO NOT re-trigger; prefer explicit label endpoints.
- Webhook payloads have changed shape across major versions; pin a payload schema version per integration.
- Personal Access Tokens have wide scopes; prefer Group/Project Access Tokens for bots, with `api`+`write_repository` only.
- Bot-created issues become bot-owned; downstream notifications fan out to thousands. Use a dedicated bot user with notifications muted.
- GraphQL pagination on Issues with many comments easily blows up — use REST for high-volume fetches.
- Service Desk emails can carry attachments with secrets; run `password-scrubber-agent` before any cross-posting.
- Iteration cadence creation requires Premium; agents that assume free-tier feature parity break on customer projects.
- Webhook signature validation is project-token based — rotate carefully or break listening agents.
- Auto-moving issues across boards by changing scoped labels can cascade through subscribed integrations; throttle.
- Rate limits on Self-Managed are admin-configurable; tune integrations with backoff and `Retry-After` honoring.
- Human-in-the-loop checkpoints (mandatory): board structure changes, label-scheme changes, auto-close rules, group-level moves.

## References
- GitLab Issue Boards — https://docs.gitlab.com/ee/user/project/issue_board.html
- GitLab Labels — https://docs.gitlab.com/ee/user/project/labels.html
- GitLab Iterations — https://docs.gitlab.com/ee/user/group/iterations/
- GitLab Quick Actions — https://docs.gitlab.com/ee/user/project/quick_actions.html
- GitLab REST API — https://docs.gitlab.com/ee/api/
- GitLab GraphQL — https://docs.gitlab.com/ee/api/graphql/
- Sibling methodologies: `gitlab-cicd/`, `jira-workflow-management/`, `pm-tools-overview/`.
