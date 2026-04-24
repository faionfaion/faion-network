# Agent Integration — Data Analysis (Business Analyst)

> Sibling note: `pro/ba/ba-modeling/data-analysis/agent-integration.md` covers the
> design-time view (data dictionary, ERD, dbt/great-expectations governance). This
> file covers the **BA-led discovery view**: using existing data to surface,
> validate, and quantify requirements, and the hand-off contract with data teams.
> Read both before invoking — the README's six-dimension scorecard and entity
> templates remain the shared backbone.

## When to use
- Pre-spec discovery: a stakeholder says "users abandon at checkout"; a BA agent profiles `orders`, `events`, and `support_tickets` to convert the assertion into a quantified requirement (`reduce 32% drop at /checkout/payment by Q3`).
- Sizing a candidate feature before it enters the backlog: BA agent runs counts (`SELECT COUNT(DISTINCT user_id) WHERE …`) to confirm population, frequency, and business value; rejects features that touch <0.5% of users without strategic justification.
- Reconciling conflicting stakeholder reports: Sales says "churn is 12%", Finance says "8%"; BA agent reads both definitions, runs a third query against the source of truth, and produces a definition + numbers memo.
- Translating BABOK Knowledge Area 7.5 (Data Analysis as part of Requirements Analysis) into reproducible SQL/notebook artifacts that live next to `spec.md`.
- Generating evidence packs for steering committees: BA agent assembles a one-page brief with three queries, two charts, one risk, one recommendation.
- Hand-off contract with the data team: BA agent drafts a `data-request.md` (question, decision it informs, deadline, acceptable accuracy, sample-size floor) instead of an open-ended Slack ask.
- Data-literacy uplift in stakeholder workshops: BA agent prepares "what this number actually means" annotations on every metric on the dashboard before a workshop.

## When NOT to use
- Statistical inference / experimentation analysis (A/B testing power, lift calculation, Bayesian uplift) — that is data-science / analytics-engineer territory; BA stops at descriptive statistics + basic segmentation.
- Production data pipeline authoring — BA writes throwaway exploratory SQL; promotion to dbt models, Airflow DAGs, or BI semantic layers must be done by analytics engineering with code review.
- Direct write access to source systems — BA queries are read-only; any "fix the data" action goes through change management (the `ba-modeling/data-analysis` governance flow).
- Heavily regulated personally identifiable data (HIPAA PHI, PCI cardholder data, GDPR special-category) without a DPIA — BA exploration on raw data is a compliance breach; require redacted / synthetic environments.
- Replacing an existing source-of-truth metric with an ad-hoc agent calculation — if Finance has a certified ARR number, BA references it, never recomputes.
- Real-time / streaming questions ("right now, how many users are stuck?") — BA discovery operates on batch snapshots; live operational telemetry is observability/SRE, not BA.

## Where it fails / limitations
- **Scope drift into data engineering.** A BA who can write SQL is tempting to push into building dashboards; the role is requirements, not delivery. Agents amplify this by happily producing dashboards no one owns.
- **Definition theatre.** Two stakeholders call the same thing "active user" with different windows; BA produces a query and "the number" gets cited as canonical without the definition. Numbers travel; definitions don't.
- **Sample-of-one trap.** A BA pulls 50 rows, eyeballs a pattern, and writes a requirement. Without a power check ("is 50 enough to detect the effect that matters?") the requirement is built on noise.
- **No counterfactual.** "Users who saw banner X converted 4x more" — selection bias; agents will rarely ask "what would these users have done without the banner?"
- **Data deserts.** The most important questions ("why did they leave?") have the worst data; BA forced to fall back to qualitative methods (interviews, ethnography) which this methodology does not cover.
- **Dictionary disconnect.** BA's exploratory SQL uses column names from the warehouse view; product spec uses business names; over time the spec and the data drift apart.
- **Org-chart-bound queries.** BA only knows the systems they were granted access to; they invent answers from incomplete tables instead of escalating "I cannot answer this without the billing DB".
- **PII leakage in screenshots.** A BA pastes a query result into a Confluence page or LLM prompt; row 3 is a real customer email. The README's "Data Security" row is not enforced at exploration time.
- **Static numbers.** A BA cites "34% churn" in a PRD; six months later the spec ships, churn is now 21%, no one updates the PRD. Snapshot timestamps are routinely omitted.
- **Confounding business calendar.** Numbers without fiscal-week alignment, holidays, or release dates produce false trends; agents will rarely overlay these annotations.

