# Agent Integration — Jira Workflow Management

## When to use
- Bootstrapping a new Jira project for Scrum/Kanban/JSM team
- Standardizing 3+ inconsistent project workflows after acquisition or reorg
- Replacing manual triage / assignment with automation rules
- Wiring Jira into CI/CD (auto-transition on deploy, link to PR)
- Migrating from Jira Server/DC to Cloud (workflow + scheme rebuild)

## When NOT to use
- Team < 5 with simple Trello-grade needs — Jira ROI inverts
- Throwaway 2-week prototype — workflow tax exceeds value
- When the goal is "make Jira look like Linear" — replace Jira instead
- Pure documentation projects — use Confluence, not Jira

## Where it fails / limitations
- Workflow editor is shared across projects via schemes; one project's change can break others
- Jira Cloud differs from Server/DC in API, automation engine, and permissions — code does not always port
- Automation library has rate limits (Cloud: rule executions/month per tier) that hit at scale
- "Required" field validators block bulk imports and bot-driven flows unless service accounts exempt
- Custom field sprawl (one project adds 30 fields) slows entire site, hits 200-field issue-view cap
- JQL `WAS` queries on transition history are slow and timeout above ~10k issues
- Permission scheme + issue security + project role tri-layer is a frequent foot-gun

## Agentic workflow
A workflow-author subagent reads a process description (DoD, RACI, gates) and generates a workflow JSON: statuses, transitions, validators, post-functions. A scheme-applier deploys it via REST API to a sandbox project, runs validation issues through it, and reports failures. An automation-author writes Jira Automation rules from natural-language requests ("when bug priority becomes blocker, page on-call"). Human reviews the rule diff before promote-to-prod. Pair with `code-review` skill for the YAML.

### Recommended subagents
- `workflow-author` — generates workflow XML/JSON from process description
- `automation-author` — writes Jira Automation rules in YAML from intent
- `jql-builder` — translates user questions into JQL with validation
- `migration-mapper` — maps source-tool fields/states to Jira target schema
- `scheme-doctor` — audits issue type, workflow, screen, permission schemes for drift

### Prompt pattern
```
You are a workflow-author. Given process {dod_yaml} for issue type {type},
emit Jira Cloud workflow JSON with statuses, transitions, validators
(required fields per transition), and post-functions. Constraint: ≤ 7
statuses, every transition has a screen, no global transitions to "Done".
```

```
You are a jql-builder. Translate "{question}" into JQL using fields {schema}.
Validate via Jira REST `/search?validateQuery=strict`. If invalid, propose
fix. Return {jql, explanation, sample_count}.
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

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Jira Cloud | SaaS | Yes | REST v3 + GraphQL alpha; OAuth 2.0 (3LO) or API token |
| Jira Data Center | Self-host | Yes | REST + Java plugins; on-prem auth |
| Jira Service Management | SaaS | Yes | ITIL-flavored, request portal API |
| Jira Automation | SaaS | Yes | Rule import/export via REST, rate-limited |
| ScriptRunner | SaaS app | Partial | Groovy scripts, code-review headache |
| Tempo Timesheets | SaaS app | Yes | Worklogs API |
| Atlassian Forge | Platform | Yes | Custom apps run inside Jira, JS runtime |
| Trello (Atlassian) | SaaS | Yes | Lighter cousin if Jira too heavy |

## Templates & scripts
See templates.md for sprint plan, DoD checklist. Inline workflow apply:

```bash
#!/usr/bin/env bash
# apply-workflow.sh — push workflow JSON to a sandbox project
set -euo pipefail
: "${JIRA_BASE:?}"; : "${JIRA_USER:?}"; : "${JIRA_TOKEN:?}"
PROJECT_KEY="${1:?usage: apply-workflow.sh <PROJECT_KEY> <workflow.json>}"
WF="${2:?}"
curl -fsSL -u "$JIRA_USER:$JIRA_TOKEN" \
  -H "Content-Type: application/json" \
  -X POST "$JIRA_BASE/rest/api/3/workflows/create" \
  -d @"$WF" | jq '.id'
echo "Associate with $PROJECT_KEY scheme via UI or scheme API."
```

```python
# bulk-jql-update.py — drive bulk transitions with rate-limit safety
import os, time, requests
S = requests.Session()
S.auth = (os.environ["JIRA_USER"], os.environ["JIRA_TOKEN"])
BASE = os.environ["JIRA_BASE"]
JQL = 'project = ABC AND status = "Awaiting QA" AND updated < -7d'
def transition(key, tid):
    r = S.post(f"{BASE}/rest/api/3/issue/{key}/transitions",
               json={"transition": {"id": tid}})
    if r.status_code == 429:
        time.sleep(int(r.headers.get("Retry-After", 5)))
        return transition(key, tid)
    r.raise_for_status()
issues = S.get(f"{BASE}/rest/api/3/search", params={"jql": JQL, "fields": "key"}).json()
for it in issues["issues"]:
    transition(it["key"], "31")  # transition id for "Reopen"
    time.sleep(0.2)
```

## Best practices
- Use one workflow per issue type at first; resist bespoke per-project workflows
- Required fields on transitions, not on creation — lowers friction for bulk imports
- Automation rules: test in a sandbox project with a copy of prod schemes before promoting
- Tag every automation-created issue with a label (`automation`) for audit
- Limit custom fields aggressively; share via Global context not project-scoped where possible
- Lock workflows after first month; further edits via PR-style proposal in Confluence
- Link branches to issues via smart commits (`PROJ-123 #fix-version`) — agents can drive this consistently
- For migrations, run a dry import on a clone site first; never iterate on prod

## AI-agent gotchas
- `validateQuery=strict` catches most JQL hallucinations; do not skip it
- LLMs invent field names; cache `/rest/api/3/field` and provide schema in system prompt
- Rate limits (Cloud: ~50 req/sec/site, automation: per-tier monthly budget) require backoff with `Retry-After`
- Permission errors return 200 with empty issue lists in some endpoints — always check the count
- Webhook signatures rotate on app reinstall; agents listening to webhooks need rotation handling
- Bulk transitions can fan out and breach rate quotas in seconds; throttle to ≤ 5 req/sec
- ADF (Atlassian Document Format) for descriptions ≠ Markdown; agents writing Markdown will produce empty fields. Use the conversion utility
- Service account that creates issues becomes the reporter; downstream notifications fan out — use bot user with notifications disabled
- Automation rule loops are easy to create (rule A triggers rule B triggers A); add cycle guards

## References
- Jira REST v3: https://developer.atlassian.com/cloud/jira/platform/rest/v3/
- JQL reference: https://support.atlassian.com/jira-software-cloud/docs/jql-fields/
- Jira Automation library: https://www.atlassian.com/software/jira/guides/automation
- ADF spec: https://developer.atlassian.com/cloud/jira/platform/apis/document/structure/
- Forge platform: https://developer.atlassian.com/platform/forge/
