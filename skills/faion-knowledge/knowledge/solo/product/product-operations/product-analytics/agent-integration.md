# Agent Integration — Product Analytics

## When to use
- Designing tracking plan for a new product/feature pre-launch.
- Auditing existing event taxonomy: detect duplicate events, naming inconsistencies, undocumented properties.
- Generating SQL/cohort queries from natural-language questions ("Why is W2 retention dropping?").
- Weekly anomaly summaries from PostHog/Amplitude/Mixpanel exports.
- Stitching multiple analytics sources (PostHog + Stripe + Customer.io) into one cohort view.

## When NOT to use
- Real-time alerting / SLO monitoring — use Prometheus/Grafana, not LLMs.
- Compliance-bound metrics (HIPAA, GDPR-deletion, SOX revenue) — agent-generated SQL needs lawyer-grade audit trail.
- High-volume operational dashboards — LLM-in-loop adds 2-10s latency, breaks "glance at" rituals.
- You don't yet have user analytics instrumented; install before agentizing.

## Where it fails / limitations
- Agents fabricate event names that "should" exist when querying — verify against schema before SQL execution.
- "Insights" generated from sample data are pattern-matched to common SaaS narratives ("activation drop at step 3"); always cross-check with raw counts.
- Cohort math is subtle — agents miscount returning users, double-count cross-platform sessions, mix DAU definitions (any-event vs. core-action). Specify in prompt explicitly.
- Privacy: shipping raw events to LLM provider may violate DPA. Use aggregates or anonymize PII first.
- Statistical significance often skipped — agent declares "Reports drives retention" off N=12 with no p-value.

## Agentic workflow
Three roles: (1) `tracking-plan-author` agent designs event taxonomy from feature spec + audience-questions; outputs Tracking Plan markdown + JSON schema. (2) `query-builder` agent translates analyst questions to validated SQL/PostHog HogQL; runs read-only against warehouse. (3) `insight-summarizer` agent runs weekly on raw query outputs, produces narrative report with explicit "limitations" section. Critical guardrail: agent never writes events or modifies dashboards; output is PR/changeset for human review.

### Recommended subagents
- `tracking-plan-author` — sonnet, decomposes feature → events; enforces `Object Action` naming.
- `sql-builder` — sonnet, schema-aware SQL gen; rejects queries on unknown columns.
- `dashboard-spec-writer` — sonnet, produces dashboard JSON for PostHog/Amplitude templates.
- `weekly-summarizer` — haiku, runs from precomputed metrics file, no live querying.
- `funnel-debugger` — opus when investigating step-by-step dropoff (multi-hypothesis reasoning).

### Prompt pattern
```
Feature spec: {one-pager}
Key questions to answer post-launch: {list}
Output Tracking Plan:
- user_properties: [{name, type, description, example}]
- events: [{name (Object Action), trigger, properties[], owner}]
- naming convention: Object Action, snake_case for property names
- minimum required: max 12 events per feature
Reject any event without a question it answers.
```

