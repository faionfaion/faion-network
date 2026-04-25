# Agent Integration — PLG Metrics & Tracking

## When to use
- Standing up a Product-Led Growth dashboard with activation, conversion, expansion, and retention metrics in one place.
- Defining or refining the activation event ("aha moment") and time-to-value (TTV) for a SaaS product.
- Designing a Product-Qualified Lead (PQL) scoring model from product behavior signals.
- Cohort analysis for retention and free-to-paid conversion across signup months or acquisition sources.
- Quarterly PLG strategy review where freemium vs trial choice and gating thresholds are on the table.

## When NOT to use
- Sales-led motions where the buyer never logs in before purchase — PLG metrics produce noise.
- Pre-product-market-fit startups: vanity metrics dominate, and PQL scoring overfits to a tiny sample.
- Self-hosted or single-tenant deployments where event telemetry is not centralized.
- Hardware or one-time-purchase products without recurring usage signals.
- Regulated industries where logging granular user behavior requires consent gates that break funnel completeness.

## Where it fails / limitations
- Activation events get over-engineered — a 7-step "fully activated" definition is unmeasurable; teams ship and forget.
- PQL scores drift as the product evolves; stale weights misroute sales motion within 1-2 quarters.
- Cohort tables become showpieces — readable but no action attached. Retention diagnosis without root-cause is theater.
- TTV is reported as a global median; it hides huge variance across segments (SMB vs Enterprise, mobile vs web).
- NRR > 100% covers up logo churn; tracking only NRR misses customer-base erosion.
- Tracking infra debt: events fire from frontend AND backend AND third-party tools, with no idempotent definition; metrics drift silently.

## Agentic workflow
A Claude subagent is well-suited for: drafting the metric catalog (definitions + SQL), proposing PQL scoring weights from a sample of converted vs churned users, reading dashboard snapshots and producing weekly executive summaries with anomalies highlighted, and translating cohort tables into prioritized hypotheses. The agent should NOT silently change metric definitions in production warehouses — its role is proposal + draft, with a human approving DDL/DML changes.

### Recommended subagents
- `faion-sdd-executor-agent` — model the metric catalog as an SDD spec (definitions, owners, SLAs, alert thresholds).
- `nero-sdd-executor-agent` — for NERO-internal product analytics tasks.
- A `plg-analytics-agent` (suggested) — sonnet for weekly summaries and PQL scoring proposals; opus for cohort diagnosis and pricing-strategy suggestions; haiku for DDL/SQL boilerplate and dashboard config.
- `faion-growth-agent` (referenced in README) — owns hypothesis prioritization downstream of metrics.

### Prompt pattern
```
Given the metric catalog <attached> and last 8 weeks of cohort retention
<csv>, identify the 3 worst-performing cohorts, the most likely root cause
per cohort, and a single experiment per cause to test next sprint. Output
as a table with hypothesis, target metric, and minimum detectable effect.
```

