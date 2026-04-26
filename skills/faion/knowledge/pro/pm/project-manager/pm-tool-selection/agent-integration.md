# Agent Integration — PM Tool Selection

## When to use
- New team picking first PM tool, or current tool causing friction (Jira slowness, Notion losing PM context)
- Vendor renewal cycle where price jump triggers re-eval (e.g., Jira Premium upcharge, ClickUp seat growth)
- Post-acquisition consolidation across two tool stacks
- Compliance shift (SOC2, HIPAA, EU data residency) forcing reassessment

## When NOT to use
- Team < 5 people with simple workflow — pick GitHub Projects or Linear free, skip the matrix
- Mid-project under deadline pressure — switching tools mid-flight burns more than it saves
- Single-issue gripe ("velocity report is ugly") — fix the report, do not migrate
- Decision already made by leadership — running theater POC erodes trust

## Where it fails / limitations
- Weighted scorecards become rationalization theater when leadership has pre-decided
- POC participants self-select toward novelty (Linear) over depth (Jira), skewing scores
- TCO models miss switching cost: lost automations, broken integrations, retrained reflexes
- Vendor sales engineers tune the POC environment; production behavior diverges
- Long-tail integrations (custom Jira plugins, Asana reporting) only surface 3-6 months in

## Agentic workflow
A subagent runs the requirements gathering by interviewing each role async (Slack thread or doc), normalizes responses into a MoSCoW matrix, and pulls live pricing/feature data via vendor APIs and G2/Capterra scraping. A second pass scores tools against weighted criteria and drafts the ADR. Human-in-loop is mandatory at three points: requirements sign-off, POC scoring, and final ADR approval — agents must not pick the tool unilaterally.

### Recommended subagents
- `requirements-gatherer` — runs structured interview templates, extracts must/should/nice into YAML
- `vendor-researcher` — pulls feature matrices, pricing, SOC2/GDPR posture from vendor docs + G2
- `tco-modeler` — builds 3-year TCO with license, implementation, training, hidden costs
- `adr-drafter` — produces ADR-005 style decision record with evaluation summary

### Prompt pattern
```
You are a vendor-researcher subagent. For each tool in {tools}, fetch:
- Current pricing tiers (per-user, per-month, annual discount)
- SSO/SAML availability per tier
- Native integrations with {required_integrations}
- API rate limits and auth model
Return JSON conforming to schema {pm_tool_profile.json}. Cite source URL per field.
```

```
Score each tool against criteria {criteria_yaml}. Use weighted formula. Flag any
score where source data is older than 90 days or marked "vendor-supplied".
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `jira` (Atlassian CLI) | Query Jira via JQL, export issues | https://github.com/ankitpokhrel/jira-cli |
| `linear-cli` | Linear issue CRUD, workflow inspect | `npm i -g @linear/cli` |
| `gh` | GitHub Projects v2 via GraphQL | https://cli.github.com |
| `glab` | GitLab issues, boards, milestones | https://gitlab.com/gitlab-org/cli |
| `clickup-cli` (community) | ClickUp tasks, lists, spaces | npm packages, varies by maintainer |
| `notion-cli` (unofficial) | Notion DB query/update | Multiple Go/Python wrappers |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Jira Cloud | SaaS | Yes | REST v3 + JQL, mature, rate-limited per tenant |
| Linear | SaaS | Yes | GraphQL API, webhooks, fast, opinionated schema |
| ClickUp | SaaS | Partial | REST API exists but quirky pagination, custom fields fragile |
| Notion | SaaS | Partial | API does not expose all UI features (timeline, formulas limited) |
| GitHub Projects v2 | SaaS | Yes | GraphQL only, no REST; tightly coupled to issues/PRs |
| GitLab | SaaS/OSS | Yes | REST + GraphQL, self-host option, full DevOps loop |
| Azure DevOps | SaaS | Yes | REST API, Azure AD auth, enterprise-strong |
| OpenProject | OSS | Yes | Self-hostable, REST API, Gantt + WBS native |
| Plane | OSS | Yes | Self-hostable Linear alternative, Python API |
| Taiga | OSS | Yes | Scrum/Kanban, REST API, Python backend |

## Templates & scripts
See templates.md for the requirements doc and ADR. Inline pricing-fetch sketch:

```bash
#!/usr/bin/env bash
# fetch-pm-pricing.sh — snapshot pricing pages for diff-review
set -euo pipefail
DEST="$(date -u +%Y-%m-%d)/pricing"
mkdir -p "$DEST"
declare -A URLS=(
  [jira]="https://www.atlassian.com/software/jira/pricing"
  [linear]="https://linear.app/pricing"
  [clickup]="https://clickup.com/pricing"
  [notion]="https://www.notion.so/pricing"
  [asana]="https://asana.com/pricing"
  [monday]="https://monday.com/pricing"
)
for tool in "${!URLS[@]}"; do
  curl -sSL --max-time 30 "${URLS[$tool]}" -o "$DEST/${tool}.html"
  echo "captured $tool"
done
git add "$DEST" && git commit -m "snapshot: PM pricing $(date -u +%F)"
```

## Best practices
- Score before POC, then re-score after — variance reveals which criteria were assumed wrong
- Run POC on a real epic with 8-15 issues, not toy tickets — toy data flatters every tool
- Force one criterion to "deal-breaker" status (e.g., "no SAML = out") to break tied scores
- Interview the admin/PMO, not just power users — admins see the migration cost
- Ask vendors for their churn-back rate (customers who came from a competitor) — Linear and ClickUp will share, Jira will not
- Test exit: run a full data export on day 3 of the POC and inspect the dump
- Pricing: always negotiate annual + multi-year, ask for "engineering discount" or "open-source-friendly" rate

## AI-agent gotchas
- LLMs hallucinate vendor features confidently — gate every feature claim on a citation, fail closed if no URL
- Pricing pages change quietly; cache + diff weekly, do not trust last month's research
- "Mobile app score: 8" without using the app on a real device is fiction — outsource to a human
- POC scorecard suffers from the agent flattering the user's apparent preference; randomize tool order in prompts
- ADR drafting agents tend toward Linear (training data bias from devtwitter); force the agent to argue the loser's case before the final write-up
- Do not let an agent commit to a multi-year contract decision; the irreversibility tier requires human sign-off

## References
- Atlassian REST v3: https://developer.atlassian.com/cloud/jira/platform/rest/v3/
- Linear GraphQL: https://developers.linear.app
- GitHub Projects v2 GraphQL: https://docs.github.com/en/graphql/reference/objects#projectv2
- Gartner Magic Quadrant for Adaptive Project Management: https://www.gartner.com
- G2 PM category: https://www.g2.com/categories/project-management
