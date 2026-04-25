# Agent Integration — GitLab Boards

## When to use
- Engineering teams already on GitLab for source control + CI/CD wanting unified DevOps + PM in one platform.
- Self-hosted or compliance-constrained orgs (defense, finance, healthcare) where GitLab CE/EE on-prem is the only option.
- Group-of-projects / program-level visibility via group boards across many repos under one namespace.
- DevSecOps pipelines feeding the same tracker that holds work (vulnerabilities → issues → boards).
- Teams using GitLab Iterations for sprint cadence and Roadmaps for portfolio-level views.
- Pairing with `kanban-fundamentals/`, `agile-ceremonies-setup/`, `risk-register/`, `change-control/`, `pm-tool-selection/`, `cross-tool-migration/`, and `geek/ai/claude-code` for CI-driven board automation.

## When NOT to use
- Teams not using GitLab for code (and unwilling to adopt) — Linear / Jira / GitHub Projects fit better.
- Heavy custom-field requirements with cross-issue rollups, formulas, and pivot dashboards — GitLab boards are deliberately simple; ClickUp / Smartsheet / Jira Plans win.
- Marketing / non-engineering teams that need rich content management — Asana / Notion / ClickUp fit better.
- Free-tier projects needing WIP limits, scoped iteration boards, or roadmap timelines — those are Premium/Ultimate features.
- Highly regulated portfolios needing earned-value management, official gantts, or PMO-grade reporting — GitLab is light on EVM.

## Where it fails / limitations
- Free tier is sparse: WIP limits, scoped labels, iteration cadence, multiple boards per project, group-level boards, Roadmaps — most are Premium+.
- Scoped labels (`workflow::*`) are powerful but invisible to API-naive tools; agents that aggregate via REST must understand the `::` mutual-exclusivity convention.
- Issue weight is a single integer, not story points + estimate + time; teams forcing both into "weight" lose information.
- Iterations cadence is per-group, not per-team — multi-team groups get coupled cadences whether they want them or not.
- Cross-project boards struggle when projects belong to different groups; you may need group-of-groups.
- GraphQL API has uneven coverage vs. REST; some board operations are REST-only and vice versa.
- Issue templates require commit access; teams without push to default branch cannot enforce them.
- Notification volume is high by default; teams that don't tune notifications burn out.
- "Closes #N" auto-close depends on default-branch merges; merge to non-default branches will not close issues.

## Agentic workflow
Drive boards through the GitLab API/CLI from CI and from a curator subagent. Encode the workflow as scoped labels (`workflow::*`, `priority::*`, `type::*`) in a YAML file under `.gitlab/labels.yaml`, applied via a CI job. A curator agent enforces label hygiene (one workflow label per issue, deprecated labels removed) and templates (bug, feature, sprint planning) sit in `.gitlab/issue_templates/`. CI moves issues across columns on MR events (open → review, merge → closed). Never let agents close issues without an MR or human approval — closure is decision authority.

### Recommended subagents
- `faion-sdd-executor-agent` — executes board setup as SDD tasks: TASK_label_taxonomy, TASK_board_layout, TASK_iteration_cadence, TASK_template_enforcement, TASK_ci_automation.
- A custom `label-curator-agent` (model: haiku per README "Apply established patterns"): nightly walk over issues; flags issues with multiple `workflow::*` labels, missing `type::*`, stale `workflow::in-progress` >14 days.
- A custom `triage-router-agent` (model: sonnet): incoming issues from Service Desk and external bots — applies `type::*` + `workflow::triage`, suggests assignee from CODEOWNERS / area expertise.
- A custom `iteration-planner-agent` (model: sonnet): converts the README "Sprint Planning Issue" template into an actual planning issue with capacity table from team availability.
- A custom `mr-board-mover-agent` (model: haiku): runs in CI on MR events; flips `workflow::in-progress` ↔ `workflow::review` based on MR state. Idempotent.
- A custom `dependency-graph-agent` (model: sonnet): walks `/blocks` and `/relate` links, produces a dependency Mermaid graph for sprint planning.
- `password-scrubber-agent` — runs over issue descriptions, comments, and Service Desk emails before any external sharing.

### Prompt pattern
Two-step: triage → label.

