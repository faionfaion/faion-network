# Agent Integration — Data-Driven Requirements (BA Core)

> Scope: **fundamentals**. When and how a BA practice should *start* doing data-driven requirements, what minimum data infrastructure is required, and how to drive the basics with Claude subagents. The deeper experimentation / metric-layer / A/B-power material lives in the `business-analyst/data-driven-requirements/agent-integration.md` sibling — read that once the basics here are in place.

## When to use
- The team has at least one production system emitting structured events for ≥ 90 days, and someone (anyone) can already pull a baseline number out of it. Without that, "data-driven" is aspirational.
- Stakeholders disagree on priority and the disagreement is *resolvable* by a metric (usage, revenue, error rate). If priorities are strategic / political, data won't unstick the decision.
- A requirement under discussion has a **measurable current state** ("checkout completes 38% of starts") and a **plausibly measurable target** ("raise to 45%"). Both halves matter.
- Recurring rework or post-launch "we shipped the wrong thing" is being attributed to opinion-based prioritization. The cost of bad requirements now exceeds the cost of standing up a thin analytics loop.
- BA is being asked for evidence by a finance / risk / steerco audience. A baseline-and-target table closes the conversation faster than a discussion deck.
- Migrating a BA practice from BABOK-style narrative requirements toward measurable acceptance criteria — data-driven is the on-ramp, not the destination.

## When NOT to use
- Pre-product / pre-launch with no users. Any "data" will be a vanity sample; use qualitative discovery instead.
- The org has zero data infrastructure: no event tracking, no warehouse, no BI, hand-cleaned spreadsheets only. Build the minimum infra (next section) before claiming the practice.
- One-off compliance / legal / contractual requirements where the answer is "must, by date X." Metrics theater wastes the BA's time.
- Pure UX / brand / accessibility floor work where the metric is downstream perception. Quantify outcomes, not the requirement itself.
- Two-day decisions where running a baseline query costs more than just shipping and reverting.
- Teams that won't agree on a single metric definition. Without a shared definition layer, "data" produces louder arguments, not faster decisions.

## Where it fails / limitations
- **Adoption-stage mismatch**: a BA practice that pushes data-driven requirements before the org has a reliable warehouse produces requirements with placeholder baselines that nobody trusts. Tag the practice's maturity (see "Adoption gates") and don't skip stages.
- **Definition drift**: "active user" means three different things in three dashboards. Without a metric catalog, two BAs pull contradicting baselines for the same KPI on the same day.
- **Survivorship bias**: heavy users skew the data. The cohort that already churned is invisible — the requirement looks well-justified and is solving the wrong problem.
- **Single-source bias**: pulling from one tool (just GA, just Mixpanel) inherits that tool's tracking gaps. Cross-check with the system of record (DB, Stripe, support tickets) before locking a baseline.
- **Confidence theater**: stamping a number doesn't make it correct. Without `n`, `as_of`, and segmentation, "12% conversion" is not a baseline, it's a quote.
- **Causal claims from correlational data**: "users of feature X retain 2x" almost never means "shipping X for everyone doubles retention." Self-selection eats the effect.
- **Privacy / consent**: requirements built on data the org cannot lawfully use under GDPR/CCPA fail at legal review even when statistically sound.
- **Dashboard fixation**: BAs start prioritizing what's easy to query (page views) over what matters (retained revenue). The fundamentals must include a "why this metric ties to a business outcome" sentence per requirement.

## Adoption gates (BA-core specific)

Don't bolt this practice on without checking the team's stage. Each gate must be cleared before the next.

| Gate | Minimum signal | Without it, you have... |
|------|----------------|-------------------------|
| G1 — Events emitted | ≥ 1 event stream with `user_id`, `event_name`, `timestamp` | guesses |
| G2 — One queryable store | DB read replica OR a warehouse OR a product-analytics tool with SQL | hostage to whoever runs reports |
| G3 — Shared metric definition | At least 3 KPIs documented (formula, owner, source, refresh) | inconsistent baselines |
| G4 — One "north-star" KPI per surface | Agreed across PM/BA/Eng | priority debates without a tiebreaker |
| G5 — Baseline freshness rule | "Stale after N days" stamped on every baseline | requirements written off ageing numbers |
| G6 — Validation discipline | Each shipped requirement has a post-hoc "did the metric move?" check | learning loop is broken |