## Agentic workflow
Drive BA Data Analysis as a **discovery-loop subagent** that takes a stakeholder question and produces a `data-brief.md` artifact, never a live dashboard. The loop: (1) **frame** — agent rewrites the question into a measurable form with a target audience, time window, and decision it informs; rejects unmeasurable framings; (2) **locate** — agent maps the question to source systems by reading `data-dictionary.md` (from `ba-modeling/data-analysis`); flags coverage gaps as blockers, not assumptions; (3) **query** — agent writes read-only SQL against a warehouse role with `SET statement_timeout`, samples conservatively, redacts PII via Presidio before any output; (4) **interpret** — agent annotates every number with definition, time window, sample size, and caveats (selection bias, data quality scores from the README scorecard); (5) **hand off** — agent emits two artifacts: `data-brief.md` for the spec, and `data-request.md` for any unanswered slice routed to the data team. Persist both in git inside the SDD feature folder; treat the brief as a versioned input to `spec.md`, not a Slack thread.

### Recommended subagents
- `faion-sdd-executor-agent` (`agents/faion-sdd-executor-agent.md`) — picks up the `data-brief.md`'s recommendation, opens an SDD task in `.product/features/<feature>/todo/`, and links the brief as evidence in `spec.md`.
- `password-scrubber-agent` (`agents/password-scrubber-agent.md`) — mandatory pre-LLM-context filter for any sample row, query result, or stack trace before it enters a prompt; BA exploration constantly surfaces emails, IDs, free text.
- A purpose-built **ba-data-discovery agent** (worth creating; not yet in repo): system prompt holds the canonical `data-dictionary.md` excerpt + the question framing rules; tools are read-only warehouse role + Presidio + a `data-brief.md` generator; output schema is `{question, framing, sources, sql, results_redacted, caveats, recommendation, decision_owner, snapshot_at}`.
- A **definition-resolver agent**: when stakeholders disagree, this agent reads the data dictionary, related dbt model docs, and the spec, then emits a single canonical definition + a SQL implementation; routes to the data team for sign-off before merge.
- A **data-request-router agent**: takes a `data-request.md`, classifies (self-serve vs analytics-engineer vs data-engineer vs governance), and posts to the right queue with the SLA.

### Prompt pattern
Frame an unmeasurable stakeholder question:
```
You are a BA data-discovery agent. The stakeholder says: <quote>.
Rewrite this as a measurable question with: (a) target population
(SQL filter), (b) metric (counted entity + aggregation), (c) time
window (anchored to fiscal calendar in <fiscal.yaml>), (d) the
decision it informs (next action if metric is X vs Y), (e) acceptable
margin of error. If any element is unknowable from the data
dictionary in <data-dictionary.md>, output a data-request.md
draft instead of guessing. No SQL yet.
```

