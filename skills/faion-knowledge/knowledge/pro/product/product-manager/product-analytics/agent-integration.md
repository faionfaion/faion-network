# Agent Integration — Product Analytics

## When to use
- Pre-launch: agent drafts the tracking plan from a feature spec, so day-1 events ship with the code (not tacked on three sprints later).
- Activation diagnosis: drop in funnel data + cohort table, ask the agent to pinpoint the highest-leakage step and propose two experiments.
- Weekly product-health digest: scheduled agent reads BI source (BigQuery / Snowflake / Postgres replica), writes a markdown summary with anomalies highlighted.
- Post-experiment readout: agent merges A/B exposure logs with metric tables, writes the analysis report, flags Simpson's-paradox segments.
- Tracking-plan audit before a vendor migration (e.g., GA4 → PostHog) — agent diffs the live event catalog against the documented plan.
- Inbound product question from a stakeholder ("did churn move after price change?") — agent runs a parameterized SQL or Mixpanel JQL and returns chart + caveats.

## When NOT to use
- Pre-PMF (<100 weekly active users) — sample sizes are too small for funnel/cohort math; talk to users instead, no analytics framework will save you.
- Causal claims with only observational data — agent will happily call a correlation a cause; if you need causality, gate behind a proper experiment design or quasi-experimental method (DiD, synthetic control), not a dashboard.
- Exec one-pagers where the audience needs judgment, not numbers — let the agent prep the data, but a human writes the recommendation.
- High-cardinality PII queries — agents pulling raw user-level data without aggregation/scrubbing is a privacy incident waiting to happen.
- Replacing a tracking plan review with a one-shot LLM call — naming, taxonomy, and ownership decisions outlive any single feature; commit them via PR, not chat.

## Where it fails / limitations
- **Vanity-metric trap:** the README's "Acquisition / Activation / Engagement / Retention / Revenue" buckets are easy to fill with totals (signups, DAU) that move with marketing spend, not product. Agents replicate this by default — they pick the metric that has data, not the one that drives a decision.
- **Naming entropy:** without a strict schema (snake_case, `object_action`, frozen taxonomy), agents and humans both invent variants — `signup_done`, `account_created`, `user_registered` — and your funnel quietly fragments. The README mentions `[Object] [Action]` but does not enforce it.
- **Server vs. client confusion:** the README says "server-side for critical events" with no decision tree. Agents will mirror the same event in both places, double-counting. Need explicit ownership per event.
- **Cohort drift:** agent-built cohort charts compare a 6-week-old cohort to a 1-week-old one; readers misread it as a retention regression. Always force fixed-window comparison.
- **Dashboard graveyard:** agents are great at producing 14 charts; they are terrible at retiring 12. Without a kill-criterion ("if no one opened this in 30 days, archive it") dashboards accumulate forever.
- **PII and consent boundary:** product-analytics events leak PII (emails in URLs, free-text inputs) — most LLM agent loops do not enforce a redaction layer between warehouse and prompt.
- **Survivorship bias in retention curves:** D7 / D30 retention computed only on users who signed up >30 days ago systematically over-states retention for fast-growing products. Agents miss this unless prompted.
- **No causal inference:** funnels and cohorts answer "what" and "where," never "why." Agents tend to confabulate causes from correlation; product analytics is descriptive by design.

## Agentic workflow
Drive product analytics as a four-stage agent pipeline: (1) **plan** — a planner agent ingests the feature spec and emits a tracking plan diff against the canonical event catalog (`.product/tracking-plan.md`); (2) **implement** — `faion-sdd-executor-agent` converts new events into typed wrappers (TS/Python) with property contracts and PR-ready code; (3) **monitor** — a scheduled BI agent reads the warehouse hourly/daily, writes anomaly notes into `.product/analytics/digest-YYYY-MM-DD.md`, and pings the team only on threshold breach; (4) **analyze** — on demand, a reporting agent runs parameterized SQL/JQL, fills the README's Analysis Report Template, and surfaces hypotheses for the next experiment. Persist the tracking plan and dashboard specs in git so agents diff before changing — never let agents mutate live dashboards without a PR.

