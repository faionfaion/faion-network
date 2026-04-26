# Agent Integration — Jira Workflow Management

## When to use
- Bootstrapping a new Jira project for Scrum/Kanban/JSM team and wiring sane defaults.
- Standardizing 3+ inconsistent project workflows after acquisition or reorg.
- Replacing manual triage / assignment with automation rules.
- Wiring Jira into CI/CD (auto-transition on deploy, link branches/PRs to issues).
- Migrating from Jira Server/DC to Cloud (workflow + scheme rebuild).
- Pair with `scrum-ceremonies/` (events on top), `gitlab-boards/` / `azure-devops-boards/` (alternatives), `pm-tools-overview/`.

## When NOT to use
- Team < 5 with simple Trello-grade needs — Jira ROI inverts.
- Throwaway 2-week prototype — workflow tax exceeds value.
- Goal is "make Jira look like Linear" — replace Jira instead.
- Pure documentation projects — use Confluence, not Jira.
- Hard compliance forbids Atlassian Cloud and budget forbids DC — stop.

## Where it fails / limitations
- Workflow editor is shared via schemes; one project's change can break others.
- Jira Cloud differs from Server/DC in API, automation engine, and permissions — code does not always port.
- Automation library has rate limits (Cloud: rule executions/month per tier) that hit at scale.
- "Required" field validators block bulk imports and bot-driven flows unless service accounts exempt.
- Custom-field sprawl (one project adds 30 fields) slows entire site, hits 200-field issue-view cap.
- JQL `WAS` queries on transition history are slow and time-out above ~10k issues.
- Permission scheme + issue security + project role tri-layer is a frequent foot-gun.
- ScriptRunner/Forge automations create cross-tool dependency that's hard to test.

## Agentic workflow
A `workflow-author` reads a process description (DoD, RACI, gates) and generates workflow JSON: statuses, transitions, validators, post-functions. A `scheme-applier` deploys it to a sandbox project, runs validation issues through it, and reports failures. An `automation-author` writes Jira Automation rules from natural-language requests ("when bug priority becomes blocker, page on-call"). A `jql-builder` translates user questions into validated JQL. Human reviews the rule diff before promote-to-prod.

### Recommended subagents
- `workflow-author` (sonnet) — generates workflow XML/JSON from process description.
- `automation-author` (sonnet) — writes Jira Automation rules in YAML from intent.
- `jql-builder` (haiku) — translates user questions into JQL with `validateQuery=strict`.
- `migration-mapper` (sonnet) — maps source-tool fields/states to Jira target schema.
- `scheme-doctor` (sonnet) — audits issue type, workflow, screen, permission schemes for drift.
- `bulk-transition-runner` (haiku) — drives bulk JQL+transition with rate-limit safety.

### Prompt pattern
```
You are workflow-author. Given process {dod_yaml} for issue type {type},
emit Jira Cloud workflow JSON with statuses, transitions, validators
(required fields per transition), and post-functions. Constraint: ≤ 7
statuses, every transition has a screen, no global transitions to "Done".
```

```
You are jql-builder. Translate "{question}" into JQL using fields {schema}.
Validate via Jira REST `/search?validateQuery=strict`. If invalid, propose
fix. Return { "jql": "...", "explanation": "...", "sample_count": N }.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `jira` (ankitpokhrel) | Query, create, transition issues from terminal | https://github.com/ankitpokhrel/jira-cli |
| `acli` (Atlassian) | Atlassian official CLI for Cloud admin | https://developer.atlassian.com/cloud/acli/ |
| `go-jira` | Scriptable Go CLI | https://github.com/go-jira/jira |
| `jirashell` (Python) | Interactive shell on top of jira-python | `pip install jira` |
| `acli jira workflow` | Workflow import/export via Cloud admin | Atlassian docs |
| `gh` + `jira-github-action` | PR ↔ issue linking | GitHub Marketplace |
| `node-jira-client` | Node integration | `npm i jira-client` |
| `pre-commit` + JQL lint | Validate JQL files in repo before merge | https://pre-commit.com |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Jira Cloud | SaaS | REST v3 + GraphQL alpha; OAuth 2.0 (3LO) or API token | Best agent target. |
| Jira Data Center | Self-host | REST + Java plugins; on-prem auth | Different API surface. |
| Jira Service Management | SaaS | REST | ITIL-flavored, request portal API. |
| Jira Automation | SaaS | REST | Rule import/export, rate-limited. |
| ScriptRunner | SaaS app | Partial | Groovy scripts; code-review pain. |
| Tempo Timesheets | SaaS app | REST | Worklogs API. |
| Atlassian Forge | Platform | REST | Custom apps inside Jira; JS runtime. |
| Trello (Atlassian) | SaaS | REST | Lighter cousin if Jira too heavy. |
| Atlassian Marketplace apps | SaaS | varies | Each adds its own automation/permissions; audit before install. |

## Templates & scripts
README ships sprint plan, DoD, custom-field config, JQL examples. Inline below: bulk transition with rate-limit safety.

```python
#!/usr/bin/env python3
"""bulk_jql_transition.py — drive bulk transitions with rate-limit safety."""
from __future__ import annotations
import os, time, sys
import requests

