# Agent Integration — Linear Issue Tracking

## When to use
- Engineering teams that ship software continuously and need fast, keyboard-first issue management with no config overhead.
- When you want native bidirectional GitHub/GitLab PR sync so issue status moves automatically on branch events.
- Solopreneur or small team (2–15 engineers) that wants velocity tracking without a Jira admin role.
- When cycle (sprint) planning, triage, and backlog grooming all need to be automatable via API.
- When you need typed GraphQL queries from agents to build custom reporting without a BI tool.

## When NOT to use
- Non-technical teams (marketing, ops, HR) — Linear's opinionated dev-centric UX is unfamiliar and unwelcoming to non-engineers.
- Projects requiring custom issue types with deeply nested hierarchical structures — Linear's hierarchy (team → project → cycle → issue → sub-issue) is fixed.
- Enterprise environments that mandate SSO, audit logs per field change, or on-premise hosting — Linear is SaaS-only.
- Teams that need time tracking, billable hours, or resource capacity planning built into the PM tool.

## Where it fails / limitations
- Linear GraphQL API has usage limits (complexity budget per query); deeply nested queries with many relations hit limits and return partial results.
- Webhooks are HTTPS push only — agents must expose a public endpoint or use a relay (ngrok, Cloudflare Tunnel) to receive events in local dev.
- Cycle (sprint) velocity data is not directly queryable via API in raw form; it must be computed by querying completed issues per cycle.
- No native file attachment API — files must be uploaded elsewhere and linked as URLs in issue descriptions.
- Triage state is team-specific; cross-team triage workflows require separate automation logic per team.
- Sub-issues cannot have their own cycles — they inherit parent issue's cycle assignment.

## Agentic workflow
A Claude subagent can drive the full Linear PM cycle: query the current cycle's issues via GraphQL, identify items with no assignee or no estimate, post a comment requesting clarification, and reassign or re-estimate based on team capacity rules. For PR-driven workflows, the agent can listen to Linear webhooks (issue transitioned to "In Review"), cross-check GitHub PR status via the GitHub API, and surface discrepancies as comments. Triage can be fully automated: agent reads new issues from the Triage inbox, applies labels and priority based on keyword rules, and moves them to backlog.

### Recommended subagents
- `linear-triage-agent` — reads inbox issues, applies priority/label heuristics, moves triaged items to backlog with a comment summary.
- `linear-cycle-reporter` — queries closed cycles via GraphQL, computes velocity, completion rate, and outputs a markdown sprint report.
- `linear-pr-sync-agent` — listens to Linear webhooks, fetches matching GitHub PRs, and updates Linear issue status or comments on discrepancy.

### Prompt pattern
```
Query Linear GraphQL for all issues in the current cycle where status is Backlog or Todo and assignee is null.
For each: return {id, title, priority, estimate}.
Do not create or modify any issues; read only.
```

```
Given this Linear issue JSON: <issue_json>
Write a one-paragraph triage comment that:
1. Confirms priority based on keywords in title/description.
2. Suggests the correct team label (Bug / Feature / Improvement).
3. Asks for estimate if missing.
Post the comment via the Linear createComment mutation.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `linear-cli` (unofficial) | Create/list/update issues from terminal | `npm install -g @linear/sdk` then custom scripts; docs: https://developers.linear.app/docs/sdk/getting-started |
| `gh` (GitHub CLI) | Cross-reference Linear issues with linked PRs | `brew install gh` / OS package manager |
| `curl` + `jq` | Ad-hoc GraphQL queries against Linear API | OS package manager |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Linear API (GraphQL) | SaaS | Yes | Full CRUD, webhook support, complexity-budgeted queries. |
| GitHub / GitLab | SaaS | Yes | Native Linear integration; PR status syncs issue state automatically. |
| Slack (Linear app) | SaaS | Partial | Notifications only; cannot create/update Linear issues from Slack without a bot. |
| n8n | OSS/SaaS | Yes | Linear trigger node + HTTP node for custom GraphQL; self-hostable. |
| Zapier | SaaS | Partial | Linear trigger/action available; limited to simple field mappings. |
| Linear SDK (JS/TS) | OSS | Yes | Official typed SDK; best for agent scripts in Node. https://github.com/linear/linear |

## Templates & scripts
See `templates.md` for issue templates and cycle goal templates.

Minimal Node.js snippet to fetch current-cycle issues:
```javascript
import { LinearClient } from "@linear/sdk";

const client = new LinearClient({ apiKey: process.env.LINEAR_API_KEY });

async function currentCycleIssues(teamKey) {
  const team = await client.team(teamKey);
  const activeCycle = await team.activeCycle;
  if (!activeCycle) return [];

  const issues = await activeCycle.issues({
    filter: { state: { name: { nin: ["Done", "Canceled"] } } },
  });
  return issues.nodes.map((i) => ({
    id: i.identifier,
    title: i.title,
    priority: i.priority,
    assignee: i.assignee?.name ?? "unassigned",
  }));
}

currentCycleIssues("BAK").then(console.log);
```

## Best practices
- Use a single Linear workspace per product, with teams mapped to engineering domains (Backend, Frontend, Infra) — avoid per-project workspaces, which fragment velocity data.
- Enforce issue templates via Linear's native template feature so agents parsing issue bodies can rely on consistent headings (Context, Acceptance Criteria, etc.).
- Link every PR to a Linear issue using `Fixes LINEAR-123` in the PR description — this activates automatic status transitions without any agent intervention.
- When querying via GraphQL, request only the fields you need; over-fetching consumes complexity budget and slows responses.
- Archive rather than delete issues — deleted issues are excluded from velocity history, corrupting cycle analytics.
- Set up Linear's built-in SLA alerts (Priority + age) before building custom agent triage — the native feature covers 80% of cases without code.

## AI-agent gotchas
- Linear's GraphQL complexity limit (~1000 complexity units per query) means fetching all issues + all fields + all relations in one query will fail; paginate with `first: 50` and `after: cursor`.
- Webhooks are signed with HMAC-SHA256 — agents must verify the signature or accept spoofed events; do not skip signature validation.
- The `assignee` field returns `null` for unassigned issues, not an empty string — agents must handle null explicitly.
- Cycle auto-archive: when a cycle ends, Linear auto-archives incomplete issues unless configured otherwise; agents that read "current cycle" may get zero results if the cycle just closed.
- Priority is an integer (0=No priority, 1=Urgent, 2=High, 3=Medium, 4=Low) in the API, not a string — agents that output strings must map back to integers before writing.
- Human checkpoint required before bulk issue reassignment or bulk cycle changes — Linear has no undo for API-driven bulk mutations.

## References
- https://developers.linear.app/docs — Official API and SDK docs
- https://linear.app/method — Linear's PM philosophy (useful for prompt context)
- https://developers.linear.app/docs/graphql/working-with-the-graphql-api — GraphQL guide
- https://github.com/linear/linear — Official Linear SDK (JS/TS)
- https://developers.linear.app/docs/webhooks — Webhook setup and signature verification
