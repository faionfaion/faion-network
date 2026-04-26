# Agent Integration — Cohort Analysis Basics

## When to use
- You have time-series user data (signup_date, event_date) and a stable user identifier in a warehouse or product analytics tool.
- Aggregate retention numbers ("D30 = 15%") feel meaningless because product, traffic mix, or pricing has changed over time.
- You need to attribute a retention shift to a specific change (onboarding redesign, pricing experiment, ICP expansion).
- Pre-A/B-test power planning — knowing baseline cohort variance is required to size experiments.

## When NOT to use
- Pre-launch / no real users — there is no cohort yet. Plan the schema, do not run analysis.
- Cohorts smaller than ~100 users — sampling noise dominates the signal; weekly buckets need at least that.
- One-off transactional products (single-purchase utilities) where "retention" is not the goal — measure repeat-purchase or NPS instead.
- Long-cycle B2B with quarterly usage — daily/weekly cohort tables are noise; switch to monthly or feature-event cohorts.

## Where it fails / limitations
- "Diagonal effect": newest cohorts have less observable history; comparing D90 across them is meaningless until they mature.
- Aggregate-cohort improvement can hide segment regressions (paid users improving while free users worsen). Layer behavioral cohorts on top.
- Survivorship bias — looking only at retained users to define behaviors makes any feature look "magic" (the `magic feature fallacy`).
- Cohort-vs-cohort comparisons assume identical traffic mix; a paid-channel change confounds the trend.
- Pivot tables with many cohort × time cells are visually noisy — heatmaps + benchmark thresholds work better.

## Agentic workflow
Use Claude subagents to (1) generate the SQL/dataframe for a fresh cohort table from a definition prompt, (2) summarize the table into 3–5 actionable bullets, and (3) flag anomalies (cohort-size shifts, suspicious trend breaks). Keep the agent in read-only mode against the warehouse; writes go through dbt models or BI tooling that humans review.

### Recommended subagents
- `data-analyst` (sonnet) — write SQL, validate joins, compute retention pct.
- `growth-marketer` (sonnet) — interpret the table, propose hypotheses, link to `cohort-implementation`.
- `bi-engineer` (sonnet) — promote validated query into a dbt model + scheduled refresh.

### Prompt pattern
```
Input: schema (users.user_id, users.signup_date, events.user_id, events.event_type, events.event_date)
Goal: weekly acquisition cohorts, retention metric = login,
      report D1 / D7 / D30 / D90 by cohort_week for last 12 weeks
Output: 1) read-only SQL (no DDL), 2) interpretation with up to 5 bullets,
        3) one suggested follow-up cohort (behavioral or feature) per insight
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `dbt-core` | Cohort models + tests in source-controlled SQL | `pip install dbt-core` |
| `duckdb` CLI | Local cohort prototyping on Parquet/CSV | `brew install duckdb` |
| `mixpanel-utils` | Bulk export retention reports for offline analysis | `pip install mixpanel-utils` |
| `posthog` CLI / SDK | Pull cohort definitions, run HogQL | `npm i -g posthog-node` |
| `bq` (BigQuery) | Run, schedule, materialize cohort views | `gcloud components install bq` |
| `pandas` + `seaborn` | Pivot, heatmap, line-chart cohort tables | `pip install pandas seaborn` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Amplitude | SaaS | Yes — REST + Cohort API | Built-in retention + behavioral cohorts |
| Mixpanel | SaaS | Yes — REST + JQL | Retention reports, formula UI, JQL for custom cohorts |
| PostHog | OSS + SaaS | Yes — REST + HogQL | Cohorts as first-class objects, queryable from agents |
| GA4 | SaaS | Partial | Cohort exploration is limited; export to BigQuery for real work |
| Heap | SaaS | Yes — REST | Auto-captured events ease behavioral cohorts |
| Looker / LookML | SaaS | Yes — content API | Define cohort models in LookML, agent edits PRs |
| Metabase | OSS | Yes — REST | Lightweight cohort visualizations |
| Mode Analytics | SaaS | Yes — REST | Notebooks with Python + SQL cells |

## Templates & scripts
See `README.md` for the cohort-table template and benchmark thresholds. The companion methodology `cohort-implementation/README.md` contains the canonical SQL and pandas snippets — point the agent there rather than rewriting. For a quick local prototype on a CSV dump:

```python
# basic_cohort.py — quick acquisition cohort table from CSV
import pandas as pd
users  = pd.read_csv("users.csv",  parse_dates=["signup_date"])
events = pd.read_csv("events.csv", parse_dates=["event_date"])
events = events[events.event_type == "login"]

users["cohort"] = users.signup_date.dt.to_period("W")
df = events.merge(users, on="user_id")
df["d"] = (df.event_date - df.signup_date).dt.days
df = df[df.d.isin([1, 7, 30, 60, 90])]

active = df.groupby(["cohort", "d"]).user_id.nunique().reset_index(name="active")
size   = users.groupby("cohort").user_id.nunique().reset_index(name="size")
ret    = active.merge(size, on="cohort")
ret["pct"] = (ret.active / ret["size"] * 100).round(1)
print(ret.pivot(index="cohort", columns="d", values="pct").to_string())
```

## Best practices
- Anchor every cohort table to one explicit retention definition (e.g. "logged in" vs "performed core action") — agents should never silently switch.
- Weekly cohorts for early-stage, monthly once volume passes ~100k signups/month — granularity should match cohort-size stability.
- Always show absolute size next to retention pct; a "30%" cell built on n=20 is a story not a stat.
- Pair acquisition cohorts with at least one behavioral cohort each review — the latter is where actionable insights live.
- For "magic feature" claims, run a propensity-matched comparison or A/B test, not a raw behavioral split — `cohort-basics` shows correlation, not causation.
- Bake benchmark thresholds (B2B vs consumer) into the dashboard so anomalies are visible at a glance.

## AI-agent gotchas
- Agents will confuse "retained" (still active in window) vs "returned" (came back exactly on day N) — pin the definition in the prompt.
- Time-zone bugs: signup at 23:55 UTC vs first event at 00:05 UTC creates fake D1 events. Force an explicit timezone and date floor.
- LLMs default to monthly buckets and SUM where COUNT(DISTINCT) is needed; review the SQL or run a row-count sanity check.
- Causal claims ("onboarding caused the lift") are out-of-scope for cohort basics; redirect to `ab-testing-basics` or `statistics-application`.
- Cohort heatmaps with >20 rows × >10 cols overflow context — instruct the agent to summarize trends, not paste the table.
- "Survivorship" filters (only users who reached D30) are easy to introduce by accident in JOINs — agent should test query against a known cohort_size.

## References
- Brian Balfour, "Retention is the King of SaaS metrics" — https://brianbalfour.com/essays/retention-engagement-growth
- Casey Winters, "How to do a retention deep dive" — https://caseyaccidental.com
- Reforge "Retention + Engagement Deep Dive" — https://www.reforge.com
- Andrew Chen, "DAU/MAU is an important metric" — https://andrewchen.com/dau-mau-is-an-important-metric
- Amplitude Mastery "Cohort Analysis" — https://amplitude.com/blog/cohort-analysis