S = requests.Session()
S.auth = (os.environ["JIRA_USER"], os.environ["JIRA_TOKEN"])
BASE = os.environ["JIRA_BASE"].rstrip("/")

def transition(key: str, tid: str) -> None:
    r = S.post(f"{BASE}/rest/api/3/issue/{key}/transitions",
               json={"transition": {"id": tid}})
    if r.status_code == 429:
        time.sleep(int(r.headers.get("Retry-After", 5)))
        return transition(key, tid)
    r.raise_for_status()

def main() -> int:
    jql = sys.argv[1]
    tid = sys.argv[2]
    start_at = 0
    while True:
        r = S.get(f"{BASE}/rest/api/3/search",
                  params={"jql": jql, "fields": "key", "startAt": start_at, "maxResults": 100})
        r.raise_for_status()
        data = r.json()
        for it in data["issues"]:
            transition(it["key"], tid)
            time.sleep(0.2)  # ≤ 5 req/s
        start_at += len(data["issues"])
        if start_at >= data["total"]:
            return 0

if __name__ == "__main__":
    sys.exit(main())
```

## Best practices
- One workflow per issue type at first; resist bespoke per-project workflows.
- Required fields on transitions, not on creation — lowers friction for bulk imports.
- Automation rules: test in a sandbox project with a copy of prod schemes before promoting.
- Tag every automation-created issue with a label (`automation`) for audit.
- Limit custom fields aggressively; share via Global context, not project-scoped.
- Lock workflows after first month; further edits via PR-style proposal in Confluence.
- Smart commits: link branches via `PROJ-123 #fix-version`.
- Migrations: dry-import on a clone site first; never iterate on prod.
- Statuses ≤ 7; every transition has a screen with relevant required fields.
- Use scoped issue types (Epic, Story, Task, Bug, Sub-task) — resist creating new ones for every workflow nuance.

## AI-agent gotchas
- `validateQuery=strict` catches most JQL hallucinations; do not skip.
- LLMs invent field names; cache `/rest/api/3/field` and provide schema in system prompt.
- Rate limits (Cloud: ~50 req/s per site; automation: per-tier monthly budget) require backoff with `Retry-After`.
- Permission errors return 200 with empty issue lists in some endpoints — always check the count.
- Webhook signatures rotate on app reinstall; agents listening must handle rotation.
- Bulk transitions can fan out and breach rate quotas in seconds; throttle to ≤ 5 req/s.
- ADF (Atlassian Document Format) ≠ Markdown; agents writing Markdown produce empty fields. Use ADF conversion.
- Service account that creates issues becomes the reporter; downstream notifications fan out — use a bot user with notifications disabled.
- Automation rule loops are easy (rule A triggers rule B triggers A); add cycle guards.
- Issue security level + project permission tri-layer: an agent reading via REST may see fewer issues than the dashboard suggests.
- Cloud vs DC API drift: code working on one frequently fails on the other; pin the deployment in agent config.
- Human-in-the-loop checkpoints (mandatory): workflow promotion, automation rule promotion, schema changes, bulk transitions.

## References
- Jira REST v3 — https://developer.atlassian.com/cloud/jira/platform/rest/v3/
- JQL reference — https://support.atlassian.com/jira-software-cloud/docs/jql-fields/
- Jira Automation library — https://www.atlassian.com/software/jira/guides/automation
- ADF spec — https://developer.atlassian.com/cloud/jira/platform/apis/document/structure/
- Forge platform — https://developer.atlassian.com/platform/forge/
- Sibling methodologies: `scrum-ceremonies/`, `gitlab-boards/`, `azure-devops-boards/`, `pm-tools-overview/`.