```
You are the triage-router agent. Inputs:
1. New issue payload (title, description, attachments).
2. Allowed labels (from .gitlab/labels.yaml).
3. CODEOWNERS map (path → maintainer).

Emit STRICT JSON:
{ "labels": ["type::<...>", "priority::<...>", "workflow::triage"],
  "milestone": <slug or null>,
  "weight": <int 0-13>,
  "assignee_suggestion": "@<username>",
  "rationale": "<= 2 sentences",
  "needs_human_review": true|false }

Rules: never apply more than one label per scoped namespace.
weight=0 means unestimated; ranges: 1-2 trivial, 3-5 standard, 8-13 large/break-down.
needs_human_review=true if priority::critical, weight>=13, or no clear type.
Quote-pick the rationale from the issue body where possible.
```

CI mover prompt is unnecessary — use a deterministic script.

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `glab` | Native GitLab CLI; create issues, MRs, comment, label, close | https://gitlab.com/gitlab-org/cli |
| `git` | Branch + commit + push; tightly integrated with issues via `Closes #N` | preinstalled |
| `python-gitlab` | Python client; ideal for the curator agent | `pip install python-gitlab` |
| `httpie` / `curl` | Quick REST/GraphQL probes during board design | https://httpie.io |
| GraphQL Explorer (built-in at `/-/graphql-explorer`) | Test queries before scripting | bundled with GitLab |
| `gitlab-runner` | Local runner for `.gitlab-ci.yml` jobs that update boards on events | https://docs.gitlab.com/runner/ |
| `pre-commit` | Lint `.gitlab/issue_templates/*.md` and `labels.yaml` | https://pre-commit.com |
| `mermaid-cli` (`mmdc`) | Render dependency graphs from issue links for sprint planning | `npm i -g @mermaid-js/mermaid-cli` |
| `yq` / `jq` | Read and patch labels, milestones, board configs | `apt install yq jq` |
| `gitlabform` | Idempotently apply project/group config (labels, MR settings) from YAML | https://github.com/gitlabform/gitlabform |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| GitLab.com | SaaS | REST + GraphQL | Hosted; tier gates Premium features (WIP, iterations, multi-board). |
| GitLab Self-Managed (CE/EE) | OSS / Commercial | REST + GraphQL | On-prem default for regulated/airgapped orgs. |
| GitLab Dedicated | SaaS | REST + GraphQL | Single-tenant SaaS; same APIs. |
| Mattermost (often paired) | OSS | REST | Slack-equivalent for GitLab-first orgs; ChatOps for board updates. |
| Jira (with bridge) | SaaS | REST | Common bridge target during migration; pair with GitLab Jira Cloud Integration. |
| Linear / Asana / ClickUp | SaaS | REST/GraphQL | Migration sources; see `cross-tool-migration/`. |
| Slack / Teams | SaaS | REST + Events | Notification bridges to non-GitLab stakeholders; throttle hard. |
| ServiceNow | SaaS | REST | Pair Service Desk → GitLab for ITSM-tracked issues. |
| Sentry / GlitchTip | SaaS / OSS | REST | Error → GitLab issue auto-creation. |
| GitLab Service Desk | Built-in | Email-in | External requests as issues with labels; great for solopreneur support flows. |
| Zenhub / Plaky / GitKraken | SaaS | REST | Third-party PM overlays; rarely needed if Premium GitLab is available. |
| Roadmunk / ProductPlan | SaaS | REST | Roadmap sources for orgs not on Premium Roadmaps. |

## Templates & scripts
The README provides extensive issue templates (Bug, Feature, Sprint Planning), MR template, and label/iteration YAML. Inline below: a Python snippet that audits a project for stale `workflow::in-progress` issues.

```python
#!/usr/bin/env python3
"""stale_in_progress.py — flag in-progress issues idle > N days."""
from __future__ import annotations
import os
import sys
from datetime import datetime, timedelta, timezone
import gitlab

def main(project_id: str, days: int = 14) -> int:
    gl = gitlab.Gitlab(
        os.environ["GITLAB_URL"], private_token=os.environ["GITLAB_TOKEN"]
    )
    project = gl.projects.get(project_id)
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)
    stale = []
    for issue in project.issues.list(
        state="opened", labels="workflow::in-progress",
        iterator=True, per_page=100,
    ):
        last = datetime.fromisoformat(issue.updated_at.replace("Z", "+00:00"))
        if last < cutoff:
            stale.append((issue.iid, issue.title, (datetime.now(timezone.utc) - last).days))
    for iid, title, age in sorted(stale, key=lambda x: -x[2]):
        print(f"!{iid:<5} {age:>3}d  {title}")
    return 1 if stale else 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 14))
```

