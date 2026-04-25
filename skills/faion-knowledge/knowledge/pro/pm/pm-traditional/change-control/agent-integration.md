# Agent Integration — Change Control

## When to use
- Fixed-bid / fixed-scope contracts where every CR has billing implications.
- Multi-stakeholder programs with a Change Control Board (CCB) and tiered authority.
- Regulated work (medical, finance, gov) where audit trail of approved changes is mandatory.
- Any project where scope creep has cost > 15% of original budget on prior runs.

## When NOT to use
- Pure agile sprints with empowered Product Owner — backlog re-ordering replaces CR ceremony.
- Internal tools / R&D where changes ARE the work.
- Solo projects (apply lightweight `CHANGES.md` instead of full register).
- Phases before scope baseline is signed off — there is nothing to "change" yet.

## Where it fails / limitations
- Process becomes theatre when the CCB rubber-stamps everything (no real bar).
- "Minor" change thresholds drift upward over time; six small CRs can equal one major.
- Slows urgent fixes in incident situations — needs an emergency-CR fast lane.
- Hidden changes (dev-driven refactors that change behavior) bypass the register entirely.
- Impact analysis quality varies wildly when done by the same person who wrote the request.

## Agentic workflow
A subagent is well-suited to: ingest free-form change requests (Slack, email), normalize into CR records, perform first-pass impact analysis (scope/schedule/cost) by reading WBS + schedule, draft CCB-ready summaries, and log decisions back to the register. Humans retain decision authority and the budget veto. Run the agent on a per-CR trigger (issue created, email forwarded) plus a weekly "stale CRs" sweep.

### Recommended subagents
- `faion-pm-agent` — owns CR lifecycle, drafts impact analyses, updates the register.
- `faion-business-analyst` agent (per skill router) — strong for impact analysis on scope and requirements traceability.
- `faion-sdd-execution` reviewer — gate that flags PRs whose diff implies an undeclared scope change.

### Prompt pattern
```
Convert this raw request into a CR record (JSON):
{cr_id, requester, date, description, business_justification, urgency,
 impact: {scope, schedule_days, cost_usd, quality, risk, resources},
 options: [{name, days, cost, recommendation}],
 decision_required_from: pm|sponsor|ccb}
Cite WBS IDs touched. Flag missing info as needs_clarification[].
```

```
Review last 7 days of merged PRs vs current scope baseline (WBS).
Output undeclared-change candidates: PR#, files, suspected scope delta,
suggested CR template entry. Do not auto-create CRs.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `gh` CLI | CRs as labelled issues + PR-linked decisions | https://cli.github.com |
| `jira-cli` | CR custom issue type with workflow states | https://github.com/ankitpokhrel/jira-cli |
| `glab` | GitLab equivalent for repo-coupled CRs | https://gitlab.com/gitlab-org/cli |
| `dsq` / `csvkit` | Query CSV/Markdown change-register tables | https://github.com/multiprocessio/dsq |
| `pandoc` | Render CR forms to PDF for client signoff | https://pandoc.org |
| `git log --shortstat` | Detect undeclared scope drift between baselines | git docs |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Jira (with custom CR issue type) | SaaS | Yes — REST + JQL | Most common; CCB transitions modeled as workflow states. |
| ServiceNow Change Management | Enterprise SaaS | Yes — REST API | Heavy ITIL flavor; overkill outside ops. |
| Smartsheet Change Log | SaaS | Yes — REST API | Good for client-facing PMOs needing audit. |
| Confluence + Jira | SaaS | Yes — REST API | CR form in Confluence, decision in Jira. |
| GitHub Issues + labels (`change-request`, `ccb-pending`) | SaaS | Yes — GitHub API | Cheapest for SDD repos. |
| Linear | SaaS | Yes — GraphQL API | Light but lacks formal CCB workflow. |
| Notion CR database | SaaS | Yes — REST API | Easy human view + agent sync. |

## Templates & scripts
See `templates.md` for the CR form and register table. Helper to compute aggregate scope drift across approved CRs:

```bash
#!/usr/bin/env bash
# cr-drift.sh — sum schedule/cost from approved CRs in a Markdown register.
set -euo pipefail
file="${1:-CHANGE-REGISTER.md}"
awk -F'|' '
  /Approved/ {
    days = $7; gsub(/[^0-9.]/,"",days)
    cost = $7; gsub(/[^0-9.]/,"",cost)  # adjust column index per template
    d += days; c += cost; n++
  }
  END { printf "approved_crs=%d total_days=%.1f total_cost=%.0f\n", n, d, c }
' "$file"
```

## Best practices
- Define decision-authority thresholds in writing at kickoff and post them on the project wall.
- Track rejected CRs with reason codes — the same request returning three times is a real signal.
- Bundle small CRs into a weekly "minor changes" approval to keep cadence without ceremony.
- Always include a "do nothing" option in the impact analysis — forces explicit cost-of-change reasoning.
- Tie every approved CR to a baseline update commit (WBS, schedule, budget) so artefacts stay in sync.
- For agile-hybrid: any backlog item that consumes contingency or shifts release date IS a CR.

## AI-agent gotchas
- LLM-drafted impact analyses underestimate testing/regression effort — require the agent to surface a "test impact" line item explicitly.
- Don't let the agent transition CRs to "Approved" — only humans with named authority approve.
- Agents that read CR descriptions written in user voice often miss implicit dependencies; pair with a WBS-aware second pass.
- Beware double-counting: a single CR touching three WBS branches must not triple-add to the register.
- Token budget: load only the open CRs and the current scope baseline — full historical register is wasteful.
- Human-in-loop checkpoints: (1) impact-analysis review before CCB, (2) decision logging, (3) baseline-document update PR.

## References
- PMI, *PMBOK Guide* 7th ed., Delivery Performance Domain — Change Management.
- ISO/IEC 20000-1:2018 — Change Management process.
- ITIL 4 — Change Enablement practice.
- A. Cockburn, *Agile Software Development* — on the cost of late-stage change.