```
Schema: {posthog_schema.json}
Question: "Why is W2 retention dropping?"
Generate HogQL with:
- explicit cohort definition (signup_week)
- baseline comparison (W2 of W-1, W-2, W-3)
- breakdown by acquisition source
Validate columns exist before returning.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `posthog-cli` | PostHog API operations | `npm i -g posthog-cli` |
| `amplitude-cli` (community) | Amplitude exports | https://github.com/amplitude/Amplitude-API-CLI |
| `mixpanel-engage` | Mixpanel queries | `pip install mixpanel-utils` |
| `dbt` | Modeled metrics layer | `pip install dbt-core` |
| `sqlglot` | LLM-safe SQL parsing/validation | `pip install sqlglot` |
| `duckdb` CLI | Local analytics on event exports | `brew install duckdb` |
| `claude` Skill tool | Drive sub-agents | https://docs.anthropic.com/en/docs/claude-code |
| `evidence` (OSS BI) | Markdown-driven reports for agents | `npm i -g @evidence-dev/evidence` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| PostHog | SaaS + OSS self-host | Excellent | HogQL, REST, webhooks; OSS variant free for solos. |
| Amplitude | SaaS | Yes (REST + Snowflake export) | Cohort/funnel APIs mature; agent-friendly. |
| Mixpanel | SaaS | Yes (JQL/SQL/REST) | Service Account Auth; cohorts via API. |
| RudderStack | OSS | Yes | Event router; pairs with warehouse for agent queries. |
| Segment | SaaS | Yes | Tracking-plan API + Protocols; spec validation built-in. |
| Snowplow | OSS | Yes | Most flexible event collection; complex setup. |
| Heap | SaaS | Limited | Auto-capture; less agent-friendly for taxonomy. |
| Plausible / Fathom | SaaS | Limited | Privacy-first web; minimal product analytics. |
| Metabase / Apache Superset | OSS BI | Yes | Agent generates SQL → embedded in dashboards. |
| Cube.dev | OSS | Yes | Semantic layer; agents target stable metric definitions. |
| dbt + Snowflake/BigQuery | Stack | Yes | Modeled marts; agents query trusted layer. |
| Statsig / GrowthBook | SaaS / OSS | Yes | Experimentation layer; pairs with analytics. |

## Templates & scripts
See `templates.md` for Tracking Plan, Dashboard Spec, Analysis Report. Schema-validated query helper:

```python
# query_safe.py — refuses LLM SQL on unknown columns
import sqlglot, json, sys
schema = json.load(open(sys.argv[1]))           # posthog_schema.json
sql    = sys.stdin.read()                       # SQL from agent
parsed = sqlglot.parse_one(sql, read="postgres")
cols   = {c.name for c in parsed.find_all(sqlglot.exp.Column)}
known  = {f"{t}.{c}" for t, fs in schema.items() for c in fs}
unk    = cols - known - {c.split(".")[-1] for c in known}
if unk:
    sys.exit(f"BLOCKED: unknown columns {unk}")
print(sql)  # safe to run
```

## Best practices
- **Tracking plan first, instrumentation second**: write the questions you'll ask, then the events. Agents that go from "track everything" produce useless data lakes.
- **`Object Action` naming, snake_case properties** — consistency matters more than cleverness.
- **Server-side for revenue/auth events**: client-side is lossy; agents that recommend "fire on button click" leak 5-15% of conversions.
- **Cap at 12 events per feature**: agents will produce 30+; force minimum-viable taxonomy.
- **Cohort by signup week, not date**: agents default to date cohorts which conflate growth + retention.
- **Document `who` for every event**: ownership matters when events break.
- **Store schema-as-code in repo**: agent edits go through PR review.
- **Sample data ≠ insight**: agents must cite N before drawing conclusions; force `n_users` in every output row.

## AI-agent gotchas
- LLM hallucinated columns are the #1 SQL bug. Use `sqlglot` + schema check before execute.
- DAU definition drift: "Daily Active Users" can mean any-event-fired, core-action-completed, or session-started. Agents pick whichever matches narrative; pin one in prompt.
- Time-zone bugs: agents mix UTC and user-local. Force `_utc` suffix on timestamp columns.
- Statistical significance routinely skipped — wire up minimum sample-size + p-value gates in summarizer prompts.
- Privacy: never paste raw event rows with email/IP to LLM. Aggregate first or hash PII.
- Cost trap: agent-driven warehouse queries can run away fast. Set query timeout + scan limit.
- **Human-in-loop checkpoint**: dashboard published to leadership = human-reviewed. Agent-generated narrative goes through PM signoff.
- "Funnel drop" narratives are seductive — agent may declare causation from correlation. Force "this is correlation; experiment to confirm".
- Cohort retention curves require 7+ data points or are noise; agents draw conclusions from W1-W2 alone.

## References
- "Lean Analytics" — Croll & Yoskovitz
- Amplitude Mastery course (free)
- PostHog HogQL docs — https://posthog.com/docs/hogql
- Segment "Analytics Academy" — tracking plan discipline
- Reforge — "Retention + Engagement" series
- Stripe + PostHog joint blog — solopreneur metrics stack
