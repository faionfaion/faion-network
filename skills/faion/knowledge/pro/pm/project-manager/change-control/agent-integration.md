# Agent Integration — Change Control

## When to use
- Fixed-scope, fixed-budget engagements (agency contracts, SoWs) where every change has billing impact.
- Regulated environments (finance, healthcare, gov) requiring audit trail of decisions.
- Projects where multiple stakeholders submit asks via different channels — register forces one queue.
- Late-stage projects (>50% complete) where every change has compounded ripple effects.
- Programs/portfolios where one project's change affects others.

## When NOT to use
- Pure agile teams with continuous backlog refinement — change is the default state, not the exception. Use sprint planning instead.
- Discovery/research phases — you want changes; controlling them defeats the purpose.
- Solo projects where you are both requester and approver — capture as a TODO, not a CR.

## Where it fails / limitations
- Bureaucracy traps: 2-week CCB cadence kills small valuable changes; tier the process by size (PM-approved minor / sponsor-approved medium / CCB-approved major).
- Requesters route around the process if it's slow — "informal asks" reappear as scope creep.
- Impact analysis is often a guess; estimate quality matches estimating quality (low for new tech).
- Rejected requests rarely die — they re-submit under a new title; track rejection reasons to detect repeats.
- "No" culture damage: too many rejections push real value out of scope; distinguish prevent-creep from prevent-improvement.

## Agentic workflow
A subagent intercepts informal change asks (Slack, email), drafts a Change Request with required fields, runs impact analysis against scope/schedule/budget/risk, and routes to the correct decision tier. The agent never auto-approves — it only prepares a packet for the human approver. Maintain the change register as data (CSV/YAML); the Markdown is a generated view. Close the loop: when an approved CR is implemented, the agent updates WBS, schedule, budget baselines simultaneously to keep them in sync.

### Recommended subagents
- `faion-pm-agent` — drafts CRs, runs impact analysis, maintains register.
- `faion-business-analyst` — refines requirements affected by the change.
- `faion-sdd-executor-agent` — opens new SDD tasks for approved CRs.
- `faion-improver` — periodic audit: rejection-rate trend, repeat-CR detection.

### Prompt pattern
```
Input: ask_text, current_scope.md, schedule.csv, budget.yaml, risk_register.yaml
Output: change_request.md with sections {Description, Justification,
Impact{scope, schedule, cost, quality, risk, resources}, Options, Routing}.
Routing rule: <1d & <$500 → PM; <5d & <$5K → Sponsor; else → CCB.
```

```
Compare CR-{id} description vs last 90 days of rejected CRs.
Flag near-duplicates with similarity > 0.7 and list reasons for prior rejection.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `gh` (GitHub CLI) | CRs as GitHub Issues with labels (CR/scope/cost/schedule) | https://cli.github.com |
| `glab` (GitLab CLI) | Same for GitLab Issues | https://gitlab.com/gitlab-org/cli |
| `jira` (jira-cli) | CRs as Jira issue type | https://github.com/ankitpokhrel/jira-cli |
| `yq`, `jq` | Process register YAML/JSON | yq.dev / stedolan.github.io/jq |
| `pandoc` | Render CRs to PDF for sponsor sign-off | https://pandoc.org |
| `gitpython` | Auto-link CR to commits implementing it | https://github.com/gitpython-developers/GitPython |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Jira (Change Mgmt template) | SaaS | Yes — REST API | Built-in workflow; ITIL-aligned |
| ServiceNow Change Management | SaaS | Yes — Table API | ITIL/CAB workflow, audit-ready |
| Atlassian Confluence | SaaS | Yes — REST API | Host change register pages |
| GitHub / GitLab Issues | SaaS | Yes — REST + GraphQL | CRs as labelled issues, link to PRs |
| Smartsheet | SaaS | Yes — REST API | Common in PMOs for change log |
| BMC Helix Remilon | SaaS | Yes — REST API | Heavy ITIL change |
| Notion / Airtable | SaaS | Yes — REST API | Lightweight register |
| DocuSign | SaaS | Yes — REST API | Electronic sign-off on major CRs |

## Templates & scripts
See `templates.md` for CR form and register layouts. Inline router (≤50 lines):

```python
# cr_router.py — assigns approval tier from impact estimates
import yaml, sys

TIERS = [
    {"name": "PM",      "max_days": 1,  "max_usd":  500},
    {"name": "Sponsor", "max_days": 5,  "max_usd": 5000},
    {"name": "CCB",     "max_days": None, "max_usd": None},
]

def route(cr):
    days = cr["impact"]["schedule_days"]
    cost = cr["impact"]["cost_usd"]
    risk = cr["impact"].get("risk", "low")
    if risk == "high":
        return "CCB"
    for t in TIERS:
        if t["max_days"] is None:
            return t["name"]
        if days <= t["max_days"] and cost <= t["max_usd"]:
            return t["name"]
    return "CCB"

if __name__ == "__main__":
    cr = yaml.safe_load(open(sys.argv[1]))
    print(f"{cr['id']}: route to {route(cr)}")
```

## Best practices
- Tier the process: minor (PM), medium (Sponsor), major (CCB) — speed is a feature.
- Every CR has Options (do, partial, defer, decline) so approvers see trade-offs, not a binary.
- Track rejected CRs forever; use them as evidence for descope discussions and to spot repeat asks.
- Keep CR data colocated with code repo; PR description references CR id; commit links back.
- Run impact analysis against current baselines (scope, schedule, budget) — not against original plan, which is stale.
- Set a CR rate metric: > 1 CR/week per million $ scope = symptom of poor initial scoping.
- Link CRs to risks: a CR that increases risk score above threshold needs CCB review even if cost is small.

## AI-agent gotchas
- LLMs underestimate ripple effects; require the impact analysis to walk specific WBS nodes by id, not handwave "schedule impact".
- Agents tend to recommend Option A (full implementation) — explicitly require ranking and a defer/decline option.
- Auto-closing implemented CRs without verifying baselines were updated leaves drift; include a checklist gate.
- Generated business justifications often paraphrase the request — useless. Force quoting metrics or stakeholder evidence.
- Beware "approval drift" via long Slack threads: the agent should refuse to mark a CR Approved without an explicit decision artefact (signed form, ticket transition, email sign-off).
- Never let the agent merge or rebase the CR-implementation branch without sponsor confirmation in the register.

## References
- PMBOK Guide 7th Edition — Delivery Performance Domain & Project Integration Management.
- ISO 21502 — Change control guidance.
- ITIL 4 — Change Enablement practice.
- PRINCE2 — Manage by Exception / Issue and Change Procedure.
- "Software Project Survival Guide" — Steve McConnell (Ch. on change control).
