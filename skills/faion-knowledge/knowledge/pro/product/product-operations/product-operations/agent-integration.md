# Agent Integration — Product Operations (Product Ops)

The methodology defines a dedicated Product Ops function whose job is to remove operational drag (process docs, tool plumbing, status updates, metric rollups, stakeholder comms) so PMs spend more time on discovery and strategy. For an agent stack this is a near-perfect fit: the work is repetitive, system-of-record-driven, and benefits from deterministic automation. The integration pattern below treats Product Ops as a set of long-running automations + on-demand subagents that read from PM tools (Jira/Linear/Productboard), write to dashboards, and post into Slack/Notion.

## When to use

- Solopreneur or small product team where a human Product Ops hire is not justified but the operational tax (status updates, roadmap snapshots, metric rollups) still needs to be paid weekly.
- Multi-product / multi-team setup where 3+ PMs work in different tools and someone has to reconcile artifact drift (different roadmap formats, different velocity definitions, different OKR templates).
- Migrating from ad-hoc PM workflows to a documented system: agents codify the templates, ceremonies and naming conventions instead of leaving them in a Notion page nobody reads.
- Pre-fundraise / board-prep cycles where a recurring "state of product" pack must be assembled from 5-10 sources on a fixed cadence.
- Org-wide release calendars, dependency maps, capacity planning across squads — work that needs aggregation across systems no single PM owns.

## When NOT to use

- A team with one PM and one product: the operational tax is too small; an agent flow adds maintenance overhead larger than it saves.
- During the first 30 days of a new product where workflows have not stabilised — automating an unstable process locks in the wrong shape.
- Strategic product decisions (pricing, positioning, kill/scale calls). Product Ops enables those decisions, it does not make them. Keep agents out of the decision seat.
- Heavily regulated environments (healthcare, fintech, defence) where every status update has compliance implications — manual review is the constraint, not throughput.
- When the PM tools used (Aha!, Productboard, Jira premium) have no public API tier the team can afford. No API → no agents, full stop.

## Where it fails / limitations