Produce a data-brief from a query result:
```
You profiled <table> answering <framed-question>. Sample size <n>,
snapshot <iso-timestamp>. Output a data-brief.md with: question,
framing, sources (with dictionary entries cited), the SQL (read-only,
parameterised), results redacted via Presidio, definition footnote
per metric, three caveats (selection bias / data quality / temporal
confounders), recommendation with a decision owner. No claim without
a count + percentage. Reject the brief if sample size is below the
floor in <power-config.yaml>.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `duckdb` | In-process SQL on Parquet/CSV/Postgres without a warehouse round-trip; ideal for BA discovery loops in CI | https://duckdb.org |
| `pandas` / `polars` | Tabular profiling, joins, frequency tables; `polars` for >10M rows | https://pandas.pydata.org / https://pola.rs |
| `ydata-profiling` (ex pandas-profiling) | One-command profile report (counts, missing, distributions) per table | https://github.com/ydataai/ydata-profiling |
| `sweetviz` | Two-cohort comparison reports (e.g. churned vs retained) | https://github.com/fbdesignpro/sweetviz |
| `great_expectations` | Codify the README's six dimensions as expectation suites; BA reuses them in briefs | https://docs.greatexpectations.io |
| `presidio` (Microsoft) | PII detection + redaction before any sample row enters a prompt or Confluence page | https://microsoft.github.io/presidio |
| `sqlglot` | Parse SQL, swap dialects, extract columns/tables programmatically; agents use it to validate a query against the dictionary | https://github.com/tobymao/sqlglot |
| `dbt` (`dbt show`, `dbt docs serve`) | Read certified models + docs; BA never authors production dbt, only references | https://docs.getdbt.com |
| `metabase` / `superset` CLI | Run saved questions / charts via API for canonical metrics | https://www.metabase.com/docs / https://superset.apache.org |
| `evidence` / `observable framework` | Markdown-first BI; agent emits `.md` reports that compile to charts; perfect for `data-brief.md` | https://evidence.dev / https://observablehq.com/framework |
| `quarto` | Reproducible analytical reports (md → HTML/PDF); pairs with Python or R | https://quarto.org |
| `papermill` | Parameterise + execute notebooks headlessly in CI for repeatable briefs | https://papermill.readthedocs.io |
| `chdb` / `clickhouse-local` | Fast OLAP scans against logs / events without a server | https://github.com/chdb-io/chdb |
| `litellm` + Claude tool calling | Wrap "ask the warehouse" as an LLM tool with strict read-only guardrails | https://docs.litellm.ai |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Metabase | OSS / SaaS | Yes — Question + Card REST API | Canonical certified-metrics layer; BA agent references "Question 217" instead of recomputing. |
| Superset | OSS | Yes — REST API | Same role as Metabase; better for SQL Lab-style ad-hoc. |
| Lightdash / Cube | OSS / SaaS | Yes — semantic layer + API | Lets BA agent query metrics by name (`weekly_active_users`) instead of raw SQL. |
| Hex / Deepnote / Mode | SaaS notebooks | Yes — API + scheduled runs | Useful for the BA agent's reproducible brief; PII risk requires careful workspace isolation. |
| Census / Hightouch | SaaS reverse-ETL | Partial | Out of BA scope; mention only because BA briefs sometimes recommend operationalising a metric. |
| Atlan / DataHub / OpenMetadata | SaaS / OSS catalogs | Yes — REST/GraphQL | BA agent reads ownership + classification before issuing a query; writes brief metadata back. |
| Monte Carlo / Bigeye / Soda Cloud | SaaS observability | Yes — incidents API | BA agent attaches the latest freshness/quality signal to the brief's caveats. |
| Looker | SaaS | Yes — LookML + API | Treat LookML as the dictionary; BA agent never bypasses with raw SQL. |
| Snowflake / BigQuery / Redshift / Databricks | DWH | Yes — read-only role mandatory | Always run the BA agent under a `ba_explorer` role with `SET statement_timeout` and row-count caps. |
| Notion / Confluence / Coda | Docs | Yes — APIs | Target for the published `data-brief.md`; redact via Presidio before upload. |
| Linear / Jira / GitHub Issues | Tracker | Yes — APIs | BA agent files a `data-request.md` as an issue with the data-team label. |
| FullStory / Heap / PostHog | Product analytics | Yes — APIs / SQL | Source for behavioural questions ("did users see X before Y?"). |

## Templates & scripts

The README ships dictionary, requirements, and quality templates but no
discovery-loop artifact. The two missing artifacts are `data-brief.md`
(answer to the spec) and `data-request.md` (ask to the data team).
Inline drop-in (≤50 lines): a tiny generator that scaffolds both from a
question + dictionary citation, ready for the BA agent to fill in:

```bash
#!/usr/bin/env bash
# ba-discovery-init.sh — scaffold a data-brief + data-request pair for
# a single stakeholder question, anchored to the SDD feature folder.
# Usage: ba-discovery-init.sh FEATURE_DIR "stakeholder question"
set -euo pipefail
feature="${1:?usage: ba-discovery-init.sh FEATURE_DIR QUESTION}"
question="${2:?usage: ba-discovery-init.sh FEATURE_DIR QUESTION}"
[ -d "$feature" ] || { echo "no such feature dir: $feature" >&2; exit 1; }
mkdir -p "$feature/data"
slug=$(printf '%s' "$question" | tr '[:upper:] ' '[:lower:]-' \
  | tr -cd 'a-z0-9-' | cut -c1-40)