Wire into a scheduled CI pipeline; failure opens a triage issue assigned to the team lead.

## Best practices
- Use scoped labels (`namespace::value`) for any state machine — `workflow::*`, `priority::*`, `type::*`, `severity::*`. Single-namespace mutual exclusion prevents conflicting states.
- Keep label count ≤ 20 active labels. Archive deprecated labels rather than reusing.
- One workflow board per team, additional boards as filtered views (Bug Triage, Tech Debt, Release N) — not as parallel state machines.
- Set WIP limits per column (Premium); enforce them — let cards block on entry, not on PMO nag.
- Use Iterations for sprint cadence at the group level; align teams to the same cadence to ease cross-team planning.
- Issue templates committed to `.gitlab/issue_templates/` enforce structure; pair with a CI lint on missing sections.
- Use weight consistently: 0 = unestimated, 1–2 = trivial, 3–5 = standard, 8–13 = large (must break down). Beyond 13 = epic candidate.
- Auto-close via `Closes #N` only on default-branch merges; for feature-branch flows use deploy-job notifications.
- Roadmaps + Epics for portfolio (Premium+); keep epics shallow (≤3 levels) to avoid drowning in nesting.
- Tie MR templates to issue templates: every MR references an issue, every closed issue has an MR (except docs).
- Service Desk for external requests — auto-label `source::service-desk` + `workflow::triage` and route via the triage-router agent.
- Use Quick Actions in commit messages and MR bodies for traceability (`Refs #N`, `/relate`, `/spend`).

## AI-agent gotchas
- Scoped labels confuse agents — they apply two `workflow::*` labels, GitLab keeps the last, the agent thinks both stuck. Verify via API read-after-write.
- Issue weight is overloaded — agents conflate it with story points, hours, or "priority". Pick one team meaning and pin it in `.gitlab/labels.yaml` notes.
- Quick Actions only work on creation/update via the body, not via API field sets — agents using REST `PUT /issues` will not trigger `/spend` or `/assign`. Use the notes API or the dedicated endpoints.
- GraphQL pagination cursors break across deploy boundaries; do not persist cursors longer than a job.
- Auto-close hallucination: an LLM-generated MR body says "Closes #999" without verifying #999 exists. Validate IDs before commit.
- Bulk label changes are dangerous; cap to N per run and require human approval beyond a threshold.
- Service Desk emails are PII (sender email, possibly customer data); scrub before any external model call.
- Notification spam: bots that comment on every state change drown teams. Prefer thread updates over new comments.
- Time arithmetic: GitLab returns ISO 8601 UTC; agents in local TZ misclassify "today vs. yesterday".
- Cross-project links via `/relate` only work if the agent token has access to both; failures are silent.
- CODEOWNERS-based assignee suggestions can violate confidentiality (suggesting an external user). Filter by membership.
- Long-context drift: agents reading 1,000 issues at once lose track. Page by board column or by label.
- Human-in-the-loop checkpoints (mandatory): label taxonomy changes, milestone closure, iteration cadence changes, board deletion, mass relabel, Service Desk auto-assignment of priority::critical.

## References
- GitLab Issue Boards — https://docs.gitlab.com/ee/user/project/issue_board.html
- GitLab Labels (incl. scoped) — https://docs.gitlab.com/ee/user/project/labels.html
- GitLab Iterations — https://docs.gitlab.com/ee/user/group/iterations/
- GitLab Quick Actions — https://docs.gitlab.com/ee/user/project/quick_actions.html
- GitLab API (REST) — https://docs.gitlab.com/ee/api/
- GitLab API (GraphQL) — https://docs.gitlab.com/ee/api/graphql/
- GitLab Service Desk — https://docs.gitlab.com/ee/user/project/service_desk/
- GitLab Roadmaps + Epics (Premium/Ultimate) — https://docs.gitlab.com/ee/user/group/roadmap/
- python-gitlab — https://python-gitlab.readthedocs.io
- gitlabform — https://github.com/gitlabform/gitlabform
- Sibling methodologies: `kanban-fundamentals/`, `agile-ceremonies-setup/`, `risk-register/`, `change-control/`, `pm-tool-selection/`, `cross-tool-migration/`.