- **Source-of-truth fragmentation.** Roadmap in Productboard, sprint in Jira, OKRs in Lattice, retros in Notion. An agent that "centralises metrics" without a canonical schema produces a different set of numbers than the PMs see in their own tools, and trust collapses.
- **Role-clarity gap (the methodology's own top challenge).** Agents accelerate delivery but cannot resolve "who owns what." If the human Product Ops charter is undefined, automating it codifies confusion.
- **Status-update theatre.** AI-generated status updates that no one reads waste tokens and kill signal-to-noise. Tie every automated post to a named consumer, or do not generate it.
- **Predictive capacity planning is fragile.** "AI predicts sprint completion" only works on a stable team with 6+ months of clean ticket history. New squads, churn, scope volatility break the model — and bad predictions are worse than none.
- **Maturity-model jumps fail.** Skipping Level 1 (process docs) to Level 3 (AI automation) means you automate undocumented chaos. Agents must enforce maturity progression, not bypass it.
- **API rate limits at scale.** A "weekly portfolio rollup" across 20 squads in Jira hits rate limits fast; without caching + incremental sync the job times out.

## Agentic workflow

Treat Product Ops as three layers: (1) **scheduled scrapers** (cron / GitHub Actions) that pull state from PM/issue/analytics tools into a normalised store (Postgres or Notion DB); (2) **on-demand subagents** invoked by PMs or dashboards for specific asks (status pack, roadmap diff, capacity check, stakeholder summary); (3) **a narrow set of write-back automations** (Jira ticket creation, OKR doc updates, Slack digests). The orchestrator is a `faion-product-ops-agent` that reads the stored state and dispatches specialised subagents per request type. Every write must be reviewable in PR-style format before it lands in a system-of-record — agents propose, humans merge.

### Recommended subagents

- `faion-product-manager` — Domain owner for portfolio/lifecycle/release questions; consumes the normalised state Product Ops produces. Pair it with this methodology when a PM asks "what changed this week?"
- `faion-research-agent` — Use in `mode=competitors` or `mode=market` when Product Ops needs to refresh the competitive snapshot inside a board pack.
- `faion-sdd` / `faion-feature-executor` — Downstream consumers: when Product Ops detects a roadmap promise without a `spec.md`, it can spawn an SDD task to fill the gap.
- `faion-brainstorm` — Use diverge-converge cycles when designing a new ceremony, template, or KPI definition; Product Ops then ships the converged template into the org.
- `faion-improver` — Run Product Ops itself through a quarterly self-audit: which automations are still read, which dashboards are stale, which templates were never used.
- General `Task` subagent with the methodology's `llm-prompts.md` as system context — when no specialised agent exists yet, e.g. one-off "explain this 60-ticket epic to a non-technical exec."

### Prompt pattern

Weekly portfolio rollup (scheduled):

```
Pull from Linear: all teams, last 7 days. From Productboard: feature status changes. From PostHog: top-20 metrics deltas.
Produce ops-rollup-<YYYY-MM-DD>.md: 1) shipped this week, 2) at-risk (slip > 2 days), 3) blocked > 3 days, 4) metric movers > 10%.
Source-link every line. Skip empty sections — do not pad. Output to Notion DB id=<xxx>.
```

On-demand status pack:

```
Generate a stakeholder pack for <audience: board | exec | engineering>.
Audience=board → 1-page TL;DR + 3 risks + 3 wins + ask. Audience=exec → 1-pager + portfolio heatmap. Audience=engineering → release calendar + dependency graph.
Use only data from /ops-store/ updated within 48h. If older, write "stale, refresh" and stop.
```

Template enforcement on a new feature:

```
A new entry was created in roadmap. Verify it has: outcome statement, target metric, dependency list, owner, AC. Missing fields → comment on the entry with a checklist; do not auto-fill.
```

## CLI tools

| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `linear` (Linear CLI / `@linear/sdk`) | Pull issues, cycles, projects | `npm i -g @linear/sdk` |
| `jira-cli` (`ankitpokhrel/jira-cli`) | Pull/post Jira tickets, JQL queries | https://github.com/ankitpokhrel/jira-cli |
| `gh` | GitHub issues, releases, projects v2 (roadmaps backed by GH) | https://cli.github.com |
| `notion-cli` / `@notionhq/client` | Read/write Notion DBs (canonical store) | https://github.com/jorgeuh/notion-md / https://developers.notion.com |
| `productboard-api` (REST + Python wrappers) | Roadmap and feature state | https://developer.productboard.com |
| `posthog` CLI / SDK | Product analytics extraction | `pip install posthog` |
| `dbt` | Modelled metrics layer (canonical KPI defs) | https://docs.getdbt.com |
| `slack-cli` (`slackapi/slack-cli`) | Post digests, threaded comments | https://api.slack.com/automation/cli |
| `gcalcli` | Release calendar / ceremony scheduling | `pip install gcalcli` |
| `mermaid-cli` (`mmdc`) | Render dependency graphs / lifecycle diagrams in packs | `npm i -g @mermaid-js/mermaid-cli` |
| `sql-fluff` + Postgres client | Validate the canonical metrics SQL before publishing | `pip install sqlfluff` |

## Services & apps

| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Linear | SaaS | Yes — GraphQL + webhooks | First-choice issue tracker; clean API, fast |
| Jira (Cloud) | SaaS | Yes — REST v3, but rate-limited | Premium tier needed for advanced JQL + roadmaps |
| Productboard | SaaS | Yes — REST API | Source-of-truth for feature/roadmap intake |
| Aha! | SaaS | Yes — REST | Heavy on enterprise PMs; agent integrations are slower |
| Notion | SaaS | Yes — REST, DB-as-API | Best canonical store for narrative artifacts; keep numbers in SQL, prose in Notion |
| PostHog | OSS / SaaS | Yes — REST + SQL | Self-hostable, perfect for an agent's metrics layer |
| Amplitude / Mixpanel | SaaS | Yes — REST | Usage analytics; Amplitude has a query API |
| Lattice / 15Five | SaaS | Yes — REST | OKR + check-ins; pull progress for status packs |
| Slack | SaaS | Yes — Bolt SDK + Webhooks | Distribution channel for digests, do not store state here |
| Pendo | SaaS | Partially — REST, paid tier | Feature adoption; expensive but widely used in Product Ops |
| Mixpanel | SaaS | Yes — REST | Same role as Amplitude, usually one or the other |
| Productlane / Canny | SaaS | Yes — REST | Customer feedback intake; feeds Productboard or replaces it |
| n8n | OSS | Yes — native nodes for Slack/Jira/Notion | Workspace already runs an n8n instance; ideal glue |
| Airtable | SaaS | Yes — REST | Lightweight canonical store for small teams |
| Metabase / Lightdash | OSS | Yes — REST + embedded SQL | Dashboards layered over the dbt model |

## Templates & scripts

Roadmap-rollup runner (drop into ops scripts; assumes Linear + PostHog tokens in env):

```bash
#!/usr/bin/env bash
# ops-rollup.sh - generate weekly Product Ops rollup from Linear + PostHog.
# Outputs Markdown to stdout. Pipe into Notion via notion-cli or commit to a docs repo.
set -euo pipefail
: "${LINEAR_API_KEY:?}"; : "${POSTHOG_API_KEY:?}"; : "${POSTHOG_HOST:?}"
since=$(date -u -d "7 days ago" +%Y-%m-%dT%H:%M:%SZ)
echo "# Product Ops rollup - $(date -u +%Y-%m-%d)"
echo
echo "## Shipped"
curl -fsSL -H "Authorization: $LINEAR_API_KEY" -X POST https://api.linear.app/graphql \
  -H 'Content-Type: application/json' \
  -d "{\"query\":\"{ issues(filter:{completedAt:{gte:\\\"$since\\\"}}, first:50){ nodes{ identifier title team{name} url } } }\"}" \
  | jq -r '.data.issues.nodes[] | "- [\(.team.name)] \(.identifier) \(.title) <\(.url)>"' || echo "_linear unavailable_"
echo
echo "## At-risk (>2d slip)"
curl -fsSL -H "Authorization: $LINEAR_API_KEY" -X POST https://api.linear.app/graphql \
  -H 'Content-Type: application/json' \
  -d "{\"query\":\"{ issues(filter:{state:{type:{eq:\\\"started\\\"}}, dueDate:{lt:\\\"$(date -u +%Y-%m-%d)\\\"}}, first:50){ nodes{ identifier title dueDate url } } }\"}" \
  | jq -r '.data.issues.nodes[] | "- \(.identifier) \(.title) due=\(.dueDate) <\(.url)>"' || echo "_linear unavailable_"
echo
echo "## Metric movers (>10%)"
curl -fsSL -H "Authorization: Bearer $POSTHOG_API_KEY" \
  "$POSTHOG_HOST/api/projects/@current/insights/trend?interval=week&date_from=-14d" \
  | jq -r '.result[]? | select((.aggregated_value // 0) != 0) | "- \(.label): \(.aggregated_value)"' \
  | head -20 || echo "_posthog unavailable_"
```

Canonical-state schema seed (`ops-store/schema.sql`, dbt-modelled afterwards):

```sql
create table feature (id text primary key, source text, title text, owner text, status text, target_date date, outcome text, metric text, updated_at timestamptz);
create table release (id text primary key, name text, ships_on date, scope_feature_ids text[], readiness_score numeric, updated_at timestamptz);
create table risk (id serial primary key, feature_id text references feature(id), kind text, severity int, opened_at timestamptz, closed_at timestamptz, note text);
create table metric_kpi (id text primary key, name text, definition_sql text, owner text, target numeric, current numeric, last_computed timestamptz);
```

## Best practices

- **Pick one canonical store and write all agents against it.** Do not let agents query Jira and Linear directly for the same question; sync into Postgres/Notion first, then the agent reads one source. Avoids cross-system reconciliation forever.
- **Define the consumer before the automation.** Every dashboard, digest and rollup must have a named human reader. If you cannot name them, kill the automation. Product Ops debt is mostly orphan reports.
- **Codify the maturity model in the agent itself.** The orchestrator should refuse "Level 3" requests (predictive analytics, AI roadmap analysis) until "Level 1" artifacts exist (template registry, ceremony list, KPI dictionary).
- **Version templates as code.** Roadmap, spec, retro, OKR templates live in the repo (`templates/`), not Notion pages. Agents read from the repo so a `git diff` shows process changes.
- **Two-week TTL on every automated insight.** Agents stamp every status pack with a freshness window; consumers see "stale" instead of stale numbers presented as fresh.
- **PR-style writes.** No agent writes to Jira/Productboard/Notion directly on a fresh observation. Open a draft, post the diff to Slack, wait for human ack, then commit.
- **Track agent ROI.** Log every Product Ops agent invocation with `consumer`, `read_seconds_estimate`, `tokens_spent`. Quarterly review kills automations no one reads.
- **Separate the metrics layer from the narrative layer.** Numbers in dbt + Postgres + Metabase. Prose in Notion + Markdown. Agents compose, never originate, the numbers.
- **Prefer webhooks over polling.** Linear/Jira/Productboard/GitHub all support webhooks; subscribe and react instead of cron-scraping. Fewer rate-limit failures, fresher data.
- **Run `faion-improver` against the Product Ops surface every quarter.** It is the methodology's own self-audit prescription, mapped to an agent.

## AI-agent gotchas

- **Hallucinated metric definitions.** "DAU = users who logged in in 24h" — but the team's actual definition excludes internal users and bots. Always pin metric SQL in `metric_kpi.definition_sql`; never let the agent re-derive a definition from prose.
- **Roadmap merge conflicts.** Two PMs edit the same Productboard feature in parallel; the agent's nightly sync overwrites one. Use `updated_at` watermarks and conflict logs, not last-write-wins.
- **Stakeholder summary tone drift.** Agents reflexively produce "all-green" digests because they pattern-match on past on-track packs. Inject a hard rule: every status pack must surface ≥1 risk or explicitly state "no risks identified, list of checks performed: ...".
- **Cross-system ID collisions.** Same feature exists in Productboard (`PB-123`), Jira (`PROD-456`) and Linear (`ENG-789`). The canonical schema needs an explicit mapping table or every join silently double-counts.
- **OKR cargo-culting.** LLMs love producing OKR docs; they are bad at saying "this OKR is meaningless, kill it." Pair OKR generation with a critique pass and require human sign-off on the kill list.
- **`AskUserQuestion` ignored in cron.** Scheduled rollups have no human; design every automation as headless-first, with Slack-based async confirmations for write actions.
- **Unbounded historical pulls.** "Show me all incidents this quarter" silently fetches 30k tickets and blows the context. Always pass `since`, `limit`, and a hard `max_pages`.
- **Privacy / PII leakage.** Customer names, email addresses, support transcripts often live in product feedback tools. Strip PII at sync time before they touch the agent context window.
- **Silent webhook drops.** Linear/Productboard webhooks fail and the agent has no idea — its dashboards keep looking fresh. Add a heartbeat ticket per source: "Source X last delivered N seconds ago."
- **Agents promoted past their charter.** A status-pack agent cannot decide to close a feature; a metric agent cannot rename a KPI. Bound write scopes per agent in code, not just in the prompt.

## References

- Methodology README: `../README.md`
- Sibling skill: `../../product-manager/CLAUDE.md` (Product Ops sits underneath product-manager)
- Solo-tier counterpart: `../../../../solo/product/product-operations/` (smaller team variant)
- Product Operations Institute: https://productoperations.com
- "State of Product Ops" (Productboard, annual): https://www.productboard.com/research/state-of-product-ops/
- Mind the Product on Product Ops: https://www.mindtheproduct.com/tag/product-ops/
- Linear API: https://developers.linear.app
- Jira REST v3: https://developer.atlassian.com/cloud/jira/platform/rest/v3
- Productboard API: https://developer.productboard.com
- PostHog API: https://posthog.com/docs/api
- Notion API: https://developers.notion.com
- dbt docs: https://docs.getdbt.com
- Slack Bolt: https://slack.dev/bolt-js