A BA practice at G1-G2 should write data-*informed* requirements (numbers as evidence, not the verdict). G3+ is where data-*driven* prioritization becomes honest.

## Minimum data infrastructure
The fundamentals do **not** require a warehouse. Below is the cheapest viable stack for a small product team to start.

| Layer | Minimum viable | Step up when |
|-------|----------------|-------------|
| Event capture | Server-side event log to a single table (`events(user_id, event, ts, props_json)`) | volume > 10M/mo or analyst can't keep up |
| Storage | Postgres read replica or a single PostHog instance | cross-source joins required |
| Query interface | psql / PostHog SQL / Metabase question | non-engineers need self-serve |
| Metric definitions | A markdown `metrics.md` in the repo with formula + owner per KPI | duplications appear; move to dbt / metric layer |
| Visualization | Metabase (OSS) or Superset (OSS); free | exec-grade dashboards or governance demanded |
| Experimentation | Manual feature flag + cohort comparison; no platform | running > 2 concurrent A/Bs |
| Catalog / lineage | The same `metrics.md`; a glossary in Notion | > 30 KPIs or multiple data producers |
| Quality checks | A weekly `SELECT count(*) WHERE props_json IS NULL` sanity script | data is loaded into customer-facing decisions |

The honest BA-core position: a Postgres read replica + Metabase + a `metrics.md` is enough to do honest data-driven requirements for a team of < 50. Anything heavier is premature.

## Agentic workflow
Drive the BA-core variant as a three-pass loop, simpler than the business-analyst pipeline. (1) **Frame** — a sonnet agent reads the requirement draft and outputs `{business_question, candidate_kpi, hypothesis, data_source_guess}`. (2) **Baseline** — a sonnet agent runs (or asks a human to run) one SQL or PostHog query, returns `{kpi, value, n, as_of, query_url}`; refuses values without `n` and `as_of`. (3) **Wire-up** — an opus agent rewrites the requirement using the README template, fills baseline + target + measurement method, and lists the *one* validation step that will be checked post-launch (no full A/B platform required for the core practice). Humans own: business-question framing, target ambition, and the post-launch yes/no review.

### Recommended subagents
- `faion-brainstorm` — diverge on candidate KPIs and on what "success" actually means *before* a baseline is fetched. Skipping this gives a clean number for the wrong question.
- `faion-sdd-executor-agent` — gate the requirement file: refuses entries with missing baseline, missing `as_of`, missing measurement method, or "TBD" success metric.
- `faion-feature-executor` — execute the implementation tasks once the requirement passes the gate, scoped by the success criteria.
- `faion-improver` — quarterly meta-loop: read the requirements shipped 1–2 quarters ago, re-fetch the success metric, log calibration error per author. Builds the post-hoc discipline (Gate G6) the BA-core practice depends on.
- A lightweight `metric-lookup-agent` worth creating: input `{kpi_name}`, output `{formula, owner, source_query, last_refresh}` from the team's `metrics.md` catalog. Refuses unknown KPI names — this is the single most effective hallucination guard at the BA-core stage.

### Prompt pattern
```
You are a BA-core data-driven requirement writer. Inputs: business_question,
draft_requirement, baseline = {kpi, value, n, as_of, source_url}, target_state.
Output the populated README template. Constraints:
- Reject if baseline.n is missing or < 30, or as_of older than 60 days.
- Every success metric MUST have a measurement_method that is either a SQL/event
  name or a dashboard URL. No "user feedback" without a structured signal.
- Define ONE primary metric and at most ONE guardrail metric. (BA-core scope —
  multi-metric portfolios belong in the business-analyst variant.)
- Output a one-line "why this metric ties to a business outcome" sentence.
- If you cannot fill any cell from the inputs, write "UNKNOWN — needs human"
  rather than inventing a number.
```