ts=$(date -u +%Y-%m-%dT%H:%MZ)
brief="$feature/data/brief-$slug.md"
ask="$feature/data/request-$slug.md"
cat >"$brief" <<EOF
# Data brief: $question
- snapshot_at: $ts
- decision_owner: TODO @handle
- framing: { population: TODO, metric: TODO, window: TODO, mde: TODO }
- sources: [ TODO dictionary entry: entity.attribute ]
- sql: |
    -- read-only; SET statement_timeout = '30s';
    -- TODO
- results: TODO (redacted via presidio)
- caveats: [ selection-bias: TODO, data-quality: TODO, temporal: TODO ]
- recommendation: TODO (next action if metric is <X> vs <Y>)
EOF
cat >"$ask" <<EOF
# Data request: $question
- requester: TODO @handle
- decision_it_informs: TODO
- deadline: TODO (ISO date)
- acceptable_accuracy: TODO (e.g. +/- 2pp)
- sample_size_floor: TODO
- pii_scope: none | redacted | restricted
- expected_owner: analytics-engineer | data-engineer | governance
EOF
echo "wrote: $brief"
echo "wrote: $ask"
```

Wire into the SDD feature template so every new feature in `todo/`
gets a `data/` folder. Pair with a pre-merge check on `spec.md` that
fails when a quantitative claim has no matching `brief-*.md` reference.

## Best practices
- **Every number carries a definition footnote.** "34% churn" without `(definition: cancelled within 30 days of paid renewal; source: dbt model fct_subscriptions; snapshot 2026-04-19)` is unsourced.
- **Reframe before you query.** A BA agent that runs SQL on the first phrasing of the question is wasting tokens; force a "framing" step first, output the framing, only then query.
- **Read-only role, statement timeout, row caps.** No exception. The BA agent's warehouse credential is `ba_explorer` with `SET statement_timeout = '30s'` and `LIMIT 1000` defaults.
- **Power floor before sample.** State the minimum detectable effect; if the candidate sample cannot detect it, refuse the brief and escalate to the data team for a longer window.
- **Redact at egress, not at ingest.** Treat every result row as PII until Presidio says otherwise; never paste raw rows into a chat or LLM prompt.
- **Cite the dictionary entry, not the column.** Citation reads `Customer.email_primary (data-dictionary.md#customer)`, not `customers.email`.
- **Compare cohorts, not totals.** A 12% churn that is 30% in segment A and 4% in segment B is two products; segmentation belongs in every brief.
- **Annotate by business calendar.** Overlay fiscal weeks, holidays, releases on every time-series chart; a spike on `Black Friday` is not a trend.
- **Brief beats dashboard.** A markdown brief committed to git outlasts a dashboard whose owner left the company. Dashboards are operational; briefs are evidential.
- **Hand off, do not hoard.** When the question requires production data engineering, write the `data-request.md` and stop. BA exploration ends at evidence; building is the data team's job.
- **Snapshot everything.** Numbers travel; without `snapshot_at`, they become folklore.
- **One question per brief.** Composite briefs ("revenue, churn, NPS, and CAC") are unreviewable. Split.

## AI-agent gotchas
- **Hallucinated tables.** Agents invent `users.last_login_at` from training data when the warehouse only has `auth.session_started_at`. Always pass an introspected schema slice for the entities the question touches; reject any column the agent names that is not in the slice.
- **Definition substitution.** Agent silently maps "active user" to `WHERE last_seen_at > now() - interval '30 days'` without citing the definition source; quietly contradicts the org's certified definition. Force a definition citation step before SQL.
- **Sample-size hallucination.** Agent quotes a percentage without computing the denominator; or computes against `LIMIT 1000` and reports as if it were the population. Require `(numerator / denominator)` literal in the brief.
- **Selection bias in framing.** Agent answers "of users who completed onboarding, how many activated?" when the stakeholder needs "of users who signed up, how many activated?". Force the population definition to be reviewed before the query.
- **Read-write footgun.** A confident agent runs `UPDATE` against a stage DB it was given for "convenience". Hard-enforce with role permissions; do not rely on prompt instructions.
- **PII in prompt.** Agent asks "show me 5 rows" to debug a join; row 1 contains a real email + phone. Pre-redact via Presidio inside the tool wrapper, not via a "please redact" instruction.
- **Forgotten time zones.** Warehouse stores `UTC`; stakeholder reports in `America/Los_Angeles`; agent reports the wrong "yesterday". Force time-zone declaration in the framing step.
- **Stale snapshots.** Agent reports yesterday's number against a table that updates weekly. Pull `last_dbt_run_at` / freshness signal from the catalog and surface as a caveat.
- **Re-derived certified metrics.** Agent recomputes ARR from `subscriptions` instead of citing Finance's `fct_arr`. Force the agent to check the certified-metrics list (Looker / Cube / dbt-metrics) before authoring SQL.
- **Cross-question leakage in context.** Agent reuses framing from the previous question for a new one with different population. Reset the conversation per brief; one brief = one context.
- **Long-tail ceiling.** Agent claims "long tail of products has no signal" without checking; the bottom 80% may carry 30% revenue. Force a Pareto check on every "top N" claim.
- **Misnamed "average".** Agent reports `AVG(revenue)` when the distribution is log-normal and the median is what the stakeholder wanted. Require both mean and median, plus skew.
- **Missing not-null nuance.** Agent reads `email IS NULL` as "no email" when the column was migrated and the real null marker is `''`. Inspect the empty-string + null + sentinel cases before counting.
- **Brief that recommends building a dashboard.** Agent's default action is "create dashboard"; that is delivery, not BA. Constrain recommendations to (a) refine the spec, (b) escalate to data team, (c) defer.

## References
- IIBA — BABOK v3, sections 3 (Business Analysis Planning), 7.5 (Data Analysis), 10.12 (Data Modelling). https://www.iiba.org/standards-and-resources/babok/
- DAMA-DMBOK 2 — Data Management Body of Knowledge (chapters on data quality and metadata). https://www.dama.org/cpages/body-of-knowledge
- Tukey, J. W. (1977). "Exploratory Data Analysis." Addison-Wesley. (Foundational EDA discipline.) https://www.pearson.com
- Wickham, H. (2014). "Tidy Data." Journal of Statistical Software. https://vita.had.co.nz/papers/tidy-data.pdf
- Maxime Beauchemin — "The Rise of the Data Engineer" + "The Downfall of the Data Engineer." https://medium.com/@maximebeauchemin
- Cassie Kozyrkov — "Decision Intelligence" (framing questions before data work). https://www.linkedin.com/in/kozyrkov/
- "Data Contracts" pattern — Andrew Jones et al. (BA-to-data-team hand-off contracts). https://datacontract.com
- ISO/IEC 25012 — Data Quality Model (companion to the README's six dimensions). https://www.iso.org/standard/35736.html
- "Effect Sizes" — Cohen, J. (1988). Statistical Power Analysis for the Behavioral Sciences. (Sample-size floors.)
- Sibling methodologies in this repo: `pro/ba/ba-modeling/data-analysis/` (design-time governance), `pro/ba/business-analyst/data-driven-requirements/`, `pro/ba/business-analyst/elicitation-techniques/`, `pro/ba/business-analyst/decision-analysis/`, `pro/research/researcher/risk-assessment/`.