### Recommended subagents
- `faion-market-researcher-agent` (declared in this README's `Agents` field) — fits the planning stage: benchmarks competitor metric definitions and surfaces category norms for retention / activation targets.
- `faion-sdd-executor-agent` (`agents/faion-sdd-executor-agent.md`) — converts new tracking-plan rows into typed event-emitter code + tests as SDD tasks (`.product/features/.../todo/`).
- `password-scrubber-agent` (`agents/password-scrubber-agent.md`) — mandatory pre-step before any prompt that includes raw event payloads; product events leak emails, tokens, vendor names.
- A purpose-built **analytics-reporter agent** (not yet in repo, worth creating with read-only DB credentials, schema docstring in system prompt, and SQL-only output): runs the warehouse queries; output is consumed by the README's Analysis Report Template.
- A **tracking-plan linter agent** (cron, weekly): diffs the runtime event catalog (PostHog `/event_definitions`, Amplitude `/api/2/taxonomy/event`, GA4 admin API) against `.product/tracking-plan.md`; opens a GitHub issue per drift.

### Prompt pattern
Tracking-plan generation:
```
You are a product analyst. Read the feature spec in <spec> and the
canonical event catalog in <tracking-plan.md>. Output the diff:
new events to add, existing events to reuse, properties to extend.
Use the schema [object]_[action] in snake_case. For every event
specify: trigger condition, server|client, owner, properties (name,
type, example, required). Reject any event without a stated decision
it will inform. Output as a markdown table compatible with the
Tracking Plan template in product-analytics/README.md.
```

Anomaly digest:
```
Given the SQL results in <data> for the last 7 days vs the prior
4-week baseline, list metrics whose 7-day mean is >2 sigma from
baseline. For each: state direction, magnitude, candidate cause
(deploy diff, marketing campaign, seasonality, instrumentation
change), and the next query that would disambiguate. No causal
claims without a stated experiment or natural experiment.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| PostHog CLI (`posthog`) | Manage event definitions, run HogQL from CI | https://posthog.com/docs/cli |
| Amplitude Taxonomy API + `httpie` | Pull live event/property catalog for drift checks | https://amplitude.com/docs/apis/taxonomy-api |
| Mixpanel JQL / Query API + `mixpanel-cli` (community) | Scriptable funnel + retention queries | https://developer.mixpanel.com/reference/query-api |
| `dbt` | Warehouse-side metric definitions (single source of truth) | https://docs.getdbt.com |
| `metricflow` / `cube` | Headless metrics layer agents can query without re-deriving | https://docs.getdbt.com/docs/build/about-metricflow / https://cube.dev |
| `sqlfluff` | Lint analyst SQL before agents run it (catch fanout joins) | https://docs.sqlfluff.com |
| `great_expectations` / `dbt test` | Data-quality gates on event tables (null user_id, future timestamps) | https://greatexpectations.io |
| `evidence` (Evidence.dev) | Markdown-as-code BI; agent-friendly because reports are git-versioned | https://evidence.dev |
| `gh` CLI | Open tracking-drift / experiment-readout issues from agents | https://cli.github.com |
| `claude` (Anthropic CLI) | Run digest + readout prompts headless on cron | https://docs.anthropic.com |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| PostHog | OSS + SaaS | Yes — full REST + HogQL | Best agent integration; self-host avoids PII boundary issues. |
| Amplitude | SaaS | Yes — Taxonomy + Dashboard REST APIs | Strong cohort + funnel APIs; rate-limited, plan accordingly. |
| Mixpanel | SaaS | Yes — JQL + Query API | JQL is JS DSL, easy for LLMs to write; expensive at scale. |
| GA4 | SaaS | Partial — Data API + Admin API | Sampling + cardinality limits hurt agent reliability for product analytics. |
| Heap | SaaS | Yes — Snapshot + REST APIs | Auto-capture is double-edged: agents drown in noise without a curated event layer. |
| Snowplow | OSS | Yes — schema-first, ideal for agents | Best when you need a strict event schema agents can validate against. |
| Segment / RudderStack | SaaS / OSS | Yes — Tracking Plan + Protocols APIs | Ideal pipe-and-router; agents can lint events at the CDP layer. |
| BigQuery / Snowflake / DuckDB | Warehouse | Yes — SQL APIs | Pair with dbt + metrics layer; gives agents a stable contract. |
| Metabase / Lightdash / Evidence | OSS BI | Yes — APIs / git | Markdown/git-driven BI lets agents PR a dashboard, not click one. |
| LaunchDarkly / Statsig / GrowthBook | SaaS / OSS | Yes — REST + SDKs | Couple flag exposure events to analytics for clean experiment readouts. |
| Notion / Linear | SaaS | Yes — APIs | Tracking plan + analytics-question backlog live here; agents read/write. |

## Templates & scripts

The README ships Tracking Plan, Dashboard Spec, and Analysis Report templates. The gap is enforcement: there is no linter for the tracking plan or for runtime drift. Inline drop-in (≤50 lines):

```bash
#!/usr/bin/env bash
# tracking-plan-lint.sh — enforce naming + required fields on a
# markdown Tracking Plan that follows product-analytics/README.md.
# Usage: tracking-plan-lint.sh path/to/tracking-plan.md
set -euo pipefail
file="${1:?usage: tracking-plan-lint.sh PLAN.md}"
python3 - "$file" <<'PY'
import re, sys, pathlib
src = pathlib.Path(sys.argv[1]).read_text()
errs = []
# Match table rows: | event | trigger | properties |
row_re = re.compile(r"^\|\s*([a-zA-Z0-9_\[\]]+)\s*\|([^|]+)\|([^|]+)\|", re.M)
seen = {}
for m in row_re.finditer(src):
    name, trigger, props = (s.strip() for s in m.groups())
    if name in ("Event", "event", "---"): continue
    if not re.fullmatch(r"[a-z][a-z0-9_]*", name):
        errs.append(f"{name}: not snake_case")
    if "_" not in name:
        errs.append(f"{name}: missing object_action shape")
    if not trigger or trigger.startswith("TODO"):
        errs.append(f"{name}: missing trigger")
    if not props or props.startswith("TODO"):
        errs.append(f"{name}: missing properties")
    if name in seen:
        errs.append(f"{name}: duplicate (also in '{seen[name]}')")
    seen[name] = trigger
if errs:
    print("Tracking-plan lint errors:")
    [print(" -", e) for e in errs]
    sys.exit(1)
print(f"OK: {len(seen)} events validated.")
PY
```

Wire into pre-commit on the repo that owns `tracking-plan.md` so naming drift fails CI. Pair with a weekly cron agent that diffs this file against the live event catalog (PostHog `/api/event_definitions`, Amplitude Taxonomy API) and opens a GitHub issue per discrepancy.

## Best practices
- **Decision-first events.** Reject any event whose row does not state which decision it informs. Stops "track everything" sprawl.
- **Freeze the taxonomy in git.** `tracking-plan.md` is the source of truth; runtime catalogs drift toward it via PR, not the other way around.
- **One owner per event, named.** "Product team" is unowned. Add a GitHub handle column.
- **Server-side for money + auth, client-side for UX.** Encode this rule in the tracking plan, not in tribal memory.
- **Cohort fixed-window or it lies.** Compare D7-of-cohort-A to D7-of-cohort-B, never D30 vs D7.
- **Kill-criterion on every dashboard.** "Archive if zero opens in 30 days" — let an agent enforce it.
- **Separate descriptive from causal.** Funnels/cohorts answer "what." Causal claims require flag-gated experiments with pre-registered hypotheses.
- **PII redaction at the warehouse boundary.** Do not let agent prompts touch raw event payloads; aggregate or hash first.
- **Diff event catalogs across releases.** New event + removed event = changelog row, just like API changes.
- **Tie metrics to the OKR they roll up to.** Orphan metrics get cut. The pyramid: company KPI → product north star → team metric → event.

## AI-agent gotchas
- **Hallucinated event names.** Agents invent `user_signed_up` when the codebase uses `signup_completed`. Always pass the canonical taxonomy in the system prompt and reject novel event names without an ADD-event task.
- **SQL fanout from naive joins.** Agent joins `events` to `users` to `sessions` and triple-counts. Require `count(distinct ...)` and gate via `sqlfluff` rules, or use a metrics layer (dbt-metrics, Cube) so agents can't write raw fanout SQL.
- **Confabulated causes.** Asked "why did retention drop?" the LLM will produce a confident, plausible, wrong story. Force the agent to list 3+ candidate causes and the disambiguating query, never a single explanation.
- **Window mismatch in cohort comparisons.** Agents will compare partial-cohort retention to mature-cohort retention. Pin window length explicitly in every prompt and chart.
- **Recency bias in anomaly detection.** Z-score against last 7 days flags every product launch as an anomaly. Use a 4-week trailing baseline with seasonal adjustment.
- **Token bombs from raw event tables.** Do not paste 50k rows into context. Pre-aggregate to ≤200 rows or use tool-use (function calling) to query the warehouse directly.
- **Privacy leak via prompt.** Event payloads include emails, IPs, free-text. Always run through a redactor before any LLM call; log the redaction.
- **Drift between code and plan.** Engineers ship new events without updating `tracking-plan.md`. The cron drift-linter is the only sustainable fix; agents themselves drift if not constrained.
- **Dashboard halucination.** Asked to "build a dashboard," agents emit chart specs against tables that do not exist. Pass the schema (or, better, a metrics-layer manifest) in the prompt and reject any chart referencing an unknown column.
- **Premature causal claims in readouts.** A/B readouts written by agents drop confidence intervals and SRM checks. Template the readout (the README's Analysis Report) and require explicit `p`, `n`, CI, and SRM-pass fields, or fail the report.

## References
- McClure, D. — "AARRR / Pirate Metrics." https://500hats.typepad.com/500blogs/2007/09/startup-metrics.html
- Amplitude — "Mastering Retention" + Taxonomy API docs. https://amplitude.com/blog and https://amplitude.com/docs/apis/taxonomy-api
- Mixpanel — "Implementation Best Practices" + JQL. https://docs.mixpanel.com
- PostHog — "Tracking events: Best practices" + HogQL. https://posthog.com/docs/product-analytics
- Reichheld, F. — Net Promoter / retention foundations. https://www.bain.com/insights/topics/net-promoter-system
- Hubbard, D. (2014). "How to Measure Anything." Wiley. (Calibration vs. vanity metrics.)
- Kohavi, R., Tang, D., Xu, Y. (2020). "Trustworthy Online Controlled Experiments." Cambridge. (SRM, peeking, Simpson's paradox.)
- Reforge — "Metrics frameworks for product growth." https://www.reforge.com/blog
- Sibling methodologies in this repo: `solo/product/product-operations/product-analytics/`, `pro/product/product-manager/success-metrics-definition/`, `pro/product/product-manager/aarrr-pirate-metrics/`, `pro/product/product-manager/cohort-analysis/`, `pro/product/product-manager/funnel-optimization/`, `pro/product/product-manager/ab-testing-framework/`.