```
You are a metric-lookup agent. Input: kpi_name. Read team metrics.md.
Output JSON: {known: bool, formula, owner, source_query, last_refresh}.
If known=false, return suggested_aliases[] from fuzzy match and refuse to
proceed. Never invent a definition.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `psql` | Run baseline SQL against the prod read replica; the cheapest viable analytics stack | bundled with PostgreSQL |
| `posthog` (REST) | Self-hosted/SaaS product analytics with first-class API; pull funnels and retention | https://posthog.com/docs/api |
| `metabase` (REST) | Open-source BI; agents read saved questions as canonical KPI sources | https://www.metabase.com/docs/latest/api |
| `dbt` (optional, post-G3) | Version-controlled metric definitions; one `models/metrics/` folder is enough at the start | https://docs.getdbt.com |
| `csvkit` / `duckdb` | Local sanity checks on exported CSVs without spinning up a warehouse | `pip install csvkit duckdb` |
| `pandas` + `scipy.stats` | Confidence intervals on baselines, segment splits, sanity stats | `pip install pandas scipy` |
| `gh` + `jq` | Pull GitHub issue counts / labels as supplementary "support load" baselines | https://cli.github.com |
| `claude` CLI | Run the frame / baseline-prompt / wire-up passes against the README template | https://docs.anthropic.com/en/docs/claude-code |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| PostHog (self-hosted) | OSS | Yes (REST + SQL) | Single-server install covers events + funnels + dashboards; ideal BA-core default |
| Metabase | OSS | Yes (REST API) | Cheap BI; agents reference saved questions as the canonical baseline source |
| Postgres read replica | OSS | Yes (psql / DB drivers) | The most underrated analytics stack; works until ~50 GB / 10M events |
| GA4 | SaaS (free) | Yes (Data API) | Web-traffic baseline; small-team default for marketing-side requirements |
| Stripe (data API) | SaaS | Yes (REST) | System of record for revenue baselines; cross-check against product analytics |
| Notion / Confluence | SaaS | Read-only | Where the `metrics.md` catalog lives if there's no monorepo |
| Superset | OSS | Yes (REST) | Heavier than Metabase; defer until governance demands it |
| Mixpanel / Amplitude | SaaS | Yes (REST) | Step up from PostHog when behavioural-graph features are needed |
| GrowthBook | OSS | Yes (REST + SDK) | Lightweight A/B platform when one experiment per quarter becomes routine |
| Atlan / OpenMetadata | SaaS / OSS | Partial | Catalog tools; overkill for BA-core stage — a `metrics.md` is enough |

## Templates & scripts
The 5-file methodology pack here (checklist / templates / examples / llm-prompts) is currently a stub; the README's "Data-Driven Requirements Template" is the canonical doc shell. Below is a minimum `metrics.md` block — the foundation the practice depends on.

```markdown
# metrics.md — team metric catalog

## checkout_conversion
- formula: COUNT(checkout_completed) / COUNT(checkout_started) within session
- owner: @growth-pm
- source: events table (server-side); confirm against Stripe `payment_intents.succeeded`
- refresh: hourly (Metabase Q-117)
- aliases: cvr, conversion, completion_rate
- last_validated: 2026-04-10
- known caveats: includes refunds for 24h; exclude with `status != 'refunded'`

## monthly_active_users
- formula: COUNT(DISTINCT user_id) WHERE event IN ('app_open','api_call') over 30d rolling
- owner: @product
- source: events; PostHog persons API as cross-check
- refresh: daily 06:00 UTC (Metabase Q-23)
- aliases: mau, active_30d
- last_validated: 2026-04-12
- known caveats: bot traffic excluded via user_agent regex; doc in source query
```

A 10-line shell helper to refuse stale baselines at requirement-finalisation time:

```bash
#!/usr/bin/env bash
# fresh_baseline.sh — usage: fresh_baseline.sh <as_of_date> <max_days>
set -euo pipefail
as_of="${1:?as_of date required (YYYY-MM-DD)}"
max="${2:-30}"
age=$(( ( $(date +%s) - $(date -d "$as_of" +%s) ) / 86400 ))
if (( age > max )); then
  echo "STALE: baseline is ${age}d old; max=${max}d. Re-run query before commit." >&2
  exit 2