```
PQL scoring proposal: from this sample of 200 paid converters and 200
churned trials <attached>, propose signal weights, score thresholds, and
expected sales workload. State assumptions; flag where sample is biased.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `dbt` | Define + test PLG metrics in the warehouse | https://docs.getdbt.com/ |
| `cube` (Cube CLI) | Semantic layer for consistent metric definitions | https://cube.dev/ |
| `metricflow` | dbt's semantic layer (now MetricFlow) | https://docs.getdbt.com/docs/build/about-metricflow |
| `posthog-cli` | Query Posthog events / cohorts | https://posthog.com/docs/cli |
| `bigquery` / `snow` (Snowflake CLI) | Run metric SQL ad hoc | https://cloud.google.com/bigquery , https://docs.snowflake.com/ |
| `evidence` | Code-as-config BI for metric narratives | https://evidence.dev/ |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Amplitude | SaaS | Yes (API) | Strong cohorting, behavioral analysis |
| Mixpanel | SaaS | Yes (API) | Funnel + cohort + JQL |
| PostHog | OSS + SaaS | Yes (API) | Self-host option; event + session + feature flags |
| Heap | SaaS | Yes (API) | Auto-capture; weaker custom event control |
| Madkudu | SaaS | Yes (API) | Built-for-PQL scoring |
| Pocus | SaaS | Yes (API) | Product-led sales workflow on top of warehouse |
| ChartMogul | SaaS | Yes (API) | Subscription analytics, NRR/MRR |
| Stripe | SaaS | Yes (API) | Source of truth for billing + expansion MRR |
| dbt Cloud / Cube Cloud | SaaS | Yes (API) | Hosted semantic layer |
| Metabase | OSS | Yes | Self-host BI for the dashboard view |

## Templates & scripts
See `templates.md` for the dashboard layout. Inline PQL scoring example (treat as scaffold):

```python
# pql_score.py — signal-weighted PQL score from raw events.
# Run weekly; output to user_pql table for sales routing.
SIGNALS = {
    "weekly_actions_gte_100": (3, "high"),
    "invited_members_gte_5":  (3, "high"),
    "tried_gated_feature":    (3, "high"),
    "hours_in_product_gte_10":(2, "medium"),
    "integrations_gte_3":     (2, "medium"),
    "exported_or_shared":     (2, "medium"),
}
def score(user_events: dict) -> dict:
    total = sum(w for k, (w, _) in SIGNALS.items() if user_events.get(k))
    band = "nurture" if total < 6 else "self_serve" if total < 9 else "sales"
    return {"score": total, "band": band}
```

## Best practices
- One owner per metric. Without an owner, definitions drift and the dashboard becomes folklore.
- Define the activation event as ONE event, in ONE table, fired in ONE place. Cross-source unions for activation always break.
- Cohort everything. Single-number metrics hide the truth; M0/M1/M3/M6 retention is the floor.
- Track both NRR and gross dollar retention (GDR). NRR-only conceals churn.
- Calibrate PQL thresholds against actual close rates monthly; adjust before sales workload drifts.
- Keep the metric catalog version-controlled (dbt + Git). Dashboards that change definitions silently are net-negative.
- Pair every dashboard tile with an "if this moves, who acts and how" runbook line.

## AI-agent gotchas
- LLMs propose plausible-but-wrong SQL aggregations on event tables (UNION over UNION ALL, missed deduplication). Always require the agent to output the SQL and a test query against a known sample.
- PQL weight proposals based on small samples overfit; force the agent to report sample size and confidence band.
- Cohort summaries paraphrased by the agent often invert direction ("retention improved" when M3 dropped 2pp). Demand verbatim numbers, no rounding.
- Anomaly detection without a baseline is hallucination. Provide last 8 weeks of values as context for any "anomaly" claim.
- Privacy: per-user event data must be aggregated before sending to an external LLM. Sanitize emails, names, IPs.
- Agents conflate "activation" with "onboarding completion"; force a glossary into the prompt and reject if the agent uses the terms interchangeably.
- Quarterly strategy outputs (freemium vs trial) are decision-grade. Never ship the agent's recommendation without a human PM/CFO review.

## References
- OpenView Partners, "Product-Led Growth Metrics" — https://openviewpartners.com/blog/product-led-growth-metrics/
- Lenny Rachitsky, "How to measure product-led growth" — https://www.lennysnewsletter.com/p/how-to-measure-product-led-growth
- Madkudu, "PQL framework" — https://www.madkudu.com/resources/product-qualified-lead
- ChartMogul, "Net Revenue Retention" — https://chartmogul.com/resources/net-revenue-retention/
- Amplitude, "Cohort analysis guide" — https://amplitude.com/blog/cohort-analysis
- dbt Labs, "Semantic layer + metrics" — https://docs.getdbt.com/docs/build/about-metricflow
- Reforge, "PLG model selection" — https://www.reforge.com/
