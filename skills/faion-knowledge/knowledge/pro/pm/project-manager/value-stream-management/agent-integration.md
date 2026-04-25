# Agent Integration — Value Stream Management

## When to use
- Engineering org has shipped DevOps automation but value-to-customer time has not improved (the AI productivity paradox)
- Cross-functional bottleneck suspected (product spec → design → eng → release → support → success)
- Quarterly OKR cycle wants to move from output metrics ("PRs merged") to flow ("lead time for changes")
- DORA metrics already in place but not improving — need upstream view (Flow Metrics)
- Org adopting SAFe / FAST Agile / Project-to-Product model

## When NOT to use
- Single-team, single-product startup pre-PMF — premature optimization
- Org without telemetry baseline (no commit timestamps, no deploy log) — instrument first
- Pure cost-cutting context — VSM exposes inefficiencies but is not a layoff lever
- Teams with no shared ownership across the stream — VSM names the bottleneck but cannot move it

## Where it fails / limitations
- Flow Metrics aggregate work types (feature/defect/risk/debt) and hide trade-offs if not split by type
- DORA is a four-tuple proxy, not the actual customer outcome — Elite DORA + falling NPS happens
- VSM workshops produce posters, not telemetry — without instrumentation, the map decays in months
- Cross-team flow data lives in 5+ tools (Jira, GitHub, PagerDuty, Salesforce, Zendesk) with mismatched IDs
- "%C/A" (complete & accurate) is hard to measure without explicit handoff QA gates
- AI-generated PRs can inflate throughput and Deployment Frequency without raising Earned Value

## Agentic workflow
A flow-instrumenter subagent maps the actual value stream by tracing IDs across tools (issue → branch → PR → deploy → incident → support ticket), normalizes timestamps into stream stages, and emits Lead Time / Cycle Time / Throughput / WIP per stage. A second agent runs DORA daily on git+deploy logs. A third (analyst) compares week-over-week, flags regressions, identifies the constraint per Theory of Constraints, and proposes 1-3 experiments. Humans choose which experiment to run; agents track its effect.

### Recommended subagents
- `flow-instrumenter` — wires together Jira/Linear, GitHub, deploy logs, Sentry; produces stream JSON
- `dora-collector` — daily DORA: deploy freq, lead time for changes, change fail rate, MTTR
- `bottleneck-analyzer` — applies TOC; identifies the slowest stage with highest WIP-aging
- `experiment-tracker` — A/B's a process change (e.g., trunk-based vs feature-branch) on flow metrics

### Prompt pattern
```
You are a flow-instrumenter. Trace work item {issue_id} across tools using
mapping {tool_id_links.yaml}. Emit JSON {item_id, stages: [{name, enter_ts,
exit_ts, blocked_h, type}], outcome: shipped|cancelled, work_type: feature|
defect|risk|debt}. Skip items with > 1 missing stage.
```

```
You are a bottleneck-analyzer. Given last 90 days of flow data {flow.json},
return: (1) constraint stage by Little's Law (highest cycle time × WIP),
(2) flow distribution across work types, (3) top 3 experiments to elevate
constraint, ranked by expected throughput lift / cost.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `four-keys` (Google) | DORA pipeline reference | https://github.com/dora-team/fourkeys |
| `dora-cli` (open) | Compute DORA from git + deploys | https://github.com/various wrappers |
| `gh api` | GitHub deployments + PR timestamps | `gh api repos/{o}/{r}/deployments` |
| `jq` | Stream join JSON across tools | https://jqlang.github.io/jq/ |
| `git log --pretty` | Cycle time inputs | core git |
| `flow-cli` (Tasktop OSS samples) | VSM data export hooks | varies |
| `pagerduty-cli` | MTTR data | https://github.com/martindstone/pagerduty-cli |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Tasktop / Planview Viz | SaaS | Partial | VSM platform, enterprise license, REST API |
| Plandek | SaaS | Yes | Flow + DORA dashboards, REST API |
| LinearB | SaaS | Yes | Engineering metrics, GitHub-native, API |
| Jellyfish | SaaS | Yes | Engineering benchmarking, API |
| Code Climate Velocity | SaaS | Yes | Cycle time, PR throughput |
| Allstacks | SaaS | Yes | Forecasting from flow data |
| Faros AI | SaaS/OSS | Yes | DORA + Flow with open data layer |
| Pluralsight Flow | SaaS | Partial | Code-centric metrics |
| Apache DevLake | OSS | Yes | Self-host DORA + Flow, plugin for tools |
| OpenDevops | OSS | Partial | DORA reference impl |

## Templates & scripts
See templates.md for VSM mapping. Inline DORA quick-calc:

```bash
#!/usr/bin/env bash
# dora-quick.sh — last-30d DORA from git + deploy log (deploy.log: ISO ts per line)
set -euo pipefail
SINCE="30 days ago"
DEPLOYS=$(awk -v cutoff="$(date -u -d "$SINCE" +%s)" '
  { cmd="date -u -d \""$0"\" +%s"; cmd | getline t; close(cmd); if (t>cutoff) c++ }
  END { print c+0 }' deploy.log)
DAYS=30
echo "Deployment Frequency: $(echo "scale=2; $DEPLOYS / $DAYS" | bc) /day"
LEAD=$(git log --since="$SINCE" --pretty=format:"%H %at" | while read sha ts; do
  dep_ts=$(grep "$sha" deploy.log | head -1 | xargs -I{} date -u -d "{}" +%s || echo "")
  [ -n "$dep_ts" ] && echo "$((dep_ts - ts))"
done | awk '{s+=$1; n++} END{ if(n) printf "%.0f\n", s/n/3600 }')
echo "Lead Time for Changes (h, mean): ${LEAD:-n/a}"
```

## Best practices
- Split flow data by work type (Mik Kersten's four: feature, defect, risk, debt) — single-number flow lies
- Never optimize one metric in isolation; always pair (e.g., DF up + CFR up = bad trade)
- Anchor VSM in customer-visible time: from "user filed request" to "user received value", not "ticket created" to "merged"
- Run quarterly VSM workshop; refresh map; do not assume the stream stays static
- When AI tooling lifts throughput, watch CFR and rework rate — productivity that creates incidents is debt
- Use Little's Law (WIP = Throughput × Cycle Time) as a sanity check on agent-collected data
- Visualize with cumulative flow diagram, not bar charts — CFD reveals stage starvation

## AI-agent gotchas
- ID linking across tools is the failure point: agents will hallucinate links if regex matching is loose; require explicit referenced-by chains
- Timezone bugs in lead-time calc are frequent — force UTC, never local
- DORA "elite" is meaningless without context; agent-driven scorecards that publish "we are elite" without trend will be gamed
- Webhook-driven instrumentation drops events under load; reconcile with periodic full pulls
- AI commits flood the repo with micro-PRs that distort throughput; tag bot PRs and report human/bot split
- "Reliability" (5th DORA metric) is org-defined; an agent should not pick the SLO target
- Constraint identification can flip month-to-month with low data volume — require ≥ 50 items per type before declaring a bottleneck

## References
- Mik Kersten, *Project to Product* (2018) — Flow Framework
- Forsgren, Humble, Kim, *Accelerate* (2018) — DORA
- Goldratt, *The Goal* (1984) — Theory of Constraints
- Google Cloud DORA report 2024: https://cloud.google.com/devops/state-of-devops
- Apache DevLake: https://devlake.apache.org
- Tasktop Viz docs: https://docs.tasktop.com