fi
echo "FRESH: baseline ${age}d old (limit ${max}d)."
```

## Best practices
- Start at G1–G2; write *data-informed* (not data-driven) requirements until G3 is real. Honesty about the stage builds trust faster than premature claims of rigor.
- Keep a single `metrics.md` in the product repo before reaching for a metric layer. The discipline of writing definitions matters more than the tool.
- Always include `n`, `as_of`, and `source_url` next to every baseline. A number without those three is gossip.
- One primary metric + one guardrail per requirement. Multi-metric optimization belongs in the business-analyst-tier playbook, not BA-core.
- Tie every metric to one sentence about the business outcome it maps to. If the BA can't write that sentence, the KPI is vanity.
- Reject any baseline that came from a screenshot. Insist on a query URL or dashboard link the next BA can re-run unattended.
- Pre-decide what counts as "post-launch success" before shipping; revisit it on a calendar trigger, not when someone remembers.
- Refuse to score requirements with KPIs not in `metrics.md`. New KPIs go through a 5-minute definition step first; this is the single highest-leverage habit.
- Slice baselines by ≥ 1 dimension (channel, plan, geo) to catch the obvious Simpson's paradox cases before they ship.
- Treat agents as drafters, humans as deciders for: (a) the business question, (b) target ambition, (c) ship/no-ship after measurement.

## AI-agent gotchas
- LLMs invent plausible KPI values. Force every cell to cite a source URL or query, and have a verifier agent re-run the query (or at minimum check that the URL exists).
- Agents collapse different metric definitions ("conversion", "completion", "purchase") into a single number. Resolving names against `metrics.md` blocks the most common silent failure.
- Date drift: an agent that fetched a baseline last week will reuse it forever unless `as_of` is enforced. Add the freshness gate above as a finalization step.
- Vanity-metric capture: agents pick the easiest-to-query metric over the most-business-relevant one. Constrain the schema to require a downstream business KPI (revenue, retention) and a "why this matters" sentence per requirement.
- Causal claims: agents will write "feature X drove +12% retention" from correlational data. Require a `causal_evidence_type ∈ {experiment, observational}` field; observational claims must be hedged in the requirement statement.
- Sycophancy: an agent will find data supporting whatever the question implies. Add a counter-evidence pass — "find the strongest signal that this requirement should NOT be built" — before finalisation.
- Privacy leak: agents may pull PII columns into the evidence section. Restrict warehouse roles, and run a redaction-checker over the requirement file before commit.
- Adoption-gate denial: agents will happily produce data-driven requirements at G1 with placeholder baselines. Hard-code the gate in the prompt: refuse to ship a requirement labeled "data-driven" if `metrics.md` has fewer than 3 KPIs.
- Human-in-the-loop checkpoints: (1) framing the business question, (2) setting the target value, (3) post-launch ship/rollback. Letting an agent close all three is how the wrong thing ships confidently.

## References
- BABOK Guide v3 — Strategy Analysis (§6) and Solution Evaluation (§8); industry-standard alignment between BA work and measured outcomes.
- Croll & Yoskovitz — *Lean Analytics* (one-metric-that-matters, stage-appropriate KPIs).
- Davenport & Harris — *Competing on Analytics* (canonical analytics-first decision-making).
- DAMA-DMBOK 2 — *Data Management Body of Knowledge*; practical data-strategy fundamentals.
- https://posthog.com/docs/data — PostHog metrics + SQL data layer (OSS reference, BA-core friendly).
- https://www.metabase.com/learn/grow-your-data-skills/data-fundamentals — Metabase fundamentals (matches BA-core readiness).
- https://docs.getdbt.com/docs/build/metrics — dbt semantic layer (step-up reference once at G3+).
- Sibling deep dive: `../../business-analyst/data-driven-requirements/agent-integration.md`.
